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
        
        # 1. ИМПОРТ ИЗ ОПЕРАТИВНОЙ ПАМЯТИ PYTHON БЕЗ ПОВТОРНЫХ ЗАПРОСОВ В СЕТЬ
        yaml_group_updates = report_item.get("yaml_group_updates", {})
        yaml_text_orig = report_item.get("yaml_text_orig", "")
        yaml_sha = report_item.get("yaml_sha", "")

        if not yaml_text_orig or not yaml_sha:
            print(f"[ШЛЮЗ] ⚠️ Оригинальные строки YAML или SHA отсутствуют в памяти для {teacher_login}. Пропуск.")
            continue

        print(f"[ШЛЮЗ] Локальная фиксация данных базы расписания преподавателя: '{teacher_login}'")
        yaml_api_url = f"{JOURNAL_YML_API_URL}/journal-attendance-{teacher_login}.yml"

        # 2. ЧИСТАЯ ОБЪЕКТНАЯ ПЕРЕЗАПИСЬ YAML В ОДНУ СТРОКУ БЕЗ ТЕКСТОВЫХ ЦИКЛОВ
        try:
            # Превращаем оригинальный текст расписания в питоновский объект-словарь
            yaml_data = yaml.safe_load(yaml_text_orig) or {}
            
            # Напрямую обновляем измененные часы групп внутри объектного дерева расписания
            if target_day in yaml_data:
                for time_slot, clean_objects_list in yaml_group_updates.items():
                    if time_slot in yaml_data[target_day]:
                        yaml_data[target_day][time_slot] = clean_objects_list

            # Выгружаем структуру обратно в идеальный стерильный текст YAML с сохранением ключей
            updated_yaml_text = yaml.dump(yaml_data, allow_unicode=True, sort_keys=False, default_flow_style=False)
        except Exception as e_yaml:
            print(f"[ШЛЮЗ] ❌ Исключение при объектной сборке YAML: {str(e_yaml)}")
            continue

        # ----------------------------------------------------------------------
        # ПРОВЕРКА НА НАЛИЧИЕ РЕАЛЬНЫХ ИЗМЕНЕНИЙ И СЕТЕВАЯ ОТПРАВКА PUT
        # ----------------------------------------------------------------------
        if updated_yaml_text.strip() == yaml_text_orig.strip():
            print(f"[ШЛЮЗ] ℹ️ Состав групп и порядок строк для {teacher_login} не изменились. Пропуск PUT-запроса YAML.")
        else:
            encoded_content = base64.b64encode(updated_yaml_text.encode('utf-8')).decode('utf-8')
            put_payload = {
                "message": f"chore: автоматическое обновление расписания {teacher_login} с сайта Журнала",
                "content": encoded_content,
                "sha": yaml_sha
            }
            res_put = requests.put(yaml_api_url, json=put_payload, headers=headers_admin, timeout=30)
            if res_put.status_code in (200, 201):
                print(f"[ШЛЮЗ] 🟢 База YAML для {teacher_login} успешно обновлена напрямую по сети через yaml.dump!")
            else:
                print(f"[ШЛЮЗ] ❌ Ошибка PUT-запроса YAML: {res_put.status_code} — {res_put.text}")

        # ----------------------------------------------------------------------
        # REST-УДАЛЕНИЕ ОБРАБОТАННЫХ JSON ИЗ ПАПКИ _OUTPUT (РАЗМОРОЗКА ШЛЮЗА)
        # ----------------------------------------------------------------------
        res_output = requests.get(JOURNAL_JSON_API_URL, headers=headers_admin, timeout=30)
        if res_output.status_code == 200:
            json_files_to_delete = [item["name"] for item in res_output.json() if f"-journal-attendance-{teacher_login}.json" in item["name"].lower()]
            print(f"[ШЛЮЗ] Запуск REST-зачистки {len(json_files_to_delete)} временных файлов JSON из папки _output...")
            
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
        else:
            print(f"[ШЛЮЗ] ⚠️ Не удалось собрать список файлов _output для удаления: {res_output.status_code}")

    print("=== [МОДУЛЬ JA_GATE_CLOSER] ВСЕ СЕТЕВЫЕ ОПЕРАЦИИ ОЧИСТКИ ЗАВЕРШЕНЫ ===")
    return True
