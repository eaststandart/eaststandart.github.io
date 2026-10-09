#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  ja_data_parser.py
@about   Сетевой парсер и сборщик сырых данных Журнала
@purpose Загрузка JSON, YAML и лечение опечаток времени напрямую по API Гитхаба
@author TechLab
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

def collect_and_parse_raw_data():
    print("\n=== [МОДУЛЬ 1: СЕТЕВОЙ ПАРСЕР] СБОР СЫРЫХ ДАННЫХ ИЗ API ===")
    
    admin_token = os.environ.get("MY_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {admin_token}", "Accept": "application/vnd.github+json"}

    # 1. АВТО-ПОИСК ЖИВЫХ ЛОГИНОВ ПРЕПОДАВАТЕЛЕЙ НАПРЯМУЮ ИЗ СЕТИ ЖУРНАЛА
    active_teachers = []
    try:
        res_yml_list = requests.get(JOURNAL_YML_API_URL, headers=headers, timeout=30)
        if res_yml_list.status_code == 200:
            for item in res_yml_list.json():
                f = item["name"]
                if f.startswith('journal-attendance-') and f.endswith('.yml'):
                    login = f.replace('journal-attendance-', '').replace('.yml', '').strip().lower()
                    if login:
                        active_teachers.append(login)
    except Exception as e_yml:
        print(f"[ПАРСЕР] ⚠️ Не удалось собрать список преподавателей по сети: {str(e_yml)}")
        return None

    print(f"[ПАРСЕР] Список active преподавателей из базы YML: {active_teachers}")

    # 2. СБОР ВСЕХ ПРИЛЕТЕВШИХ JSON ФАЙЛОВ ГРУПП ИЗ СЕТИ
    try:
        response = requests.get(JOURNAL_JSON_API_URL, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"[ПАРСЕР] Временные файлы журналов в папке _output отсутствуют (Код API: {response.status_code}). Выход.")
            return None
            
        output_contents = response.json()
        json_download_urls = {item["name"]: item["download_url"] for item in output_contents if '-journal-attendance-' in item["name"] and item["name"].endswith('.json')}
        all_json_files = list(json_download_urls.keys())
        
    except Exception as err:
        print(f"[ПАРСЕР] ❌ Ошибка сетевого запроса к _output Журнала: {str(err)}")
        return None

    if not all_json_files:
        print("[ПАРСЕР] Временные файлы журналов групп в папке _output отсутствуют. Выход.")
        return None

    print(f"[ПАРСЕР] Обнаружено JSON-файлов в сети Журнала (_output): {len(all_json_files)} шт.")
    parsed_teachers_package = {}

    # ЗАПУСКАЕМ ИЗОЛИРОВАННЫЙ ЦИКЛ СБОРА ПО КАЖДОМУ ПРЕПОДАВАТЕЛЮ
    for current_teacher in active_teachers:
        teacher_json_files = [f for f in all_json_files if f.lower().endswith(f"-journal-attendance-{current_teacher}.json")]
        
        if not teacher_json_files:
            continue
            
        print(f"\n👉 [ПАРСЕР ЦИКЛ] Найдена пачка файлов для преподавателя: '{current_teacher}' ({len(teacher_json_files)} шт.)")

        try:
            sample_download_url = json_download_urls[teacher_json_files[0]]
            sample_data = requests.get(sample_download_url, headers=headers, timeout=30).json()
        except Exception as e:
            print(f"[ПАРСЕР] ❌ Ошибка интернет-чтения файла {teacher_json_files[0]}: {str(e)}")
            continue
            
        target_day = sample_data.get('day', '').lower().strip()
        date_str = sample_data.get('date', '')
        teacher_username = sample_data.get('teacher_username', 'Преподаватель')
        teacher_login = current_teacher  

        file_api_url = f"{JOURNAL_YML_API_URL}/journal-attendance-{teacher_login}.yml"
        write_token = os.environ.get("JOURNAL_WRITE_TOKEN")

        headers_pub = {
            "Authorization": f"token {write_token if write_token else admin_token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json"
        }

        res_info = requests.get(file_api_url, headers=headers_pub, timeout=30)
        if res_info.status_code != 200:
            print(f"[ПАРСЕР] ⚠️ Не удалось получить YAML с GitHub для {teacher_login}: {res_info.status_code}")
            continue

        res_json = res_info.json()
        yaml_sha = res_json.get("sha")

        yaml_content_bytes = base64.b64decode(res_json.get("content", ""))
        yaml_text_orig = yaml_content_bytes.decode('utf-8')
        yaml_data = yaml.safe_load(yaml_text_orig) or {}

        # === ЖЕСТКИЙ ВХОДНОЙ ЩИТ: АВТО-ИСПРАВЛЕНИЕ ВРЕМЕНИ В ФАЙЛЕ НА СТАРТЕ ===
        students_data = {}
        file_needs_repair = False
        updated_yaml_text = yaml_text_orig

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
                        
                        if clean_time_str != normalized_time:
                            print(f"[ПАРСЕР РЕДАКТОР] Найдена опечатка '{clean_time_str}'. Заменяем на '{normalized_time}'")
                            updated_yaml_text = updated_yaml_text.replace(f"'{clean_time_str}':", f'"{normalized_time}":')
                            updated_yaml_text = updated_yaml_text.replace(f'"{clean_time_str}":', f'"{normalized_time}":')
                            updated_yaml_text = updated_yaml_text.replace(f"{clean_time_str}:", f'"{normalized_time}":')
                            file_needs_repair = True
                    else:
                        students_data[day_name][clean_time_str] = kids_list if isinstance(kids_list, list) else []

        if file_needs_repair:
            try:
                encoded_repair = base64.b64encode(updated_yaml_text.encode('utf-8')).decode('utf-8')
                repair_payload = {
                    "message": f"fix: автоматическое исправление опечаток времени для {teacher_login}",
                    "content": encoded_repair,
                    "sha": yaml_sha
                }
                res_repair = requests.put(file_api_url, json=repair_payload, headers=headers_pub, timeout=30)
                if res_repair.status_code in (200, 201):
                    print(f"[ПАРСЕР РЕДАКТОР] 🟢 Файл расписания для {teacher_login} успешно вылечен напрямую по сети!")
                    yaml_sha = res_repair.json().get("content", {}).get("sha", yaml_sha)
                else:
                    print(f"[ПАРСЕР РЕДАКТОР] ❌ Не удалось отправить вылеченный YAML по сети: {res_repair.status_code}")
            except Exception as e_repair:
                print(f"[ПАРСЕР РЕДАКТОР] ⚠️ Исключение при сетевом лечении YAML: {str(e_repair)}")
        config_data = yaml_data.get('config', {})
        publish_as_bot = config_data.get('publish_as_bot', False)
        show_projects_column = config_data.get('show_projects_column', True)
        discussion_number = config_data.get('discussion_number', 38)
        
        raw_categories = config_data.get('project_category_name', ['Галерея'])
        project_categories = [raw_categories] if isinstance(raw_categories, str) else raw_categories

        # ЧТЕНИЕ СЫРЫХ ВНУТРЕННОСТЕЙ JSON ИЗ СЕТИ ДЛЯ СЛЕДУЮЩЕГО МОДУЛЯ
        temp_journal = {}
        for file in teacher_json_files:
            try:
                file_url = json_download_urls[file]
                file_data = requests.get(file_url, headers=headers, timeout=30).json()
                temp_journal[file_data["time"]] = file_data
            except Exception as e:
                print(f"[ПАРСЕР] ❌ Ошибка интернет-чтения файла {file}: {str(e)}")
                continue

        # УПАКОВКА АБСОЛЮТНО ЧИСТЫХ ДАННЫХ ПРЕПОДАВАТЕРА В ПАКЕТ
        parsed_teachers_package[teacher_login] = {
            "teacher_login": teacher_login,
            "teacher_username": teacher_username,
            "target_day": target_day,
            "date_str": date_str,
            "publish_as_bot": publish_as_bot,
            "show_projects_column": show_projects_column,
            "discussion_number": discussion_number,
            "project_categories": project_categories,
            "students_data": students_data,
            "temp_journal": temp_journal,
            "teacher_json_files": teacher_json_files
        }
        print(f"[ПАРСЕР] 🟢 Данные для '{teacher_login}' успешно собраны по сети и упакованы.")

    print("=== [МОДУЛЬ 1: ПАРСЕР] СБОР ДАННЫХ ПО ВСЕМ УЧИТЕЛЯМ ЗАВЕРШЕН ===")
    return parsed_teachers_package

