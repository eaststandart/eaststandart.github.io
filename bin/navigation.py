#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation
@about Универсальный менеджер метаданных, валидатор связей и сборщик дерева навигации сайта.
@purpose Автоматизирует генерацию тегов, категорий и permalink на основе чистых свойств Obsidian,
         вычисляя разделы по имени физических папок.
@author TechLab
@version 4.0.0-smart
"""

import os
import re
import yaml

def translit_title(text):
    """Очищает заголовок, превращая его в монолитный тег строчными буквами без пробелов и знаков."""
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
    """Записывает обновленные свойства в файл и сохраняет копию для Artifacts."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..'))
        debug_dir = os.path.join(root_dir, '_processed_files')
        os.makedirs(debug_dir, exist_ok=True)
        
        file_name = os.path.basename(file_path)
        debug_file_path = os.path.join(debug_dir, f"processed-{file_name}")
        
        with open(debug_file_path, 'w', encoding='utf-8') as df:
            df.write(f"---\n{front_text}---\n[Тело статьи успешно обработано и скрыто для компактности]")

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

    # 1. АВТОМАТИЧЕСКИЙ СБОР РАЗДЕЛОВ И СЛАГОВ ПРОЕКТОВ (Полный автомат по папкам)
    EXCLUDED_FOLDERS = {'_posts', '_includes', '_data', '_layouts', '_people', '_processed_files', 'assets', 'bin', '.git', '.github'}
    
    supported_sections = []
    valid_slugs = set()
    slug_to_section_map = {}

    # Находим живые папки разделов в корнях сайта
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            if not name.startswith('.') and not name.startswith('_') and name not in EXCLUDED_FOLDERS:
                supported_sections.append(name)
                
    print(f"[NAV-INFO] Автоматически обнаружены разделы сайта: {supported_sections}")

    # Заглядываем внутрь файлов разделов и собираем эталонные слаги по свойству 'slug'
    for section in supported_sections:
        section_dir = os.path.join(root_dir, section)
        for root, _, files in os.walk(section_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                full_path = os.path.join(root, file)
                data, _, _ = parse_yaml_front_matter(full_path)
                
                if data and data.get('published') is not False:
                    file_slug = data.get('slug')
                    if file_slug:
                        valid_slugs.add(file_slug)
                        slug_to_section_map[file_slug] = section
                
    print(f"[NAV-INFO] Белый список слагов успешно собран: {list(valid_slugs)}")

    # Универсальная древовидная карта данных под кодовым именем 'sections'
    nav_tree = {
        'sections': {section: [] for section in supported_sections}
    }
    
    posts_registry = {}
    related_posts_map = {slug: {'journal': [], 'media': []} for slug in valid_slugs}

    # 2. ЭТАП СБОРКИ И АНАЛИЗА ПАПКИ _POSTS (Маленькие заметки по новому стандарту)
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                if data is None or data.get('published') is False: continue
                
                # Извлекаем имя раздела по слагу проекта из нашей карты
                post_slug = data.get('slug')
                if not post_slug or post_slug not in valid_slugs: continue
                
                post_date = str(data.get('date', ''))
                post_page_type = data.get('post-page') # Новое свойство 'post-page' вместо 'type'

                # Защита от дубликатов дат
                registry_key = (post_slug, post_date, post_page_type)
                if registry_key in posts_registry:
                    print(f"\n[❌ КРИТИЧЕСКАЯ ОШИБКА] Конфликт дат в '{file}' и '{posts_registry[registry_key]}'.")
                    exit(1)
                posts_registry[registry_key] = file

                # Автоматическая генерация тегов по новым чистым свойствам
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

                # Автоматически прописываем Jekyll категории и раздел
                data['categories'] = [post_page_type, post_slug]
                data['section'] = slug_to_section_map.get(post_slug, '')
                write_yaml_front_matter(full_path, data, body)

                file_name_clean, _ = os.path.splitext(file)
                file_name_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)
                short_url = f"/{post_page_type}/{post_slug}/{post_date.replace('-', '/')}/{file_name_clean}.html"

                if post_page_type in ['journal', 'media']:
                    related_posts_map[post_slug][post_page_type].append({
                        'title': data.get('title', file_name_clean),
                        'url': short_url,
                        'date': post_date
                    })

    # 3. ЭТАП СБОРКИ И АВТОМАТИЧЕСКОЙ ДОПИСИ PROPERTIES ГЛАВНЫХ СТРАНИЦ
    for section in supported_sections:
        section_dir = os.path.join(root_dir, section)
        if os.path.exists(section_dir):
            for root, _, files in os.walk(section_dir):
                for file in files:
                    if not file.endswith('.md'): continue
                    
                    full_path = os.path.join(root, file)
                    data, front_text, body = parse_yaml_front_matter(full_path)
                    if data is None or data.get('published') is False: continue

                    project_slug = data.get('slug')
                    if not project_slug: continue

                    # Прогоняем формулу автоматических тегов для главной страницы
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

                    # 🔥 ГЕНИАЛЬНОЕ УПРОЩЕНИЕ: Автоматически формируем и вшиваем permalink!
                    # Берем section (имя папки раздела) и project_slug (свойство slug из файла)
                    final_url = f"/{section}/{project_slug}/"
                    data['permalink'] = final_url
                    data['section'] = section

                    # Перезаписываем md-файл проекта со всеми сгенерированными полями
                    write_yaml_front_matter(full_path, data, body)

                    # Сортируем связанные посты проекта по дате (от новых к старым)
                    journal_sorted = sorted(related_posts_map.get(project_slug, {}).get('journal', []), key=lambda x: x['date'], reverse=True)
                    media_sorted = sorted(related_posts_map.get(project_slug, {}).get('media', []), key=lambda x: x['date'], reverse=True)

                    # Упаковываем проект со всеми его внутренними списками в дерево навигации
                    nav_tree['sections'][section].append({
                        'title': data.get('title', project_slug),
                        'slug': project_slug,
                        'url': final_url,
                        'direction': data.get('direction', ''),
                        'level': data.get('level', ''),
                        'journal_posts': journal_sorted,
                        'media_posts': media_sorted
                    })

        # Сортируем список самих проектов на этой полочке раздела по алфавиту
        nav_tree['sections'][section] = sorted(nav_tree['sections'][section], key=lambda x: x['title'].lower())

    # 4. ЗАПИСЬ СТРУКТУРИРОВАННОГО УМНОГО ДЕРЕВА В _DATA/NAVIGATION.YML
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(nav_tree, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print("[NAV-SUCCESS] Карта навигации и связей 'sections' успешно сохранена в _data/navigation.yml")

        # 📂 АВТОГЕНЕРАЦИЯ СТРАНИЦ-ЛЕНТ ДЛЯ КНОПКИ "0" (Для всех найденных проектов)
        for section in supported_sections:
            for project in nav_tree['sections'][section]:
                slug = project['slug']
                
                for post_type in ['journal', 'media']:
                    dir_path = os.path.join(root_dir, post_type, slug)
                    os.makedirs(dir_path, exist_ok=True)
                    
                    file_path = os.path.join(dir_path, 'index.md')
                    with open(file_path, 'w', encoding='utf-8') as pf:
                    with open(file_path, 'w', encoding='utf-8') as pf:
                        type_title = "посты журнала проекта" if post_type == "journal" else "посты галереи проекта"
                        
                        pf.write(f"---\n")
                        pf.write(f"layout: page\n")
                        pf.write(f"title: \"{project['title']}: {type_title}\"\n")
                        pf.write(f"slug: {slug}\n")
                        pf.write(f"section: {section}\n")  # 🔥 ДОБАВЛЕНО: передаём раздел!
                        pf.write(f"type: {post_type}\n")
                        pf.write(f"mathjax: true\n")
                        pf.write(f"---\n\n")
                        pf.write(f"{{% include posts-page-open.liquid type='{post_type}' %}}\n")

    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации: {e}")

if __name__ == '__main__':
    build_navigation_tree()
