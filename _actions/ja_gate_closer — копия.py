#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  ja_gate_closer.py
@about   Шлюзовой модуль закрытия смены
@purpose Сетевое обновление YAML базы расписания и удаление отработанных JSON
@author  TechLab
@version 1.0.0
"""

import os
import json
import yaml
import base64
import re
import requests

DATA_REPO_OWNER = "eaststandart"
DATA_REPO_NAME = "techlab-journal-attendance"

JOURNAL_YML_API_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_data"
JOURNAL_JSON_API_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_output"

def close_gate_pipeline(reports_list):
    print("\n=== [МОДУЛЬ JA_GATE_CLOSER] ЗАПУСК ЗАКРЫВАТЕЛЯ ШЛЮЗА ===")
    
    admin_token = os.environ.get("MY_ADMIN_TOKEN")
    if not admin_token:
        print("[ЗАКРЫВАТЕЛЬ] ❌ КРИТИЧЕСКАЯ ОШИБКА: Токен MY_ADMIN_TOKEN не найден. Зачистка отменена.")
        return False

    headers_admin = {
        "Authorization": f"token {admin_token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

    for report_item in reports_list:
        teacher_login = report_item.get("teacher_login")
        target_day = report_item.get("day")
        
        print(f"\n👉 [ШЛЮЗ] Обработка фиксации данных для преподавателя: '{teacher_login}'")

        yaml_api_url = f"{JOURNAL_YML_API_URL}/journal-attendance-{teacher_login}.yml"
        
        res_info = requests.get(yaml_api_url, headers=headers_admin, timeout=30)
        if res_info.status_code != 200:
            print(f"[ШЛЮЗ] ⚠️ Не удалось получить YAML для обновления: {res_info.status_code}")
            continue

        res_json = res_info.json()
        yaml_sha = res_json.get("sha")
        yaml_content_bytes = base64.b64decode(res_json.get("content", ""))
        orig_lines = yaml_content_bytes.decode('utf-8').split('\n')
        yaml_data = yaml.safe_load(yaml_content_bytes.decode('utf-8')) or {}

        # 1. СНАЧАЛА ГАРАНТИРОВАННО И БЕЗ ОШИБОК СОБИРАЕМ КАРТУ РАСПИСАНИЯ
        students_data = {}
        for key, value in yaml_data.items():
            if key == 'config':
                continue
            day_name = str(key).lower().strip()
            students_data[day_name] = {}
            if isinstance(value, dict):
                for raw_time, kids_list in value.items():
                    clean_time_str = str(raw_time).strip()
                    match_time = re.search(r'(\d{1,2})\D*(\d{2})', clean_time_str)
                    if match_time:
                        normalized_time = f"{match_time.group(1)}:{match_time.group(2)}"
                        students_data[day_name][normalized_time] = kids_list if isinstance(kids_list, list) else []
                    else:
                        students_data[day_name][clean_time_str] = kids_list if isinstance(kids_list, list) else []

        # 2. ТЕПЕРЬ ОБЪЯВЛЯЕМ ОРИГИНАЛЬНЫЕ ФУНКЦИИ ОБРАБОТКИ СТРОК YAML 1 В 1 ИЗ ГЕНЕРАТОРА
        def translit_rus_to_lat(text):
            rus = "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я".split()
            lat = "a b v g d e yo zh z i y k l m n o p r s t у f kh ts ch sh shch  y  e yu ya".split()
            res = ""
            lower_text = text.lower()
            for char in lower_text:
                if char in rus:
                    res += lat[rus.index(char)]
                elif char in [" ", "-"]:
                    res += "-"
                elif char.isalnum() or char == "_":
                    res += char
            return re.sub(r'-+', '-', res).strip('-')

        def process_kid_row(raw_name, status_text):
            track = ""
            match_ready = re.search(r'(@[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+)', raw_name)
            target_tag = match_ready.group(0) if match_ready else ""
            need_auto_generate = not target_tag and "#" in raw_name
            normalized = raw_name.replace("[c]", "[с]").replace("[C]", "[с]").replace('"', '').strip()
            if "[э]" in normalized.lower():
                track = "электроника"
            elif "[с]" in normalized.lower():
                track = "столярное"
            if need_auto_generate:
                name_for_tag = normalized.replace("[э]", "").replace("[с]", "").replace("[Э]", "").replace("[С]", "").replace("#", "").strip()
                name_for_tag = re.sub(r'\s+', ' ', name_for_tag).strip()
                target_tag = f"#techlab-{translit_rus_to_lat(name_for_tag)}"
                normalized = normalized.replace("#", target_tag).strip()
            print_name = normalized.replace('"', '')
            print_name = re.sub(r'\[э\]|\[с\]', '', print_name, flags=re.IGNORECASE)
            print_name = re.sub(r'(@[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+)', '', print_name)
            print_name = re.sub(r'\s+', ' ', print_name).strip()
            direction_suffix = " [э]" if track == "электроника" else " [с]" if track == "столярное" else ""
            tag_suffix = f" {target_tag}" if target_tag else ""
            final_yaml_line = f"{print_name}{direction_suffix}{tag_suffix}"
            return {"name_for_sort": print_name, "yaml_line": final_yaml_line}

        # 3. ЗАПРАШИВАЕМ СПИСОК JSON-ФАЙЛОВ ИЗ СЕТИ С ЖЕСТКИМ ОТСТУПОМ ПРОГРАММЫ
        print(f"[ШЛЮЗ] Запрос списка JSON-файлов из _output Журнала...")
        res_output = requests.get(JOURNAL_JSON_API_URL, headers=headers_admin, timeout=30)
        if res_output.status_code != 200:
            print(f"[ШЛЮЗ] ❌ Ошибка получения списка файлов: {res_output.status_code}")
            continue

        json_files_to_delete = [item["name"] for item in res_output.json() if f"-journal-attendance-{teacher_login}.json" in item["name"].lower()]
        print(f"[ШЛЮЗ] Обнаружено файлов для обработки ({len(json_files_to_delete)} шт.): {json_files_to_delete}")

        if not json_files_to_delete:
            continue

        # 4. ЧТЕНИЕ ВНУТРЕННОСТЕЙ JSON И СБОРКА ОБНОВЛЕНИЙ ПО ОРИГИНАЛЬНОМУ ДВИЖКУ
        temp_journal = {}
        for file_name in json_files_to_delete:
            try:
                file_url = f"{JOURNAL_JSON_API_URL}/{file_name}"
                file_data = requests.get(file_url, headers=headers_admin, timeout=30).json()
                js_bytes = base64.b64decode(file_data.get("content", ""))
                js_obj = json.loads(js_bytes.decode('utf-8'))
                temp_journal[js_obj["time"]] = js_obj
            except Exception:
                continue

        schedule_groups = sorted(list(students_data.get(target_day, {}).keys()))
        yaml_group_updates = {}

        # 5. ОРИГИНАЛЬНАЯ ЛОГИКА СОРТИРОВКИ И УПАКОВКИ YAML 1 В 1 ИЗ СТАРОГО ГЕНЕРАТОРА
        for time_key in schedule_groups:
            group_payload = temp_journal.get(time_key, {"present_permanent": [], "newbies": [], "probation": []})
            permanent_kids = students_data.get(target_day, {}).get(time_key, [])
            current_group_yaml_rows = []
            
            for kid in permanent_kids:
                processed = process_kid_row(kid, "")
                current_group_yaml_rows.append(processed["yaml_line"])
                
            for newbie in group_payload.get("newbies", []):
                if newbie.strip():
                    processed = process_kid_row(newbie, "🟡 Новичок")
                    current_group_yaml_rows.append(processed["yaml_line"])
                    
            current_group_yaml_rows.sort(key=lambda x: re.sub(r'\[э\]|\[с\]|@[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+', '', x, flags=re.IGNORECASE).strip().lower())
            yaml_group_updates[time_key] = current_group_yaml_rows

        # 6. ОРИГИНАЛЬНЫЙ ЦИКЛ ПОСТРОЧНОЙ ПЕРЕЗАПИСИ ТЕКСТА YAML 1 В 1 ИЗ СТАРОГО ГЕНЕРАТОРА
        new_lines = []
        inside_day = False
        idx = 0
        while idx < len(orig_lines):
            line = orig_lines[idx]
            trimmed = line.rstrip()
            indent = len(line) - len(line.lstrip())
            
            if indent == 0 and trimmed.endswith(':'):
                inside_day = (trimmed[:-1].lower().strip() == target_day)
                new_lines.append(line)
                idx += 1
                continue
                
            if inside_day and indent == 2 and trimmed.endswith(':'):
                group_time_clean = trimmed.strip().strip(':').strip('"').strip("'").strip()
                new_lines.append(line)
                
                final_rows = yaml_group_updates.get(group_time_clean, students_data.get(target_day, {}).get(group_time_clean, []))
                for kid_line in final_rows:
                    clean_row = kid_line.replace('"', '').replace("'", "").strip()
                    new_lines.append(f'    - "{clean_row}"')
                    
                while idx + 1 < len(orig_lines):
                    next_line = orig_lines[idx + 1]
                    if (len(next_line) - len(next_line.lstrip())) == 4 and next_line.strip().startswith('-'):
                        idx += 1
                    else:
                        break
                idx += 1
                continue
                
            new_lines.append(line)
            idx += 1

        # ----------------------------------------------------------------------
        # СЕТЕВАЯ ОТПРАВКА ОБНОВЛЕННОГО YAML
        # ----------------------------------------------------------------------
        updated_yaml_text = '\n'.join(new_lines)
        encoded_content = base64.b64encode(updated_yaml_text.encode('utf-8')).decode('utf-8')
        
        put_payload = {
            "message": f"chore: автоматическое обновление расписания {teacher_login} с сайта",
            "content": encoded_content,
            "sha": yaml_sha
        }
        
        res_put = requests.put(yaml_api_url, json=put_payload, headers=headers_admin, timeout=30)
        if res_put.status_code in (200, 201):
            print(f"[ШЛЮЗ] 🟢 База YAML для {teacher_login} успешно обновлена напрямую по сети!")
        else:
            print(f"[ШЛЮЗ] ❌ Ошибка PUT-запроса YAML: {res_put.status_code}")

        # ----------------------------------------------------------------------
        # СЕТЕВОЕ УДАЛЕНИЕ JSON ИЗ ПАПКИ _OUTPUT (РАЗМОРОЗКА ШЛЮЗА)
        # ----------------------------------------------------------------------
        print(f"[ШЛЮЗ] Запуск REST-зачистки {len(json_files_to_delete)} файлов JSON...")
        for file_name in json_files_to_delete:
            file_api_url = f"{JOURNAL_JSON_API_URL}/{file_name}"
            res_file = requests.get(file_api_url, headers=headers_admin, timeout=30)
            if res_file.status_code == 200:
                file_sha = res_file.json().get("sha")
                delete_payload = {
                    "message": f"Delete _output processed file {file_name}",
                    "sha": file_sha
                }
                res_del = requests.delete(file_api_url, json=delete_payload, headers=headers_admin, timeout=30)
                if res_del.status_code == 200:
                    print(f"[ШЛЮЗ] 🟢 Файл {file_name} успешно стёрт из _output Журнала!")

    print("=== [МОДУЛЬ JA_GATE_CLOSER] ВСЕ СЕТЕВЫЕ ОПЕРАЦИИ ОЧИСТКИ ЗАВЕРШЕНЫ ===")
    return True
