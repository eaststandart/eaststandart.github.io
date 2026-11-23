#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_media_uploader.py
@about   Загрузка медиафайлов комплекта в GitHub Attachments.
@purpose Сопоставляет локальные Markdown-ссылки с файлами, загружает фотографии и видео, подставляет URL вложений в текст комментария.
@author  TechLab
@version 1.2.0
"""

import logging
import os
import re
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests


UPLOAD_URL = "https://uploads.github.com/user-attachments/assets"
TARGET_REPOSITORY_ID = 1218168867
REQUEST_TIMEOUT = 120
MAX_429_ATTEMPTS = 4
RETRY_DELAYS = (5, 15, 30)
MEDIA_EXTENSIONS = {".webp", ".webm"}
MEDIA_LINK_PATTERN = re.compile(
    r"(?P<wiki_marker>!?)\[\[(?P<wiki_target>[^\]]+)\]\]"
    r"|(?P<md_marker>!?)\[(?P<md_alt>[^\]]*)\]\((?P<md_target>[^)]+)\)"
)

logger = logging.getLogger(__name__)


class CommentBuilderMediaUploadError(Exception):
    """Ошибка загрузки вложения или преобразования ссылок."""


def _local_media_reference(target):
    """Возвращает имя локального медиафайла; внешние URL и другие файлы игнорирует."""
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("//"):
        return None
    clean_target = target.split("#", 1)[0].split("?", 1)[0]
    name = unquote(Path(clean_target.replace("\\", "/")).name)
    if Path(name).suffix.lower() not in MEDIA_EXTENSIONS:
        return None
    return name


def _preflight(body, media):
    """Проверяет соответствие всех локальных медиа-ссылок и файлов до первого POST."""
    if not isinstance(media, list):
        raise CommentBuilderMediaUploadError("Список медиафайлов некорректен.")

    by_name = {}
    for item in media:
        if not isinstance(item, dict):
            raise CommentBuilderMediaUploadError(
                "В списке медиафайлов обнаружена некорректная запись."
            )
        name = item.get("name")
        local_path = item.get("local_path")
        if not isinstance(name, str) or not name:
            raise CommentBuilderMediaUploadError("У медиафайла отсутствует имя.")
        if name in by_name:
            raise CommentBuilderMediaUploadError(
                f"Повторяющаяся запись медиафайла: {name}."
            )
        if Path(name).suffix.lower() not in MEDIA_EXTENSIONS:
            raise CommentBuilderMediaUploadError(
                f"Неподдерживаемый формат вложения: {name}."
            )
        if not isinstance(local_path, str) or not os.path.isfile(local_path):
            raise CommentBuilderMediaUploadError(
                f"Локальный файл вложения не найден: {name}."
            )
        if os.path.getsize(local_path) <= 0:
            raise CommentBuilderMediaUploadError(f"Файл вложения {name} пуст.")
        by_name[name] = item

    logger.info("Предварительная проверка: файлов в пакете=%d.", len(by_name))
    references = []
    for match in MEDIA_LINK_PATTERN.finditer(body):
        target = (
            match.group("wiki_target")
            if match.group("wiki_target") is not None
            else match.group("md_target")
        )
        name = _local_media_reference(target)
        if name:
            references.append(name)

    logger.info("Найдено локальных ссылок на медиафайлы: %d.", len(references))
    logger.info("Файлы пакета: %s", ", ".join(sorted(by_name)) if by_name else "нет")
    missing = sorted(set(references) - set(by_name))
    unreferenced = sorted(set(by_name) - set(references))
    if missing:
        raise CommentBuilderMediaUploadError(
            "В Markdown есть ссылки на отсутствующие в пакете медиафайлы: "
            + ", ".join(missing)
        )
    if unreferenced:
        raise CommentBuilderMediaUploadError(
            "В пакет включены медиафайлы без ссылок в Markdown: "
            + ", ".join(unreferenced)
        )

    logger.info("Предварительная проверка пройдена: %d файлов сопоставлено со ссылками.", len(by_name))
    return by_name


def _upload_one(session, token, item):
    """Загружает один файл; неоднозначный результат POST автоматически не повторяет."""
    name = item["name"]
    local_path = item["local_path"]
    mime_type = {
        ".webp": "image/webp",
        ".webm": "video/webm",
    }[Path(name).suffix.lower()]

    params = {
        "name": name,
        "content_type": mime_type,
        "repository_id": str(TARGET_REPOSITORY_ID),
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": mime_type,
        "User-Agent": "TechLab-Comment-Builder",
    }
    file_size = os.path.getsize(local_path)
    logger.info(
        "Загрузка вложения: %s (%d байт, %s).",
        name, file_size, mime_type,
    )

    for attempt in range(MAX_429_ATTEMPTS):
        try:
            with open(local_path, "rb") as source:
                response = session.post(
                    UPLOAD_URL,
                    params=params,
                    headers=headers,
                    data=source,
                    timeout=REQUEST_TIMEOUT,
                )
        except requests.RequestException as error:
            raise CommentBuilderMediaUploadError(
                f"Неоднозначный сетевой результат загрузки {name}; "
                "автоматический повтор POST остановлен во избежание дубликата. "
                f"Проверьте вложения перед повторным запуском. Причина: {error}"
            ) from error

        if response.status_code == 429:
            if attempt == MAX_429_ATTEMPTS - 1:
                raise CommentBuilderMediaUploadError(
                    f"GitHub Attachments вернул HTTP 429 для {name} "
                    f"после {MAX_429_ATTEMPTS} попыток: {response.text[:1000]}"
                )
            delay = RETRY_DELAYS[attempt]
            logger.warning(
                "GitHub Attachments вернул HTTP 429 для %s. "
                "Повтор %d/%d через %d сек.",
                name, attempt + 2, MAX_429_ATTEMPTS, delay,
            )
            response.close()
            time.sleep(delay)
            continue

        if response.status_code < 200 or response.status_code >= 300:
            raise CommentBuilderMediaUploadError(
                f"GitHub Attachments вернул HTTP {response.status_code} "
                f"для {name}. Повтор POST не выполняется: {response.text[:1500]}"
            )

        try:
            payload = response.json()
        except ValueError as error:
            raise CommentBuilderMediaUploadError(
                f"GitHub Attachments вернул некорректный JSON для {name}; "
                "повтор POST не выполняется."
            ) from error
        finally:
            response.close()

        attachment_url = payload.get("url") or payload.get("href")
        if not isinstance(attachment_url, str):
            raise CommentBuilderMediaUploadError(
                f"В ответе GitHub Attachments отсутствует URL для {name}: "
                f"{str(payload)[:1000]}"
            )

        parsed = urlparse(attachment_url)
        if parsed.scheme != "https" or parsed.netloc not in (
            "github.com", "user-images.githubusercontent.com"
        ):
            raise CommentBuilderMediaUploadError(
                f"GitHub вернул неожиданный адрес вложения для {name}: "
                f"{attachment_url}"
            )

        logger.info("Вложение загружено: %s -> %s", name, attachment_url)
        return attachment_url

    raise CommentBuilderMediaUploadError(f"Не удалось загрузить вложение {name}.")


def _replace_media_links(body, urls, media_by_name):
    """Преобразует ссылки в формат GitHub Discussions по типу файла."""

    def replace(match):
        is_wiki = match.group("wiki_target") is not None
        if is_wiki:
            raw = match.group("wiki_target").strip()
            target, separator, alias = raw.partition("|")
            name = _local_media_reference(target)
            if not name or name not in urls:
                return match.group(0)
            alt = alias.strip() if separator and alias.strip() else name
        else:
            target = match.group("md_target").strip()
            name = _local_media_reference(target)
            if not name or name not in urls:
                return match.group(0)
            alt = match.group("md_alt").strip() or name

        media_type = media_by_name[name].get("type")
        if media_type not in ("photo", "video"):
            media_type = "photo" if Path(name).suffix.lower() == ".webp" else "video"

        if media_type == "video":
            return f"[{alt}]({urls[name]})"
        return f"![{alt}]({urls[name]})"

    updated = MEDIA_LINK_PATTERN.sub(replace, body)

    unresolved = []
    for match in MEDIA_LINK_PATTERN.finditer(updated):
        target = (
            match.group("wiki_target")
            if match.group("wiki_target") is not None
            else match.group("md_target")
        )
        name = _local_media_reference(target)
        if name:
            unresolved.append(name)
    if unresolved:
        raise CommentBuilderMediaUploadError(
            "После замены остались локальные ссылки на медиафайлы: "
            + ", ".join(sorted(set(unresolved)))
        )
    return updated


def upload_media(package):
    """
    Загружает все медиафайлы пакета и заменяет локальные ссылки в Markdown.
    Возвращает копию пакета с обновлённым body и картой URL.
    """
    if not isinstance(package, dict):
        raise CommentBuilderMediaUploadError("Передан некорректный пакет.")

    body = package.get("body")
    if not isinstance(body, str):
        raise CommentBuilderMediaUploadError("В пакете отсутствует Markdown-тело.")

    media = package.get("media", [])
    media_by_name = _preflight(body, media)
    if not media_by_name:
        logger.info("Медиафайлы отсутствуют. Загрузка не требуется.")
        return dict(package)

    token = os.environ.get("MY_ADMIN_TOKEN")
    if not token:
        raise CommentBuilderMediaUploadError(
            "Для загрузки вложений не найден MY_ADMIN_TOKEN."
        )

    logger.info("Начинаю загрузку медиа: файлов=%d.", len(media_by_name))
    urls = {}
    with requests.Session() as session:
        for name, item in media_by_name.items():
            urls[name] = _upload_one(session, token, item)

    logger.info("Загрузка завершена: получено URL=%d. Подставляю ссылки в Markdown.", len(urls))
    updated_body = _replace_media_links(body, urls, media_by_name)
    logger.info("Markdown обновлён: исходное тело=%d символов; итоговое=%d символов.", len(body), len(updated_body))
    result = dict(package)
    result["body"] = updated_body
    result["media_urls"] = urls
    logger.info(
        "Загрузка завершена: файлов — %d; Markdown обновлён.",
        len(urls),
    )
    return result
