#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_wabot_personal.py
@about   Модуль отправки персональных уведомлений об Инженерных занятиях в WhatsApp.
@purpose Формирует компактное сообщение со ссылкой на опубликованный комментарий GitHub Discussions и отправляет его адресатам из wa_personal_id через GREEN-API.
@author  TechLab
@version 1.0.0
"""

import json
import logging
import os
import re
import urllib.request


GREEN_API_URL = "https://api.green-api.com"
logger = logging.getLogger(__name__)


def _build_message(markdown_body, comment_url, teacher):
    """Формирует текст WhatsApp-уведомления по опубликованному комментарию."""
    if not isinstance(markdown_body, str):
        logger.error("Не передано Markdown-тело опубликованного комментария.")
        return None

    heading_match = re.search(r"^##\s+(.+?)\s*$", markdown_body, re.MULTILINE)
    if not heading_match:
        logger.error("В опубликованном комментарии не найден главный заголовок H2.")
        return None

    heading = heading_match.group(1).strip()
    heading = re.sub(r"\s*[·•]\s*", " ", heading).strip()

    teacher_login = str(teacher or "eaststandart").strip().lstrip("@")
    if teacher_login.casefold() in {"techlab", "eaststandart"}:
        teacher_name = "TechLab"
    else:
        teacher_name = teacher_login

    safe_url = str(comment_url or "").strip()
    if not safe_url:
        logger.error("Не передана ссылка на опубликованный комментарий.")
        return None

    return (
        "🏢🏃‍♀️🏃‍♂️ *Инженерные занятия*\n\n"
        f"📢 {heading}\n\n"
        "👀 Посмотреть на GitHub Discussions\n"
        f"{safe_url}\n\n"
        f"Преподаватель: *{teacher_name}*"
    )


def send_personal_notification(markdown_body, comment_url, teacher, personal_ids):
    """Последовательно отправляет персональные уведомления адресатам wa_personal_id."""
    logger.info("Запуск персонального WhatsApp-информатора.")

    if not personal_ids:
        logger.info("Список wa_personal_id пуст. Персональная WhatsApp-рассылка пропущена.")
        return True

    if not isinstance(personal_ids, (list, tuple)):
        logger.error("Поле wa_personal_id должно содержать список номеров WhatsApp.")
        return False

    instance_id = os.environ.get("GREEN_API_ID", "").strip()
    api_token = os.environ.get("GREEN_API_TOKEN", "").strip()
    if not instance_id or not api_token:
        logger.error("Не найдены секреты GREEN_API_ID или GREEN_API_TOKEN.")
        return False

    message_text = _build_message(markdown_body, comment_url, teacher)
    if not message_text:
        return False

    endpoint = (
        f"{GREEN_API_URL}/waInstance{instance_id}/"
        f"sendMessage/{api_token}"
    )
    logger.info("Начинаем рассылку по списку персональных адресатов WhatsApp.")

    successful_sends = 0
    total_sends = 0

    for phone in personal_ids:
        if isinstance(phone, bool) or not isinstance(phone, (int, str)):
            logger.warning("Некорректный номер WhatsApp %r. Пропуск.", phone)
            continue

        clean_phone = str(phone).strip()
        if not clean_phone:
            logger.warning("Обнаружен пустой номер WhatsApp. Пропуск.")
            continue

        chat_id = (
            clean_phone
            if clean_phone.endswith("@c.us")
            else f"{clean_phone}@c.us"
        )
        if not re.fullmatch(r"\\+?\\d+@c\\.us", chat_id):
            logger.warning("Некорректный Chat ID WhatsApp %r. Пропуск.", chat_id)
            continue

        total_sends += 1
        logger.info("Подготовка отправки получателю %s.", chat_id)

        payload = {
            "chatId": chat_id,
            "message": message_text,
            "linkPreview": False,
        }
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.getcode() == 200:
                    successful_sends += 1
                    logger.info("Персональное WhatsApp-уведомление принято API для %s.", chat_id)
                else:
                    logger.warning(
                        "GREEN-API вернул HTTP %s для получателя %s.",
                        response.getcode(),
                        chat_id,
                    )
        except Exception as error:
            logger.error(
                "Ошибка отправки WhatsApp-уведомления получателю %s: %s",
                chat_id,
                error,
            )

    if total_sends == 0:
        logger.error("Нет корректных номеров для WhatsApp-рассылки.")
        return False

    if successful_sends:
        logger.info(
            "WhatsApp-рассылка завершена: успешно принято API %d из %d сообщений.",
            successful_sends,
            total_sends,
        )
        return True

    logger.error("Ни одно WhatsApp-уведомление не удалось отправить.")
    return False
