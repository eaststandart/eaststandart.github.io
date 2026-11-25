#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_tgbot_notify.py
@about   Модуль отправки уведомлений о публикации Инженерных занятий в Telegram.
@purpose Рассылает уведомления по адресатам tg_public_notify со ссылкой на опубликованный комментарий GitHub Discussions.
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



def _get_discussion_title(token, discussion_number):
    """Получает реальный заголовок Discussion через GitHub GraphQL API."""
    query = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        discussion(number: $number) {
          title
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "owner": "eaststandart",
            "repo": "eaststandart.github.io",
            "number": int(discussion_number),
        },
    }
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "TechLab-Comment-Builder",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception as error:
        logger.error("Не удалось получить заголовок Discussion #%s: %s", discussion_number, error)
        return None

    errors = result.get("errors") if isinstance(result, dict) else None
    if errors:
        logger.error("GitHub GraphQL вернул ошибку при чтении Discussion #%s: %s",
                     discussion_number, errors)
        return None

    discussion = (
        result.get("data", {}).get("repository", {}).get("discussion")
        if isinstance(result, dict) else None
    )
    title = discussion.get("title") if isinstance(discussion, dict) else None
    if not isinstance(title, str) or not title.strip():
        logger.error("GitHub не вернул заголовок Discussion #%s.", discussion_number)
        return None

    return title.strip()


def send_public_notification(markdown_body, comment_url, discussion_number,
                             public_config, media_count=0):
    """Отправляет уведомления по плоскому списку адресатов tg_public_notify."""
    logger.info("Запуск публичного Telegram информатора.")

    if not public_config:
        logger.info("Список tg_public_notify пуст. Рассылка пропущена.")
        return True

    if not media_count:
        logger.info("Медиаматериалы отсутствуют. Рассылка пропущена.")
        return True

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        logger.error("Критическая ошибка: секрет TELEGRAM_BOT_TOKEN не найден.")
        return False

    github_token = (
        os.environ.get("MY_ADMIN_TOKEN", "").strip()
        or os.environ.get("GITHUB_TOKEN", "").strip()
    )
    if not github_token:
        logger.error("Не найден токен MY_ADMIN_TOKEN или GITHUB_TOKEN для GitHub API.")
        return False

    discussion_title = _get_discussion_title(github_token, discussion_number)
    if not discussion_title:
        return False

    # Вторая строка берётся из главного заголовка опубликованного комментария.
    heading_match = re.search(r"^##\s+(.+?)\s*$", markdown_body, re.MULTILINE)
    if not heading_match:
        logger.error("В опубликованном комментарии не найден главный заголовок уровня H2.")
        return False

    comment_heading = heading_match.group(1).strip()
    safe_url = html.escape(comment_url, quote=True)
    safe_title = html.escape(discussion_title, quote=False)
    safe_heading = html.escape(comment_heading, quote=False)
    message_text = (
        f'<a href="{safe_url}">&#8203;</a><b>{safe_title}</b>\\n\\n'
        f'📢 {safe_heading}\\n\\n'
        f'👀 <a href="{safe_url}">Посмотреть на GitHub Discussions</a>'
    )

    logger.info("Начинаем рассылку по плоскому списку адресатов.")
    successful_broadcasts = 0
    total_broadcasts = 0

    for recipient in public_config:
        raw_recipient = str(recipient).strip().lower()
        if not raw_recipient:
            continue

        if "_" not in raw_recipient:
            logger.warning("Некорректный адресат: %r. Пропуск.", recipient)
            continue

        channel_id, topic_value = raw_recipient.rsplit("_", 1)
        if not re.fullmatch(r"-?\d+", channel_id):
            logger.warning("Некорректный ID канала: %r. Пропуск.", recipient)
            continue

        is_general_topic = topic_value.endswith("g")
        topic_digits = re.sub(r"[^\d]", "", topic_value)
        if not is_general_topic and not topic_digits:
            logger.warning("Некорректный ID темы: %r. Пропуск.", recipient)
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
        if is_general_topic:
            logger.info("Подготовка отправки в канал %s (основная ветка).", channel_id)
        else:
            logger.info("Подготовка отправки в канал %s (чат #%s).", channel_id, int(topic_digits))

        request = urllib.request.Request(
            f"{TELEGRAM_API_URL}/bot{token}/sendMessage",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.getcode() == 200:
                    successful_broadcasts += 1
                    thread_log = " (основная ветка)" if is_general_topic else f" (чат #{int(topic_digits)})"
                    logger.info("Уведомление доставлено в канал %s%s.", channel_id, thread_log)
                else:
                    logger.warning(
                        "Получен статус %s для канала %s.",
                        response.getcode(),
                        channel_id,
                    )
        except Exception as error:
            thread_log = " (основная ветка)" if is_general_topic else f" (чат #{int(topic_digits)})"
            logger.error("Ошибка сети в канале %s%s: %s", channel_id, thread_log, error)

    if total_broadcasts == 0:
        logger.error("Нет корректных адресатов для отправки.")
        return False

    if successful_broadcasts > 0:
        logger.info(
            "Рассылка завершена: успешно доставлено %s из %s.",
            successful_broadcasts,
            total_broadcasts,
        )
        return True

    logger.error("Ни одно уведомление не удалось доставить.")
    return False
