import os
import json
import sys
import yaml

def main():
    print("=== ЛОГ РОБОТА PYTHON: ИНИЦИАЛИЗАЦИЯ ===")
    
    data_dir = os.path.join(os.getcwd(), '_data')
    if not os.path.exists(data_dir):
        print(f"КРИТИЧЕСКАЯ ОШИБКА: Папка с данными не найдена: {data_dir}")
        return

    # 1. Ищем временные файлы журналов групп за сегодняшний день
    all_files = os.listdir(data_dir)
    group_files = [f for f in all_files if '-journal-attendance-' in f and f.endswith('.json')]
    
    if not group_files:
        print("Временные файлы журналов групп не найдены.")
        return

    # Читаем первый попавшийся JSON-файл с сайта, чтобы определить параметры дня
    sample_path = os.path.join(data_dir, group_files[0])
    with open(sample_path, 'r', encoding='utf-8') as f:
        sample_data = json.load(f)
        
    target_day = sample_data.get('day', '').lower().strip()
    date_str = sample_data.get('date', '')
    teacher_username = sample_data.get('teacher_username', 'Преподаватель')
    teacher_login = sample_data.get('teacher_login', '')

    print(f"Обнаружена дата занятия: {date_str} ({target_day})")

    # 2. Считываем настройки из личного YAML-файла расписания учителя
    yaml_path = os.path.join(data_dir, f"journal-attendance-{teacher_login}.yml")
    if not os.path.exists(yaml_path):
        print(f"КРИТИЧЕСКАЯ ОШИБКА: Личный файл расписания не найден: {yaml_path}")
        return

    with open(yaml_path, 'r', encoding='utf-8') as f:
        # PyYAML автоматически превращает весь YAML в удобный словарь Python!
        yaml_data = yaml.safe_load(f) or {}

    # ИСПРАВЛЕНО: Создаем чистую переменную расписания студентов, убирая из нее технический блок config
    students_data = {k: v for k, v in yaml_data.items() if k != 'config'}

    # Вытаскиваем блок config с дефолтными значениями-страховками
    config_data = yaml_data.get('config', {})
    
    publish_as_bot = config_data.get('publish_as_bot', False)
    show_projects_column = config_data.get('show_projects_column', True)
    discussion_number = config_data.get('discussion_number', 38)
    
    # Забираем категории: если там одна строка, превращаем в список, если список — берем как есть
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

    # === ШАГ 2: ГЛОБАЛЬНЫЙ СБОР ВСЕХ ПОДЕЛКОВ ИЗ СОВПАВШИХ КАТЕГОРИЙ ЧЕРЕЗ API ===
    global_gallery_comments = []
    
    if show_projects_column:
        import requests
        print("\n=== [РАДАР КАТЕГОРИЙ GITHUB НА PYTHON] ===")
        print(f"Запуск сканирования для категорий: {project_categories}")
        
        # Получаем административный токен из системного окружения виртуальной машины
        admin_token = os.environ.get("MY_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not admin_token:
            print("[ШАГ 2] ❌ КРИТИЧЕСКАЯ ОШИБКА: Токен авторизации GitHub не найден в окружении!")
            return

        # Наш пуленепробиваемый GraphQL-запрос к серверу GitHub
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
            # Отправляем сетевой запрос на сервер GitHub
            response = requests.post("https://api.github.com/graphql", json=payload, headers=headers)
            if response.status_code != 200:
                print(f"[ШАГ 2] ❌ Ошибка сети API GitHub: Статус {response.status_code}")
                return
                
            res_json = response.json()
            if "errors" in res_json:
                print(f"[ШАГ 2] ❌ Ошибка GraphQL от сервера: {json.dumps(res_json['errors'])}")
                return
                
            discussions = res_json.get("data", {}).get("repository", {}).get("discussions", {}).get("nodes", [])
            
            # Собираем все реально существующие в репозитории категории для вывода в отладочный лог
            all_repo_categories = list(set([d["category"]["name"] for d in discussions if d.get("category")]))
            print(f"Обнаружены категории в Discussions: {all_repo_categories}")
            
            # Переводим список категорий учителя в нижний регистр для безопасной сверки без учета регистра
            search_cats_lower = [c.lower().strip() for c in project_categories]
            
            # Фильтруем топики: оставляем только те категории, которые указал учитель в Obsidian!
            for d in discussions:
                if d.get("category") and d["category"]["name"].lower().strip() in search_cats_lower:
                    comments_nodes = d.get("comments", {}).get("nodes", [])
                    if comments_nodes:
                        global_gallery_comments.extend(comments_nodes)
                        
            print(f"[ШАГ 2] Успешно загружено комментов для анализа из всех совпавших категорий: {len(global_gallery_comments)}")
            print("=========================================\n")
            
        except Exception as err:
            print(f"[ШАГ 2] ❌ Исключение при глобальном сборе поделок: {str(err)}")
            
    # === ВНУТРЕННИЕ ФУНКЦИИ КОНВЕЙЕРА ОБРАБОТКИ ИМЁН И ТРАНСЛИТА ===
    def translit_rus_to_lat(text):
        rus = "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я".split()
        lat = "a b v g d e yo zh z i y k l m n o p r s t u f kh ts ch sh shch  y  e yu ya".split()
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
        print(f"\n=== [РАДАР YAML БАЗЫ PYTHON] ===")
        print(f"Функция получила rawName: '{raw_name}' (Длина: {len(raw_name)})")
        print(f"Посимвольный код rawName: {' '.join(str(ord(c)) for c in raw_name)}")

        track = ""
        project_link = ""

        # Находим готовый тег (@ник или #тег)
        import re
        match_ready = re.search(r'(@[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+)', raw_name)
        target_tag = match_ready.group(0) if match_ready else ""
        print(f"Результат поиска готового тега: '{target_tag}'")

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
            print(f"[АВТОГЕНЕРАЦИЯ] Одиночный знак # успешно заменен на латинский тег: {target_tag}")

        # ГЛОБАЛЬНЫЙ РАДАР ПОИСКА ПОДЕЛКИ В НАШЕМ СКАЧАННОМ МЕШКЕ ИЗ 38 КОММЕНТОВ (ИСПРАВЛЕНО НАЧИСТО!)
        if show_projects_column and target_tag:
            matches = []
            for c in global_gallery_comments:
                if c.get("body") and target_tag in c["body"]:
                    matches.append(c)
            if matches:
                # Сортируем от свежих к старым
                matches.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
                # Исправлено: убран бэктик в конце скобки и добавлен индекс [0]
                project_link = f"[🔍 Поделка]({matches[0]['url']})"
                
                # Ищем, к какому топику и категории принадлежал этот коммент
                parent_cat = "Неизвестная категория"
                for d in discussions:
                    if d.get("comments") and any(com["url"] == matches[0]["url"] for com in d["comments"].get("nodes", [])):
                        parent_cat = d["category"]["name"]
                        break
                        
                print(f"[РАДАР] Робот нашёл поделку в категории \"{parent_cat}\" для {normalized} по тегу {target_tag} -> {matches[0]['url']}")

        # Вычисляем чистое имя для вывода в журнал на сайт
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

    # === ШАГ 3: ПОСЛЕДОВАТЕЛЬНАЯ ГЕНЕРАЦИЯ СВОДНОГО ОТЧЕТА ТАБЛИЦЫ (ЭТАЛОННАЯ JS-ЛОГИКА) ===
    # Собираем данные из всех прилетевших сегодня JSON файлов с сайта
    temp_journal = {}
    todays_files = [f for f in os.listdir(data_dir) if f.startswith(f"{date_str}-") and f.endswith(".json")]
    for file in todays_files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8') as f:
            file_data = json.load(f)
            temp_journal[file_data["time"]] = file_data

    # Зеркально берем запланированные группы дня строго из YAML базы расписания
    schedule_groups = sorted(list(students_data.get(target_day, {}).keys()))
    print(f"Запланированные группы из YAML базы: {schedule_groups}")
    
    filled_times = sorted(list(temp_journal.keys()))
    print(f"Полученные группы с сайта за сегодня: {filled_times}")

    # ЗЕРКАЛЬНАЯ СТРАХОВКА КОМПЛЕКТНОСТИ ДНЯ: Если прилетели еще не все группы, останавливаем шаг!
    if len(filled_times) < len(schedule_groups):
        print("=== СТАТУС СБОРКИ ===")
        print(f"Ожидаем остальные группы. Комплект не собран ({len(filled_times)} из {len(schedule_groups)}). Завершаем шаг.")
        return

    print("=== СТАТУС СБОРКИ ===")
    print("Все группы дня получены! Запускаем склейку и генерацию итогового отчета...")

    import re
    date_parts = date_str.split('-')
    formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]} г."
    
    markdown_body = f"### 📅 Журнал посещений за {formatted_date} ({sample_data.get('day', '')})\n\n"
    if show_projects_column:
        markdown_body += "| Группа / Ученик | Статус | Направление | Чем занят? |\n"
        markdown_body += "| :--- | :--- | :--- | :--- |\n"
    else:
        markdown_body += "| Группа / Ученик | Статус | Направление |\n"
        markdown_body += "| :--- | :--- | :--- |\n"

    yaml_group_updates = {}

    for time in schedule_groups:
        print(f"\n--- Обработка группы {time} ---")
        if show_projects_column:
            markdown_body += f"| **⏰ ГРУППА {time}** | | | |\n"
        else:
            markdown_body += f"| **⏰ ГРУППА {time}** | | |\n"

        group_payload = temp_journal.get(time, {"present_permanent": [], "newbies": [], "probation": []})
        # ИСПРАВЛЕНО НАЧИСТО: Извлекаем список реальных имен детей из расписания
        permanent_kids = students_data.get(target_day, {}).get(time, [])

        block_permanent = []
        block_newbies = []
        block_probation = []
        current_group_yaml_rows = []

        # 3.1. Разбор постоянного состава из YAML базы
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

        # 3.2. Разбор новичков с сайта
        for newbie in group_payload.get("newbies", []):
            if newbie.strip():
                processed = process_kid_row(newbie, "🟡 Новичок")
                block_newbies.append(processed)
                current_group_yaml_rows.append(processed["yaml_line"])

        # 3.3. Разбор временных пробных детей
        for prob in group_payload.get("probation", []):
            if prob.strip():
                processed = process_kid_row(prob, "🔵 Пробное")
                block_probation.append(processed)

        # Алфавитная сортировка по чистому имени от А до Я
        block_permanent.sort(key=lambda x: x["name_for_sort"].lower())
        block_newbies.sort(key=lambda x: x["name_for_sort"].lower())
        block_probation.sort(key=lambda x: x["name_for_sort"].lower())

        # Печать в Markdown ячейки отчета
        for row in block_permanent:
            markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"
        for row in block_newbies:
            markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"
        for row in block_probation:
            markdown_body += f"| {row['name_for_sort']} | {row['status']} | {row['track']} | {row['project'] if row['project'] else ' '} |\n" if show_projects_column else f"| {row['name_for_sort']} | {row['status']} | {row['track']} |\n"

        # Алфавитная сортировка списка для перезаписи YAML базы преподавателя
        current_group_yaml_rows.sort(key=lambda x: re.sub(r'\[э\]|\[с\]|@[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+', '', x, flags=re.IGNORECASE).strip().lower())
        yaml_group_updates[time] = current_group_yaml_rows

    markdown_body += f"\n*Проверил и отправил преподаватель: **{teacher_username}***\n"
    print("\n[ШАГ 3] Итоговая таблица Markdown успешно сформирована в памяти!")

if __name__ == "__main__":
    main()
