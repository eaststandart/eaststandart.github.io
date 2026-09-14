#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation
@about Универсальный статический препроцессор метаданных и карт на чистом автомате суффиксов.
@purpose Реализует сквозной закон сбора полной карты сайта без "белых пятен".
@author TechLab
@version 9.0.0-tracy-complete-map
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

        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..'))
        debug_dir = os.path.join(root_dir, '_processed_files')
        os.makedirs(debug_dir, exist_ok=True)
        
        debug_file_path = os.path.join(debug_dir, f"processed-{f_name}")
        with open(debug_file_path, 'w', encoding='utf-8') as df:
            df.write(f"---\n{front_text}---\n[Тело статьи успешно обработано]")

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

    debug_dir = os.path.join(root_dir, '_processed_files')
    if os.path.exists(debug_dir):
        for f in os.listdir(debug_dir):
            try: os.remove(os.path.join(debug_dir, f))
            except: pass
    os.makedirs(debug_dir, exist_ok=True)

    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    RESOURCE_FOLDERS = {'img', 'images', 'files', 'res', 'resources', 'video', 'photo'}
    
    supported_sections = []
    valid_slugs = set()
    slug_to_section_map = {}
    sections_with_index = set()
    collections_folders = set()
    
    # Сбор корневых папок контента (Категория 1) и коллекций (Категория 3)
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            # Обычные корневые папки контента
            if not name.startswith('.') and name != '_posts' and name not in EXCLUDED_FOLDERS:
                clean_section_name = name.lstrip('_')
                supported_sections.append(clean_section_name)
                
                if name.startswith('_'):
                    collections_folders.add(clean_section_name)
                
                section_dir = os.path.join(root_dir, name)
                if os.path.exists(os.path.join(section_dir, 'index.md')) or os.path.exists(os.path.join(section_dir, 'index.html')):
                    sections_with_index.add(clean_section_name)
                
                for entry in os.scandir(section_dir):
                    if entry.is_dir() and not entry.name.startswith('.') and entry.name not in RESOURCE_FOLDERS:
                        valid_slugs.add(entry.name)
                        slug_to_section_map[entry.name] = clean_section_name

    log_artifact(f"[NAV-INFO] Обнаружены разделы контента: {supported_sections}")
    log_artifact(f"[NAV-INFO] Разделы со стандартными index-вывесками (Режим А): {list(sections_with_index)}")

    # Анализ папки _pages/ и вывесок разделов
    pages_dir = os.path.join(root_dir, '_pages')
    custom_permalinks_map = {}
    pages_navtitle_map = {}

    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                p_path = os.path.join(pages_dir, file)
                p_data, p_front, p_body = parse_yaml_front_matter(p_path)
                if p_data is None: continue
                
                p_slug, _ = os.path.splitext(file)
                if p_data.get('navtitle'):
                    pages_navtitle_map[p_slug] = p_data['navtitle']
                elif p_data.get('title'):
                    pages_navtitle_map[p_slug] = p_data['title']
                
                if p_slug in supported_sections and p_slug not in sections_with_index:
                    ready_permalink = p_data.get('permalink')
                    if ready_permalink:
                        custom_permalinks_map[p_slug] = "/" + ready_permalink.strip("/") + "/"
                    else:
                        calculated_url = f"/{p_slug}/"
                        p_data['permalink'] = calculated_url
                        custom_permalinks_map[p_slug] = calculated_url
                        write_yaml_front_matter(p_path, p_data, p_body)

    nav_tree = {
        'sections': {section: [] for section in supported_sections}
    }
    
    posts_registry = {}
    related_posts_map = {slug: {} for slug in valid_slugs} 
    detected_post_types = set(['journal', 'media']) 

    # 2. КАТЕГОРИЯ 2: ТОТАЛЬНЫЙ АНАЛИЗ ПАПКИ _POSTS
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                if data is None or data.get('published') is False: continue

                file_name_clean, _ = os.path.splitext(file)
                file_name_clean_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)

                post_slug = None
                post_page_type = None

                # Динамический автомат суффиксов (Первое слово перед дефисом может быть любым)
                for key in list(data.keys()):
                    if str(key).endswith('-post-page'):
                        possible_type = str(key).split('-')[0]
                        detected_post_types.add(possible_type)
                        if file_name_clean_no_date in valid_slugs:
                            post_slug = file_name_clean_no_date
                            post_page_type = possible_type
                        break

                if not post_slug and file_name_clean_no_date in valid_slugs:
                    post_slug = file_name_clean_no_date
                    post_page_type = data.get('post-page', 'journal')

                # 🔥 УНИВЕРСАЛЬНЫЙ АВТОМАТ ДАТ ДЛЯ ВСЕХ ПОСТОВ (НЕЗАВИСИМО ОТ ПЕРМАЛИНКА)
                if data and data.get('date'):
                    post_date = str(data['date'])
                else:
                    match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                    if match_date:
                        post_date = match_date.group(1)
                    else:
                        import datetime
                        mtime = os.path.getmtime(full_path)
                        post_date = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                    log_artifact(f"[NAV-WARNING] Извлечена дата для поста: {file} | Назначено: {post_date}")

                # ВЕТКА 2.2: АВТОНОМНЫЕ ПОСТЫ (Без привязки к Ярмарке — как Мультивибратор)
                if not post_slug:
                    ready_permalink = data.get('permalink')
                    if ready_permalink:
                        path_parts = [p for p in ready_permalink.split('/') if p]
                        if path_parts:
                            detected_section = path_parts[0]
                            data['section'] = detected_section
                            
                            if detected_section not in nav_tree['sections']:
                                nav_tree['sections'][detected_section] = []
                            
                            short_url = ready_permalink
                            write_yaml_front_matter(full_path, data, body)
                            
                            # 🔥 ИСПРАВЛЕНО: Записываем дату автономного поста в карту сайта
                            nav_tree['sections'][detected_section].append({
                                'title': data.get('title', file_name_clean_no_date),
                                'slug': file_name_clean_no_date,
                                'url': short_url,
                                'direction': data.get('direction', ''),
                                'level': data.get('level', ''),
                                'date': post_date
                            })
                    continue

                # 🔥 ШАГ Б: ДЛЯ СВЯЗАННЫХ ПОСТОВ ХРОНИКИ ИЗ _POSTS (Где нет ручного пермалинка)
                # Автомат извлечения даты из имени файла, если она стерта в Front Matter
                if data and data.get('date'):
                    post_date = str(data['date'])
                else:
                    match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                    post_date = match_date.group(1) if match_date else "2026-01-01"
                    log_artifact(f"[NAV-WARNING] У связанного поста извлечена дата из имени файла: {file} | Назначено: {post_date}")

                # Контроль уникальности дат для связанных постов хроники
                registry_key = (post_slug, post_date, post_page_type)
                if registry_key in posts_registry:
                    print(f"\n[❌ КРИТИЧЕСКАЯ ОШИБКА] Конфликт дат в '{file}' и '{posts_registry[registry_key]}'.")
                    exit(1)
                posts_registry[registry_key] = file

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

                data['categories'] = [post_page_type, post_slug]
                data['post-page'] = post_page_type
                current_clean_section = slug_to_section_map.get(post_slug, '')
                data['section'] = current_clean_section

                write_yaml_front_matter(full_path, data, body)

                short_url = f"/{post_page_type}/{post_slug}/{post_date.replace('-', '/')}/{file_name_clean_no_date}.html"

                if post_page_type not in related_posts_map[post_slug]:
                    related_posts_map[post_slug][post_page_type] = []
                related_posts_map[post_slug][post_page_type].append({
                    'title': data.get('title', file_name_clean_no_date),
                    'url': short_url,
                    'date': post_date,
                    'pinnednews': data.get('pinnednews', False)
                })

    # 3. ЭТАП СВЯЗЫВАНИЯ ГЛАВНЫХ СТРАНИЦ ПРОЕКТОВ И ПАПОК-КОЛЛЕКЦИЙ
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

                        # 🔥 УНИВЕРСАЛЬНЫЙ ЗАКОН АДРЕСОВ (TRACY HYBRID)
                        ready_permalink = data.get('permalink')
                        
                        if ready_permalink:
                            # Шаг 1: Если в самом файле руками прописан permalink — берем его намертво!
                            final_url = ready_permalink
                        elif clean_section_name in sections_with_index:
                            # Режим А (Стандартный Jekyll с index.md): Удаляем пермалинки карточек контента
                            if project_slug == 'index':
                                final_url = f"/{clean_section_name}/"
                            else:
                                final_url = f"/{clean_section_name}/{project_slug}.html"
                            if 'permalink' in data: del data['permalink']
                        else:
                            # Режим Б и Категория 3 (Без index.md / Специальные коллекции)
                            base_parent_url = custom_permalinks_map.get(clean_section_name, f"/{clean_section_name}/")
                            if project_slug == 'index':
                                final_url = base_parent_url
                            else:
                                final_url = f"{base_parent_url}{project_slug}/"
                            data['permalink'] = final_url

                        # Вшиваем строгое, очищенное имя раздела контента
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
                            'level': data.get('level', ''),
                            'date': str(data.get('date', '')) if data.get('date') else ''
                        }

                        project_node.update(project_posts_data)
                        
                        if clean_section_name not in nav_tree['sections']:
                            nav_tree['sections'][clean_section_name] = []
                        nav_tree['sections'][clean_section_name].append(project_node)

    # Добавление нативных index-вывесок для автономных категорий из _pages/
    for section_key, title_text in pages_navtitle_map.items():
        if section_key in nav_tree['sections']:
            # Проверяем, нет ли уже узла index в этой секции
            has_index_node = any(node.get('slug') == 'index' for node in nav_tree['sections'][section_key])
            if not has_index_node and section_key not in sections_with_index:
                base_url = custom_permalinks_map.get(section_key, f"/{section_key}/")
                nav_tree['sections'][section_key].append({
                    'title': title_text,
                    'slug': 'index',
                    'url': base_url,
                    'direction': '',
                    'level': ''
                })

    # Сортировка всех элементов дерева по алфавиту
    for section_name in list(nav_tree['sections'].keys()):
        nav_tree['sections'][section_name] = sorted(
            nav_tree['sections'][section_name], 
            key=lambda x: x['title'].lower()
        )

    nav_tree['post_types'] = sorted(list(detected_post_types))

    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        # 1. ЗАПИСЬ ГОТОВОЙ КАРТЫ НА ДИСК (ИСПРАВЛЕНО: БЕЗ ЗНАЧКОВ *ID)
        # Отключаем оптимизацию ссылок, чтобы писать чистый плоский текст
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(nav_tree, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
        log_artifact("[NAV-SUCCESS] Карта навигации 'sections' успешно обновлена без системных указателей.")

        # 2. ГЕНЕРАЦИЯ ФИЗИЧЕСКИХ ПАПОК ВКЛАДОК НА СЕРВЕРЕ
        for section_name, projects in nav_tree['sections'].items():
            for project in projects:
                slug = project['slug']
                
                # Пропускаем общие вивески разделов
                if slug == 'index': continue
                
                # Физические папки создаем строго при наличии связанных постов хроники
                if slug not in related_posts_map or not related_posts_map[slug]:
                    continue
                
                # Собираем динамический список типов
                detected_types = sorted(list(detected_post_types))
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

    # 3. ВЫГРУЗКА ДЕТАЛЬНЫХ ЛОГОВ В АРХИВ АРТЕФАКТОВ (ВОССТАНОВЛЕНО)
    try:
        log_file_path = os.path.join(debug_dir, 'navigation_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print(f"[NAV-SUCCESS] Файл отладочных логов успешно направлен в zip-архив: _processed_files/navigation_debug.log")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось сохранить файл отладочного лога в артефакты: {e}")

if __name__ == '__main__':
    build_navigation_tree()
