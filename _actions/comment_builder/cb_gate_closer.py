#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_gate_closer.py
@about   Очистка обработанного комплекта в буферном шлюзе Конструктора.
@purpose После подтверждённой обработки удаляет только манифест и связанные медиафайлы из _output через GitHub REST API с проверкой SHA.
@author  TechLab
@version 1.4.0
"""

import logging
import os
from urllib.parse import quote

import requests


logger = logging.getLogger(__name__)

SOURCE_OWNER = "eaststandart"
SOURCE_REPOSITORY = "techlab-comment-builder"
SOURCE_BRANCH = "main"
OUTPUT_DIRECTORY = "_output"
KEEP_FILE = ".gitkeep"
API_BASE = (
    f"https://api.github.com/repos/{SOURCE_OWNER}/{SOURCE_REPOSITORY}"
)
REQUEST_TIMEOUT = 30


class CommentBuilderCleanupError(Exception):
    """Ошибка безопасного завершения обработки комплекта."""


def _safe_output_name(value, field_name):
    """Разрешает только имя файла непосредственно внутри _output."""
    if (
        not isinstance(value, str)
        or not value
        or value in (".", "..", KEEP_FILE)
        or "/" in value
        or "\\" in value
    ):
        raise CommentBuilderCleanupError(
            f"Недопустимое имя файла в пакете ({field_name}): {value!r}"
        )
    return value


def _request(session, method, url, **kwargs):
    """Выполняет REST-запрос и сообщает об ошибке с деталями GitHub."""
    try:
        response = session.request(
            method,
            url,
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )
    except requests.RequestException as error:
        raise CommentBuilderCleanupError(
            f"Сетевая ошибка GitHub API ({method}): {error}"
        ) from error

    if response.status_code < 200 or response.status_code >= 300:
        raise CommentBuilderCleanupError(
            f"GitHub API {method} {url} вернул HTTP "
            f"{response.status_code}: {response.text[:1000]}"
        )
    return response


def clean_source_output(package, processing_confirmed=False):
    """
    Удаляет только манифест и медиафайлы переданного пакета.

    SHA сверяются с конкретным commit main. Удаление выполняется одним
    Git-commit через REST Git Database API; остальные файлы не затрагиваются.
    """
    if processing_confirmed is not True:
        raise CommentBuilderCleanupError(
            "Очистка запрещена: успешная обработка комплекта не подтверждена."
        )
    if not isinstance(package, dict):
        raise CommentBuilderCleanupError("Не передан пакет для очистки.")

    token = os.environ.get("MY_ADMIN_TOKEN")
    if not token:
        raise CommentBuilderCleanupError(
            "Токен MY_ADMIN_TOKEN не найден. Очистка отменена."
        )

    manifest_name = _safe_output_name(
        package.get("manifest_name"),
        "manifest_name",
    )
    manifest_sha = package.get("manifest_sha")
    if not isinstance(manifest_sha, str) or not manifest_sha:
        raise CommentBuilderCleanupError(
            "В пакете отсутствует SHA манифеста."
        )

    media = package.get("media")
    if not isinstance(media, list):
        raise CommentBuilderCleanupError(
            "В пакете отсутствует корректный список медиафайлов."
        )

    expected_files = [(manifest_name, manifest_sha)]
    for item in media:
        if not isinstance(item, dict):
            raise CommentBuilderCleanupError(
                "В списке медиафайлов обнаружена некорректная запись."
            )
        name = _safe_output_name(item.get("name"), "media.name")
        sha = item.get("sha")
        if not isinstance(sha, str) or not sha:
            raise CommentBuilderCleanupError(
                f"Для вложения {name} отсутствует SHA."
            )
        expected_files.append((name, sha))

    names = [name for name, _ in expected_files]
    if len(names) != len(set(names)):
        raise CommentBuilderCleanupError(
            "В пакете обнаружены повторяющиеся имена файлов."
        )

    logger.info("Подготовка очистки _output: манифест=%s; медиафайлов=%d.", manifest_name, len(media))
    logger.info("Файлы для удаления: %s", ", ".join(names))
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "TechLab-Comment-Builder",
    }

    with requests.Session() as session:
        session.headers.update(headers)

        ref_response = _request(
            session,
            "GET",
            f"{API_BASE}/git/ref/heads/{SOURCE_BRANCH}",
        )
        parent_sha = ref_response.json()["object"]["sha"]
        logger.info("Текущий commit ветки %s: %s.", SOURCE_BRANCH, parent_sha)

        commit_response = _request(
            session,
            "GET",
            f"{API_BASE}/git/commits/{parent_sha}",
        )
        base_tree_sha = commit_response.json()["tree"]["sha"]

        tree_entries = []
        for name, expected_sha in expected_files:
            relative_path = f"{OUTPUT_DIRECTORY}/{name}"
            contents_url = (
                f"{API_BASE}/contents/{OUTPUT_DIRECTORY}/{quote(name, safe='')}"
                f"?ref={parent_sha}"
            )
            file_response = _request(session, "GET", contents_url)
            actual_sha = file_response.json().get("sha")
            if actual_sha != expected_sha:
                raise CommentBuilderCleanupError(
                    f"SHA файла {relative_path} не совпадает с SHA, "
                    "полученным парсером. Возможно, исходный комплект изменился. "
                    "Очистка отменена."
                )

            logger.info("SHA подтверждён: %s.", relative_path)
            tree_entries.append({
                "path": relative_path,
                "mode": "100644",
                "type": "blob",
                "sha": None,
            })

        tree_response = _request(
            session,
            "POST",
            f"{API_BASE}/git/trees",
            json={
                "base_tree": base_tree_sha,
                "tree": tree_entries,
            },
        )
        new_tree_sha = tree_response.json()["sha"]
        logger.info("Дерево очистки сформировано: %s.", new_tree_sha)

        new_commit_response = _request(
            session,
            "POST",
            f"{API_BASE}/git/commits",
            json={
                "message": "очистка обработанного комплекта из _output",
                "tree": new_tree_sha,
                "parents": [parent_sha],
            },
        )
        new_commit_sha = new_commit_response.json()["sha"]
        logger.info("Создан commit очистки: %s.", new_commit_sha)

        _request(
            session,
            "PATCH",
            f"{API_BASE}/git/refs/heads/{SOURCE_BRANCH}",
            json={"sha": new_commit_sha, "force": False},
        )

    logger.info(
        "Комплект удалён из %s: файлов — %d; commit — %s. Остальные файлы сохранены.",
        OUTPUT_DIRECTORY,
        len(expected_files),
        new_commit_sha,
    )
    return {
        "success": True,
        "deleted_files": len(expected_files),
        "commit": new_commit_sha,
    }

