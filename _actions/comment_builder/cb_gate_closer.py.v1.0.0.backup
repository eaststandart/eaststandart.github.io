#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_gate_closer.py
@about   Завершение обработки комплекта Конструктора комментариев.
@purpose Удаляет файлы комплекта из _output после подтверждённой публикации комментария.
@author  TechLab
@version 1.0.0
"""

import logging
import os
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


def clean_source_output(repository_path, publication_confirmed=False):
    """
    Очищает _output в checkout репозитория Конструктора.

    Очистка разрешена только после явного подтверждения успешной публикации.
    Файл _output/.gitkeep сохраняется. Диспетчер вызывает метод только после
    успешного возврата подтверждения от модуля публикации.
    """
    if publication_confirmed is not True:
        raise CommentBuilderCleanupError(
            "Очистка запрещена: успешная публикация комментария не подтверждена."
        )

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

    tracked = _run_git(repository, "ls-files", "-z", "--", OUTPUT_DIRECTORY)
    files_to_remove = [
        item for item in tracked.split("\0")
        if item and item != f"{OUTPUT_DIRECTORY}/{KEEP_FILE}"
    ]

    if files_to_remove:
        _run_git(repository, "rm", "-f", "--", *files_to_remove)

    keep_path = output_dir / KEEP_FILE
    if not keep_path.exists():
        keep_path.write_text("\n", encoding="utf-8")
        _run_git(repository, "add", "--", f"{OUTPUT_DIRECTORY}/{KEEP_FILE}")

    changes = subprocess.run(
        ["git", "-C", str(repository), "diff", "--cached", "--quiet"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if changes.returncode == 0:
        logger.info("В _output нет файлов для удаления.")
        return {"success": True, "deleted_files": 0, "commit": None}
    if changes.returncode != 1:
        raise CommentBuilderCleanupError(
            f"Не удалось проверить индекс Git: {changes.stderr.strip()}"
        )

    _run_git(
        repository,
        "config", "user.name", "TechLab Comment Bot"
    )
    _run_git(
        repository,
        "config", "user.email", "comment-bot@techlab.local"
    )
    _run_git(
        repository,
        "commit",
        "-m",
        "очистка _output после публикации комментария",
    )
    commit_sha = _run_git(repository, "rev-parse", "HEAD")
    _run_git(repository, "push", "origin", "HEAD:main")

    logger.info(
        "Очистка _output завершена: удалено файлов — %d; commit — %s.",
        len(files_to_remove),
        commit_sha,
    )
    return {
        "success": True,
        "deleted_files": len(files_to_remove),
        "commit": commit_sha,
    }
