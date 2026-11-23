#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  comment_builder.py
@about   Модуль диспетчера конвейера публикации комментариев.
@purpose Получает комплект из _output репозитория eaststandart/techlab-comment-builder, передаёт медиафайлы в GitHub Attachments, публикует комментарий в GitHub Discussions репозитория eaststandart/eaststandart.github.io и после подтверждённой обработки очищает исходный комплект.
@author  TechLab
@version 1.0.0
"""

import logging
import sys

import cb_data_parser
import cb_comment_builder
import cb_media_uploader
import cb_gate_closer


LOGGER_NAME = "comment_builder"
LOG_FORMAT = "[%(name)s] %(message)s"

logger = logging.getLogger(LOGGER_NAME)


def configure_logging():
    """Настраивает единый формат сообщений конвейера."""
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )


def main():
    """Запускает полный цикл реальной публикации комментария."""
    configure_logging()
    package = None
    exit_code = 1

    logger.info("Запуск конвейера публикации комментария.")

    try:
        logger.info("Этап 1/3: получение и проверка комплекта Конструктора.")
        package = cb_data_parser.collect_and_parse_raw_data()

        if not isinstance(package, dict):
            raise RuntimeError("Парсер не вернул готовый пакет данных.")

        logger.info(
            "Комплект получен: манифест=%s, вложений=%d, Discussion #%s.",
            package.get("manifest_name", "неизвестно"),
            len(package.get("media", [])),
            (package.get("metadata") or {}).get("discussion_number", "не указан"),
        )

        logger.info("Этап 2/3: загрузка медиафайлов в GitHub Attachments.")
        package = cb_media_uploader.upload_media(package)

        logger.info("Этап 3/3: реальная публикация комментария.")
        result = cb_comment_builder.publish_comment(package)

        if not isinstance(result, dict) or not result.get("success"):
            raise RuntimeError("Модуль публикации не подтвердил успешный результат.")

        logger.info("Очистка обработанного комплекта после подтверждённой публикации.")
        cleanup_result = cb_gate_closer.clean_source_output(
            package,
            processing_confirmed=True,
        )
        if not cleanup_result.get("success"):
            raise RuntimeError("Модуль очистки не подтвердил завершение.")

        logger.info(
            "Конвейер завершён успешно. Ссылка на комментарий: %s",
            result["url"],
        )
        exit_code = 0

    except Exception:
        logger.exception("Конвейер завершился с ошибкой.")

    finally:
        logger.info("Завершение конвейера. Код результата: %s.", exit_code)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
