#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  ja_report_builder.py
@about   Маркдаун-дизайнер и GraphQL-публикатор отчётов Журнала
@purpose Импорт сырых данных из парсера, сборка таблиц и отправка в Discussions
@author  TechLab
@version 1.0.0
"""

import os
import json
import requests
import re

# Импортируем модуль данных Журнала
import ja_data_parser

# ГЛОБАЛЬНЫЕ НАСТРОЙКИ API GITHUB И РЕПОЗИТОРИЕВ
GRAPHQL_URL = "https://api.github.com/graphql"
BASE_DISCUSSION_URL = "https://github.com/eaststandart/eaststandart.github.io/discussions"

def run_generator():
    print("\n=== [МОДУЛЬ: СБОРЩИК ОТЧЕТОВ] ЗАПУСК ЦИКЛИЧЕСКОЙ СБОРКИ МАРКДАУН ===")
    
    # Вызываем Сетевой Парсер и забираем карту уже проверенных данных
    raw_packages = ja_data_parser.collect_and_parse_raw_data()
    
    if not raw_packages:
        print("[СТРОИТЕЛЬ] Очередь сырых пакетов данных от парсера пуста. Выход.")
        return False, []

    all_generated_reports = []

    # РАБОТАЕМ С ИЗОЛИРОВАННЫМИ ДАННЫМИ КАЖДОГО ПРЕПОДАВАТЕЛЯ ИЗ СЕТЕВОГО ПАКЕТА
    for teacher_login, pack in raw_packages.items():
        print(f"\n[СТРОИТЕЛЬ] Построение Маркдаун-отчёта для: '{teacher_login}'")
        
        target_day = pack["target_day"]
        date_str = pack["date_str"]
        teacher_username = pack["teacher_username"]
        publish_as_bot = pack["publish_as_bot"]
        show_projects_column = pack["show_projects_column"]
        discussion_number = pack["discussion_number"]
        project_categories = pack["project_categories"]
        students_data = pack["students_data"]
        temp_journal = pack["temp_journal"]
        teacher_json_files = pack["teacher_json_files"]

        print(f"\n[СТРОИТЕЛЬ] НАСТРОЙКИ ДЛЯ {teacher_login}:")
        print(f"Режим публикации через Бота: {publish_as_bot}")
        print(f"Показывать колонку проектов: {show_projects_column}")
        print(f"Целевой номер Дискуссии: #{discussion_number}")
        print(f"Категории поделок: {project_categories}")

        # === СБОР ПОДЕЛКОВ ИЗ СОВПАВШИХ КАТЕГОРИЙ ЧЕРЕЗ API GITHUB DISCUSSIONS (1 В 1 ОРИГИНАЛ) ===
        global_gallery_comments = []
        discussions = []
        
        if show_projects_column:
            print("\n=== [РАДАР КАТЕГОРИЙ GITHUB DISCUSSIONS] ===")
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
                    print(f"[СТРОИТЕЛЬ] Загружено комментов для анализа проектов: {len(global_gallery_comments)}")
            except Exception as err:
                print(f"[СТРОИТЕЛЬ] ⚠️ Исключение при сборе поделок: {str(err)}")

        # ОРИГИНАЛЬНАЯ ФУНКЦИЯ ТРАНСЛИТЕРАЦИИ ДЛЯ АВТОГЕНЕРАЦИИ ТЕГОВ ПО СИМВОЛУ '#'
        def translit_rus_to_lat(text):
            rus = "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я".split()
            lat = "a b v g d e yo zh z i y k l m n o p r s t u f kh ts ch sh shch y e yu ya".split()
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

        # === СБОРКА ИТОГОВОЙ МАРКДАУН ТАБЛИЦЫ ДЛЯ ПРЕПОДАВАТЕЛЯ (1 В 1 ОРИГИНАЛ) ===
        schedule_groups = sorted(list(students_data.get(target_day, {}).keys()))
        print(f"[СТРОИТЕЛЬ] Запланировано групп у {teacher_login} по YAML: {schedule_groups}")
        
        filled_times = sorted(list(temp_journal.keys()))
        print(f"[СТРОИТЕЛЬ] Получено групп от {teacher_login} с сайта: {filled_times}")

        # ПРОВЕРКА КОМПЛЕКТНОСТИ ГРУПП КОНКРЕТНОГО УЧИТЕЛЯ
        if len(filled_times) < len(schedule_groups):
            print(f"[СТРОИТЕЛЬ] ⏳ Комплект для '{teacher_login}' не собран ({len(filled_times)} из {len(schedule_groups)}). Пропускаем.")
            continue

        print(f"[СТРОИТЕЛЬ] 🟢 Полный комплект для '{teacher_login}' собран! Запускаем склейку...", flush=True)

        print(f"[ОТЛАДКА ДАТЫ] Значение date_str: {date_str!r} | Тип: {type(date_str)}", flush=True)
        date_parts = date_str.split('-')
        print(f"[ОТЛАДКА ДАТЫ] Результат split: {date_parts!r}", flush=True)
        formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]} г."
        
        markdown_body = f"### 📅 Журнал посещений за {formatted_date} ({pack.get('target_day', '')})\n\n"
        if show_projects_column:
            markdown_body += "| Группа / Ученик | Status | Направление | Чем занят |\n"
            markdown_body += "| :--- | :--- | :--- | :--- |\n"
        else:
            markdown_body += "| Группа / Ученик | Status | Направление |\n"
            markdown_body += "| :--- | :--- | :--- |\n"

        yaml_group_updates = {}

        for time in schedule_groups:
            print(f"\n[ОТЛАДКА ГРУППЫ] Обработка времени: {time!r}", flush=True)
            if show_projects_column:
                markdown_body += f"| **⏰ ГРУППА {time}** | | | |\n"
            else:
                markdown_body += f"| **⏰ ГРУППА {time}** | | |\n"

            group_payload = temp_journal.get(time, {"present_permanent": [], "newbies": [], "probation": []})
            permanent_kids = students_data.get(target_day, {}).get(time, [])
            
            print(f"[ОТЛАДКА payload] Ключи group_payload: {list(group_payload.keys())}", flush=True)
            print(f"[ОТЛАДКА YML] permanent_kids из базы YML: {permanent_kids!r} | Тип: {type(permanent_kids)}", flush=True)

            block_permanent = []
            block_newbies = []
            block_probation = []
            current_group_yaml_rows = []

            # 1. КОНТУР РЕГУЛЯРНЫХ УЧЕНИКОВ ИЗ YAML БАЗЫ РАСПИСАНИЯ
            for kid in permanent_kids:
                print(f"  • Опрос kid: {kid!r} | Тип: {type(kid)}", flush=True)
                kid_clean = str(kid).strip()
                kid_track = ""
                kid_tag = ""

                # Проверяем структуру элементов внутри входящего массива с сайта перед сверкой
                present_list = group_payload.get("present_permanent", [])
                print(f"  • Содержимое present_permanent с сайта: {present_list!r}", flush=True)
                for index, p_item in enumerate(present_list):
                    print(f"    - Элемент JSON [{index}]: {p_item!r} | Тип: {type(p_item)}", flush=True)

                # Намертво защищённая сверка факта присутствия по плоскому ключу name из JSON с сайта
                is_present = any(isinstance(p, dict) and p.get("name", "").strip().lower() == kid_clean.lower() for p in present_list)
               
                processed = {
                    "name_for_sort": kid_clean,
                    "track": kid_track,
                    "status": "🟢 Присутствовал" if is_present else "🔴 Отсутствовал",
                    "project": "",
                    "yaml_line": kid_clean
                }
                block_permanent.append(processed)
                current_group_yaml_rows.append(processed["yaml_line"])

            # 2. КОНТУР НОВИЧКОВ ИЗ JSON ОБЪЕКТОВ С САЙТА
            for newbie in group_payload.get("newbies", []):
                if isinstance(newbie, dict) and newbie.get("name", "").strip():
                    newbie_name = newbie["name"].strip()
                    raw_dir = newbie.get("direction", "").strip().lower()
                    
                    newbie_track = "электроника" if "электронное конструирование" in raw_dir else "столярное" if "столярное дело" in raw_dir else ""
                    newbie_tag = newbie.get("tag", "").strip()

                    if newbie_tag == "#":
                        newbie_tag = f"#techlab-{translit_rus_to_lat(newbie_name)}"

                    project_link = ""
                    if show_projects_column and newbie_tag:
                        matches = [c for c in global_gallery_comments if c.get("body") and newbie_tag in c["body"]]
                        if matches:
                            matches.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
                            project_link = f"🗂️ [Проект]({matches[0]['url']})"

                    direction_suffix = " [э]" if newbie_track == "электроника" else " [с]" if newbie_track == "столярное" else ""
                    tag_suffix = f" {newbie_tag}" if newbie_tag else ""
                    final_yaml_line = f"{newbie_name}{direction_suffix}{tag_suffix}"

                    processed = {
                        "name_for_sort": newbie_name,
                        "track": newbie_track,
                        "status": "🟡 Новичок",
                        "project": project_link,
                        "yaml_line": final_yaml_line
                    }
                    block_newbies.append(processed)
                    current_group_yaml_rows.append(processed["yaml_line"])

            # 3. КОНТУР ПРОБНЫХ ЗАНЯТИЙ ИЗ JSON ОБЪЕКТОВ С САЙТА
            for prob in group_payload.get("probation", []):
                if isinstance(prob, dict) and prob.get("name", "").strip():
                    prob_name = prob["name"].strip()
                    raw_dir = prob.get("direction", "").strip().lower()
                    
                    prob_track = "электроника" if "электронное конструирование" in raw_dir else "столярное" if "столярное дело" in raw_dir else ""
                    prob_tag = prob.get("tag", "").strip()

                    if prob_tag == "#":
                        prob_tag = f"#techlab-{translit_rus_to_lat(prob_name)}"

                    project_link = ""
                    if show_projects_column and prob_tag:
                        matches = [c for c in global_gallery_comments if c.get("body") and prob_tag in c["body"]]
                        if matches:
                            matches.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
                            project_link = f"🗂️ [Проект]({matches[0]['url']})"

                    processed = {
                        "name_for_sort": prob_name,
                        "track": prob_track,
                        "status": "🔵 Пробное",
                        "project": project_link,
                        "yaml_line": ""
                    }
                    block_probation.append(processed)

            # Алфавитная сортировка карточек учеников для вывода в Маркдаун
            block_permanent.sort(key=lambda x: x["name_for_sort"].lower())
            block_newbies.sort(key=lambda x: x["name_for_sort"].lower())
            block_probation.sort(key=lambda x: x["name_for_sort"].lower())

            # Запись строк в итоговое тело таблицы Markdown
            for row in block_permanent:
                markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"
            for row in block_newbies:
                markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"
            for row in block_probation:
                markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"

            # Алфавитная сортировка строк для обновления YAML-файла базы расписания
            current_group_yaml_rows.sort(key=lambda x: re.sub(r'\[э\]|\[с\]|@[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+', '', x, flags=re.IGNORECASE).strip().lower())
            yaml_group_updates[time] = current_group_yaml_rows

        markdown_body += f"\n*Проверил и отправил преподаватель: **{teacher_username}***\n"
        print(f"[СТРОИТЕЛЬ] Таблица Markdown для {teacher_login} сформирована успешно!")

        # === ПУБЛИКАЦИЯ В GITHUB DISCUSSIONS ===
        bot_token = os.environ.get("GITHUB_TOKEN")
        admin_token = os.environ.get("MY_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN")
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
                print(f"[СТРОИТЕЛЬ] ❌ Ошибка мутации GraphQL для {teacher_login}: {json.dumps(res_mut['errors'])}")
                continue
                
            comment_id = res_mut["data"]["addDiscussionComment"]["comment"]["databaseId"]
            comment_url = f"{BASE_DISCUSSION_URL}/{discussion_number}?sort=new#discussioncomment-{comment_id}"
            print(f"[СТРОИТЕЛЬ] 🟢 Отчёт для {teacher_login} опубликован: {comment_url}")
        except Exception as e:
            print(f"[СТРОИТЕЛЬ] ❌ Ошибка связи с API при публикации отчета {teacher_login}: {str(e)}")
            continue

        # Упаковываем данные текущего учителя в изолированный пакет и добавляем в список
        report_packet = {
            "teacher_login": teacher_login,
            "markdown": markdown_body,
            "url": comment_url,
            "day": target_day
        }
        all_generated_reports.append(report_packet)
        print(f"[СТРОИТЕЛЬ] 📦 Пакет отчета для '{teacher_login}' успешно добавлен в очередь Телеграма.")

    # ФИНАЛЬНЫЙ СИГНАЛ КОНВЕЙЕРА ДЛЯ ГЛАВНОГО ДИСПЕТЧЕРА ТЕЛЕГРАМА (ВНЕ ЦИКЛА FOR)
    success_status = len(all_generated_reports) > 0
    return success_status, all_generated_reports
