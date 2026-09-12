#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation
@about Универсальный статический препроцессор метаданных и карты разделов.
@purpose Автоматически вычисляет разделы по физическим папкам на диске,
         извлекает слаги и типы постов из имён файлов и строит дерево sections в _data/navigation.yml.
@author TechLab
@version 5.0.0-blind-automaton
"""

import os
import re
import yaml

def translit_title(text):
    """Очищает заголовок, превращая его в монолитный тег строчными буквами без пробелов."""
    if not text: return ""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9а-яё]', '', text)
    return text

def clean_tag(text):
    """Сжимает пробелы внутри тега, приводя его к нижнему регистру."""
    if not text: return ""
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

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match: return None, None, content

    front_matter_text = match.group(1)
    body_content = content[match.end():]

    try:
        data = yaml.safe_load(front_matter_text)
        return data if data else {}, front_matter_text, body_content
    except Exception as e:
        print(f"[NAV-ERROR] Сбой синтаксиса YAML во Front Matter в {file_path}: {e}")
        return None, None, content

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства обратно в файл и создает отладочные логи."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..'))
        debug_dir = os.path.join(root_dir, '_processed_files')
        os.makedirs(debug_dir, exist_ok=True)
        
        file_name = os.path.basename(file_path)
        debug_file_path = os.path.join(debug_dir, f"processed-{file_name}")
        
        with open(debug_file_path, 'w', encoding='utf-8') as df:
            df.write(f"---\n{front_text}---\n[Тело статьи успешно обработано]")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось перезаписать файл {file_path}: {e}")

def build_navigation_tree():
    """Главный конвейер сборки дерева навигации сайта."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    # 1. АВТОМАТИЧЕСКИЙ СБОР РАЗДЕЛОВ И КОЛЛЕКЦИЙ С ДИСКА (Исключаем только служебные папки)
    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    
    supported_sections = []
    valid_slugs = set()
    slug_to_section_map = {}

    # Сканируем корень сайта и автоматически определяем живые разделы и коллекции
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            # Пропускаем только системный мусор и служебные папки из EXCLUDED_FOLDERS
            if not name.startswith('.') and name != '_posts' and name not in EXCLUDED_FOLDERS:
                # Очищаем имя от нижнего подчёркивания для карты данных (_people -> people)
                clean_section_name = name.lstrip('_')
                supported_sections.append(clean_section_name)
                
                # Заходим внутрь папки раздела и собираем имена подпапок проектов в качестве слагов
                section_dir = os.path.join(root_dir, name)
                for entry in os.scandir(section_dir):
                    if entry.is_dir() and not entry.name.startswith('.'):
                        valid_slugs.add(entry.name)
                        # Связываем слаг проекта с чистым именем его раздела
                        slug_to_section_map[entry.name] = clean_section_name

    print(f"[NAV-INFO] Автоматически обнаружены разделы сайта: {supported_sections}")
    print(f"[NAV-INFO] Белый список слагов проектов собран с диска: {list(valid_slugs)}")

    # Инициализируем чистую древовидную структуру разделов под имя 'sections'
    nav_tree = {
        'sections': {section: [] for section in supported_sections}
    }
    
    posts_registry = {}
    related_posts_map = {slug: {'journal': [], 'media': []} for slug in valid_slugs}

    # 2. ЭТАП АНАЛИЗА ПАПКИ _POSTS (Умный алгоритм разделения слага и типа поста по белому списку)
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                if data is None or data.get('published') is False: continue

                # Отрезаем расширение и дату с начала файла
                file_name_clean, _ = os.path.splitext(file)
                file_name_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean) # Получаем 'muzykalnyj-karandash-journal'

                # ВАШ ЗОЛОТОЙ АЛГОРИТМ: Разбираем хвост по последнему дефису
                post_slug = None
                post_page_type = None

                if '-' in file_name_clean:
                    # Разделяем строго по последнему дефису справа
                    possible_slug, possible_type = file_name_clean.rsplit('-', 1)
                    
                    # Железная проверка: если полученный слаг реально существует в белом списке проектов на диске
                    if possible_slug in valid_slugs:
                        post_slug = possible_slug
                        post_page_type = possible_type  # Это гарантированно служебное слово (journal, media, questions и т.д.)
                
                # Если проверка не прошла (как в случае с muzykalnyj-golos-media), считаем это обычным автономным постом
                if not post_slug:
                    print(f"[NAV-NOTE] Файл '{file}' признан обычным автономным постом, пропускаем интеграцию во вкладки.")
                    continue

                post_date = str(data.get('date', ''))

                # Защита от дубликатов дат внутри одного проекта
                registry_key = (post_slug, post_date, post_page_type)
                if registry_key in posts_registry:
                    print(f"\n[❌ КРИТИЧЕСКАЯ ОШИБКА] Конфликт дат в '{file}' и '{posts_registry[registry_key]}'.")
                    exit(1)
                posts_registry[registry_key] = file

                # Автоматическая генерация тегов по чистому стандарту
                calculated_tags = []
                if data.get('direction'): calculated_tags.append(clean_tag(data['direction']))
                if data.get('entity'): calculated_tags.append(clean_tag(data['entity']))
                if data.get('level'): calculated_tags.append(f"{str(data['level']).strip()}класс")
                if data.get('title'): calculated_tags.append(translit_title(data['title']))
                if data.get('keywords'):
                    if isinstance(data['keywords'], list):
                        for kw in data['keywords']: calculated_tags.append(clean_tag(kw))
                    else: calculated_tags.append(clean_tag(data['keywords']))

                final_tags = []
                for t in calculated_tags:
                    if t and t not in final_tags: final_tags.append(t)

                data['tags'] = final_tags
                if 'keywords' in data: del data['keywords']

                # 🔥 СОХРАНЯЕМ ДВОЙНЫЕ КАТЕГОРИИ ДЛЯ ВНУТРЕННИХ СКРИПТОВ JEKYLL
                data['categories'] = [post_page_type, post_slug]
                
                # Записываем служебный тип в поле section, чтобы шапка нашла вывеску архива
                data['section'] = post_page_type
                
                # Перезаписываем файл со всеми системными свойствами
                write_yaml_front_matter(full_path, data, body)

                # Рассчитываем адрес ссылки строго по новой лаконичной маске конфига (БЕЗ слова journal в путях!)
                short_url = f"/{post_date.replace('-', '/')}/{file_name_clean}.html"

                # Направляем запись на нужную локальную полочку проекта для построения дерева навигации
                if post_page_type in related_posts_map[post_slug]:
                    related_posts_map[post_slug][post_page_type].append({
                        'title': data.get('title', file_name_clean),
                        'url': short_url,
                        'date': post_date
                    })
                else:
                    # Если появилось новое служебное слово (например, 'questions'), динамически создаём под него полочку
                    if post_page_type not in related_posts_map[post_slug]:
                        related_posts_map[post_slug][post_page_type] = []
                    related_posts_map[post_slug][post_page_type].append({
                        'title': data.get('title', file_name_clean),
                        'url': short_url,
                        'date': post_date
                    })

    # 3. ЭТАП СБОРКИ ГЛАВНЫХ СТРАНИЦ ПРОЕКТОВ И СВОЙСТВ КОЛЛЕКЦИЙ (Люди, Справки и т.д.)
    # Сканируем физические папки на диске, соответствующие обнаруженным разделам
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            if not name.startswith('.') and name != '_posts' and name not in EXCLUDED_FOLDERS:
                clean_section_name = name.lstrip('_')
                section_dir = os.path.join(root_dir, name)
                
                # Обходим все .md файлы внутри этого раздела/коллекции
                for root_walk, _, files in os.walk(section_dir):
                    for file in files:
                        if not file.endswith('.md'): continue
                        
                        full_path = os.path.join(root_walk, file)
                        data, front_text, body = parse_yaml_front_matter(full_path)
                        if data is None or data.get('published') is False: continue

                        # Вычисляем слаг: для подпапок это имя подпапки, для плоских файлов - имя файла
                        relative_path = os.path.relpath(root_walk, section_dir)
                        if relative_path == '.':
                            # Файл лежит прямо в корне папки раздела (например, _people/fran-blanche.md)
                            project_slug, _ = os.path.splitext(file)
                        else:
                            # Файл лежит внутри подпапки проекта (например, faire/muzykalnyj-karandash/muzykalnyj-karandash.md)
                            project_slug = relative_path.split(os.sep)[0]

                        # Формируем и вшиваем автоматические теги
                        proj_tags = []
                        if data.get('direction'): proj_tags.append(clean_tag(data['direction']))
                        if data.get('entity'): proj_tags.append(clean_tag(data['entity']))
                        if data.get('level'): proj_tags.append(f"{str(data['level']).strip()}класс")
                        if data.get('title'): proj_tags.append(translit_title(data['title']))
                        if data.get('keywords'):
                            if isinstance(data['keywords'], list):
                                for kw in data['keywords']: proj_tags.append(clean_tag(kw))
                            else: proj_tags.append(clean_tag(data['keywords']))

                        final_proj_tags = []
                        for t in proj_tags:
                            if t and t not in final_proj_tags: final_proj_tags.append(t)

                        data['tags'] = final_proj_tags
                        if 'keywords' in data: del data['keywords']

                        # 🔥 ЖЕЛЕЗНЫЙ ЗАКОН ССЫЛОК: Автоматически формируем permalink и section
                        final_url = f"/{clean_section_name}/{project_slug}/"
                        data['permalink'] = final_url
                        data['section'] = clean_section_name

                        # Перезаписываем md-файл со всеми сгенерированными полями
                        write_yaml_front_matter(full_path, data, body)

                        # Собираем все динамические типы постов, которые нашлись для этого проекта
                        project_posts_data = {}
                        if project_slug in related_posts_map:
                            for p_type, p_list in related_posts_map[project_slug].items():
                                project_posts_data[f"{p_type}_posts"] = sorted(p_list, key=lambda x: x['date'], reverse=True)

                        # Базовые свойства проекта для дерева навигации
                        project_node = {
                            'title': data.get('title', project_slug),
                            'slug': project_slug,
                            'url': final_url,
                            'direction': data.get('direction', ''),
                            'level': data.get('level', '')
                        }
                        
                        # Динамически подмешиваем все массивы постов (journal_posts, media_posts, questions_posts и т.д.)
                        project_node.update(project_posts_data)

                        # Кладём проект на полочку его раздела в дереве
                        nav_tree['sections'][clean_section_name].append(project_node)

        # Сортируем элементы внутри каждого раздела по алфавиту заголовков
        if clean_section_name in nav_tree['sections']:
            nav_tree['sections'][clean_section_name] = sorted(
                nav_tree['sections'][clean_section_name], 
                key=lambda x: x['title'].lower()
            )

    # 4. ЗАПИСЬ СТРУКТУРИРОВАННОГО УМНОГО ДЕРЕВА В _DATA/NAVIGATION.YML
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(nav_tree, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print("[NAV-SUCCESS] Карта навигации 'sections' успешно сохранена в _data/navigation.yml")

        # 📂 АВТОГЕНЕРАЦИЯ СТРАНИЦ-ЛЕНТ ДЛЯ КНОПКИ "0" (Для всех динамических типов постов)
        for section_name, projects_list in nav_tree['sections'].items():
            for project in projects_list:
                slug = project['slug']
                
                # Ищем, какие типы постов реально привязаны к этому проекту в памяти
                detected_types = ['journal', 'media'] # Базовые дефолтные типы
                if slug in related_posts_map:
                    for found_type in related_posts_map[slug].keys():
                        if found_type not in detected_types:
                            detected_types.append(found_type)

                # Штампуем страницы index.md под каждый обнаруженный тип контента проекта
                for post_type in detected_types:
                    dir_path = os.path.join(root_dir, post_type, slug)
                    os.makedirs(dir_path, exist_ok=True)
                    
                    file_path = os.path.join(dir_path, 'index.md')
                    with open(file_path, 'w', encoding='utf-8') as pf:
                        type_title = f"публикации типа {post_type}"
                        if post_type == "journal": type_title = "посты журнала"
                        elif post_type == "media": type_title = "посты галереи"
                        
                        pf.write(f"---\n")
                        pf.write(f"layout: page\n")
                        pf.write(f"title: \"{project['title']}: {type_title}\"\n")
                        pf.write(f"slug: {slug}\n")
                        pf.write(f"section: {section_name}\n")
                        pf.write(f"post-page: {post_type}\n")
                        pf.write(f"mathjax: true\n")
                        pf.write(f"---\n\n")
                        pf.write(f"{{% include posts-page-open.liquid type='{post_type}' %}}\n")

    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации или автогенерации кнопка '0': {e}")

if __name__ == '__main__':
    build_navigation_tree()
