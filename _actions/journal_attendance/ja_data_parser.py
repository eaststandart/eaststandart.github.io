#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  ja_data_parser.py
@about   Модуль сетевого парсинга и сборщика отчетов.
@purpose Загрузка JSON, YAML и транзит плоских структур для генератора отчетов.
@author  TechLab
@version 1.0.0
"""

import os
import json
import yaml
import base64
import requests

DATA_REPO_OWNER = "eaststandart"
DATA_REPO_NAME = "techlab-journal-attendance"

JOURNAL_YML_API_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_data"
JOURNAL_JSON_API_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_output"

def collect_and_parse_raw_data():
    print("\n=== [МОДУЛЬ: ПАРСЕР] СБОР ДАННЫХ ИЗ API ===")
    
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
            
        print(f"[ПАРСЕР] Найдена пачка файлов для преподавателя: '{current_teacher}' ({len(teacher_json_files)} шт.)")

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
        yaml_content_bytes = base64.b64decode(res_json.get("content", ""))
        yaml_text_orig = yaml_content_bytes.decode('utf-8')
        
        yaml_data = yaml.safe_load(yaml_text_orig) or {}

        # ПОСТРОЧНЫЙ СБОР КАРТЫ РАСПИСАНИЯ В ПАМЯТЬ PYTHON ДЛЯ ТРАНЗИТА
        students_data = {}
        for key, value in yaml_data.items():
            if key == 'config':
                continue
            day_name = str(key).lower().strip()
            students_data[day_name] = {}
            
            if isinstance(value, dict):
                for raw_time, kids_list in value.items():
                    clean_time_str = str(raw_time).strip()
                    students_data[day_name][clean_time_str] = kids_list if isinstance(kids_list, list) else []

        config_data = yaml_data.get('config', {})
        publish_as_bot = config_data.get('publish_as_bot', False)
        show_projects_column = config_data.get('show_projects_column', True)
        discussion_number = config_data.get('discussion_number', 38)
        
        raw_categories = config_data.get('project_category_name', ['Галерея'])
        project_categories = [raw_categories] if isinstance(raw_categories, str) else raw_categories

        # ЧТЕНИЕ СЫРЫХ ВНУТРЕННОСТЕЙ JSON ИЗ СЕТИ БЕЗ ИЗМЕНЕНИЙ СТРУКТУРЫ
        temp_journal = {}
        for file in teacher_json_files:
            try:
                file_url = json_download_urls[file]
                file_data = requests.get(file_url, headers=headers, timeout=30).json()
                temp_journal[file_data["time"]] = file_data
            except Exception as e:
                print(f"[ПАРСЕР] ❌ Ошибка интернет-чтения файла {file}: {str(e)}")
                continue

        # УПАКОВКА ДАННЫХ ПРЕПОДАВАТЕЛЯ В ПАКЕТ
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
            "teacher_json_files": teacher_json_files,
            "yaml_text_orig": yaml_text_orig,
            "yaml_sha": res_json.get("sha", "")
        }

    print("=== [МОДУЛЬ: ПАРСЕР] СБОР ДАННЫХ ЗАВЕРШЕН ===")
    return parsed_teachers_package
