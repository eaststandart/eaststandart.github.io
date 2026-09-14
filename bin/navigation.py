#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 3)
@about Универсальный плоский препроцессор однотипной карты метаданных контента.
@purpose Подготавливает базовый парсер и изолированные буферы выгрузки серверных логов.
@author TechLab
@version 11.1.0-flat-pure-part1
"""

import os
import re
import sys
import yaml

def parse_yaml_front_matter(file_path):
    """Извлекает блок Front Matter из markdown-файла контента сайта."""
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
    """Выводит строку лога в консоль Actions и буферизирует её для архива артефактов."""
    print(text)
    artifacts_log_buffer.append(text)

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства обратно в md-файл на диске."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
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
    os.makedirs(debug_dir, exist_ok=True)

    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    RESOURCE_FOLDERS = {'img', 'images', 'files', 'res', 'resources', 'video', 'photo'}
    
    # Результирующая плоская однотипная база метаданных контента заметок
    flat_map = {}
    
    # Буфер для выявления Режима А (наличие физического index.md внутри папки)
    folders_with_index = set()
    
    # Шаг 1: Автоматическое определение разделов, коллекций и выявление Режима А
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.'):
            if name != '_posts':
                if os.path.exists(os.path.join(full_path, 'index.md')) or os.path.exists(os.path.join(full_path, 'index.html')):
                    folders_with_index.add(name)

    # Шаг 2: Обход всех физических markdown-файлов репозитория контента без исключений
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_') # Для _people -> people, для tools -> tools
            is_jekyll_collection = name.startswith('_') # Проверка: это встроенная коллекция?
            
            for root_walk, _, files in os.walk(full_path):
                for file in files:
                    if not file.endswith('.md'): continue
                    if os.path.basename(root_walk) in RESOURCE_FOLDERS: continue
                    
                    file_path = os.path.join(root_walk, file)
                    data, front_text, body = parse_yaml_front_matter(file_path)
                    if data is None or data.get('published') is False: continue

                    # Вычисляем слаг (имя файла без расширения)
                    file_slug, _ = os.path.splitext(file)
                    
                    # 🔥 УНИВЕРСАЛЬНЫЙ РАСЧЁТ URL РЕЖИМОВ А И Б (БЕЗ КОНСТАНТ И ПРИВЯЗОК)
                    ready_permalink = data.get('permalink')
                    if ready_permalink:
                        final_url = ready_permalink
                    elif name in folders_with_index:
                        # Режим А (index.md есть в папке) -> файлы с расширением .html
                        if file_slug == 'index':
                            final_url = f"/{clean_section_name}/"
                        else:
                            final_url = f"/{clean_section_name}/{file_slug}.html"
                    else:
                        # Режим Б и Коллекции (индекса нет) -> усовершенствованное плоское правило
                        if file_slug == 'index':
                            final_url = f"/{clean_section_name}/"
                        else:
                            final_url = f"/{clean_section_name}/{file_slug}/"

                    # Записываем очищенное имя секции в Front Matter самого md-файла
                    data['section'] = clean_section_name
                    write_yaml_front_matter(file_path, data, body)

                    # 🔥 СБОР ПАСПОРТА СТРОГО В ВАШЕМ ПОРЯДКЕ СВОЙСТВ (БЕЗ ССЫЛОК И МУСОРА)
                    node = {}
                    node['title'] = data.get('title', file_slug)
                    node['url'] = final_url
                    if data.get('navtitle'):
                        node['navtitle'] = data['navtitle']
                        
                    # 🔥 РАЗДЕЛЕНИЕ НА СЕКЦИИ И КОЛЛЕКЦИИ НА БУДУЩЕЕ ПО ВАШЕЙ СТРАТЕГИИ
                    if is_jekyll_collection:
                        node['relatedcollection'] = clean_section_name
                    else:
                        node['relatedsection'] = clean_section_name
                        
                    node['slug'] = file_slug

                    # Служебные свойства пишем строго при наличии в самом md-файле
                    if data.get('direction'):
                        node['direction'] = data['direction']
                    if data.get('level'):
                        node['level'] = str(data['level']).strip()

                    # Ключом плоской карты становится точное имя файла на диске репозитория
                    flat_map[file] = node

    # Шаг 3: Тотальный обход папки _posts по вашему правилу №4
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                file_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(file_path)
                if data is None or data.get('published') is False: continue

                file_name_clean, _ = os.path.splitext(file)
                # Очищаем имя файла от даты, получая чистый слаг проекта
                file_slug_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)

                # Выделяем тип поста (journal или media)
                post_page_type = data.get('post-page', 'journal')
                for key in list(data.keys()):
                    if str(key).endswith('-post-page'):
                        post_page_type = str(key).split('-')[0]
                        break

                # Автомат дат для постов хроники
                if data and data.get('date'):
                    post_date = str(data['date'])
                else:
                    match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                    post_date = match_date.group(1) if match_date else "2026-01-01"

                # Вычисляем каноничный URL поста по стандарту Tracy Hybrid
                short_url = f"/{post_page_type}/{file_slug_no_date}/{post_date.replace('-', '/')}/{file_name_clean_no_date}.html"

                # На этапе сборки ищем родительскую карточку, чтобы вычислить parent-раздел
                calculated_parent_section = ""
                parent_file_key = f"{file_slug_no_date}.md"
                if parent_file_key in flat_map:
                    # Извлекаем родной раздел или коллекцию родительской страницы контента
                    parent_node = flat_map[parent_file_key]
                    calculated_parent_section = parent_node.get('relatedsection', parent_node.get('relatedcollection', ''))

                # Записываем вычисленные свойства обратно во Front Matter md-файла поста
                data['categories'] = [post_page_type, file_slug_no_date]
                data['post-page'] = post_page_type
                if calculated_parent_section:
                    data['section'] = calculated_parent_section
                write_yaml_front_matter(file_path, data, body)

                # 🔥 СБОР ПАСПОРТА ПОСТА СТРОГО В ВАШЕМ ПОРЯДКЕ СВОЙСТВ (БЕЗ ССЫЛОК И МУСОРА)
                node = {}
                node['title'] = data.get('title', file_slug_no_date)
                node['url'] = short_url
                if data.get('navtitle'):
                    node['navtitle'] = data['navtitle']
                
                # 🔥 Нативно прописываем принадлежность к странице по вашему правилу
                node['relatedpages'] = file_slug_no_date
                node['slug'] = file_slug_no_date
                node['posttype'] = post_page_type

                # Служебные свойства пишем строго при наличии в самом файле поста
                if data.get('pinnednews') is True:
                    node['pinnednews'] = True
                if data.get('direction'):
                    node['direction'] = data['direction']
                if data.get('level'):
                    node['level'] = str(data['level']).strip()

                # Ключом в карте становится точное имя файла поста на диске
                flat_map[file] = node
                
                log_artifact(f"[NAV-DEBUG] Добавлен пост: {file} | relatedpages: {file_slug_no_date}")

    # 🔥 ЧИСТАЯ ВЫГРУЗКА БЕЗ ЗНАЧКОВ *ID И &ID ЧЕРЕЗ SAFEDUMPER
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(flat_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
        log_artifact("[NAV-SUCCESS] Однотипная плоская карта метаданных заметок контента успешно сохранена.")
    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи итоговой карты навигации: {e}")

    # Создание физических папок-вкладок для Jekyll на сервере из собранной базы
    for file_key, node in flat_map.items():
        if node.get('posttype') is None and file_key != 'index.md':
            slug = node['slug']
            sect = node.get('relatedsection', node.get('relatedcollection', 'faire'))
            for p_type in ['journal', 'media']:
                dir_path = os.path.join(root_dir, p_type, slug)
                os.makedirs(dir_path, exist_ok=True)
                with open(os.path.join(dir_path, 'index.md'), 'w', encoding='utf-8') as pf:
                    pf.write(f"---\nlayout: page\ntitle: \"Публикации проекта {slug}\"\nslug: {slug}\nsection: {sect}\npost-page: {p_type}\nmathjax: true\n---\n\n{{% include posts-page-open.liquid type='{p_type}' %}}\n")

    # Выгрузка отчёта буфера логов в артефакты сервера Actions
    try:
        log_file_path = os.path.join(debug_dir, 'navigation_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print("[NAV-SUCCESS] Технический отчёт успешно выгружен в артефакты _processed_files.")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось сохранить отладочный лог: {e}")

if __name__ == '__main__':
    build_navigation_tree()
