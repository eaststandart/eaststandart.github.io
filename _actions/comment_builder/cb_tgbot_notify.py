#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_tgbot_notify.py
@about   Модуль отправки уведомлений о публикации Творческого процесса в Telegram.
@purpose Рассылает уведомления по адресатам tg_public_notify со ссылкой на опубликованный комментарий GitHub Discussions.
@author  TechLab
@version 1.0.0
"""

import datetime
import html
import json
import os
import re
import urllib.request


TELEGRAM_API_URL = "https://api.telegram.org"


def send_public_notification(markdown_body, comment_url, discussion_number,
                             public_config, media_count=0):
    """Отправляет уведомления по плоскому списку адресатов tg_public_notify."""
    if not public_config:
        print("[БОТ ТГ] Список tg_public_notify пуст. Рассылка пропущена.")
        return True

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("[БОТ ТГ] Ошибка: секрет TELEGRAM_BOT_TOKEN не найден.")
        return False

    date_match = re.search(
        r"Творческий процесс за ([\d.]+ г\.)",
        markdown_body,
        re.IGNORECASE,
    )
    if date_match:
        formatted_date = date_match.group(1).strip()
    else:
        formatted_date = f"{datetime.date.today().strftime('%d.%m.%Y')} г."

    announcement_text = f"Обновлён Творческий процесс за {formatted_date}"
    if media_count:
        announcement_text += "\\n(Добавлены медиаматериалы занятий)"

    safe_url = html.escape(comment_url, quote=True)
    message_text = (
        f'<a href="{safe_url}">&#8203;</a>'
        f"<b>Творческий процесс #{discussion_number}</b>\\n\\n"
        f"{announcement_text}\\n\\n"
        f'<a href="{safe_url}">Посмотреть на GitHub Discussions</a>'
    )

    successful_broadcasts = 0
    total_broadcasts = 0

    for recipient in public_config:
        raw_recipient = str(recipient).strip().lower()
        if not raw_recipient:
            continue

        if "_" not in raw_recipient:
            print(f"[БОТ ТГ] Некорректный адресат: {recipient!r}. Пропуск.")
            continue

        channel_id, topic_value = raw_recipient.rsplit("_", 1)
        if not re.fullmatch(r"-?\d+", channel_id):
            print(f"[БОТ ТГ] Некорректный ID канала: {recipient!r}. Пропуск.")
            continue

        is_general_topic = topic_value.endswith("g")
        topic_digits = re.sub(r"[^\d]", "", topic_value)
        if not is_general_topic and not topic_digits:
            print(f"[БОТ ТГ] Некорректный ID темы: {recipient!r}. Пропуск.")
            continue

        payload = {
            "chat_id": int(channel_id),
            "text": message_text,
            "parse_mode": "HTML",
            "link_preview_options": {
                "is_disabled": False,
                "prefer_small_media": True,
            },
        }
        if not is_general_topic:
            payload["message_thread_id"] = int(topic_digits)

        total_broadcasts += 1
        request = urllib.request.Request(
            f"{TELEGRAM_API_URL}/bot{token}/sendMessage",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.getcode() == 200:
                    successful_broadcasts += 1
                    print(f"[БОТ ТГ] Уведомление доставлено: {recipient}.")
                else:
                    print(
                        f"[БОТ ТГ] HTTP {response.getcode()} для адресата "
                        f"{recipient}."
                    )
        except Exception as error:
            print(f"[БОТ ТГ] Ошибка отправки {recipient}: {error}")

    if total_broadcasts == 0:
        print("[БОТ ТГ] Нет корректных адресатов для отправки.")
        return False

    return successful_broadcasts > 0
