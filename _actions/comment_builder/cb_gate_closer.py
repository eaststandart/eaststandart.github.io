#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_gate_closer.py
@about   Завершение обработки комплекта Конструктора комментариев.
@purpose Удаляет только файлы подтверждённо опубликованного комплекта из _output.
@author  TechLab
@version 1.1.0
"""

import logging
import subprocess
from pathlib import Path


logger = logging.getLogger(__name__)
OUTPUT_DIRECTORY = "_output"
KEEP_FILE = ".gitkeep"


class CommentBuilderCleanupError(Exception):
    """Ошибка безопасной очистки исходного комплекта."""


def _run_git(repository_path, *arguments):
    """Запускает Git-команду в указанном checkout и возвращает stdout."""
    result = subprocess.run(
        ["git", "-C", str(repository_path), *arguments],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise CommentBuilderCleanupError(
            f"Команда git {' '.join(arguments)} завершилась ошибкой: {detail}"
        )
    return result.stdout.strip()


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


def clean_source_output(
    repository_path,
    package,
    publication_confirmed=False,
):
    """
    Удаляет только манифест и медиафайлы переданного опубликованного пакета.

    Перед удалением сверяет Git blob SHA каждого файла с SHA, полученными
    парсером из GitHub. Остальные файлы _output и .gitkeep не затрагиваются.
    """
    if publication_confirmed is not True:
        raise CommentBuilderCleanupError(
            "Очистка запрещена: успешная публикация комментария не подтверждена."
        )
    if not isinstance(package, dict):
        raise CommentBuilderCleanupError("Не передан пакет для очистки.")

    repository = Path(repository_path).resolve()
    if not repository.is_dir() or not (repository / ".git").exists():
        raise CommentBuilderCleanupError(
            f"Указанный путь не является checkout Git-репозитория: {repository}"
        )

    output_dir = (repository / OUTPUT_DIRECTORY).resolve()
    if output_dir.parent != repository or output_dir.name != OUTPUT_DIRECTORY:
        raise CommentBuilderCleanupError(
            "Путь к _output не прошёл проверку безопасности."
        )
    if not output_dir.is_dir():
        raise CommentBuilderCleanupError(
            f"В checkout отсутствует каталог {OUTPUT_DIRECTORY}."
        )

    manifest_name = _safe_output_name(
        package.get("manifest_name"),
        "manifest_name",
    )
    manifest_sha = package.get("manifest_sha")
    if not isinstance(manifest_sha, str) or not manifest_sha:
        raise CommentBuilderCleanupError(
            "В пакете отсутствует SHA манифеста; безопасная очистка невозможна."
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

    dirty_state = _run_git(repository, "status", "--porcelain")
    if dirty_state:
        raise CommentBuilderCleanupError(
            "Checkout исходного репозитория содержит посторонние изменения; "
            "очистка отменена."
        )

    paths_to_remove = []
    for name, expected_sha in expected_files:
        relative_path = f"{OUTPUT_DIRECTORY}/{name}"
        actual_sha = _run_git(repository, "rev-parse", f"HEAD:{relative_path}")
        if actual_sha != expected_sha:
            raise CommentBuilderCleanupError(
                f"SHA файла {relative_path} не совпадает с полученным парсером. "
                "Возможно, комплект в исходном репозитории уже изменился; "
                "очистка отменена."
            )
        paths_to_remove.append(relative_path)

    _run_git(repository, "rm", "-f", "--", *paths_to_remove)

    keep_path = output_dir / KEEP_FILE
    if not keep_path.exists():
        keep_path.write_text("\n", encoding="utf-8")
        _run_git(repository, "add", "--", f"{OUTPUT_DIRECTORY}/{KEEP_FILE}")

    _run_git(repository, "config", "user.name", "TechLab Comment Bot")
    _run_git(repository, "config", "user.email", "comment-bot@techlab.local")
    _run_git(
        repository,
        "commit",
        "-m",
        "очистка опубликованного комплекта из _output",
    )
    commit_sha = _run_git(repository, "rev-parse", "HEAD")
    _run_git(repository, "push", "origin", "HEAD:main")

    logger.info(
        "Комплект очищен из _output: файлов — %d; commit — %s. .gitkeep сохранён.",
        len(paths_to_remove),
        commit_sha,
    )
    return {
        "success": True,
        "deleted_files": len(paths_to_remove),
        "commit": commit_sha,
    }
