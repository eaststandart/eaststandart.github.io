#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module ja_report_generator.py
@about Формирование Журнала посещений
@purpose Сбор данных с сайта, интеграция с GraphQL API GitHub Discussions и обновление YAML базы расписания
@author TechLab
@version 1.0.0
"""

import os
import json
import sys
import yaml
import requests
import re

# ГЛОБАЛЬНЫЕ НАСТРОЙКИ API GITHUB И РЕПОЗИТОРИЕВ
GRAPHQL_URL = "https://api.github.com/graphql"
BASE_DISCUSSION_URL = "https://github.com/eaststandart/eaststandart.github.io/discussions"

# Изолированный репозиторий баз данных преподавателей
DATA_REPO_OWNER = "eaststandart"
DATA_REPO_NAME = "techlab-journal-attendance"

# Базовый служебный API-путь для управления файлами базы данных
# Базовые служебные API-пути к двум разным папкам удалённого репозитория Журнала
JOURNAL_YML_API_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_data"
JOURNAL_JSON_API_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_output"

def run_generator():
    print("\n=== [МОДУЛЬ JA_REPORT_GENERATOR] ЗАПУСК ЦИКЛИЧЕСКОЙ СБОРКИ ===")
    
    data_dir = os.path.join(os.getcwd(), '_data')
    if not os.path.exists(data_dir):
        print(f"[ГЕНЕРАТОР] ❌ КРИТИЧЕСКАЯ ОШИБКА: Папка с данными не найдена: {data_dir}")
        return False, []

    # АВТО-ПОИСК ЖИВЫХ ЛОГИНОВ ПРЕПОДАВАТЕЛЕЙ ПО ФАЙЛАМ РАСПИСАНИЙ .YML
    all_files = os.listdir(data_dir)
    active_teachers = []
    for f in all_files:
        if f.startswith('journal-attendance-') and f.endswith('.yml'):
            login = f.replace('journal-attendance-', '').replace('.yml', '').strip().lower()
            if login:
                active_teachers.append(login)

    print(f"[ГЕНЕРАТОР] Список active преподавателей из базы YML: {active_teachers}")

    # СБОР ВСЕХ ПРИЛЕТЕВШИХ JSON ФАЙЛОВ ГРУПП ИЗ СЕТИ ГИТХАБА ЧЕРЕЗ API
    admin_token = os.environ.get("MY_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {admin_token}", "Accept": "application/vnd.github+json"}
    
    try:
        response = requests.get(JOURNAL_JSON_API_URL, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"[ГЕНЕРАТОР] Временные файлы журналов в папке _output отсутствуют (Код API: {response.status_code}). Выход.")
            return False, []
            
        output_contents = response.json()
        # Создаём словарь {имя_файла: url_скачивания} прямо из ответа API
        json_download_urls = {item["name"]: item["download_url"] for item in output_contents if '-journal-attendance-' in item["name"] and item["name"].endswith('.json')}
        all_json_files = list(json_download_urls.keys())
        
    except Exception as err:
        print(f"[ГЕНЕРАТОР] ❌ Ошибка сетевого запроса к _output Журнала: {str(err)}")
        return False, []

    if not all_json_files:
        print("[ГЕНЕРАТОР] Временные файлы журналов групп в папке _output отсутствуют. Выход.")
        return False, []

    print(f"[ГЕНЕРАТОР] Обнаружено JSON-файлов в сети Журнала (_output): {len(all_json_files)} шт.")
    all_generated_reports = []

    # ЗАПУСКАЕМ ИЗОЛИРОВАННЫЙ ЦИКЛ ПО КАЖДОМУ ПРЕПОДАВАТЕЛЮ
    for current_teacher in active_teachers:
        teacher_json_files = [f for f in all_json_files if f.lower().endswith(f"-journal-attendance-{current_teacher}.json")]
        
        if not teacher_json_files:
            continue
            
        print(f"\n👉 [ЦИКЛ] Найдена пачка файлов для преподавателя: '{current_teacher}' ({len(teacher_json_files)} шт.)")

        # Скачиваем содержимое пилотного JSON-файла напрямую из сети Гитхаба
        try:
            sample_download_url = json_download_urls[teacher_json_files[0]]
            sample_data = requests.get(sample_download_url, headers=headers, timeout=30).json()
        except Exception as e:
            print(f"[ГЕНЕРАТОР] ❌ Ошибка интернет-чтения файла {teacher_json_files[0]}: {str(e)}")
            continue
            
        target_day = sample_data.get('day', '').lower().strip()
        date_str = sample_data.get('date', '')
        teacher_username = sample_data.get('teacher_username', 'Преподаватель')
        teacher_login = current_teacher  

        yaml_path = os.path.join(data_dir, f"journal-attendance-{teacher_login}.yml")
        if not os.path.exists(yaml_path):
            print(f"[ГЕНЕРАТОР] ❌ Пропуск: Личный файл расписания не найден: {yaml_path}")
            continue

        # Сетевой адрес конкретного YAML-файла в репозитории Журнала
        file_api_url = f"{JOURNAL_YML_API_URL}/journal-attendance-{teacher_login}.yml"

        # Извлечение изолированного персонального токена, переданного специально для перезаписи YAML
        write_token = os.environ.get("JOURNAL_WRITE_TOKEN")

        # Подготовка сетевых заголовков авторизации для работы с приватным репозиторием Журнала
        headers_pub = {
            "Authorization": f"token {write_token if write_token else admin_token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json"
        }

        res_info = requests.get(file_api_url, headers=headers_pub, timeout=30)
        if res_info.status_code != 200:
            print(f"[ГЕНЕРАТОР] ⚠️ Не удалось получить YAML с GitHub для {teacher_login}: {res_info.status_code}")
            continue

        res_json = res_info.json()
        yaml_sha = res_json.get("sha")

        # Декодируем текстовое содержимое файла из формата base64, в котором его отдал GitHub
        import base64
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
                            print(f"[РЕДАКТОР] Найдена опечатка '{clean_time_str}'. Заменяем на '{normalized_time}'")
                            updated_yaml_text = updated_yaml_text.replace(f"'{clean_time_str}':", f'"{normalized_time}":')
                            updated_yaml_text = updated_yaml_text.replace(f'"{clean_time_str}":', f'"{normalized_time}":')
                            updated_yaml_text = updated_yaml_text.replace(f"{clean_time_str}:", f'"{normalized_time}":')
                            file_needs_repair = True
                    else:
                        students_data[day_name][clean_time_str] = kids_list if isinstance(kids_list, list) else []

        if file_needs_repair:
            with open(yaml_path, 'w', encoding='utf-8') as f:
                f.write(updated_yaml_text)
            print("[РЕДАКТОР] Файл расписания успешно вылечен!")
        config_data = yaml_data.get('config', {})
        publish_as_bot = config_data.get('publish_as_bot', False)
        show_projects_column = config_data.get('show_projects_column', True)
        discussion_number = config_data.get('discussion_number', 38)
        
        raw_categories = config_data.get('project_category_name', ['Галерея'])
        project_categories = [raw_categories] if isinstance(raw_categories, str) else raw_categories

        print(f"\n=== ЛОГ РОБОТА PYTHON: НАСТРОЙКИ ДЛЯ {teacher_login} ===")
        print(f"Режим публикации через Бота: {publish_as_bot}")
        print(f"Показывать колонку проектов: {show_projects_column}")
        print(f"Целевой номер Дискуссии: #{discussion_number}")
        print(f"Категории поделок: {project_categories}")

        # === СБОР ПОДЕЛКОВ ИЗ СОВПАВШИХ КАТЕГОРИЙ ЧЕРЕЗ API ===
        global_gallery_comments = []
        discussions = []
        
        if show_projects_column:
            print("\n=== [РАДАР КАТЕГОРИЙ GITHUB НА PYTHON] ===")
            query_gql = """
            query($owner: String!, $repo: String!) {
              repository(owner: $owner, name: $repo) {
                discussions(first: 100) {
                  nodes {
                    category { name }
                    comments(first: 100) {
                      nodes { url createdAt body }
                    }
                  }
                }
              }
            }
            """
            try:
                admin_token = os.environ.get("MY_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN")
                response = requests.post(GRAPHQL_URL, json={"query": query_gql, "variables": {"owner": "eaststandart", "repo": "eaststandart.github.io"}}, headers={"Authorization": f"token {admin_token}", "Content-Type": "application/json"})
                if response.status_code == 200:
                    discussions = response.json().get("data", {}).get("repository", {}).get("discussions", {}).get("nodes", [])
                    search_cats_lower = [c.lower().strip() for c in project_categories]
                    for d in discussions:
                        if d.get("category") and d["category"]["name"].lower().strip() in search_cats_lower:
                            comments_nodes = d.get("comments", {}).get("nodes", [])
                            if comments_nodes:
                                global_gallery_comments.extend(comments_nodes)
                    print(f"[ГЕНЕРАТОР] Загружено комментов для анализа проектов: {len(global_gallery_comments)}")
            except Exception as err:
                print(f"[ГЕНЕРАТОР] ⚠️ Исключение при сборе поделок: {str(err)}")
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
            project_link = ""
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

            if show_projects_column and target_tag:
                matches = []
                for c in global_gallery_comments:
                    if c.get("body") and target_tag in c["body"]:
                        matches.append(c)
                if matches:
                    matches.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
                    project_link = f"🗂️ [Проект]({matches[0]['url']})"

            print_name = normalized.replace('"', '')
            print_name = re.sub(r'\[э\]|\[с\]', '', print_name, flags=re.IGNORECASE)
            print_name = re.sub(r'(@[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+)', '', print_name)
            print_name = re.sub(r'\s+', ' ', print_name).strip()

            direction_suffix = " [э]" if track == "электроника" else " [с]" if track == "столярное" else ""
            tag_suffix = f" {target_tag}" if target_tag else ""
            final_yaml_line = f"{print_name}{direction_suffix}{tag_suffix}"

            return {
                "name_for_sort": print_name,
                "track": track,
                "status": status_text,
                "project": project_link,
                "yaml_line": final_yaml_line
            }

        # === СБОРКА ИТОГОВОЙ МАРКДАУН ТАБЛИЦЫ ДЛЯ ПРЕПОДАВАТЕЛЯ ===
        temp_journal = {}
        for file in teacher_json_files:
            try:
                file_url = json_download_urls[file]
                file_data = requests.get(file_url, headers=headers, timeout=30).json()
                temp_journal[file_data["time"]] = file_data
            except Exception as e:
                print(f"[ГЕНЕРАТОР] ❌ Ошибка интернет-чтения файла {file} при сборке таблицы: {str(e)}")
                continue

        schedule_groups = sorted(list(students_data.get(target_day, {}).keys()))
        print(f"[ГЕНЕРАТОР] Запланировано групп у {teacher_login} по YAML: {schedule_groups}")
        
        filled_times = sorted(list(temp_journal.keys()))
        print(f"[ГЕНЕРАТОР] Получено групп от {teacher_login} с сайта: {filled_times}")

        # ПРОВЕРКА КОМПЛЕКТНОСТИ ГРУПП КОНКРЕТНОГО УЧИТЕЛЯ
        if len(filled_times) < len(schedule_groups):
            print(f"[ГЕНЕРАТОР] ⏳ Комплект для '{teacher_login}' не собран ({len(filled_times)} из {len(schedule_groups)}). Пропускаем.")
            continue

        print(f"[ГЕНЕРАТОР] 🟢 Полный комплект для '{teacher_login}' собран! Запускаем склейку...")

        date_parts = date_str.split('-')
        formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]} г."
        
        markdown_body = f"### 📅 Журнал посещений за {formatted_date} ({sample_data.get('day', '')})\n\n"
        if show_projects_column:
            markdown_body += "| Группа / Ученик | Status | Направление | Чем занят |\n"
            markdown_body += "| :--- | :--- | :--- | :--- |\n"
        else:
            markdown_body += "| Группа / Ученик | Status | Направление |\n"
            markdown_body += "| :--- | :--- | :--- |\n"

        yaml_group_updates = {}

        for time in schedule_groups:
            if show_projects_column:
                markdown_body += f"| **⏰ ГРУППА {time}** | | | |\n"
            else:
                markdown_body += f"| **⏰ ГРУППА {time}** | | |\n"

            group_payload = temp_journal.get(time, {"present_permanent": [], "newbies": [], "probation": []})
            permanent_kids = students_data.get(target_day, {}).get(time, [])

            block_permanent = []
            block_newbies = []
            block_probation = []
            current_group_yaml_rows = []

            for kid in permanent_kids:
                processed = process_kid_row(kid, "")
                is_present = False
                for p in group_payload.get("present_permanent", []):
                    if p.replace('"', '').replace("'", "").strip().lower() == processed["name_for_sort"].lower():
                        is_present = True
                        break
                processed["status"] = "🟢 Присутствовал" if is_present else "🔴 Отсутствовал"
                block_permanent.append(processed)
                current_group_yaml_rows.append(processed["yaml_line"])

            for newbie in group_payload.get("newbies", []):
                if newbie.strip():
                    processed = process_kid_row(newbie, "🟡 Новичок")
                    block_newbies.append(processed)
                    current_group_yaml_rows.append(processed["yaml_line"])

            for prob in group_payload.get("probation", []):
                if prob.strip():
                    processed = process_kid_row(prob, "🔵 Пробное")
                    block_probation.append(processed)

            block_permanent.sort(key=lambda x: x["name_for_sort"].lower())
            block_newbies.sort(key=lambda x: x["name_for_sort"].lower())
            block_probation.sort(key=lambda x: x["name_for_sort"].lower())

            for row in block_permanent:
                markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"
            for row in block_newbies:
                markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"
            for row in block_probation:
                markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"

            current_group_yaml_rows.sort(key=lambda x: re.sub(r'\[э\]|\[с\]|@[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+', '', x, flags=re.IGNORECASE).strip().lower())
            yaml_group_updates[time] = current_group_yaml_rows

        markdown_body += f"\n*Проверил и отправил преподаватель: **{teacher_username}***\n"
        print(f"[ГЕНЕРАТОР] Таблица Markdown для {teacher_login} сформирована успешно!")

        # === ПУБЛИКАЦИЯ В GITHUB DISCUSSIONS ===
        bot_token = os.environ.get("GITHUB_TOKEN")
        active_token = bot_token if publish_as_bot else (admin_token if admin_token else bot_token)
        
        headers_pub = {
            "Authorization": f"token {active_token}",
            "Content-Type": "application/json"
        }

        try:
            id_payload = {
                "query": "query($owner: String!, $repo: String!, $num: Int!) { repository(owner: $owner, name: $repo) { discussion(number: $num) { id } } }",
                "variables": {"owner": "eaststandart", "repo": "eaststandart.github.io", "num": discussion_number}
            }
            response_id = requests.post(GRAPHQL_URL, json=id_payload, headers=headers_pub)
            discussion_id = response_id.json()["data"]["repository"]["discussion"]["id"]
            
            mutation_payload = {
                "query": "mutation($discId: ID!, $bodyText: String!) { addDiscussionComment(input: {discussionId: $discId, body: $bodyText}) { comment { databaseId } } }",
                "variables": {"discId": str(discussion_id), "bodyText": str(markdown_body)}
            }
            res_mut = requests.post(GRAPHQL_URL, json=mutation_payload, headers=headers_pub).json()
           
            if "errors" in res_mut:
                print(f"[ГЕНЕРАТОР] ❌ Ошибка мутации GraphQL для {teacher_login}: {json.dumps(res_mut['errors'])}")
                continue
                
            comment_id = res_mut["data"]["addDiscussionComment"]["comment"]["databaseId"]
            comment_url = f"{BASE_DISCUSSION_URL}/{discussion_number}?sort=new#discussioncomment-{comment_id}"
            print(f"[ГЕНЕРАТОР] 🟢 Отчёт для {teacher_login} опубликован: {comment_url}")
        except Exception as e:
            print(f"[ГЕНЕРАТОР] ❌ Ошибка связи с API при публикации отчета {teacher_login}: {str(e)}")
            continue

        # === ОБНОВЛЕНИЕ YAML БАЗЫ РАСПИСАНИЯ С АЛФАВИТНОЙ СОРТИРОВКОЙ ===
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                orig_lines = f.read().split('\n')
                
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

            # ==================================================================
            # ДИАГНОСТИЧЕСКИЙ ЛОГ СЕТЕВОГО СОХРАНЕНИЯ YAML
            # ==================================================================
            updated_yaml_text = '\n'.join(new_lines)
            encoded_content = base64.b64encode(updated_yaml_text.encode('utf-8')).decode('utf-8')
            
            put_payload = {
                "message": f"chore: автоматическое обновление расписания {teacher_login} с сайта",
                "content": encoded_content,
                "sha": yaml_sha
            }
            
            print(f"\n[ДИАГНОСТИКА YAML] Выполняем PUT-запрос сохранения расписания.")
            print(f"[ДИАГНОСТИКА YAML] Целевой URL: {file_api_url}")
            print(f"[ДИАГНОСТИКА YAML] Переданный SHA-хэш: {yaml_sha}")
            
            res_put = requests.put(file_api_url, json=put_payload, headers=headers_pub, timeout=30)
            
            print(f"[ДИАГНОСТИКА YAML] Код ответа сервера GitHub: {res_put.status_code}")
            print(f"[ДИАГНОСТИКА YAML] Полный текст ответа GitHub: {res_put.text}")
            
            if res_put.status_code in (200, 201):
                print(f"[ГЕНЕРАТОР] 🟢 База YAML для {teacher_login} успешно обновлена напрямую в репозитории Журнала!")
            else:
                print(f"[ГЕНЕРАТОР] ❌ Ошибка сетевого сохранения YAML для {teacher_login}: {res_put.status_code}")

        except Exception as e:
            print(f"[ГЕНЕРАТОР] ⚠️ Ошибка сохранения YAML для {teacher_login}: {str(e)}")

        # === ХИРУРГИЧЕСКАЯ ЗАЧИСТКА JSON В БАЗЕ ДАННЫХ ЧЕРЕЗ GITHUB REST API ===
        print(f"[ЗАЧИСТКА] Удаляем отработанные файлы JSON для '{teacher_login}' из репозитория баз...")
        for file_name in teacher_json_files:
            file_api_url = f"{JOURNAL_JSON_API_URL}/{file_name}"
            
            res_info = requests.get(file_api_url, headers={"Authorization": f"token {admin_token}"})
            if res_info.status_code == 200:
                file_sha = res_info.json().get("sha")
                
                delete_payload = {
                    "message": f"cleanup: удаление {file_name}",
                    "sha": file_sha
                }
                res_del = requests.delete(file_api_url, json=delete_payload, headers={"Authorization": f"token {admin_token}"})
                if res_del.status_code == 200:
                    print(f"[ЗАЧИСТКА API] 🟢 Файл {file_name} успешно стёрт с GitHub!")
                else:
                    print(f"[ЗАЧИСТКА API] ⚠️ Не удалось стереть {file_name}: {res_del.status_code}")
            else:
                print(f"[ЗАЧИСТКА API] ⚠️ Файл {file_name} не найден на GitHub для удаления.")

        # Упаковываем все данные текущего учителя в изолированный пакет и добавляем в список
        report_packet = {
            "teacher_login": teacher_login,
            "markdown": markdown_body,
            "url": comment_url,
            "day": target_day
        }
        all_generated_reports.append(report_packet)
        print(f"[ГЕНЕРАТОР] 📦 Пакет отчета для '{teacher_login}' успешно добавлен в очередь Телеграма.")

    # ФИНАЛЬНЫЙ СИГНАЛ КОНВЕЙЕРА ДЛЯ ГЛАВНОГО ДИСПЕТЧЕРА ТЕЛЕГРАМА (ВНЕ ЦИКЛА FOR)
    success_status = len(all_generated_reports) > 0
    return success_status, all_generated_reports
