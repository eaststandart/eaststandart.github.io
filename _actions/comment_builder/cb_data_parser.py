#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_data_parser.py
@about   Модуль получения и проверки комплекта комментария.
@purpose Получает комплект из _output репозитория eaststandart/techlab-comment-builder через GitHub REST API, разбирает Front Matter и Markdown, проверяет метаданные и ссылки, скачивает связанные медиафайлы для дальнейшей обработки в репозитории eaststandart/eaststandart.github.io.
@author  TechLab
@version 1.0.0
"""

import ast
import logging
import os
import re
import tempfile
import time
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

import requests


SOURCE_OWNER = "eaststandart"
SOURCE_REPOSITORY = "techlab-comment-builder"
SOURCE_BRANCH = "main"
SOURCE_OUTPUT_PATH = "_output"

API_URL = (
    f"https://api.github.com/repos/{SOURCE_OWNER}/"
    f"{SOURCE_REPOSITORY}/contents/{SOURCE_OUTPUT_PATH}"
)

REQUEST_TIMEOUT = 30
MAX_ATTEMPTS = 4
RETRY_DELAYS = (5, 15, 30)

PHOTO_EXTENSIONS = {".webp"}
VIDEO_EXTENSIONS = {".webm"}

logger = logging.getLogger(__name__)
MEDIA_LINK_PATTERN = re.compile(
    r"(!?)\[\[([^\]]+)\]\]|(!?)\[([^\]]*)\]\(([^)]+)\)"
)


class CommentBuilderDataError(Exception):
    """Ошибка получения, проверки или разбора комплекта."""


def _request_with_retry(session, url, headers=None, stream=False):
    """Выполняет GET с повторами только для временных сетевых и HTTP-ошибок."""
    for attempt in range(MAX_ATTEMPTS):
        try:
            response = session.get(
                url,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                stream=stream
            )
        except (requests.Timeout, requests.ConnectionError) as error:
            if attempt == MAX_ATTEMPTS - 1:
                raise CommentBuilderDataError(
                    f"Сетевая ошибка после {MAX_ATTEMPTS} попыток: {error}"
                ) from error
            delay = RETRY_DELAYS[attempt]
            logger.warning(
                "Временная сетевая ошибка GET %s: %s. Повтор %d/%d через %d сек.",
                url, error, attempt + 2, MAX_ATTEMPTS, delay,
            )
            time.sleep(delay)
            continue

        status = response.status_code
        retryable = status == 429 or 500 <= status <= 599

        # GitHub может возвращать 403 при исчерпании лимита API.
        if status == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
            retryable = True

        if retryable:
            if attempt == MAX_ATTEMPTS - 1:
                detail = response.text[:500]
                response.close()
                raise CommentBuilderDataError(
                    f"GitHub API вернул HTTP {status} после "
                    f"{MAX_ATTEMPTS} попыток: {detail}"
                )
            delay = RETRY_DELAYS[attempt]
            logger.warning(
                "GitHub API вернул HTTP %s для %s. Повтор %d/%d через %d сек.",
                status, url, attempt + 2, MAX_ATTEMPTS, delay,
            )
            response.close()
            time.sleep(delay)
            continue

        if status < 200 or status >= 300:
            detail = response.text[:500]
            response.close()
            raise CommentBuilderDataError(
                f"GitHub вернул HTTP {status}: {detail}"
            )

        return response

    raise CommentBuilderDataError("Не удалось выполнить сетевой запрос.")



def _download_to_path(session, url, headers, local_path, file_name):
    """Скачивает файл целиком; повторяет также обрыв соединения во время чтения."""
    for attempt in range(MAX_ATTEMPTS):
        response = None
        try:
            response = _request_with_retry(
                session, url, headers=headers, stream=True
            )
            with open(local_path, "wb") as output_file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output_file.write(chunk)
            if not os.path.isfile(local_path) or os.path.getsize(local_path) == 0:
                raise CommentBuilderDataError(
                    f"Вложение {file_name} скачано пустым."
                )
            return
        except requests.RequestException as error:
            if os.path.exists(local_path):
                os.remove(local_path)
            if attempt == MAX_ATTEMPTS - 1:
                raise CommentBuilderDataError(
                    f"Сетевая ошибка при скачивании {file_name} "
                    f"после {MAX_ATTEMPTS} попыток: {error}"
                ) from error
            delay = RETRY_DELAYS[attempt]
            logger.warning(
                "Скачивание %s прервано: %s. Повтор %d/%d через %d сек.",
                file_name, error, attempt + 2, MAX_ATTEMPTS, delay,
            )
            time.sleep(delay)
        finally:
            if response is not None:
                response.close()


def _parse_scalar(value):
    """Разбирает простые скалярные значения Front Matter без внешнего YAML-пакета."""
    value = value.strip()
    if not value:
        return ""

    if value[0:1] in ("'", '"'):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            raise CommentBuilderDataError(
                f"Некорректное значение Front Matter: {value}"
            )

    lowered = value.lower()
    if lowered in ("true", "false"):
        return lowered == "true"
    if lowered in ("null", "~"):
        return None

    if re.fullmatch(r"-?\d+", value):
        return int(value)

    return value


def _parse_front_matter(manifest_text):
    """Извлекает метаданные и тело Markdown из Front Matter."""
    match = re.match(
        r"^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)",
        manifest_text
    )
    if not match:
        raise CommentBuilderDataError(
            "В манифесте отсутствует или повреждён Front Matter."
        )

    metadata = {}
    for line_number, line in enumerate(match.group(1).splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise CommentBuilderDataError(
                f"Некорректная строка Front Matter №{line_number}: {line}"
            )
        key, value = line.split(":", 1)
        key = key.strip().lower()
        if not key:
            raise CommentBuilderDataError(
                f"Пустое имя поля Front Matter в строке №{line_number}."
            )
        metadata[key] = _parse_scalar(value)

    body = manifest_text[match.end():]
    return metadata, body


def _extract_media(body):
    """Извлекает локальные ссылки на фото и видео, сохраняя порядок в манифесте."""
    media = []
    seen = set()

    for match in MEDIA_LINK_PATTERN.finditer(body):
        if match.group(2) is not None:
            raw_name = match.group(2).split("|", 1)[0].strip()
        else:
            raw_name = match.group(5).strip()
            if raw_name.startswith("<") and raw_name.endswith(">"):
                raw_name = raw_name[1:-1]

        if re.match(r"^[a-z][a-z0-9+.-]*:", raw_name, re.IGNORECASE):
            continue
        if raw_name.startswith("//"):
            continue

        name = unquote(raw_name)
        path = PurePosixPath(name)
        if path.is_absolute() or len(path.parts) != 1 or name in ("", ".", ".."):
            raise CommentBuilderDataError(
                f"Недопустимый путь вложения в манифесте: {raw_name}"
            )

        extension = Path(name).suffix.lower()
        if extension in PHOTO_EXTENSIONS:
            media_type = "photo"
        elif extension in VIDEO_EXTENSIONS:
            media_type = "video"
        else:
            continue

        if name not in seen:
            seen.add(name)
            media.append({"name": name, "type": media_type})

    return media


def _validate_metadata(metadata, manifest_name):
    """Проверяет минимально необходимые поля для создания комментария."""
    discussion_number = metadata.get("discussion_number")
    if isinstance(discussion_number, bool):
        raise CommentBuilderDataError(
            f"{manifest_name}: discussion_number должен быть положительным числом."
        )

    try:
        discussion_number = int(discussion_number)
    except (TypeError, ValueError):
        raise CommentBuilderDataError(
            f"{manifest_name}: отсутствует корректный discussion_number."
        )

    if discussion_number < 1:
        raise CommentBuilderDataError(
            f"{manifest_name}: discussion_number должен быть больше нуля."
        )

    if metadata.get("published") is not True:
        raise CommentBuilderDataError(
            f"{manifest_name}: манифест не помечен published: true."
        )

    metadata["discussion_number"] = discussion_number
    return metadata


def collect_and_parse_raw_data():
    """
    Загружает один полный комплект из _output.

    Возвращает словарь с метаданными, исходным Markdown, списком медиафайлов
    и локальными путями к ним. Исходный репозиторий не изменяется.
    """
    logger.info("=== ЭТАП ПОЛУЧЕНИЯ КОМПЛЕКТА ИЗ _output ===")
    logger.info(
        "Источник: %s/%s, ветка %s, каталог %s.",
        SOURCE_OWNER, SOURCE_REPOSITORY, SOURCE_BRANCH, SOURCE_OUTPUT_PATH,
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "TechLab-Comment-Builder"
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with requests.Session() as session:
        listing_response = _request_with_retry(
            session,
            f"{API_URL}?ref={SOURCE_BRANCH}",
            headers=headers
        )
        try:
            listing = listing_response.json()
        except ValueError as error:
            raise CommentBuilderDataError(
                "GitHub вернул некорректный JSON со списком _output."
            ) from error
        finally:
            listing_response.close()

        if not isinstance(listing, list):
            raise CommentBuilderDataError(
                "GitHub API вернул неожиданный формат списка _output."
            )

        logger.info("GitHub API вернул записей в _output: %d.", len(listing))
        files = {
            item.get("name"): item
            for item in listing
            if item.get("type") == "file" and item.get("name") != ".gitkeep"
        }

        logger.info(
            "Файлы комплекта: %s",
            ", ".join(sorted(files)) if files else "нет файлов",
        )
        manifests = [
            name for name in files
            if name.lower().endswith(".md")
        ]

        logger.info("Найдено Markdown-манифестов: %d.", len(manifests))
        if not manifests:
            raise CommentBuilderDataError(
                "В _output не найден Markdown-манифест комплекта."
            )
        if len(manifests) != 1:
            raise CommentBuilderDataError(
                f"В _output найдено манифестов: {len(manifests)}. "
                "Для одного комплекта должен быть ровно один."
            )

        manifest_name = manifests[0]
        manifest_item = files[manifest_name]
        logger.info(
            "Выбран манифест: %s (SHA %s, размер %s байт).",
            manifest_name, manifest_item.get("sha", "не указан"),
            manifest_item.get("size", "не указан"),
        )
        manifest_url = manifest_item.get("download_url")
        if not manifest_url:
            raise CommentBuilderDataError(
                f"Для манифеста {manifest_name} отсутствует download_url."
            )

        manifest_response = _request_with_retry(
            session, manifest_url, headers=headers
        )
        try:
            manifest_text = manifest_response.content.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise CommentBuilderDataError(
                f"Манифест {manifest_name} не является корректным UTF-8 файлом."
            ) from error
        finally:
            manifest_response.close()

        logger.info("Манифест %s загружен: %d символов.", manifest_name, len(manifest_text))
        metadata, body = _parse_front_matter(manifest_text)
        logger.info(
            "Front Matter разобран. Поля: %s.",
            ", ".join(sorted(metadata)) if metadata else "нет",
        )
        metadata = _validate_metadata(metadata, manifest_name)
        logger.info(
            "Параметры публикации проверены: published=%s, Discussion #%s.",
            metadata.get("published"), metadata["discussion_number"],
        )
        logger.info("Тело Markdown: %d символов.", len(body))
        media = _extract_media(body)
        logger.info("В Markdown найдено локальных медиафайлов: %d.", len(media))
        for item in media:
            logger.info("Медиа в манифесте: %s (%s).", item["name"], item["type"])

        for item in media:
            if item["name"] not in files:
                raise CommentBuilderDataError(
                    f"В манифесте указано вложение, которого нет в _output: "
                    f"{item['name']}"
                )
            item["download_url"] = files[item["name"]].get("download_url")
            if not item["download_url"]:
                raise CommentBuilderDataError(
                    f"Для вложения {item['name']} отсутствует download_url."
                )
            item["sha"] = files[item["name"]].get("sha", "")

        work_dir = tempfile.mkdtemp(prefix="techlab-comment-builder-")
        downloaded_media = []

        for item in media:
            local_path = os.path.join(work_dir, item["name"])
            logger.info(
                "Скачивание вложения: %s (SHA %s, URL %s).",
                item["name"], item["sha"], item["download_url"],
            )
            try:
                _download_to_path(
                    session,
                    item["download_url"],
                    headers,
                    local_path,
                    item["name"]
                )
            except OSError as error:
                raise CommentBuilderDataError(
                    f"Не удалось сохранить вложение {item['name']}: {error}"
                ) from error

            logger.info(
                "Вложение получено: %s (%d байт).",
                item["name"], os.path.getsize(local_path),
            )
            downloaded_media.append({
                "name": item["name"],
                "type": item["type"],
                "sha": item["sha"],
                "local_path": local_path
            })

    package = {
        "manifest_name": manifest_name,
        "manifest_sha": manifest_item.get("sha", ""),
        "manifest_text": manifest_text,
        "metadata": metadata,
        "body": body,
        "media": downloaded_media,
        "work_dir": work_dir
    }

    logger.info(
        "Комплект полностью получен: манифест=%s; Discussion #%s; "
        "медиафайлов=%d; временный каталог=%s.",
        manifest_name, metadata["discussion_number"], len(downloaded_media), work_dir,
    )
    logger.info("=== ЭТАП ПОЛУЧЕНИЯ КОМПЛЕКТА ЗАВЕРШЁН ===")
    return package
