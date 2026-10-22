#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  ja_wabot_personal.py
@about   Модуль отправки персональных отчетов в WhatsApp.
@purpose Формирование сжатого текста журнала и отправка личных уведомлений через GREEN API.
@author  TechLab
@version 1.0.0
"""

import os
import json
import urllib.request
import re

def send_whatsapp_report(markdown_body, target_day, wa_personal_ids):
    print("\n=== [МОДУЛЬ JA_WABOT_PERSONAL] ЗАПУСК WHATSAPP ИНФОРМАТОРА ===")
    
    # 1. Считываем секреты GREEN API из окружения
    id_instance = os.environ.get("GREEN_API_ID", "").strip()
    api_token = os.environ.get("GREEN_API_TOKEN", "").strip()
    
    if not id_instance or not api_token:
        print("[БОТ ВА ЛИЧНЫЙ] ❌ ОШИБКА: Секреты GREEN_API_ID или GREEN_API_TOKEN не найдены!")
        return False

    # 2. Сопоставление и урезание полных дней недели до короткого формата
    day_short_map = {
        "понедельник": "пн",
        "вторник": "вт",
        "среда": "ср",
        "четверг": "чт",
        "пятница": "пт",
        "суббота": "сб",
        "воскресенье": "вс"
    }
    day_suffix = day_short_map.get(target_day.lower().strip(), target_day)

    # 3. ПОСТРОЧНОЕ СЖАТИЕ И АДАПТАЦИЯ ПОД WHATSAPP (Без ссылок, жирный шрифт через *)
    clean_lines = []
    
    for line in markdown_body.split("\n"):
        line_str = line.strip()
        if "| :---" in line_str or "Группа / Ученик" in line_str or "Статус" in line_str:
            continue
            
        if line_str.startswith("|"):
            parts = [p.strip() for p in line_str.split("|") if p.strip()]
            if len(parts) >= 1:
                left_cell = parts[0].replace("**", "")
                if "ГРУППА" in left_cell or "⏰" in left_cell:
                    clean_lines.append(f"\n*{left_cell}*")
                elif len(parts) >= 2:
                    status_cell = parts[1]
                    only_emoji = status_cell[0] if status_cell else "⚪"
                    clean_lines.append(f"{only_emoji} {left_cell}")
                    
        elif "📅" in line_str or "Преподаватель:" in line_str or "Проверил" in line_str:
            if "Журнал посещений за" in line_str:
                # Извлекаем сырую дату занятия и очищаем от скобок
                raw_date_segment = line_str.split("за")[-1].replace("г.", "").replace("###", "").strip()
                date_part = re.sub(r'\(.*?\)', '', raw_date_segment).strip()
                # Чистый заголовок без ссылок, разметка жирности для WhatsApp через звезды
                clean_lines.append(f"📅 *Отчет за {date_part} ({day_suffix})*")
            elif "Преподаватель:" in line_str or "Проверил" in line_str:
                raw_name = line_str.split(":")[-1].replace("*", "").strip()
                clean_lines.append(f"\nПреподаватель: *{raw_name}*")
            else:
                clean_lines.append(line_str)

    message_text = "\n".join([l for l in clean_lines if l.strip()]).strip()

    if not message_text:
        print("[БОТ ВА ЛИЧНЫЙ] ℹ️ Сформированный текст отчета пуст. Выходим.")
        return False

    # 4. ЦИКЛ ОТПРАВКИ ПО СПИСКУ ТЕЛЕФОНОВ ЧЕРЕЗ GREEN API
    print(f"[БОТ ВА ЛИЧНЫЙ] Начинаем отправку для списка номеров: {wa_personal_ids}")
    send_errors = 0

    for phone in wa_personal_ids:
        clean_phone = str(phone).strip()
        if not clean_phone:
            continue
            
        # Автоматически приводим Вариант А к техническому chatId для WhatsApp
        chat_id = f"{clean_phone}@c.us" if "@c.us" not in clean_phone else clean_phone
        
        # URL метода sendMessage в GREEN API
        url_wa = f"https://green-api.com{id_instance}/sendMessage/{api_token}"
        
        payload = {
            "chatId": chat_id,
            "message": message_text
        }

        req_wa = urllib.request.Request(
            url_wa, 
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req_wa) as response:
                if response.getcode() == 200:
                    print(f"[БОТ ВА ЛИЧНЫЙ] 🚀 Успех: Отчёт успешно доставлен на номер {chat_id}!")
                else:
                    print(f"[БОТ ВА ЛИЧНЫЙ] ⚠️ Предупреждение: Получен статус {response.getcode()} для {chat_id}")
        except Exception as e:
            print(f"[БОТ ВА ЛИЧНЫЙ] ❌ Ошибка API при отправке на номер {chat_id}: {str(e)}")
            send_errors += 1

    return send_errors < len(wa_personal_ids)
