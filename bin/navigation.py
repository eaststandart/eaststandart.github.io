#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation
@about Умный менеджер метаданных, валидатор связей и сборщик дерева навигации сайта.
@purpose Автоматизирует генерацию тегов (tags) и категорий (categories) для Jekyll 
         на основе свойств Obsidian, защищает сборку от опечаток и дубликатов в faire.
@author TechLab
@version 3.0-smart
"""

import os
import re
import yaml  # Используем стандартный PyYAML, доступный в GitHub Actions

def translit_title(text):
    """Очищает заголовок, превращая его в монолитный тег строчными буквами без пробелов и знаков."""
    if not text:
        return ""
    text = text.lower().strip()
    # Оставляем только буквы (русские и латинские) и цифры, удаляя пробелы и знаки
    text = re.sub(r'[^a-z0-9а-яё]', '', text)
    return text

def clean_tag(text):
    """Сжимает пробелы внутри тега, приводя его к нижнему регистру."""
    if not text:
        return ""
    return re.sub(r'\s+', '', str(text).lower().strip())

def parse_yaml_front_matter(file_path):
    """Извлекает и безопасно парсит блок Front Matter из markdown-файла."""
    content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось прочитать файл {file_path}: {e}")
        return None, None, content

    # Ищем блок между первыми двумя разделителями ---
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None, None, content

    front_matter_text = match.group(1)
    body_content = content[match.end():]

    try:
        data = yaml.safe_load(front_matter_text)
        return data if data else {}, front_matter_text, body_content
    except Exception as e:
        print(f"[NAV-ERROR] Сбой синтаксиса YAML во Front Matter в {file_path}: {e}")
        return None, None, content

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства в файл и сохраняет копию для Artifacts."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        # 📂 СОХРАНЕНИЕ КОПИИ ДЛЯ АРТЕФАКТОВ
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..'))
        debug_dir = os.path.join(root_dir, '_processed_files')
        os.makedirs(debug_dir, exist_ok=True)
        
        file_name = os.path.basename(file_path)
        debug_file_path = os.path.join(debug_dir, f"processed-{file_name}")
        
        # Записываем копию только с блоком свойств Front Matter (без тяжелого тела статьи)
        with open(debug_file_path, 'w', encoding='utf-8') as df:
            df.write(f"---\n{front_text}---\n[Тело статьи успешно обработано и скрыто для компактности]")

        # Основная перезапись файла для Jekyll
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось перезаписать файл {file_path}: {e}")

def build_navigation_tree():
    """Главный конвейер сборки дерева навигации и точечной обработки свойств."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    # 1. АВТОМАТИЧЕСКИЙ СБОР БЕЛОГО СПИСКА ПРОЕКТОВ (Валидатор)
    # Скрипт сканирует папки внутри faire/ и берет их латинские имена за эталон
    faire_dir = os.path.join(root_dir, 'faire')
    valid_slugs = set()
    
    if os.path.exists(faire_dir):
        for entry in os.scandir(faire_dir):
            if entry.is_dir() and not entry.name.startswith('.'):
                valid_slugs.add(entry.name)
                
    print(f"[NAV-INFO] Автоматически собран белый список проектов faire: {list(valid_slugs)}")

    # Инициализация дерева для вывода в navigation.yml
    nav_tree = {
        'faire': []
    }
    
    # Внутренний реестр для отслеживания уникальности (контроль дубликатов по датам)
    # Ключ: (проект, дата, тип), Значение: имя_файла
    posts_registry = {}
    
    # Временное хранилище для сопутствующих постов, чтобы потом привязать их к проектам
    related_posts_map = {slug: {'journal': [], 'media': []} for slug in valid_slugs}

    # 2. ЭТАП СБОРКИ И АНАЛИЗА ПАПКИ _POSTS (Маленькие заметки)
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'):
                    continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                
                if data is None:
                    continue
                
                # Проверяем, относится ли этот пост к разделу faire
                section = data.get('githubpages-section')
                if section != 'faire':
                    continue # Пока работаем локально только с faire

                # Проверка статуса публикации (Черновики полностью игнорируем)
                if data.get('published') is False:
                    continue

                post_slug = data.get('githubpages-slug')
                post_date = str(data.get('date', ''))
                post_type = data.get('githubpages-type') # journal или media

                # А. Защита от опечаток в слагах проектов
                if post_slug not in valid_slugs:
                    print(f"\n[❌ КРИТИЧЕСКАЯ ОШИБКА] В файле {file} указан неизвестный githubpages-slug: '{post_slug}'.")
                    print(f"Такого проекта нет в папке faire/. Сборка сайта ОСТАНОВЛЕНА!")
                    exit(1)

                # Б. Защита от дубликатов дат в рамках одного проекта
                registry_key = (post_slug, post_date, post_type)
                if registry_key in posts_registry:
                    print(f"\n[❌ КРИТИЧЕСКАЯ ОШИБКА] Обнаружен конфликт имен и дат!")
                    print(f"Файлы '{file}' и '{posts_registry[registry_key]}' имеют одинаковую дату ({post_date}) и тип ({post_type}) внутри проекта '{post_slug}'.")
                    print(f"Пожалуйста, сделайте даты или имена уникальными. Сборка сайта ОСТАНОВЛЕНА!")
                    exit(1)
                else:
                    posts_registry[registry_key] = file

                # В. Автоматическая генерация тегов (tags) по нашей формуле
                calculated_tags = []
                
                # 1. Из направления (direction)
                if data.get('githubpages-direction'):
                    calculated_tags.append(clean_tag(data['githubpages-direction']))
                # 2. Из сущности (entity)
                if data.get('githubpages-entity'):
                    calculated_tags.append(clean_tag(data['githubpages-entity']))
                # 3. Из уровня/класса (level)
                if data.get('githubpages-level'):
                    level_clean = str(data['githubpages-level']).strip()
                    calculated_tags.append(f"{level_clean}класс")
                # 4. Автоматический тег из заголовка (title) без пробелов строчными
                if data.get('title'):
                    calculated_tags.append(translit_title(data['title']))
                # 5. Из дополнительных ключевых слов (keywords)
                if data.get('keywords'):
                    if isinstance(data['keywords'], list):
                        for kw in data['keywords']:
                            calculated_tags.append(clean_tag(kw))
                    else:
                        calculated_tags.append(clean_tag(data['keywords']))

                # Очищаем от пустых элементов и дубликатов, сохраняя порядок
                final_tags = []
                for t in calculated_tags:
                    if t and t not in final_tags:
                        final_tags.append(t)

                # Записываем сгенерированные теги в стандартное поле Jekyll
                data['tags'] = final_tags
                # Удаляем временное поле keywords из выгрузки сайта для чистоты
                if 'keywords' in data:
                    del data['keywords']

                # Г. Автоматическая генерация категорий (categories) для Jekyll
                data['categories'] = [post_type, post_slug]

                # Перезаписываем .md файл со стандартными для Jekyll полями
                write_yaml_front_matter(full_path, data, body)

                # Вычисляем короткий будущий URL-адрес для записи в navigation.yml
                file_name_clean, _ = os.path.splitext(file)
                file_name_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)

                short_url = f"/{post_type}/{post_slug}/{post_date.replace('-', '/')}/{file_name_clean}.html"

                # Сохраняем пост в карту связей проекта
                if post_type in ['journal', 'media']:
                    related_posts_map[post_slug][post_type].append({
                        'title': data.get('title', file_name_clean),
                        'url': short_url,
                        'date': post_date
                    })

    # 3. ЭТАП СБОРКИ ГЛАВНЫХ СТРАНИЦ ПРОЕКТОВ ИЗ ПАПКИ FAIRE
    if os.path.exists(faire_dir):
        for root, _, files in os.walk(faire_dir):
            for file in files:
                if not file.endswith('.md'):
                    continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                
                if data is None:
                    continue

                if data.get('published') is False:
                    continue

                project_slug = data.get('githubpages-slug')
                if not project_slug:
                    continue

                # Также прогоняем формулу автоматических тегов для главной страницы проекта
                proj_tags = []
                if data.get('githubpages-direction'):
                    proj_tags.append(clean_tag(data['githubpages-direction']))
                if data.get('githubpages-entity'):
                    proj_tags.append(clean_tag(data['githubpages-entity']))
                if data.get('githubpages-level'):
                    proj_tags.append(f"{str(data['githubpages-level']).strip()}класс")
                if data.get('title'):
                    proj_tags.append(translit_title(data['title']))
                if data.get('keywords'):
                    if isinstance(data['keywords'], list):
                        for kw in data['keywords']: proj_tags.append(clean_tag(kw))
                    else:
                        proj_tags.append(clean_tag(data['keywords']))

                final_proj_tags = []
                for t in proj_tags:
                    if t and t not in final_proj_tags: final_proj_tags.append(t)

                data['tags'] = final_proj_tags
                if 'keywords' in data: 
                    del data['keywords']

                write_yaml_front_matter(full_path, data, body)

                # Вычисляем URL главной страницы проекта
                final_url = data.get('permalink', f"/faire/{project_slug}/")

                # Сортируем связанные посты проекта по дате (от новых к старым)
                journal_sorted = sorted(related_posts_map[project_slug]['journal'], key=lambda x: x['date'], reverse=True)
                media_sorted = sorted(related_posts_map[project_slug]['media'], key=lambda x: x['date'], reverse=True)

                # Упаковываем проект со всеми его внутренними списками в дерево навигации
                nav_tree['faire'].append({
                    'title': data.get('title', project_slug),
                    'url': final_url,
                    'direction': data.get('githubpages-direction', ''),
                    'level': data.get('githubpages-level', ''),
                    'journal_posts': journal_sorted,
                    'media_posts': media_sorted
                })

        # Сортируем список самих проектов в разделе faire по алфавиту заголовков
        nav_tree['faire'] = sorted(nav_tree['faire'], key=lambda x: x['title'].lower())

    # 4. ЗАПИСЬ СТРУКТУРИРОВАННОГО УМНОГО ДЕРЕВА В _DATA/NAVIGATION.YML
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        with open(output_file, 'w', encoding='utf-8') as yml:
            yml.write("# Умная автоматическая карта метаданных сайта Jekyll. НЕ ПРАВИТЬ РУКАМИ!\n")
            yaml.dump(nav_tree, yml, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[NAV-SUCCESS] Карта навигации и связей успешно сохранена в _data/navigation.yml")
    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации: {e}")

if __name__ == '__main__':
    build_navigation_tree()
