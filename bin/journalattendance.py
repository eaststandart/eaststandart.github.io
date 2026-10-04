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
            response = requests.post("https://github.com", json=payload, headers=headers)
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

if __name__ == "__main__":
    main()

