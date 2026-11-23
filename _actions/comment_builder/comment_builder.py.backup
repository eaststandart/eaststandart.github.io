#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  comment_builder.py
@about   Диспетчер конвейера Конструктора комментариев.
@purpose Координирует получение комплекта, публикацию комментария и очистку временных файлов.
@author  TechLab
@version 1.0.0
"""

import argparse
import logging
import os
import shutil
import sys
import tempfile

import cb_data_parser
import cb_comment_builder


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
        logger.info("Этап 1/2: получение и проверка комплекта Конструктора.")
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
            "Этап 2/2: %s.",
            "реальная публикация нового комментария"
            if args.publish else "проверка в пробном режиме",
        )
        result = cb_comment_builder.publish_comment(
            package,
            dry_run=not args.publish,
        )

        if not result.get("success"):
            raise RuntimeError("Модуль публикации не подтвердил успешный результат.")

        if result.get("dry_run"):
            logger.info(
                "Пробная проверка завершена. Discussion #%s, тело: %d символов. "
                "Комментарий не публиковался.",
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
        if isinstance(package, dict):
            work_dir = package.get("work_dir")
            if work_dir:
                safe_root = os.path.realpath(tempfile.gettempdir())
                candidate = os.path.realpath(work_dir)
                is_temp_child = (
                    os.path.commonpath([safe_root, candidate]) == safe_root
                    and candidate != safe_root
                )
                has_expected_prefix = os.path.basename(candidate).startswith(
                    "techlab-comment-builder-"
                )
                if not (is_temp_child and has_expected_prefix and os.path.isdir(candidate)):
                    logger.error(
                        "Временная директория не удалена: путь не прошёл проверку безопасности: %s",
                        work_dir,
                    )
                    exit_code = 1
                else:
                    try:
                        shutil.rmtree(candidate)
                        logger.info("Временная директория удалена: %s", candidate)
                    except OSError:
                        logger.exception(
                            "Не удалось удалить временную директорию: %s",
                            candidate,
                        )
                        exit_code = 1

        logger.info("Завершение конвейера. Код результата: %s.", exit_code)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
