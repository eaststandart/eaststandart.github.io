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
    print("\n=== [МОДУЛЬ: СТРОИТЕЛЬ] ЗАПУСК СБОРКИ ОТЧЕТА ===")
    
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

        print(f"[СТРОИТЕЛЬ] === НАСТРОЙКИ ДЛЯ {teacher_login}: ===")
        print(f"Режим публикации через Бота: {publish_as_bot}")
        print(f"Показывать колонку проектов: {show_projects_column}")
        print(f"Целевой номер Дискуссии: #{discussion_number}")
        print(f"Категории поделок: {project_categories}")

        # === СБОР ПОДЕЛКОВ ИЗ СОВПАВШИХ КАТЕГОРИЙ ЧЕРЕЗ API GITHUB DISCUSSIONS (1 В 1 ОРИГИНАЛ) ===
        global_gallery_comments = []
        discussions = []
        
        if show_projects_column:
            print("\n[СТРОИТЕЛЬ] === РАДАР КАТЕГОРИЙ GITHUB DISCUSSIONS ===")
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
            lat = ["a", "b", "v", "g", "d", "e", "yo", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "yu", "ya"]
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

        # === СБОРКА ИТОГОВОЙ МАРКДАУН ТАБЛИЦЫ ДЛЯ ПРЕПОДАВАТЕЛЯ ===
        schedule_groups = sorted(list(students_data.get(target_day, {}).keys()))
        print(f"[СТРОИТЕЛЬ] Запланировано групп у {teacher_login} по YAML: {schedule_groups}")
        
        filled_times = sorted(list(temp_journal.keys()))
        print(f"[СТРОИТЕЛЬ] Получено групп от {teacher_login} с сайта: {filled_times}")

        # ПРОВЕРКА КОМПЛЕКТНОСТИ ГРУПП КОНКРЕТНОГО УЧИТЕЛЯ
        if len(filled_times) < len(schedule_groups):
            print(f"[СТРОИТЕЛЬ] ⏳ Комплект для '{teacher_login}' не собран ({len(filled_times)} из {len(schedule_groups)}). Пропускаем.")
            continue

        print(f"[СТРОИТЕЛЬ] 🟢 Полный комплект для '{teacher_login}' собран! Запускаем склейку...", flush=True)

        date_parts = date_str.split('-')
        formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]} г."
        
        markdown_body = f"### 📅 Журнал посещений за {formatted_date} ({pack.get('target_day', '')})\n\n"
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

            # 1. КОНТУР РЕГУЛЯРНЫХ УЧЕНИКОВ ИЗ YAML БАЗЫ РАСПИСАНИЯ (СОХРАНЯЕМ ИСХОДНЫЙ ОБЪЕКТ)
            for kid in permanent_kids:
                if not isinstance(kid, dict):
                    continue
                    
                kid_clean = kid.get("name", "").strip()
                raw_dir = kid.get("direction", "").strip().lower()
                kid_track = "электроника" if "электронное конструирование" in raw_dir else "столярное" if "столярное дело" in raw_dir else ""
                kid_tag = kid.get("tag", "").strip()

                # Намертво защищённая сверка факта присутствия по плоскому ключу name из JSON с сайта
                is_present = any(isinstance(p, dict) and p.get("name", "").strip().lower() == kid_clean.lower() for p in group_payload.get("present_permanent", []))
                
                # ЛОГИКА 1 В 1: Радар проектов в Discussions по хэштегу постоянного ученика
                project_link = ""
                if show_projects_column and kid_tag:
                    matches = [c for c in global_gallery_comments if c.get("body") and kid_tag in c["body"]]
                    if matches:
                        matches.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
                        project_link = f"🗂️ [Проект]({matches[0]['url']})"

                processed = {
                    "name_for_sort": kid_clean,
                    "track": kid_track,
                    "status": "🟢 Присутствовал" if is_present else "🔴 Отсутствовал",
                    "project": project_link,
                    "yaml_obj": kid  # Транзитом сохраняем исходный чистый объект расписания
                }
                block_permanent.append(processed)
                current_group_yaml_rows.append(processed["yaml_obj"])

            # 2. КОНТУР НОВИЧКОВ ИЗ JSON ОБЪЕКТОВ С САЙТА (ФОРМИРУЕМ ЧИСТЫЙ ОБЪЕКТ ДЛЯ БАЗЫ)
            for newbie in group_payload.get("newbies", []):
                if isinstance(newbie, dict) and newbie.get("name", "").strip():
                    newbie_name = newbie["name"].strip()
                    raw_dir = newbie.get("direction", "").strip().lower()
                    
                    newbie_track = "электроника" if "электронное конструирование" in raw_dir else "столярное" if "столярное дело" in raw_dir else ""
                    newbie_tag = newbie.get("tag", "").strip()

                    # ЛОГИКА 1 В 1: Автогенерация транслит-тега, если препод передал одиночный знак '#'
                    if newbie_tag == "#":
                        newbie_tag = f"#techlab-{translit_rus_to_lat(newbie_name)}"

                    # ЛОГИКА 1 В 1: Радар проектов в Discussions по хэштегу ученика
                    project_link = ""
                    if show_projects_column and newbie_tag:
                        matches = [c for c in global_gallery_comments if c.get("body") and newbie_tag in c["body"]]
                        if matches:
                            matches.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
                            project_link = f"🗂️ [Проект]({matches[0]['url']})"

                    # Строим кристально чистую объектную структуру для YAML базы расписания
                    new_yaml_obj = {"name": newbie_name}
                    if newbie_track:
                        new_yaml_obj["direction"] = "электронное конструирование" if newbie_track == "электроника" else "столярное дело"
                    if newbie_tag:
                        new_yaml_obj["tag"] = newbie_tag

                    processed = {
                        "name_for_sort": newbie_name,
                        "track": newbie_track,
                        "status": "🟡 Новичок",
                        "project": project_link,
                        "yaml_obj": new_yaml_obj
                    }
                    block_newbies.append(processed)
                    current_group_yaml_rows.append(processed["yaml_obj"])

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
                        "yaml_obj": None
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

        # Упаковываем все данные в изолированный пакет и добавляем в список
        report_packet = {
            "teacher_login": teacher_login,
            "markdown": markdown_body,
            "url": comment_url,
            "day": target_day,
            "yaml_group_updates": yaml_group_updates,
            "yaml_text_orig": pack["yaml_text_orig"],
            "yaml_sha": pack["yaml_sha"]
        }
        all_generated_reports.append(report_packet)
        print(f"\n[СТРОИТЕЛЬ] 📦 Пакет отчета для '{teacher_login}' успешно добавлен в очередь Телеграма.")
    
    print("=== [МОДУЛЬ: СТРОИТЕЛЬ] СБОРКА ОТЧЕТА ЗАВЕРШЕНА ===")

    # ФИНАЛЬНЫЙ СИГНАЛ КОНВЕЙЕРА ДЛЯ ГЛАВНОГО ДИСПЕТЧЕРА ТЕЛЕГРАМА (ВНЕ ЦИКЛА FOR)
    success_status = len(all_generated_reports) > 0
    return success_status, all_generated_reports
