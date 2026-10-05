#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module ja_tgbot_notify.py
@about Отправка публичных анонсов для родителей
@purpose Уведомление родителей в группах и ветках со ссылкой на журнал посещений
@author TechLab
@version 1.0.0
"""

import os
import json
import sys
import re
import urllib.request

# Фиксируем базовый адрес Telegram API константой в шапке модуля
TELEGRAM_API_URL = "https://api.telegram.org"

def send_public_notification(markdown_body, comment_url, public_config):
    print("\n=== [МОДУЛЬ JA_TGBOT_NOTIFY] ЗАПУСК РОДИТЕЛЬСКОГО ИНФОРМАТОРА ===")
    
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("[БОТ РОДИТЕЛЕЙ] ❌ КРИТИЧЕСКАЯ ОШИБКА: Секрет TELEGRAM_BOT_TOKEN не найден!")
        return False

    # 1. АВТО-ПЕРЕХВАТ ДАТЫ ЗАНЯТИЯ ИЗ МАРКДАУНА
    date_match = re.search(r'Журнал посещений за ([\d.]+ г\.)', markdown_body)
    if date_match:
        formatted_date = date_match.group(1).strip()
    else:
        import datetime
        formatted_date = f"{datetime.date.today().strftime('%d.%m.%Y')} г."

    # 2. СБОРКА УПРОЩЕННОГО ШАБЛОНА (Невидимая ссылка ведет строго на коммент журнала)
    announcement_text = f"📢 Обновлён журнал посещений за {formatted_date}"
    
    message_text = (
        f'<a href="{comment_url}">&#8203;</a><b>📅 Детско-юношеский инженерный клуб</b>\n\n'
        f'{announcement_text}\n\n'
        f'👀 <a href="{comment_url}">Посмотреть журнал на GitHub Discussions</a>'
    )

    # 3. ДВОЙНОЙ ВЛОЖЕННЫЙ ЦИКЛ РАССЫЛКИ ПО ГРУППАМ И ВЕТКАМ РОДИТЕЛЕЙ
    print(f"[БОТ РОДИТЕЛЕЙ] Начинаем вещание для древовидного списка групп...")
    send_errors = 0
    total_broadcasts = 0

    for group in public_config:
        chat_id = str(group.get("chat_id", "")).strip()
        thread_ids = group.get("message_thread_id", [])
        
        if not chat_id:
            continue
            
        if isinstance(thread_ids, (int, str)):
            thread_ids = [thread_ids]
        elif not thread_ids:
            thread_ids = [0]

        for thread in thread_ids:
            thread_id = int(str(thread).strip())
            total_broadcasts += 1
            
            url_tg = f"{TELEGRAM_API_URL}/bot{token}/sendMessage"
            
            payload = {
                "chat_id": chat_id,
                "text": message_text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
            
            if thread_id > 0:
                payload["message_thread_id"] = thread_id

            req_tg = urllib.request.Request(
                url_tg, 
                data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            
            try:
                with urllib.request.urlopen(req_tg) as response:
                    if response.getcode() == 200:
                        thread_log = f" (ветка #{thread_id})" if thread_id > 0 else ""
                        print(f"[БОТ РОДИТЕЛЕЙ] 🚀 УСПЕХ: Анонс доставлен в чат {chat_id}{thread_log}!")
                    else:
                        print(f"[БОТ РОДИТЕЛЕЙ] ⚠️ Предупреждение: Получен статус {response.getcode()} для чата {chat_id}")
            except Exception as e:
                thread_log = f" (ветка #{thread_id})" if thread_id > 0 else ""
                print(f"[БОТ РОДИТЕЛЕЙ] ❌ Ошибка сети в чате {chat_id}{thread_log}: {str(e)}")
                send_errors += 1

    if total_broadcasts > 0 and send_errors < total_broadcasts:
        return True
    else:
        print("[БОТ РОДИТЕЛЕЙ] ❌ Ни одно родительское уведомление не удалось доставить.")
        return False
