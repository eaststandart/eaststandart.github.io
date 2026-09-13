#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation
@about Универсальный статический препроцессор метаданных и карт на чистом автомате суффиксов.
@purpose Автоматически вычисляет типы постов по ключам *-post-page, вшивает нативные
         категории Jekyll и генерирует карты навигации в артефакты Actions.
@author TechLab
@version 7.0.0-suffix-automaton
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

# Глобальный буфер для отладочного лога, который полетит в zip-архив Actions
artifacts_log_buffer = []

def log_artifact(text):
    """Выводит строку лога в консоль Actions и параллельно буферизирует её."""
    print(text)
    artifacts_log_buffer.append(text)

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает свойства в файл и дублирует их в папку серверных артефактов."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        f_name = os.path.basename(file_path)
        cats = data.get('categories', 'НЕТ')
        sect = data.get('section', 'НЕТ')
        log_artifact(f"[NAV-DEBUG] Файл: {f_name} | Раздел (section): {sect} | Категории: {cats}")

        # Создаем или проверяем серверную папку артефактов _processed_files/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..'))
        debug_dir = os.path.join(root_dir, '_processed_files')
        os.makedirs(debug_dir, exist_ok=True)
        
        # Штампуем файл отладки свойств jekyll-processed-md-properties
        debug_file_path = os.path.join(debug_dir, f"processed-{f_name}")
        with open(debug_file_path, 'w', encoding='utf-8') as df:
            df.write(f"---\n{front_text}---\n[Тело статьи успешно обработано]")

        # Перезаписываем сам рабочий md-файл
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

    # Очищаем или создаем целевую папку _processed_files перед стартом сборки
    debug_dir = os.path.join(root_dir, '_processed_files')
    if os.path.exists(debug_dir):
        for f in os.listdir(debug_dir):
            try: os.remove(os.path.join(debug_dir, f))
            except: pass
    os.makedirs(debug_dir, exist_ok=True)

    # 1. АВТОМАТИЧЕСКИЙ СБОР РАЗДЕЛОВ И КОЛЛЕКЦИЙ С ДИСКА
    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
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
    related_posts_map = {slug: {} for slug in valid_slugs} # Динамические полочки типов постов

    # 2. ЭТАП УМНОГО АНАЛИЗА ПАПКИ _POSTS (Автомат по суффиксу *-post-page)
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                if data is None or data.get('published') is False: continue

                # Очищаем имя файла от даты для вычисления слага по умолчанию
                file_name_clean, _ = os.path.splitext(file)
                file_name_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)

                post_slug = None
                post_page_type = None

                # РУБЕЖ А: Если категории уже прописаны вручную (старые файлы)
                if data.get('categories') and isinstance(data['categories'], list) and len(data['categories']) >= 2:
                    post_page_type = data['categories'][0]
                    post_slug = data['categories'][1]

                # РУБЕЖ Б: Умный радар суффиксов *-post-page (новые файлы)
                if not post_slug:
                    for key in list(data.keys()):
                        if str(key).endswith('-post-page'):
                            # Отсекаем суффикс и забираем первое служебное слово (journal, media и т.д.)
                            post_page_type = str(key).split('-')[0]
                            # Имя файла целиком становится латинским слагом проекта
                            if file_name_clean in valid_slugs:
                                post_slug = file_name_clean
                            break

                # Если файл не прошёл ни один рубеж, значит это автономная новость
                if not post_slug or post_slug not in valid_slugs:
                    log_artifact(f"[NAV-NOTE] Файл '{file}' не привязан к проектам, пропускаем интеграцию во вкладки.")
                    continue

                post_date = str(data.get('date', ''))

                registry_key = (post_slug, post_date, post_page_type)
                if registry_key in posts_registry:
                    log_artifact(f"\n[❌ КРИТИЧЕСКАЯ ОШИБКА] Конфликт дат в '{file}' и '{posts_registry[registry_key]}'.")
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

                # АВТОМАТИЧЕСКАЯ ЗАПИСЬ НАТИВНЫХ СВОЙСТВ ДЛЯ JEKYLL
                data['categories'] = [post_page_type, post_slug]
                data['post-page'] = post_page_type
                
                # Записываем строго родительскую контентную папку с диска (faire, projects и т.д.)
                current_clean_section = slug_to_section_map.get(post_slug, '')
                data['section'] = current_clean_section

                write_yaml_front_matter(full_path, data, body)

                short_url = f"/{post_page_type}/{post_slug}/{post_date.replace('-', '/')}/{file_name_clean}.html"

                # Направляем запись на динамическую полочку проекта для дерева navigation.yml
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
                if section_name == 'people': continue
                
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
                        pf.write(f"{{% include posts-page-open.liquid type='{post_type}' %}}\n")

    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи дерева или страниц лент: {e}")

    # 📂 ФИЗИЧЕСКАЯ ЗАПИСЬ ЛОГОВ-АРТЕФАКТОВ СТРОГО В ПАПКУ СЕРВЕРНОГО АРХИВА
    try:
        log_file_path = os.path.join(debug_dir, 'navigation_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print(f"[NAV-SUCCESS] Файл отладочных логов успешно направлен в zip-архив: _processed_files/navigation_debug.log")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось сохранить файл отладочного лога в артефакты: {e}")

if __name__ == '__main__':
    build_navigation_tree()
