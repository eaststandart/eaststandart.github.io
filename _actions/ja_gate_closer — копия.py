#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  ja_gate_closer.py
@about   Финальный шлюзовой модуль закрытия смены
@purpose Сетевое обновление YAML базы расписания и удаление отработанных JSON
@author  TechLab
@version 1.0.0
"""

import os
import json
import base64
import requests

DATA_REPO_OWNER = "eaststandart"
DATA_REPO_NAME = "techlab-journal-attendance"

JOURNAL_YML_API_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_data"
JOURNAL_JSON_API_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_output"

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
        target_day = report_item.get("day")  # Берём имя дня напрямую из оригинального пакета
        
        # Автоматически восстанавливаем массивы обновлений из внутренностей генератора
        yaml_group_updates = report_item.get("markdown") # Текст отчета
        
        print(f"\n👉 [ШЛЮЗ] Обработка фиксации данных для преподавателя: '{teacher_login}'")

        # ----------------------------------------------------------------------
        # ЭТАП 1: СЕТЕВАЯ ПЕРЕЗАПИСЬ YAML БАЗЫ РАСПИСАНИЯ ЧЕРЕЗ API
        # ----------------------------------------------------------------------
        yaml_api_url = f"{JOURNAL_YML_API_URL}/journal-attendance-{teacher_login}.yml"
        print(f"[ШЛЮЗ] Запрос оригинального YAML по сети: {yaml_api_url}")
        
        res_info = requests.get(yaml_api_url, headers=headers_admin, timeout=30)
        if res_info.status_code == 200:
            res_json = res_info.json()
            yaml_sha = res_json.get("sha")
            
            yaml_content_bytes = base64.b64decode(res_json.get("content", ""))
            orig_lines = yaml_content_bytes.decode('utf-8').split('\n')
            
            # Сканируем репозиторий Журнала через API для сбора точного списка JSON
            # Так как мы не меняли генератор, Модуль Б сам соберёт имена файлов из сети
            # Открытый диагностический запрос списка файлов в сети Журнала
            print(f"[ШЛЮЗ] Запрос списка JSON-файлов из _output Журнала...")
            res_output = requests.get(JOURNAL_JSON_API_URL, headers=headers_admin, timeout=30)
            print(f"[ШЛЮЗ] Ответ сервера GitHub: {res_output.status_code}")

            if res_output.status_code == 200:
                json_files_to_delete = [item["name"] for item in res_output.json() if f"-journal-attendance-{teacher_login}.json" in item["name"].lower()]
                print(f"[ШЛЮЗ] Обнаружено файлов для обработки ({len(json_files_to_delete)} шт.): {json_files_to_delete}")
            else:
                print(f"[ШЛЮЗ] ❌ Ошибка получения списка файлов: {res_output.status_code}")
                json_files_to_delete = []

            # Если файлы найдены, извлекаем из них локальные структуры обновлений расписания
            # Это позволяет Модулю Б работать автономно, вообще не трогая код старого генератора!
            yaml_group_updates_local = {}
            for file_name in json_files_to_delete:
                try:
                    file_url = f"{JOURNAL_JSON_API_URL}/{file_name}"
                    file_data = requests.get(file_url, headers=headers_admin, timeout=30).json()
                    # Декодируем содержимое JSON из base64
                    js_bytes = base64.b64decode(file_data.get("content", ""))
                    js_obj = json.loads(js_bytes.decode('utf-8'))
                    
                    # Собираем строки учеников по маске оригинального редактора
                    time_key = js_obj.get("time")
                    present_kids = js_obj.get("present_permanent", [])
                    newbies_kids = js_obj.get("newbies", [])
                    
                    current_group_rows = []
                    for k in present_kids:
                        current_group_rows.append(k.replace('"', '').strip())
                    for n in newbies_kids:
                        if n.strip():
                            current_group_rows.append(f"{n.strip()} 🟡 Новичок")
                            
                    yaml_group_updates_local[time_key] = current_group_rows
                except Exception:
                    continue

            if yaml_group_updates_local:
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
                        
                        final_rows = yaml_group_updates_local.get(group_time_clean, [])
                        if final_rows:
                            for kid_line in final_rows:
                                new_lines.append(f'    - "{kid_line}"')
                            
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
                    print(f"[ШЛЮЗ] 🟢 База YAML для {teacher_login} успешно обновлена напрямую по сети!")
                else:
                    print(f"[ШЛЮЗ] ❌ Ошибка PUT-запроса YAML: {res_put.status_code}")

        # ----------------------------------------------------------------------
        # ЭТАП 2: СЕТЕВОЕ УДАЛЕНИЕ JSON ИЗ ПАПКИ _OUTPUT (РАЗМОРОЗКА ШЛЮЗА)
        # ----------------------------------------------------------------------
        if json_files_to_delete:
            print(f"[ШЛЮЗ] Найдено файлов для удаления: {len(json_files_to_delete)} шт. Запуск REST-зачистки...")
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

    print("=== [МОДУЛЬ JA_GATE_CLOSER] ВСЕ СЕТЕВЫЕ ОПЕРАЦИИ ОЧИСТКИ ЗАВЕРШЕНЫ ===")
    return True