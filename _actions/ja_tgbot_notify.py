#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module ja_tgbot_notify.py
@about Отправка публичных анонсов для родителей
@purpose Рассылка уведомлений по каналам и чатам Телеграм со ссылкой на журнал посещений
@author TechLab
@version 1.0.0
"""

import os
import json
import sys
import re
import urllib.request

# Константа адреса Telegram API
TELEGRAM_API_URL = "https://telegram.org"

def send_public_notification(markdown_body, comment_url, public_config):
    print("\n=== [МОДУЛЬ JA_TGBOT_NOTIFY] ЗАПУСК РОДИТЕЛЬСКОГО ИНФОРМАТОРА ===")
    
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("[БОТ РОДИТЕЛЕЙ] ❌ КРИТИЧЕСКАЯ ОШИБКА: Секрет TELEGRAM_BOT_TOKEN не найден!")
        return False

    # 1. Перехват даты занятия из заголовка Markdown
    date_match = re.search(r'Журнал посещений за ([\d.]+ г\.)', markdown_body)
    if date_match:
        formatted_date = date_match.group(1).strip()
    else:
        import datetime
        formatted_date = f"{datetime.date.today().strftime('%d.%m.%Y')} г."

    # 2. Сборка текста сообщения с невидимым символом ссылки
    announcement_text = f"📢 Обновлён журнал посещений за {formatted_date}"
    
    message_text = (
        f'<a href="{comment_url}">&#8203;</a><b>📅 Журнал посещений регулярных занятий #38</b>\n\n'
        f'{announcement_text}\n\n'
        f'👀 <a href="{comment_url}">Посмотреть на GitHub Discussions</a>'
    )

    # 3. Цикл рассылки по конфигурации каналов и чатов (веток)
    print("[БОТ РОДИТЕЛЕЙ] Начинаем вещание для древовидного списка каналов...")
    send_errors = 0
    total_broadcasts = 0
    successful_broadcasts = 0

    for group in public_config:
        channel_id = str(group.get("channel_id", "")).strip()
        chat_ids = group.get("chat_id", [])
        
        if not channel_id:
            continue
            
        # Информирование о пропуске, если список чатов (веток) пуст или закомментирован
        if not chat_ids:
            print(f"[БОТ РОДИТЕЛЕЙ] Пропуск канала {channel_id}: нет чатов для отправки.")
            continue
            
        if isinstance(chat_ids, (int, str)):
            chat_ids = [chat_ids]

        for chat in chat_ids:
            raw_chat_str = str(chat).strip().lower()
            total_broadcasts += 1
            
            # Распознавание флага основной ветки (General)
            is_general_topic = 'g' in raw_chat_str
            
            # Извлечение цифрового ID чата (ветки)
            clean_chat_digits = re.sub(r'[^\d]', '', raw_chat_str)
            chat_id = int(clean_chat_digits) if clean_chat_digits else 0
            
            url_tg = f"{TELEGRAM_API_URL}/bot{token}/sendMessage"
            
            # Сборка пакета с новыми именами переменных
            payload = {
                "chat_id": channel_id,
                "text": message_text,
                "parse_mode": "HTML",
                "link_preview_options": {
                    "is_disabled": False,
                    "prefer_small_media": True
                }
            }
            
            # Исключение message_thread_id при наличии флага 'g'
            if chat_id > 0 and not is_general_topic:
                payload["message_thread_id"] = chat_id
                print(f"[БОТ РОДИТЕЛЕЙ] Подготовка отправки в обычный чат #{chat_id}")
            elif is_general_topic:
                print(f"[БОТ РОДИТЕЛЕЙ] Обнаружен флаг основной ветки ({raw_chat_str}). Идентификатор чата исключен из запроса.")
            elif chat_id == 0 and not is_general_topic:
                payload["message_thread_id"] = 0
                print(f"[БОТ РОДИТЕЛЕЙ] Подготовка отправки в чат №0")

            req_tg = urllib.request.Request(
                url_tg, 
                data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            
            try:
                with urllib.request.urlopen(req_tg) as response:
                    if response.getcode() == 200:
                        thread_log = f" (основная ветка)" if is_general_topic else f" (чат #{chat_id})"
                        print(f"[БОТ РОДИТЕЛЕЙ] 🚀 УСПЕХ: Анонс доставлен в канал {channel_id}{thread_log}!")
                        successful_broadcasts += 1
                    else:
                        print(f"[БОТ РОДИТЕЛЕЙ] ⚠️ Предупреждение: Получен статус {response.getcode()} для канала {channel_id}")
            except Exception as e:
                thread_log = f" (чат #{chat_id})" if chat_id > 0 else ""
                print(f"[БОТ РОДИТЕЛЕЙ] ❌ Ошибка сети в канале {channel_id}{thread_log}: {str(e)}")
                send_errors += 1

    if total_broadcasts == 0:
        return True
    elif successful_broadcasts > 0:
        return True
    else:
        print("[БОТ РОДИТЕЛЕЙ] ❌ Ни одно родительское уведомление не удалось доставить из-за ошибок сети.")
        return False
