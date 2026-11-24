#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_comment_dispatcher.py
@about   Модуль выбора форматтера комментария по номеру GitHub Discussion.
@purpose Выбирает специализированный модуль форматирования по discussion_number из метаданных комплекта, передаёт ему Markdown после замены ссылок на медиа и возвращает пакет с подготовленным телом комментария.
@author  TechLab
@version 1.0.0
"""

import importlib
import logging


DISCUSSION_FORMATTERS = {
    0: "cb_discussion_0",
    83: "cb_discussion_83",
}
DEFAULT_FORMATTER = 0

logger = logging.getLogger(__name__)


class CommentDispatchError(Exception):
    """Ошибка выбора или выполнения форматтера комментария."""


def dispatch_comment(package):
    """
    Выбирает форматтер по discussion_number и возвращает обновлённый пакет.

    Неизвестный номер направляется в форматтер по умолчанию.
    Ошибка зарегистрированного форматтера прерывает обработку без fallback.
    """
    if not isinstance(package, dict):
        raise CommentDispatchError("Передан некорректный пакет комментария.")

    metadata = package.get("metadata")
    if not isinstance(metadata, dict):
        raise CommentDispatchError("В пакете отсутствуют метаданные.")

    discussion_number = metadata.get("discussion_number")
    if (
        isinstance(discussion_number, bool)
        or not isinstance(discussion_number, int)
        or discussion_number < 1
    ):
        raise CommentDispatchError(
            "discussion_number должен быть целым положительным числом."
        )

    markdown = package.get("body")
    if not isinstance(markdown, str):
        raise CommentDispatchError("В пакете отсутствует Markdown-тело.")

    formatter_number = (
        discussion_number
        if discussion_number in DISCUSSION_FORMATTERS
        else DEFAULT_FORMATTER
    )
    formatter_name = DISCUSSION_FORMATTERS[formatter_number]

    logger.info(
        "Discussion #%s: выбран форматтер %s.",
        discussion_number,
        formatter_name,
    )

    try:
        formatter = importlib.import_module(formatter_name)
        format_comment = getattr(formatter, "format_comment", None)
        if not callable(format_comment):
            raise CommentDispatchError(
                f"В модуле {formatter_name} отсутствует функция format_comment()."
            )
        formatted_markdown = format_comment(markdown)
    except CommentDispatchError:
        raise
    except Exception as error:
        raise CommentDispatchError(
            f"Ошибка форматирования Discussion #{discussion_number} "
            f"модулем {formatter_name}: {error}"
        ) from error

    if not isinstance(formatted_markdown, str):
        raise CommentDispatchError(
            f"Форматтер {formatter_name} вернул результат неверного типа."
        )

    result = dict(package)
    result["body"] = formatted_markdown

    logger.info(
        "Форматирование завершено: Discussion #%s; символов Markdown=%d.",
        discussion_number,
        len(formatted_markdown),
    )
    return result
