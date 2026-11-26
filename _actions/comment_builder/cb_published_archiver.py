#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_published_archiver.py
@about   Модуль сохранения опубликованного манифеста в архив Конструктора.
@purpose Формирует архивную копию исходного манифеста, добавляет ID и URL опубликованного комментария и заменяет локальные ссылки на URL загруженных медиа; сохраняет файл с исходным именем в _published репозитория eaststandart/techlab-comment-builder.
@author  TechLab
@version 1.0.0
"""

import base64
import json
import logging
import os
import re
import time
from urllib.parse import quote

import requests


SOURCE_OWNER = "eaststandart"
SOURCE_REPOSITORY = "techlab-comment-builder"
SOURCE_BRANCH = "main"
PUBLISHED_DIRECTORY = "_published"
API_BASE = (
    f"https://api.github.com/repos/{SOURCE_OWNER}/{SOURCE_REPOSITORY}"
)
REQUEST_TIMEOUT = 30
RETRY_DELAYS = (300, 1800, 3600)

logger = logging.getLogger(__name__)


class CommentBuilderArchiveError(Exception):
    """Ошибка формирования или сохранения архивного манифеста."""


def _safe_manifest_name(value):
    """Разрешает только имя Markdown-файла без вложенных путей."""
    if (
        not isinstance(value, str)
        or not value
        or value in (".", "..")
        or "/" in value
        or "\\" in value
        or not value.lower().endswith(".md")
    ):
        raise CommentBuilderArchiveError(
            f"Недопустимое имя архивного манифеста: {value!r}"
        )
    return value


def _build_archived_manifest(package, publish_result):
    """Сохраняет исходный Front Matter и структуру Markdown, заменяя локальные ссылки на URL медиа."""
    source_text = package.get("manifest_text")
    comment_id = publish_result.get("comment_id")
    source_url = publish_result.get("url")

    if not isinstance(source_text, str):
        raise CommentBuilderArchiveError("В пакете отсутствует исходный текст манифеста.")
    if isinstance(comment_id, bool) or not isinstance(comment_id, int) or comment_id < 1:
        raise CommentBuilderArchiveError("GitHub не вернул корректный ID опубликованного комментария.")
    if not isinstance(source_url, str) or not source_url.startswith("https://github.com/"):
        raise CommentBuilderArchiveError("GitHub не вернул корректную ссылку на комментарий.")

    match = re.match(
        r"^(---[ \t]*\r?\n)([\s\S]*?)(\r?\n---[ \t]*(?:\r?\n|$))",
        source_text,
    )
    if not match:
        raise CommentBuilderArchiveError("Не удалось разобрать Front Matter исходного манифеста.")

    front_matter_lines = []
    for line in match.group(2).splitlines():
        if re.match(r"^\s*(discussion_comment|source)\s*:", line, re.IGNORECASE):
            continue
        front_matter_lines.append(line)

    front_matter_lines.extend([
        f"discussion_comment: \"{comment_id}\"",
        f"source: {json.dumps(source_url, ensure_ascii=False)}",
    ])

    archived_front_matter = (
        match.group(1)
        + "\n".join(front_matter_lines)
        + match.group(3)
    )
    media = package.get("media", [])
    media_urls = package.get("media_urls", {})
    if not isinstance(media, list) or not isinstance(media_urls, dict):
        raise CommentBuilderArchiveError("В пакете отсутствуют корректные данные медиафайлов.")

    media_by_name = {}
    for item in media:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise CommentBuilderArchiveError("Обнаружена некорректная запись медиафайла.")
        name = item["name"]
        url = media_urls.get(name)
        if not isinstance(url, str) or not url.startswith("https://"):
            raise CommentBuilderArchiveError(
                f"Для медиафайла {name} отсутствует загруженный URL."
            )
        media_by_name[name] = item

    source_body = source_text[match.end():]
    if not source_body.strip():
        raise CommentBuilderArchiveError("В исходном манифесте отсутствует тело Markdown.")

    try:
        import cb_media_uploader
        archived_body = cb_media_uploader._replace_media_links(
            source_body, media_urls, media_by_name
        )
    except Exception as error:
        raise CommentBuilderArchiveError(
            f"Не удалось заменить ссылки на медиа в исходном манифесте: {error}"
        ) from error

    return archived_front_matter + archived_body


def _request(session, method, url, **kwargs):
    """Выполняет один запрос к GitHub Contents API."""
    try:
        response = session.request(
            method,
            url,
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )
    except requests.RequestException as error:
        raise CommentBuilderArchiveError(
            f"Сетевая ошибка GitHub API ({method}): {error}"
        ) from error
    return response


def _save_once(session, path, content):
    """Идемпотентно создаёт архивный файл; существующий иной файл не перезаписывает."""
    encoded_path = quote(path, safe="/")
    url = f"{API_BASE}/contents/{encoded_path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "TechLab-Comment-Builder",
    }

    existing = _request(
        session,
        "GET",
        url,
        headers=headers,
        params={"ref": SOURCE_BRANCH},
    )
    if existing.status_code == 200:
        try:
            payload = existing.json()
            current = base64.b64decode(payload["content"]).decode("utf-8")
        except (ValueError, KeyError, TypeError) as error:
            raise CommentBuilderArchiveError(
                f"Не удалось проверить существующий архивный файл {path}: {error}"
            ) from error
        finally:
            existing.close()

        if current == content:
            logger.info("Архивный манифест уже сохранён и совпадает: %s.", path)
            return {"success": True, "already_exists": True}

        raise CommentBuilderArchiveError(
            f"В _published уже существует {path} с другим содержимым. "
            "Перезапись запрещена."
        )

    if existing.status_code != 404:
        status = existing.status_code
        detail = existing.text[:1000]
        existing.close()
        raise CommentBuilderArchiveError(
            f"GitHub API GET вернул HTTP {status} для {path}: {detail}"
        )
    existing.close()

    created = _request(
        session,
        "PUT",
        url,
        headers=headers,
        json={
            "message": f"Архив опубликованного манифеста: {path.rsplit('/', 1)[-1]}",
            "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
            "branch": SOURCE_BRANCH,
        },
    )
    if 200 <= created.status_code < 300:
        logger.info("Архивный манифест сохранён: %s.", path)
        created.close()
        return {"success": True, "already_exists": False}

    status = created.status_code
    detail = created.text[:1000]
    created.close()
    raise CommentBuilderArchiveError(
        f"GitHub API PUT вернул HTTP {status} для {path}: {detail}"
    )


def archive_published_manifest(package, publish_result):
    """Создаёт архивную копию после публикации и всех уведомлений."""
    if not isinstance(package, dict) or not isinstance(publish_result, dict):
        raise CommentBuilderArchiveError("Переданы некорректные данные для архивирования.")
    if publish_result.get("success") is not True:
        raise CommentBuilderArchiveError("Архивирование запрещено без подтверждения публикации.")

    manifest_name = _safe_manifest_name(package.get("manifest_name"))
    media = package.get("media", [])
    media_urls = package.get("media_urls", {})
    if not isinstance(media, list) or not isinstance(media_urls, dict):
        raise CommentBuilderArchiveError("В пакете отсутствуют корректные данные медиафайлов.")
    archived_content = _build_archived_manifest(package, publish_result)
    archive_path = f"{PUBLISHED_DIRECTORY}/{manifest_name}"

    token = os.environ.get("MY_ADMIN_TOKEN", "").strip()
    if not token:
        raise CommentBuilderArchiveError(
            "Токен MY_ADMIN_TOKEN не найден. Архивирование отменено."
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "TechLab-Comment-Builder",
    }

    logger.info(
        "Архивирование манифеста %s в %s (Discussion #%s, комментарий #%s).",
        manifest_name,
        archive_path,
        publish_result.get("discussion_number"),
        publish_result.get("comment_id"),
    )

    last_error = None
    with requests.Session() as session:
        session.headers.update(headers)
        for attempt in range(len(RETRY_DELAYS) + 1):
            try:
                result = _save_once(session, archive_path, archived_content)
                logger.info(
                    "Архивирование завершено: %s; попытка %d/%d.",
                    archive_path,
                    attempt + 1,
                    len(RETRY_DELAYS) + 1,
                )
                return result
            except CommentBuilderArchiveError as error:
                last_error = error
                if attempt >= len(RETRY_DELAYS):
                    break
                delay = RETRY_DELAYS[attempt]
                logger.warning(
                    "Архивирование %s не удалось: %s. "
                    "Повтор %d/%d через %d минут.",
                    archive_path,
                    error,
                    attempt + 2,
                    len(RETRY_DELAYS) + 1,
                    delay // 60,
                )
                time.sleep(delay)

    raise CommentBuilderArchiveError(
        f"Не удалось сохранить {archive_path} после "
        f"{len(RETRY_DELAYS) + 1} попыток: {last_error}"
    ) from last_error
