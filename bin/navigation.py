#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation
@about Универсальный статический препроцессор метаданных и карты разделов.
@purpose Автоматически вычисляет разделы по имени папок, убирает избыточность Front Matter
         и генерирует умное дерево sections в _data/navigation.yml.
@author TechLab
@version 1.0.0
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
    """Записывает обновленные свойства обратно в файл и создает отладочные логи для Artifacts."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        # 📂 ВОЗВРАЩАЕМ ГЕНЕРАЦИЮ ЛОГОВ ДЛЯ ARTIFACTS
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..'))
        debug_dir = os.path.join(root_dir, '_processed_files')
        os.makedirs(debug_dir, exist_ok=True)
        
        file_name = os.path.basename(file_path)
        debug_file_path = os.path.join(debug_dir, f"processed-{file_name}")
        
        with open(debug_file_path, 'w', encoding='utf-8') as df:
            df.write(f"---\n{front_text}---\n[Тело статьи успешно обработано и скрыто для компактности]")

        # Запись в основной рабочий файл
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

    # 1. АВТОМАТИЧЕСКИЙ СБОР РАЗДЕЛОВ И СЛАГОВ ПРОЕКТОВ (Без жестких списков папок)
    # Список системных папок-исключений, которые Python должен пропустить
    EXCLUDED_FOLDERS = {'_posts', '_includes', '_data', '_layouts', '_people', '_processed_files', 'assets', 'bin', '.git', '.github'}
    
    supported_sections = []
    valid_slugs = set()
    slug_to_section_map = {}

    # А. Автоматически находим все папки разделов в корне сайта
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            if not name.startswith('.') and not name.startswith('_') and name not in EXCLUDED_FOLDERS:
                supported_sections.append(name)
                
    print(f"[NAV-INFO] Автоматически обнаружены разделы сайта: {supported_sections}")

    # Б. Заходим в каждую найденную папку и собираем слаги ИЗНУТРИ файлов (по свойству slug)
    for section in supported_sections:
        section_dir = os.path.join(root_dir, section)
        for root, _, files in os.walk(section_dir):
            for file in files:
                if not file.endswith('.md'):
                    continue
                
                full_path = os.path.join(root, file)
                data, _, _ = parse_yaml_front_matter(full_path)
                
                if data and data.get('published') is not False:
                    file_slug = data.get('slug')
                    if file_slug:
                        valid_slugs.add(file_slug)
                        slug_to_section_map[file_slug] = section
                
    print(f"[NAV-INFO] Белый список слагов успешно собран из Front Matter: {list(valid_slugs)}")

    # Инициализируем древовидную структуру разделов под новые найденные папки
    nav_tree = {
        'sections': {section: [] for section in supported_sections}
    }
    
    posts_registry = {}
    related_posts_map = {slug: {'journal': [], 'media': []} for slug in valid_slugs}

    # 2. АНАЛИЗ И ОБРАБОТКА ПАПКИ _POSTS (Маленькие заметки)
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                if data is None or data.get('published') is False: continue

                # Читаем чистые свойства по новому стандарту
                post_slug = data.get('slug')
                post_date = str(data.get('date', ''))
                post_page_type = data.get('post-page') # Ваше новое имя свойства

                if not post_slug: continue

                # Защита от опечаток в слагах
                if post_slug not in valid_slugs:
                    print(f"\n[❌ ОШИБКА] В посте {file} указан неизвестный slug: '{post_slug}'.")
                    exit(1)

                # Защита от конфликтов дат
                registry_key = (post_slug, post_date, post_page_type)
                if registry_key in posts_registry:
                    print(f"\n[❌ ОШИБКА] Конфликт дат в '{file}' и '{posts_registry[registry_key]}'.")
                    exit(1)
                posts_registry[registry_key] = file

                # Генерация тегов
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

                # Автоматически прописываем Jekyll категории: [тип, слаг_проекта]
                data['categories'] = [post_page_type, post_slug]
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

    # 3. СБОРКА И ПЕРЕЗАПИСЬ ГЛАВНЫХ СТРАНИЦ ПРОЕКТОВ ИЗ ПАПОК
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

                    # Генерация тегов для главной страницы
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

                    write_yaml_front_matter(full_path, data, body)

                    # Автоматически вычисляем permalink на основе физической папки раздела
                    final_url = f"/{section}/{project_slug}/"

                    journal_sorted = sorted(related_posts_map.get(project_slug, {}).get('journal', []), key=lambda x: x['date'], reverse=True)
                    media_sorted = sorted(related_posts_map.get(project_slug, {}).get('media', []), key=lambda x: x['date'], reverse=True)

                    # Складываем проект строго на полочку его родного раздела внутри sections
                    nav_tree['sections'][section].append({
                        'title': data.get('title', project_slug),
                        'slug': project_slug,
                        'url': final_url,
                        'direction': data.get('direction', ''),
                        'level': data.get('level', ''),
                        'journal_posts': journal_sorted,
                        'media_posts': media_sorted
                    })

        # Сортируем проекты на полочке по алфавиту
        nav_tree['sections'][section] = sorted(nav_tree['sections'][section], key=lambda x: x['title'].lower())

    # 4. ЗАПИСЬ ОБЩЕЙ КАРТЫ СЛУЖЕБНЫХ ДАННЫХ И СТРАНИЦ КНОПКИ "0"
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(nav_tree, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print("[NAV-SUCCESS] Карта разделов 'sections' успешно сохранена.")

        # Автогенерация страниц-лент для кнопки "0" для ВСЕХ проектов всех разделов
        for section in supported_sections:
            for project in nav_tree['sections'][section]:
                slug = project['slug']
                
                for post_type in ['journal', 'media']:
                    dir_path = os.path.join(root_dir, post_type, slug)
                    os.makedirs(dir_path, exist_ok=True)
                    
                    file_path = os.path.join(dir_path, 'index.md')
                    with open(file_path, 'w', encoding='utf-8') as pf:
                        type_title = "посты журнала проекта" if post_type == "journal" else "посты галереи проекта"
                        
                        pf.write(f"---\n")
                        pf.write(f"layout: page\n")
                        pf.write(f"title: \"{project['title']}: {type_title}\"\n")
                        pf.write(f"slug: {slug}\n")
                        pf.write(f"type: {post_type}\n")
                        pf.write(f"mathjax: true\n")
                        pf.write(f"---\n\n")
                        pf.write(f"[% include posts-page-open.liquid type='{post_type}' %]\n")

    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи: {e}")

if __name__ == '__main__':
    build_navigation_tree()
