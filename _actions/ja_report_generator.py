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
BASE_API_CONTENTS_URL = f"https://api.github.com/repos/{DATA_REPO_OWNER}/{DATA_REPO_NAME}/contents/_data"

def run_generator():
    print("\n=== [МОДУЛЬ JA_REPORT_GENERATOR] ЗАПУСК ЦИКЛИЧЕСКОЙ СБОРКИ ===")
    
    data_dir = os.path.join(os.getcwd(), '_data')
    if not os.path.exists(data_dir):
        print(f"[ГЕНЕРАТОР] ❌ КРИТИЧЕСКАЯ ОШИБКА: Папка с данными не найдена: {data_dir}")
        return False, None, None, None

    # АВТО-ПОИСК ЖИВЫХ ЛОГИНОВ ПРЕПОДАВАТЕЛЕЙ ПО ФАЙЛАМ РАСПИСАНИЙ .YML
    all_files = os.listdir(data_dir)
    active_teachers = []
    for f in all_files:
        if f.startswith('journal-attendance-') and f.endswith('.yml'):
            login = f.replace('journal-attendance-', '').replace('.yml', '').strip().lower()
            if login:
                active_teachers.append(login)

    print(f"[ГЕНЕРАТОР] Список активных преподавателей из базы YML: {active_teachers}")

    # СБОР ВСЕХ ПРИЛЕТЕВШИХ JSON ФАЙЛОВ ГРУПП ОТ ВСЕХ УЧИТЕЛЕЙ
    all_json_files = [f for f in all_files if '-journal-attendance-' in f and f.endswith('.json')]
    if not all_json_files:
        print("[ГЕНЕРАТОР] Временные файлы журналов групп в папке отсутствуют. Выход.")
        return False, None, None, None

    # НАСТРОЙКА ПЕРЕМЕННЫХ ДЛЯ ОТВЕТА ДИСПЕТЧЕРУ (ПО ПОСЛЕДНЕМУ УСПЕШНОМУ ПРОГОНУ)
    last_success = False
    last_markdown = None
    last_url = None
    last_day = None

    # ЗАПУСКАЕМ ИЗОЛИРОВАННЫЙ ЦИКЛ ПО КАЖДОМУ ПРЕПОДАВАТЕЛЮ
    for current_teacher in active_teachers:
        # Отбираем JSON-файлы строго текущего преподавателя из списка всех файлов
        teacher_json_files = [f for f in all_json_files if f.lower().endswith(f"-journal-attendance-{current_teacher}.json")]
        
        if not teacher_json_files:
            continue
            
        print(f"\n👉 [ЦИКЛ] Найдена пачка файлов для преподавателя: '{current_teacher}' ({len(teacher_json_files)} шт.)")

        # Читаем первый файл этой пачки, чтобы узнать параметры текущего дня занятия
        sample_path = os.path.join(data_dir, teacher_json_files[0])
        with open(sample_path, 'r', encoding='utf-8') as f:
            sample_data = json.load(f)
            
        target_day = sample_data.get('day', '').lower().strip()
        date_str = sample_data.get('date', '')
        teacher_username = sample_data.get('teacher_username', 'Преподаватель')
        teacher_login = current_teacher  # Жестко фиксируем логин из нашего цикла

        # Формируем путь к личному расписанию преподавателя
        yaml_path = os.path.join(data_dir, f"journal-attendance-{teacher_login}.yml")
    if not os.path.exists(yaml_path):
        print(f"[ГЕНЕРАТОР] ❌ КРИТИЧЕСКАЯ ОШИБКА: Личный файл расписания не найден: {yaml_path}")
        return False, None

    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_text_orig = f.read()
        f.seek(0)
        yaml_data = yaml.safe_load(f) or {}

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
                        print(f"[РЕДАКТОР ШАГА 0] Найдена опечатка '{clean_time_str}'. Заменяем в файле на '{normalized_time}'")
                        updated_yaml_text = updated_yaml_text.replace(f"'{clean_time_str}':", f'"{normalized_time}":')
                        updated_yaml_text = updated_yaml_text.replace(f'"{clean_time_str}":', f'"{normalized_time}":')
                        updated_yaml_text = updated_yaml_text.replace(f"{clean_time_str}:", f'"{normalized_time}":')
                        file_needs_repair = True
                else:
                    students_data[day_name][clean_time_str] = kids_list if isinstance(kids_list, list) else []

    if file_needs_repair:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(updated_yaml_text)
        print("[РЕДАКТОР ШАГА 0] Файл расписания успешно вылечен на самом старте конвейера!")

    config_data = yaml_data.get('config', {})
    
    publish_as_bot = config_data.get('publish_as_bot', False)
    show_projects_column = config_data.get('show_projects_column', True)
    discussion_number = config_data.get('discussion_number', 38)
    
    raw_categories = config_data.get('project_category_name', ['Галерея'])
    if isinstance(raw_categories, str):
        project_categories = [raw_categories]
    else:
        project_categories = raw_categories

    print("\n=== ЛОГ РОБОТА PYTHON: ИНДИВИДУАЛЬНЫЕ НАСТРОЙКИ УЧИТЕЛЯ ===")
    print(f"Режим публикации через Бота (считано из YAML): {publish_as_bot}")
    print(f"Показывать колонку проектов (считано из YAML): {show_projects_column}")
    print(f"Целевой номер Дискуссии (считано из YAML): #{discussion_number}")
    print(f"Категории для поиска поделок (считано из YAML): {project_categories}")

    # === СБОР ПОДЕЛКОВ ИЗ СОВПАВШИХ КАТЕГОРИЙ ЧЕРЕЗ API ===
    global_gallery_comments = []
    
    if show_projects_column:
        print("\n=== [РАДАР КАТЕГОРИЙ GITHUB НА PYTHON] ===")
        admin_token = os.environ.get("MY_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not admin_token:
            print("[ГЕНЕРАТОР] ❌ КРИТИЧЕСКАЯ ОШИБКА: Токен авторизации GitHub не найден!")
            return False, None

        query_gql = """
        query($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            discussions(first: 100) {
              nodes {
                category { name }
                comments(first: 100) {
                  nodes {
                    url
                    createdAt
                    body
                  }
                }
              }
            }
          }
        }
        """
        
        headers = {
            "Authorization": f"token {admin_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": query_gql,
            "variables": {
                "owner": "eaststandart",
                "repo": "eaststandart.github.io"
            }
        }
        
        try:
            response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
            if response.status_code != 200:
                print(f"[ГЕНЕРАТОР] ❌ Ошибка сети API GitHub: Статус {response.status_code}")
                return False, None
                
            res_json = response.json()
            discussions = res_json.get("data", {}).get("repository", {}).get("discussions", {}).get("nodes", [])
            search_cats_lower = [c.lower().strip() for c in project_categories]
            
            for d in discussions:
                if d.get("category") and d["category"]["name"].lower().strip() in search_cats_lower:
                    comments_nodes = d.get("comments", {}).get("nodes", [])
                    if comments_nodes:
                        global_gallery_comments.extend(comments_nodes)
                        
            print(f"[ГЕНЕРАТОР] Успешно загружено комментов для анализа: {len(global_gallery_comments)}")
            
        except Exception as err:
            print(f"[ГЕНЕРАТОР] ❌ Исключение при сборе поделок: {str(err)}")
            return False, None

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
        import re
        res = re.sub(r'-+', '-', res)
        return res.strip('-')

    def process_kid_row(raw_name, status_text):
        track = ""
        project_link = ""
        import re
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
                
                parent_cat = "Неизвестная категория"
                for d in discussions:
                    if d.get("comments") and any(com["url"] == matches[0]["url"] for com in d["comments"].get("nodes", [])):
                        parent_cat = d["category"]["name"]
                        break

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

    # === СБОРКА ИТОГОВОЙ МАРКДАУН ТАБЛИЦЫ ===
    temp_journal = {}
    todays_files = [f for f in os.listdir(data_dir) if f.startswith(f"{date_str}-") and f.endswith(".json")]
    for file in todays_files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8') as f:
            file_data = json.load(f)
            # ВЫЧИЩЕНО НАЧИСТО: Сайт всегда отдает нормальное время с двоеточием, берем ключ напрямую!
            temp_journal[file_data["time"]] = file_data

    schedule_groups = sorted(list(students_data.get(target_day, {}).keys()))
    print(f"[ГЕНЕРАТОР] Запланировано групп у {teacher_login} по YAML: {schedule_groups}")
    
    filled_times = sorted(list(temp_journal.keys()))
    print(f"[ГЕНЕРАТОР] Получено групп от {teacher_login} с сайта: {filled_times}")

    # СРАВНИВАЕМ КОЛИЧЕСТВО ФАЙЛОВ С ПЛАНОМ ДЛЯ ТЕКУЩЕГО УЧИТЕЛЯ
    if len(filled_times) < len(schedule_groups):
        print(f"[ГЕНЕРАТОР] ⏳ Комплект для '{teacher_login}' не собран ({len(filled_times)} из {len(schedule_groups)}). Пропускаем его до следующего запуска.")
        continue  # ИСПРАВЛЕНО: Мягко переходим к следующему учителю в цикле, не роняя диспетчер!

    print(f"[ГЕНЕРАТОР] 🟢 Полный комплект для '{teacher_login}' собран! Запускаем склейку отчета...")

    date_parts = date_str.split('-')
    formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]} г."
    
    markdown_body = f"### 📅 Журнал посещений за {formatted_date} ({sample_data.get('day', '')})\n\n"
    if show_projects_column:
        markdown_body += "| Группа / Ученик | Статус | Направление | Чем занят |\n"
        markdown_body += "| :--- | :--- | :--- | :--- |\n"
    else:
        markdown_body += "| Группа / Ученик | Статус | Направление |\n"
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
    print("[ГЕНЕРАТОР] Итоговая таблица Markdown сформирована успешно!")

    # === ПУБЛИКАЦИЯ В GITHUB DISCUSSIONS ===
    bot_token = os.environ.get("GITHUB_TOKEN")
    admin_token = os.environ.get("MY_ADMIN_TOKEN")
    active_token = bot_token if publish_as_bot else (admin_token if admin_token else bot_token)
    
    if not active_token:
        print("[ГЕНЕРАТОР] ❌ Ошибка: Токен для публикации отчета не найден!")
        return False, None

    headers = {
        "Authorization": f"token {active_token}",
        "Content-Type": "application/json"
    }

    id_query_gql = """
    query($owner: String!, $repo: String!, $num: Int!) {
      repository(owner: $owner, name: $repo) {
        discussion(number: $num) { id }
      }
    }
    """
    
    try:
        id_payload = {
            "query": id_query_gql,
            "variables": {
                "owner": "eaststandart",
                "repo": "eaststandart.github.io",
                "num": discussion_number
            }
        }
        response_id = requests.post(GRAPHQL_URL, json=id_payload, headers=headers)
        res_id = response_id.json()
        discussion_id = res_id["data"]["repository"]["discussion"]["id"]
        
        mutation_gql = "mutation($discId: ID!, $bodyText: String!) { addDiscussionComment(input: {discussionId: $discId, body: $bodyText}) { comment { databaseId } } }"
        mutation_payload = {
            "query": mutation_gql,
            "variables": {
                "discId": str(discussion_id),
                "bodyText": str(markdown_body)
            }
        }
        response_mut = requests.post(GRAPHQL_URL, json=mutation_payload, headers=headers)
        res_mut = response_mut.json()
       
        if "errors" in res_mut:
            print(f"[ГЕНЕРАТОР] ❌ Ошибка мутации GraphQL: {json.dumps(res_mut['errors'])}")
            return False, None, None, None
            
        # Сборка прямой ссылки на созданный комментарий
        try:
            comment_id = res_mut["data"]["addDiscussionComment"]["comment"]["databaseId"]
            comment_url = f"{BASE_DISCUSSION_URL}/{discussion_number}?sort=new#discussioncomment-{comment_id}"
            print(f"[ГЕНЕРАТОР РОБОТА] 🟢 ПРЯМАЯ ССЫЛКА НА КОММЕНТАРИЙ СФОРМИРОВАНА: {comment_url}")
        except Exception as link_err:
            print(f"[ГЕНЕРАТОР] ⚠️ Предупреждение: Не удалось склеить прямую ссылку: {str(link_err)}")
            comment_url = f"{BASE_DISCUSSION_URL}/{discussion_number}"
            
        author_name = "Бота" if publish_as_bot else "Администратора"
        print(f"[УСПЕХ] Журнал опубликован в Обсуждении #{discussion_number} от лица {author_name}!")

        # === ОБНОВЛЕНИЕ YAML БАЗЫ РАСПИСАНИЯ С АЛФАВИТНОЙ СОРТИРОВКОЙ ===
        print("[ГЕНЕРАТОР] Сортировка и перезапись YAML базы...")
        with open(yaml_path, 'r', encoding='utf-8') as f:
            orig_lines = f.read().split('\n')
            
        new_lines = []
        inside_day = False
        i = 0
        while i < len(orig_lines):
            line = orig_lines[i]
            trimmed = line.rstrip()
            indent = len(line) - len(line.lstrip())
            
            if indent == 0 and trimmed.endswith(':'):
                inside_day = (trimmed[:-1].lower().strip() == target_day)
                new_lines.append(line)
                i += 1
                continue
                
            if inside_day and indent == 2 and trimmed.endswith(':'):
                # ВЫЧИЩЕНО НАЧИСТО: используется наш простой, безопасный метод краев .strip()
                group_time_clean = trimmed.strip().strip(':').strip('"').strip("'").strip()
                new_lines.append(line)
                
                final_rows = yaml_group_updates.get(group_time_clean, students_data.get(target_day, {}).get(group_time_clean, []))
                for kid_line in final_rows:
                    clean_row = kid_line.replace('"', '').replace("'", "").strip()
                    new_lines.append(f'    - "{clean_row}"')
                    
                while i + 1 < len(orig_lines):
                    next_line = orig_lines[i + 1]
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent == 4 and next_line.strip().startswith('-'):
                        i += 1
                    else:
                        break
                i += 1
                continue
                
            new_lines.append(line)
            i += 1
            
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print("[ГЕНЕРАТОР] База YAML успешно отсортирована и сохранена!")

        # === ХИРУРГИЧЕСКАЯ ЗАЧИСТКА JSON В БАЗЕ ДАННЫХ ЧЕРЕЗ GITHUB REST API ===
        print(f"[ЗАЧИСТКА] Удаляем отработанные файлы JSON для '{teacher_login}' из репозитория баз...")
        for file_name in teacher_json_files:
            file_api_url = f"{BASE_API_CONTENTS_URL}/{file_name}"
            
            # Шаг 1: Запрашиваем актуальный SHA-маркер файла в Git истории
            res_info = requests.get(file_api_url, headers={"Authorization": f"token {admin_token}"})
            if res_info.status_code == 200:
                file_sha = res_info.json().get("sha")
                
                # Шаг 2: Отправляем официальный DELETE запрос на удаление из веб-интерфейса
                delete_payload = {
                    "message": f"cleanup: автоматическое удаление отработанного файла {file_name}",
                    "sha": file_sha
                }
                res_del = requests.delete(file_api_url, json=delete_payload, headers={"Authorization": f"token {admin_token}"})
                if res_del.status_code == 200:
                    print(f"[ЗАЧИСТКА API] 🟢 Файл {file_name} успешно стёрт с GitHub!")
                else:
                    print(f"[ЗАЧИСТКА API] ⚠️ Не удалось стереть {file_name}: {res_del.status_code}")
            else:
                print(f"[ЗАЧИСТКА API] ⚠️ Файл {file_name} не найден на GitHub для удаления.")

        # Фиксируем параметры текущего успешного учителя для передачи наверх в Телеграм
        last_success = True
        last_markdown = markdown_body
        last_url = comment_url
        last_day = target_day

    except Exception as err:
        print(f"[ГЕНЕРАТОР] ❌ Критический сбой в блоке учителя '{current_teacher}': {str(err)}")
        continue

    # ФИНАЛЬНЫЙ СИГНАЛ ДЛЯ ГЛАВНОГО ДИСПЕТЧЕРА КОНВЕЙЕРА ТЕЛЕГРАМА
    return last_success, last_markdown, last_url, last_day
