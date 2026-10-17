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
        
        # 1. СНАЙПЕРСКИЙ ИМПОРТ ИЗ ОПЕРАТИВНОЙ ПАМЯТИ PYTHON БЕЗ ПОВТОРНЫХ ЗАПРОСОВ В СЕТЬ
        yaml_group_updates = report_item.get("yaml_group_updates", {})
        yaml_text_orig = report_item.get("yaml_text_orig", "")
        yaml_sha = report_item.get("yaml_sha", "")

        if not yaml_text_orig or not yaml_sha:
            print(f"[ШЛЮЗ] ⚠️ Оригинальные строки YAML или SHA отсутствуют в памяти для {teacher_login}. Пропуск.")
            continue

        print(f"[ШЛЮЗ] Построчно обновляем базу расписания преподавателя: '{teacher_login}'")
        yaml_api_url = f"{JOURNAL_YML_API_URL}/journal-attendance-{teacher_login}.yml"
        orig_lines = yaml_text_orig.split('\n')

        # 2. ЗРЯЧИЙ ПОСТРОЧНЫЙ ЦИКЛ ОБНОВЛЕНИЯ С СОХРАНЕНИЕМ 100% КОММЕНТАРИЕВ И ОТСТУПОВ
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
                
                # Забираем отсортированные объекты из памяти и формируем идеальный многострочный YAML
                final_rows = yaml_group_updates.get(group_time_clean, [])
                
                # Принудительная алфавитная сортировка объектов Журнала прямо перед записью в файл
                if isinstance(final_rows, list):
                    final_rows.sort(key=lambda x: x.get("name", "").lower() if isinstance(x, dict) else str(x).lower())

                for kid_obj in final_rows:
                    if isinstance(kid_obj, dict):
                        new_lines.append(f"    - name: \"{kid_obj.get('name', '').strip()}\"")
                        if kid_obj.get("direction"):
                            new_lines.append(f"      direction: \"{kid_obj.get('direction').strip()}\"")
                        if kid_obj.get("tag"):
                            new_lines.append(f"      tag: \"{kid_obj.get('tag').strip()}\"")
                
                # Полностью вычищаем и пропускаем весь старый блок многострочной структуры группы
                while idx + 1 < len(orig_lines):
                    next_line = orig_lines[idx + 1]
                    next_trimmed = next_line.rstrip()
                    if not next_trimmed:
                        idx += 1
                        continue
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent >= 4:
                        idx += 1
                    else:
                        break
                idx += 1
                continue
                
            new_lines.append(line)
            idx += 1

        updated_yaml_text = '\n'.join(new_lines)

        # ----------------------------------------------------------------------
        # ПРОВЕРКА НА ИЗМЕНЕНИЯ И СЕТЕВАЯ ОТПРАВКА PUT
        # ----------------------------------------------------------------------
        if updated_yaml_text.strip() == yaml_text_orig.strip():
            print(f"[ШЛЮЗ] ℹ️ Состав групп для {teacher_login} не изменился. Пропуск PUT-запроса YAML.")
        else:
            encoded_content = base64.b64encode(updated_yaml_text.encode('utf-8')).decode('utf-8')
            put_payload = {
                "message": f"chore: автоматическое обновление расписания {teacher_login} с сайта Журнала",
                "content": encoded_content,
                "sha": yaml_sha
            }
            res_put = requests.put(yaml_api_url, json=put_payload, headers=headers_admin, timeout=30)
            if res_put.status_code in (200, 201):
                print(f"[ШЛЮЗ] 🟢 База YAML для {teacher_login} успешно обновлена построечно с сохранением структуры!")
            else:
                print(f"[ШЛЮЗ] ❌ Ошибка PUT-запроса YAML: {res_put.status_code} — {res_put.text}")

        # ----------------------------------------------------------------------
        # REST-УДАЛЕНИЕ ОБРАБОТАННЫХ JSON ИЗ ПАПКИ _OUTPUT (РАЗМОРОЗКА ШЛЮЗА)
        # ----------------------------------------------------------------------
        res_output = requests.get(JOURNAL_JSON_API_URL, headers=headers_admin, timeout=30)
        if res_output.status_code == 200:
            json_files_to_delete = [item["name"] for item in res_output.json() if f"-journal-attendance-{teacher_login}.json" in item["name"].lower()]
            print(f"[ШЛЮЗ] Запуск REST-зачистки {len(json_files_to_delete)} файлов JSON из папки _output...")
            
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
