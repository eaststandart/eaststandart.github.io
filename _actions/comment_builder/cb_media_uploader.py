#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_media_uploader.py
@about   Загрузка медиафайлов в хранилище GitHub Attachments.
@purpose Загружает подготовленные файлы и преобразует локальные Markdown/Wiki-ссылки в URL вложений.
@author  TechLab
@version 1.0.0
"""

import logging
import mimetypes
import re
import os
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests


UPLOAD_URL = "https://uploads.github.com/user-attachments/assets"
TARGET_REPOSITORY_ID = 1218168867
REQUEST_TIMEOUT = 120
MAX_ATTEMPTS = 4
RETRY_DELAYS = (5, 15, 30)

logger = logging.getLogger(__name__)


class CommentBuilderMediaUploadError(Exception):
    """Ошибка загрузки вложения или преобразования ссылок."""


def _upload_one(session, token, item):
    """Загружает один файл и возвращает постоянный URL GitHub Attachment."""
    name = item.get("name")
    local_path = item.get("local_path")
    if not isinstance(name, str) or not name:
        raise CommentBuilderMediaUploadError("У медиафайла отсутствует имя.")
    if not isinstance(local_path, str) or not os.path.isfile(local_path):
        raise CommentBuilderMediaUploadError(
            f"Локальный файл вложения не найден: {name}."
        )

    allowed_types = {".webp": "image/webp", ".webm": "video/webm"}
    mime_type = allowed_types.get(Path(name).suffix.lower())
    if not mime_type:
        raise CommentBuilderMediaUploadError(
            f"Неподдерживаемый формат вложения: {name}."
        )

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
    if file_size <= 0:
        raise CommentBuilderMediaUploadError(
            f"Файл вложения {name} пуст."
        )

    logger.info(
        "Загрузка вложения: %s (%d байт, %s).",
        name, file_size, mime_type,
    )

    for attempt in range(MAX_ATTEMPTS):
        try:
            with open(local_path, "rb") as source:
                response = session.post(
                    UPLOAD_URL,
                    params=params,
                    headers=headers,
                    data=source,
                    timeout=REQUEST_TIMEOUT,
                )
        except (requests.Timeout, requests.ConnectionError) as error:
            if attempt == MAX_ATTEMPTS - 1:
                raise CommentBuilderMediaUploadError(
                    f"Сетевая ошибка при загрузке {name} после "
                    f"{MAX_ATTEMPTS} попыток: {error}"
                ) from error
            delay = RETRY_DELAYS[attempt]
            logger.warning(
                "Временная сетевая ошибка загрузки %s. Повтор %d/%d через %d сек.",
                name, attempt + 2, MAX_ATTEMPTS, delay,
            )
            time.sleep(delay)
            continue

        if response.status_code == 429 or 500 <= response.status_code <= 599:
            if attempt == MAX_ATTEMPTS - 1:
                raise CommentBuilderMediaUploadError(
                    f"GitHub Attachments вернул HTTP {response.status_code} "
                    f"для {name}: {response.text[:1000]}"
                )
            delay = RETRY_DELAYS[attempt]
            logger.warning(
                "Временная ошибка HTTP %s для %s. Повтор %d/%d через %d сек.",
                response.status_code, name, attempt + 2, MAX_ATTEMPTS, delay,
            )
            time.sleep(delay)
            continue

        if response.status_code < 200 or response.status_code >= 300:
            raise CommentBuilderMediaUploadError(
                f"GitHub Attachments отклонил {name}: HTTP "
                f"{response.status_code}: {response.text[:1500]}"
            )

        try:
            payload = response.json()
        except ValueError as error:
            raise CommentBuilderMediaUploadError(
                f"GitHub Attachments вернул некорректный JSON для {name}."
            ) from error

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

    raise CommentBuilderMediaUploadError(
        f"Не удалось загрузить вложение {name}."
    )


def upload_media(package):
    """
    Загружает все медиафайлы пакета и заменяет локальные ссылки в Markdown.
    Возвращает копию пакета с обновлённым body и картой URL.
    """
    if not isinstance(package, dict):
        raise CommentBuilderMediaUploadError("Передан некорректный пакет.")

    media = package.get("media", [])
    if not isinstance(media, list):
        raise CommentBuilderMediaUploadError("Список медиафайлов некорректен.")

    body = package.get("body")
    if not isinstance(body, str):
        raise CommentBuilderMediaUploadError("В пакете отсутствует Markdown-тело.")

    if not media:
        logger.info("Медиафайлы отсутствуют. Загрузка не требуется.")
        return dict(package)

    token = os.environ.get("MY_ADMIN_TOKEN")
    if not token:
        raise CommentBuilderMediaUploadError(
            "Для загрузки вложений не найден MY_ADMIN_TOKEN."
        )

    urls = {}
    with requests.Session() as session:
        for item in media:
            if not isinstance(item, dict):
                raise CommentBuilderMediaUploadError(
                    "В списке медиафайлов обнаружена некорректная запись."
                )
            name = item.get("name")
            if name in urls:
                continue
            urls[name] = _upload_one(session, token, item)

    def wiki_replace(match):
        raw = match.group(1).strip()
        target, separator, alias = raw.partition("|")
        target = target.strip()
        filename = unquote(Path(target.split("#", 1)[0]).name)
        url = urls.get(filename)
        if not url:
            return match.group(0)
        alt = alias.strip() if separator and alias.strip() else filename
        return f"![{alt}]({url})"

    body = re.sub(r"!\[\[([^\]]+)\]\]", wiki_replace, body)

    def markdown_replace(match):
        marker, alt, target = match.groups()
        target = target.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        parsed = urlparse(target)
        if parsed.scheme or target.startswith("//"):
            return match.group(0)
        filename = unquote(Path(target.split("#", 1)[0].split("?", 1)[0]).name)
        url = urls.get(filename)
        if not url:
            return match.group(0)
        return f"{marker}[{alt}]({url})"

    body = re.sub(
        r"(!?)\[([^\]]*)\]\(([^)]+)\)",
        markdown_replace,
        body,
    )

    unresolved = [
        item.get("name") for item in media
        if item.get("name") and item["name"] not in urls
    ]
    if unresolved:
        raise CommentBuilderMediaUploadError(
            "Не удалось получить URL для вложений: " + ", ".join(unresolved)
        )

    result = dict(package)
    result["body"] = body
    result["media_urls"] = urls
    logger.info(
        "Загрузка завершена: файлов — %d; Markdown обновлён.",
        len(urls),
    )
    return result
