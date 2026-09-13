#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation
@about Универсальный статический препроцессор метаданных, карт и отладочных логов.
@purpose Автоматически вычисляет разделы по физическим папкам на диске,
         извлекает слаги и типы постов из имён файлов и пишет логи в артефакты.
@author TechLab
@version 6.0.0-artifacts-log
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

# Глобальный массив для сбора логов-артефактов в файл прямо в Obsidian
artifacts_log_buffer = []

def log_artifact(text):
    """Выводит строку лога в консоль Actions и параллельно буферизирует в файл-артефакт."""
    print(text)
    artifacts_log_buffer.append(text)

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства обратно в файл и создает отладочные логи."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        f_name = os.path.basename(file_path)
        p_link = data.get('permalink', 'НЕТ (нативный путь Jekyll)')
        cats = data.get('categories', 'НЕТ')
        sect = data.get('section', 'НЕТ')
        log_artifact(f"[NAV-DEBUG] Файл: {f_name} | Раздел (section): {sect} | Категории: {cats} | URL (permalink): {p_link}")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось перезаписать файл {file_path}: {e}")

def build_navigation_tree():
    global artifacts_log_buffer
    artifacts_log_buffer.clear()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    # 1. АВТОМАТИЧЕСКИЙ СБОР РАЗДЕЛОВ И КОЛЛЕКЦИЙ С ДИСКА
    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    # Жёсткий фильтр ресурсов контента, чтобы 'img' и 'files' не создавали ложных проектов
    RESOURCE_FOLDERS = {'img', 'images', 'files', 'res', 'resources', 'video', 'photo'}
    
    supported_sections = []
    valid_slugs = set()
    slug_to_section_map = {}

    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            if not name.startswith('.') and name != '_posts' and name not in EXCLUDED_FOLDERS:
                clean_section_name = name.lstrip('_')
                supported_sections.append(clean_section_name)
                
                section_dir = os.path.join(root_dir, name)
                for entry in os.scandir(section_dir):
                    if entry.is_dir() and not entry.name.startswith('.') and entry.name not in RESOURCE_FOLDERS:
                        valid_slugs.add(entry.name)
                        slug_to_section_map[entry.name] = clean_section_name

    log_artifact(f"[NAV-INFO] Автоматически обнаружены разделы сайта: {supported_sections}")
    log_artifact(f"[NAV-INFO] Белый список слагов проектов собран с диска (без мусора ресурсов): {list(valid_slugs)}")

    nav_tree = {
        'sections': {section: [] for section in supported_sections}
    }
    
    posts_registry = {}
    related_posts_map = {slug: {'journal': [], 'media': []} for slug in valid_slugs}

    # 2. ЭТАП УМНОГО АНАЛИЗА ПАПКИ _POSTS (Улучшенный алгоритм распознавания)
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                if data is None or data.get('published') is False: continue

                file_name_clean, _ = os.path.splitext(file)
                file_name_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)

                post_slug = None
                post_page_type = "journal" # Дефолтное значение

                # ПРОВЕРКА АЛГОРИТМА: Есть ли служебный хвостик на конце названия?
                if '-' in file_name_clean:
                    possible_slug, possible_type = file_name_clean.rsplit('-', 1)
                    if possible_type in ['journal', 'media', 'diary', 'questions']:
                        if possible_slug in valid_slugs:
                            post_slug = possible_slug
                            post_page_type = possible_type
                
                # Если дефиса на конце нет или имя файла целиком совпадает с проектом на диске
                if not post_slug and file_name_clean in valid_slugs:
                    post_slug = file_name_clean
                    post_page_type = data.get('post-page', 'journal')

                # РЕЗЕРВНАЯ СТРАХОВКА: Если имя файла уникальное, ищем слаг внутри категорий Front Matter
                if not post_slug and data.get('categories'):
                    for cat in data['categories']:
                        if cat in valid_slugs:
                            post_slug = cat
                            if data.get('post-page'):
                                post_page_type = data['post-page']
                            elif data['categories'][0] in ['journal', 'media', 'diary', 'questions']:
                                post_page_type = data['categories'][0]
                            break

                if not post_slug:
                    log_artifact(f"[NAV-NOTE] Файл '{file}' не привязан ни к одному проекту на диске, пропускаем.")
                    continue

                post_date = str(data.get('date', ''))

                registry_key = (post_slug, post_date, post_page_type)
                if registry_key in posts_registry:
                    log_artifact(f"\n[❌ КРИТИЧЕСКАЯ ОШИБКА] Конфликт дат в '{file}' и '{posts_registry[registry_key]}'.")
                    exit(1)
                posts_registry[registry_key] = file

                # Тегирование
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

                # ЗАПИСЫВАЕМ СВОЙСТВА: категории и родительский раздел проекта с диска (faire/projects)
                data['categories'] = [post_page_type, post_slug]
                current_clean_section = slug_to_section_map.get(post_slug, '')
                data['section'] = current_clean_section
                data['post-page'] = post_page_type

                write_yaml_front_matter(full_path, data, body)

                short_url = f"/{post_date.replace('-', '/')}/{file_name_clean}.html"

                if post_page_type not in related_posts_map[post_slug]:
                    related_posts_map[post_slug][post_page_type] = []
                related_posts_map[post_slug][post_page_type].append({
                    'title': data.get('title', file_name_clean),
                    'url': short_url,
                    'date': post_date
                })

    # 3. ЭТАП СВЯЗЫВАНИЯ ГЛАВНЫХ СТРАНИЦ ПРОЕКТОВ И СВОЙСТВ КОЛЛЕКЦИЙ
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            if not name.startswith('.') and name != '_posts' and name not in EXCLUDED_FOLDERS:
                clean_section_name = name.lstrip('_')
                section_dir = os.path.join(root_dir, name)
                
                for root_walk, _, files in os.walk(section_dir):
                    for file in files:
                        if not file.endswith('.md'): continue
                        if os.path.basename(root_walk) in RESOURCE_FOLDERS: continue
                        
                        full_path = os.path.join(root_walk, file)
                        data, front_text, body = parse_yaml_front_matter(full_path)
                        if data is None or data.get('published') is False: continue

                        relative_path = os.path.relpath(root_walk, section_dir)
                        if relative_path == '.':
                            project_slug, _ = os.path.splitext(file)
                        else:
                            project_slug = relative_path.replace(os.sep, '-')

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

                        final_url = f"/{clean_section_name}/{project_slug}/"
                        data['permalink'] = final_url
                        data['section'] = clean_section_name

                        write_yaml_front_matter(full_path, data, body)

                        project_posts_data = {}
                        if project_slug in related_posts_map:
                            for p_type, p_list in related_posts_map[project_slug].items():
                                project_posts_data[f"{p_type}_posts"] = sorted(p_list, key=lambda x: x['date'], reverse=True)

                        project_node = {
                            'title': data.get('title', project_slug),
                            'slug': project_slug,
                            'url': final_url,
                            'direction': data.get('direction', ''),
                            'level': data.get('level', '')
                        }
                        project_node.update(project_posts_data)
                        nav_tree['sections'][clean_section_name].append(project_node)

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
        log_artifact("[NAV-SUCCESS] Карта навигации 'sections' успешно сохранена в _data/navigation.yml")

        # АВТОГЕНЕРАЦИЯ СТРАНИЦ-ЛЕНТ ДЛЯ КНОПКИ "0"
        for section_name, projects_list in nav_tree['sections'].items():
            for project in projects_list:
                slug = project['slug']
                if section_name == 'people': continue # Людям ленты кнопки "0" не нужны
                
                detected_types = ['journal', 'media']
                if slug in related_posts_map:
                    for found_type in related_posts_map[slug].keys():
                        if found_type not in detected_types:
                            detected_types.append(found_type)

                for post_type in detected_types:
                    dir_path = os.path.join(root_dir, post_type, slug)
                    os.makedirs(dir_path, exist_ok=True)
                    
                    file_path = os.path.join(dir_path, 'index.md')
                    with open(file_path, 'w', encoding='utf-8') as pf:
                        type_title = f"публикации типа {post_type}"
                        if post_type == "journal": type_title = "посты журнала проекта"
                        elif post_type == "media": type_title = "посты галереи проекта"
                        
                        pf.write(f"---\nlayout: page\ntitle: \"{project['title']}: {type_title}\"\nslug: {slug}\nsection: {section_name}\npost-page: {post_type}\nmathjax: true\n---\n\n")
                        pf.write(f"[% include posts-page-open.liquid type='{post_type}' %]\n")

    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи дерева или страниц лент: {e}")

    # 📂 ФИЗИЧЕСКАЯ ЗАПИСЬ ЛОГОВ-АРТЕФАКТОВ НА ДИСК РЕПОЗИТОРИЯ (В АРТЕФАКТЫ)
    try:
        log_file_path = os.path.join(current_dir, 'navigation_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print(f"[NAV-SUCCESS] Файл отладочных логов успешно записан на диск: bin/navigation_debug.log")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось сохранить файл артефактов лога: {e}")

if __name__ == '__main__':
    build_navigation_tree()
