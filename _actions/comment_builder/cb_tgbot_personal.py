#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_tgbot_personal.py
@about   Модуль отправки персональных уведомлений об Инженерных занятиях в Telegram.
@purpose Формирует компактное уведомление со ссылкой на опубликованный комментарий GitHub Discussions и отправляет его адресатам из tg_personal_id.
@author  TechLab
@version 1.0.0
"""

import html
import json
import logging
import os
import re
import urllib.request


TELEGRAM_API_URL = "https://api.telegram.org"

logger = logging.getLogger(__name__)


def _build_message(markdown_body, comment_url, teacher):
    """Формирует компактное HTML-сообщение по опубликованному комментарию."""
    if not isinstance(markdown_body, str):
        logger.error("Не передано Markdown-тело опубликованного комментария.")
        return None

    heading_match = re.search(r"^##\\s+(.+?)\\s*$", markdown_body, re.MULTILINE)
    if not heading_match:
        logger.error("В опубликованном комментарии не найден главный заголовок H2.")
        return None

    heading = heading_match.group(1).strip()
    heading = re.sub(r"\\s*[·•]\\s*", " ", heading).strip()
    safe_heading = html.escape(heading, quote=False)

    teacher_login = str(teacher or "eaststandart").strip().lstrip("@")
    if teacher_login.casefold() in {"techlab", "eaststandart"}:
        teacher_name = "TechLab"
    else:
        teacher_name = teacher_login

    safe_teacher = html.escape(teacher_name, quote=False)
    safe_url = html.escape(str(comment_url or "").strip(), quote=True)
    if not safe_url:
        logger.error("Не передана ссылка на опубликованный комментарий.")
        return None

    return (
        "<b>🏢🏃‍♀️🏃‍♂️ Инженерные занятия</b>\\n\\n"
        f"📢 {safe_heading}\\n\\n"
        f'👀 <a href="{safe_url}">Посмотреть на GitHub Discussions</a>\\n\\n'
        f"Преподаватель: <b>{safe_teacher}</b>"
    )


def send_personal_notification(markdown_body, comment_url, teacher, personal_ids):
    """Последовательно отправляет персональное уведомление адресатам tg_personal_id."""
    logger.info("Запуск персонального Telegram-информатора.")

    if not personal_ids:
        logger.info("Список tg_personal_id пуст. Персональная рассылка пропущена.")
        return True

    if not isinstance(personal_ids, (list, tuple)):
        logger.error("Поле tg_personal_id должно содержать список Telegram ID.")
        return False

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        logger.error("Критическая ошибка: секрет TELEGRAM_BOT_TOKEN не найден.")
        return False

    message_text = _build_message(markdown_body, comment_url, teacher)
    if not message_text:
        return False

    logger.info("Начинаем персональную рассылку: получателей в манифесте %d.", len(personal_ids))
    successful_sends = 0
    total_sends = 0

    for chat_id in personal_ids:
        if isinstance(chat_id, bool) or not isinstance(chat_id, (int, str)):
            logger.warning("Некорректный Telegram ID %r. Пропуск.", chat_id)
            continue

        target_id = str(chat_id).strip()
        if not target_id:
            logger.warning("Обнаружен пустой Telegram ID. Пропуск.")
            continue

        total_sends += 1
        payload = {
            "chat_id": target_id,
            "text": message_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        request = urllib.request.Request(
            f"{TELEGRAM_API_URL}/bot{token}/sendMessage",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.getcode() == 200:
                    successful_sends += 1
                    logger.info("Персональное уведомление доставлено получателю %s.", target_id)
                else:
                    logger.warning(
                        "Telegram вернул HTTP %s для получателя %s.",
                        response.getcode(),
                        target_id,
                    )
        except Exception as error:
            logger.error(
                "Ошибка отправки персонального уведомления получателю %s: %s",
                target_id,
                error,
            )

    if successful_sends:
        logger.info(
            "Персональная рассылка завершена: успешно доставлено %d из %d.",
            successful_sends,
            total_sends,
        )
        return True

    logger.error("Ни одно персональное уведомление не удалось доставить.")
    return False
