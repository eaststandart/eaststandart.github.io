#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module ja_tgbot_notify.py
@about 
@purpose 
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

    # 1. АВТО-ПЕРЕХВАТ ДАТЫ ЗАНЯТИЯ ИЗ МАРКДАУНА (Для красивого анонса)
    date_match = re.search(r'Журнал посещений за ([\d.]+ г\.)', markdown_body)
    if date_match:
        formatted_date = date_match.group(1).strip()
    else:
        # Страховочный вариант на случай сбоя re.search
        import datetime
        formatted_date = f"{datetime.date.today().strftime('%d.%m.%Y')} г."

    # 2. РАДАР ПОИСКА МЕДИА-ОБЛОЖКИ (Твой фирменный невидимый хак)
    # Ищем в тексте таблицы самую первую ссылку на детскую поделку
    media_url_match = re.search(r'https://github\.com[^\) \s\|]+', markdown_body)
    if media_url_match:
        media_url = media_url_match.group(0).strip()
        print(f"[БОТ РОДИТЕЛЕЙ] Радар успешно нашел поделку для обложки поста: {media_url}")
    else:
        # Если поделок сегодня не выкладывали, обложкой поста станет сам комментарий Дискуссии
        media_url = comment_url
        print("[БОТ РОДИТЕЛЕЙ] Сегодня поделок нет, обложкой поста назначена ссылка на Дискуссию.")

    # 3. СБОРКА КРАСИВОГО ШАБЛОНА СООБЩЕНИЯ С НЕВИДИМЫМ СИМВОЛОМ &#8203;
    announcement_text = f"📢 Обновлён журнал посещений за {formatted_date}"
    
    # Собираем монолитный макет текста по твоему стандарту
    message_text = (
        f'<a href="{media_url}">&#8203;</a><b>📅 Детско-юношеский инженерный клуб</b>\n\n'
        f'{announcement_text}\n\n'
        f'👀 <a href="{comment_url}">Посмотреть журнал на GitHub Discussions</a>'
    )

    # 4. ДВОЙНОЙ ВЛОЖЕННЫЙ ЦИКЛ РАССЫЛКИ ПО ДРЕВОВИДНОЙ СТРУКТУРЕ (Твой движок отправки)
    print(f"[БОТ РОДИТЕЛЕЙ] Начинаем вещание для древовидного списка групп...")
    send_errors = 0
    total_broadcasts = 0

    for group in public_config:
        chat_id = str(group.get("chat_id", "")).strip()
        thread_ids = group.get("message_thread_id", [])
        
        if not chat_id:
            continue
            
        # Если ветки указаны одиночным числом или строкой, превращаем в список для безопасности
        if isinstance(thread_ids, (int, str)):
            thread_ids = [thread_ids]
        elif not thread_ids:
            # Если список веток пуст, добавляем заглушку 0 (обычное сообщение без топика)
            thread_ids = [0]

        # Внутренний цикл: бежим строго по списку веток конкретного чата!
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
            
            # Если указан реальный номер ветки, принудительно добавляем его в пакет!
            if thread_id > 0:
                payload["message_thread_id"] = thread_id

            # Отправляем JSON-пакет по сети
            req_tg = urllib.request.Request(
                url_tg, 
                data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            
            try:
                with urllib.request.urlopen(req_tg) as response:
                    if response.getcode() == 200:
                        thread_log = f" (ветка #{thread_id})" if thread_id > 0 else ""
                        print(f"[БОТ РОДИТЕЛЕЙ] 🚀 Успех: Анонс доставлен в чат {chat_id}{thread_log}!")
                    else:
                        print(f"[БОТ РОДИТЕЛЕЙ] ⚠️ Предупреждение: Получен статус {response.getcode()} для чата {chat_id}")
            except Exception as e:
                thread_log = f" (ветка #{thread_id})" if thread_id > 0 else ""
                print(f"[БОТ РОДИТЕЛЕЙ] ❌ Ошибка сети в чате {chat_id}{thread_log}: {str(e)}")
                send_errors += 1

    # Возвращаем True диспетчеру, если хотя бы один анонс улетел успешно
    if total_broadcasts > 0 and send_errors < total_broadcasts:
        return True
    else:
        print("[БОТ РОДИТЕЛЕЙ] ❌ Ни одно родительское уведомление не удалось доставить.")
        return False
