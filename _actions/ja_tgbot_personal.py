import os
import json
import sys
import urllib.request

# Фиксируем базовый адрес Telegram API константой в шапке модуля
TELEGRAM_API_URL = "https://api.telegram.org"

def send_personal_report(markdown_body, comment_url, target_day, personal_ids):
    print("\n=== [МОДУЛЬ JA_TGBOT_PERSONAL] ЗАПУСК ПЕРСОНАЛЬНОГО ИНФОРМАТОРА ===")
    
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("[ЛИЧНЫЙ БОТ] ❌ КРИТИЧЕСКАЯ ОШИБКА: Секрет TELEGRAM_BOT_TOKEN не найден в окружении!")
        return False

    # 1. Сопоставление и урезание полных дней недели до короткого формата
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

    # 2. ПОСТРОЧНОЕ СЖАТИЕ МАРКДАУН-ТАБЛИЦЫ (Твоя оригинальная логика 1 в 1)
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
                    clean_lines.append(f"\n<b>{left_cell}</b>")
                elif len(parts) >= 2:
                    status_cell = parts[1]
                    only_emoji = status_cell[0] if status_cell else "⚪"
                    clean_lines.append(f"{only_emoji} {left_cell}")
                    
        elif "📅" in line_str or "Преподаватель:" in line_str or "Проверил" in line_str:
            if "Журнал посещений за" in line_str:
                # Извлекаем дату и превращаем заголовок в кликабельную HTML ссылку на коммент!
                date_part = line_str.split("за")[-1].replace("г.", "").replace("###", "").strip()
                clean_lines.append(f'📅 <a href="{comment_url}">Отчет за {date_part} ({day_suffix})</a>')
            elif "Преподаватель:" in line_str or "Проверил" in line_str:
                raw_name = line_str.split(":")[-1].replace("*", "").strip()
                clean_lines.append(f"\nПреподаватель: <b>{raw_name}</b>")
            else:
                clean_lines.append(line_str)

    message_text = "\n".join([l for l in clean_lines if l.strip()]).strip()

    if not message_text:
        print("[ЛИЧНЫЙ БОТ] ℹ️ Сформированный текст сжатого отчета пуст. Выходим.")
        return False

    # 3. ЦИКЛ РАССЫЛКИ ПО ОТКРЫТОМУ СПИСКУ ID ИЗ YAML (Твой движок отправки)
    print(f"[ЛИЧНЫЙ БОТ] Начинаем отправку для списка пользователей: {personal_ids}")
    send_errors = 0

    for chat_id in personal_ids:
        target_id = str(chat_id).strip()
        if not target_id:
            continue
            
        # Формируем адрес запроса к Telegram API на основе константы из шапки
        url_tg = f"{TELEGRAM_API_URL}/bot{token}/sendMessage"
        
        payload = {
            "chat_id": target_id,
            "text": message_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }

        # Отправляем JSON-пакет по сети
        req_tg = urllib.request.Request(
            url_tg, 
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req_tg) as response:
                if response.getcode() == 200:
                    print(f"[ЛИЧНЫЙ БОТ] 🚀 Успех: Отчёт успешно доставлен пользователю {target_id}!")
                else:
                    print(f"[ЛИЧНЫЙ БОТ] ⚠️ Предупреждение: Получен статус {response.getcode()} для {target_id}")
        except Exception as e:
            print(f"[ЛИЧНЫЙ БОТ] ❌ Ошибка сети при отправке пользователю {target_id}: {str(e)}")
            send_errors += 1

    # Возвращаем True диспетчеру, если хотя бы одно сообщение улетело успешно
    if send_errors < len(personal_ids):
        return True
    else:
        print("[ЛИЧНЫЙ БОТ] ❌ Ни одно личное сообщение не удалось доставить.")
        return False
