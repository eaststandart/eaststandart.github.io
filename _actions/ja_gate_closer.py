#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  ja_gate_closer.py
@about   Финальный шлюзовой модуль закрытия смены
@purpose Сетевое обновление YAML базы расписания и удаление отработанных JSON
@author TechLab
@version 1.0.0
"""

import os
import json
import base64
import requests

DATA_REPO_OWNER = "eaststandart"
DATA_REPO_NAME = "techlab-journal-attendance"

JOURNAL_YML_API_URL = f"https://github.com{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_data"
JOURNAL_JSON_API_URL = f"https://github.com{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_output"

def close_gate_pipeline(reports_list):
    print("\n=== [МОДУЛЬ JA_GATE_CLOSER] ЗАПУСК ЗАКРЫВАТЕЛЯ ШЛЮЗА ===")
    
    # Принудительно берём только административный токен владельца
    admin_token = os.environ.get("MY_ADMIN_TOKEN")
    if not admin_token:
        print("[ЗАКРЫВАТЕЛЬ] ❌ КРИТИЧЕСКАЯ ОШИБКА: Токен MY_ADMIN_TOKEN не найден в системе. Зачистка отменена.")
        return False

    headers_admin = {
        "Authorization": f"token {admin_token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

    for report_item in reports_list:
        teacher_login = report_item.get("teacher_login")
        target_day = report_item.get("target_day")
        yaml_group_updates = report_item.get("yaml_updates", {})
        json_files_to_delete = report_item.get("json_files", [])

        print(f"\n👉 [ШЛЮЗ] Обработка фиксации данных для преподавателя: '{teacher_login}'")

        # ----------------------------------------------------------------------
        # ЭТАП 1: СЕТЕВАЯ ПЕРЕЗАПИСЬ YAML БАЗЫ РАСПИСАНИЯ
        # ----------------------------------------------------------------------
        if yaml_group_updates:
            yaml_api_url = f"{JOURNAL_YML_API_URL}/journal-attendance-{teacher_login}.yml"
            print(f"[ШЛЮЗ] Запрос оригинального YAML по сети: {yaml_api_url}")
            
            res_info = requests.get(yaml_api_url, headers=headers_admin, timeout=30)
            if res_info.status_code == 200:
                res_json = res_info.json()
                yaml_sha = res_json.get("sha")
                
                yaml_content_bytes = base64.b64decode(res_json.get("content", ""))
                orig_lines = yaml_content_bytes.decode('utf-8').split('\n')
                
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
                        
                        final_rows = yaml_group_updates.get(group_time_clean, [])
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

                updated_yaml_text = '\n'.join(new_lines)
                encoded_content = base64.b64encode(updated_yaml_text.encode('utf-8')).decode('utf-8')
                
                put_payload = {
                    "message": f"chore: автоматическое обновление расписания {teacher_login} с сайта",
                    "content": encoded_content,
                    "sha": yaml_sha
                }
                
                res_put = requests.put(yaml_api_url, json=put_payload, headers=headers_admin, timeout=30)
                if res_put.status_code in (200, 201):
                    print(f"[ШЛЮЗ] 🟢 База YAML для {teacher_login} успешно обновлена в репозитории Журнала.")
                else:
                    print(f"[ШЛЮЗ] ❌ Ошибка PUT-запроса YAML: {res_put.status_code}")
            else:
                print(f"[ШЛЮЗ] ⚠️ Не удалось скачать YAML для обновления: {res_info.status_code}")

        # ----------------------------------------------------------------------
        # ЭТАП 2: СЕТЕВОЕ УДАЛЕНИЕ JSON ИЗ ПАПКИ _OUTPUT (РАЗМОРОЗКА ШЛЮЗА)
        # ----------------------------------------------------------------------
        if json_files_to_delete:
            print(f"[ШЛЮЗ] Удаление {len(json_files_to_delete)} отработанных файлов JSON...")
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
                        print(f"[ШЛЮЗ] ⚠️ Не удалось стереть файл {file_name}: {res_del.status_code}")
                else:
                    print(f"[ШЛЮЗ] ⚠️ Файл {file_name} не найден в сети Журнала для удаления.")

    print("=== [МОДУЛЬ JA_GATE_CLOSER] ВСЕ СЕТЕВЫЕ ОПЕРАЦИИ ОЧИСТКИ ЗАВЕРШЕНЫ ===")
    return True
