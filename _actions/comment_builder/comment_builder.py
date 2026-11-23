#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  comment_builder.py
@about   Диспетчер конвейера Конструктора комментариев.
@purpose Координирует получение комплекта, публикацию или имитацию публикации и очистку.
@author  TechLab
@version 1.2.0
"""

import argparse
import logging
import sys

import cb_data_parser
import cb_comment_builder
import cb_gate_closer


LOGGER_NAME = "comment_builder"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger(LOGGER_NAME)


def configure_logging():
    """Настраивает единый формат сообщений конвейера."""
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        stream=sys.stdout,
        force=True,
    )


def main(argv=None):
    """Запускает полный цикл; реальная публикация требует флага --publish."""
    parser = argparse.ArgumentParser(
        description="Получение комплекта и публикация комментария TechLab."
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Разрешить реальную публикацию в GitHub Discussions.",
    )
    args = parser.parse_args(argv)

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

        logger.info(
            "Этап 2/3: %s.",
            "реальная публикация нового комментария"
            if args.publish else "имитация публикации в пробном режиме",
        )
        result = cb_comment_builder.publish_comment(
            package,
            dry_run=not args.publish,
        )

        if not isinstance(result, dict) or not result.get("success"):
            raise RuntimeError("Модуль публикации не подтвердил успешный результат.")

        logger.info(
            "Этап 3/3: очистка обработанного комплекта%s.",
            " после реальной публикации" if args.publish
            else " после успешной имитации публикации",
        )
        cleanup_result = cb_gate_closer.clean_source_output(
            package,
            processing_confirmed=True,
        )
        if not cleanup_result.get("success"):
            raise RuntimeError("Модуль очистки не подтвердил завершение.")

        if result.get("dry_run"):
            logger.info(
                "Пробный цикл завершён успешно. Discussion #%s, тело: %d символов. "
                "Комментарий не публиковался; комплект удалён из _output.",
                result["discussion_number"],
                result["body_length"],
            )
        else:
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
