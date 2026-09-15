#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 3)
@about Универсальный плоский препроцессор однотипной карты метаданных контента.
@purpose Этаж 1, 2 и подготовка Диспетчера к каскадному Шагу 1.
@author TechLab
@version 19.0.0-split-cascade
"""

import os
import re
import sys
import yaml

# =====================================================================
# ЭТАЖ 1: СИСТЕМНЫЕ УТИЛИТЫ (Парсер Front Matter и перезапись на диск)
# =====================================================================
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

# =====================================================================
# ЭТАЖ 2: ПОДКЛЮЧАЕМЫЙ МОДУЛЬ НОВОСТЕЙ (Чистый калькулятор памяти)
# =====================================================================
def navigation_news_properties(data, passport):
    """Работает строго в оперативной памяти с готовым словарем 'data'.
    Тут живёт ВАШ ОРИГИНАЛЬНЫЙ РАБОЧИЙ КОД сплита типов постов хроники 1 в 1!"""
    has_post_page_property = False
    post_page_type = ""
    
    if 'post-page' in data:
        has_post_page_property = True
        post_page_type = str(data['post-page'])
    else:
        for key in list(data.keys()):
            if str(key).endswith('-post-page'):
                has_post_page_property = True
                post_page_type = str(key).split('-')[0]
                break

    if has_post_page_property and post_page_type:
        passport['posttype'] = post_page_type
        
    return passport

# =====================================================================
# ЭТАЖ 3: ГЛАВНЫЙ УПРАВЛЯЮЩИЙ КОНВЕЙЕР (Диспетчер обхода)
# =====================================================================
def build_navigation_tree():
    global artifacts_log_buffer
    artifacts_log_buffer.clear()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    debug_dir = os.path.join(root_dir, '_navigation_files')
    os.makedirs(debug_dir, exist_ok=True)

    # Список жестких технических исключений корневых папок диска
    EXCLUDED_FOLDERS = {'_includes', '_layouts', '_pages', 'assets', 'bin', '.git', '.github', '_data', '_navigation_files'}
    
    flat_map = {}
    root_dirs_present = set()
    folders_with_index = set()
    
    # Собираем имена всех физических папок в корне диска строго с фильтром исключений
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and not name.startswith('.') and name not in EXCLUDED_FOLDERS:
            root_dirs_present.add(name)

    # 🔥 ШАГ 1: ОБРАБОТКА КОРНЕВЫХ ПАПОК (БЕЗ ФАЙЛОВ И ИНДЕКСОВ) СТРОГО ПО ВАШЕЙ КАСКАДНОЙ ТАБЛИЦЕ
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_')
            is_under_dir = name.startswith('_')
            
            # Локальные буферы каскада
            front_data = None
            index_file_path = ""
            
            # --- ПРИОРИТЕТ 1: Поиск физического индекса прямо внутри папки ---
            possible_index_md = os.path.join(full_path, 'index.md')
            possible_index_html = os.path.join(full_path, 'index.html')
            
            if os.path.exists(possible_index_md):
                index_file_path = possible_index_md
            elif os.path.exists(possible_index_html):
                index_file_path = possible_index_html
                
            if index_file_path:
                front_data, _, _ = parse_yaml_front_matter(index_file_path)
                folders_with_index.add(name)
                
            # --- ПРИОРИТЕТ 2: Поиск совпадения в папке _pages/ ---
            if not front_data:
                possible_page = os.path.join(root_dir, '_pages', f"{clean_section_name}.md")
                if os.path.exists(possible_page):
                    front_data, _, _ = parse_yaml_front_matter(possible_page)

            # Собираем паспорт раздела
            node = {}
            
            # Вычисление заголовков и crumbtitle (Приоритет 1 и 2)
            if front_data:
                node['title'] = front_data.get('title', clean_section_name.capitalize())
                if 'crumbtitle' in front_data:
                    node['crumbtitle'] = front_data['crumbtitle']
                
                # Вычисление URL по пермалинку
                if front_data.get('permalink'):
                    node['url'] = front_data['permalink'].strip()
                else:
                    # --- ПРИОРИТЕТ 3 (Сброс URL на автомат папки, если пермалинка в шапке не было) ---
                    node['url'] = f"/{clean_section_name}/"
            
            # --- ПРИОРИТЕТ 3: Полный автомат, если файлов на диске вообще не найдено ---
            else:
                node['title'] = clean_section_name.capitalize()
                node['url'] = f"/{clean_section_name}/"

            # Назначение прямых свойств связи в зависимости от наличия подчёркивания папки на диске
            if is_under_dir:
                node['collection'] = clean_section_name
            else:
                node['section'] = clean_section_name
                
            flat_map[clean_section_name] = [node]

    # 🔥 ШАГ 2: ОБХОД ФИЗИЧЕСКИХ ФАЙЛОВ СТАТЕЙ И ПРОЕКТОВ (ИНДЕКСЫ ПОЛНОСТЬЮ ИГНОРИРУЮТСЯ) - 1 В 1 ВАШ ФАЙЛ
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            for root_walk, _, files in os.walk(full_path):
                for file in files:
                    if not (file.endswith('.md') or file.endswith('.html')): continue
                    
                    file_slug, _ = os.path.splitext(file)
                    if file_slug == 'index': continue
                    
                    file_path = os.path.join(root_walk, file)
                    data, front_text, body = parse_yaml_front_matter(file_path)
                    if data is None or data.get('published') is False: continue

                    ready_permalink = data.get('permalink', '').strip()
                    relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')

                    node = {}
                    node['title'] = data.get('title', file_slug)

                    # 1. Если у файла ЕСТЬ permalink
                    if ready_permalink:
                        node['url'] = ready_permalink
                        permalink_clean = ready_permalink.strip('/')
                        first_word = permalink_clean.split('/')[0] if permalink_clean else ''
                        
                        has_clean_dir = first_word in root_dirs_present
                        has_under_dir = f"_{first_word}" in root_dirs_present
                        
                        if has_clean_dir and has_under_dir:
                            pass
                        elif has_under_dir:
                            node['relatedcollection'] = first_word
                        elif has_clean_dir:
                            node['relatedsection'] = first_word

                    # 2. Если у файла НЕТ permalink
                    else:
                        clean_section_name = name.lstrip('_')
                        is_under_dir = name.startswith('_')
                        
                        node['url'] = f"/{clean_section_name}/{file_slug}/"

                        if name not in folders_with_index:                        
                            data['permalink'] = node['url']
                            log_artifact(f"[NAV-DEBUG] Файл: {relative_file_key} | Записано permalink: {data['permalink']}")

                        if is_under_dir:
                            node['relatedcollection'] = clean_section_name
                        else:
                            node['relatedsection'] = clean_section_name

                    data['section'] = name.lstrip('_')
                    write_yaml_front_matter(file_path, data, body)

                    flat_map[relative_file_key] = [node]

    # 🔥 ШАГ 3: ОБРАБОТКА ПАПКИ СВЯЗАННЫХ ПОСТОВ ХРОНИКИ _POSTS/ (СТРОГО 1 В 1 ВАШ ФАЙЛ)
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not (file.endswith('.md') or file.endswith('.html')): continue
                
                file_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(file_path)
                if data is None or data.get('published') is False: continue

                file_name_clean, _ = os.path.splitext(file)
                file_slug_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)
                ready_permalink = data.get('permalink', '').strip()
                relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')

                match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                post_date = match_date.group(1) if match_date else "2026-01-01"

                # Извлечение типа post-page без дублирования массивов строго по вашему коду
                has_post_page_property = False
                post_page_type = ""
                if 'post-page' in data:
                    has_post_page_property = True
                    post_page_type = str(data['post-page'])
                else:
                    for key in list(data.keys()):
                        if str(key).endswith('-post-page'):
                            has_post_page_property = True
                            post_page_type = str(key).split('-')[0]
                            break

                # Вычисляем полный физический путь к родителю
                calculated_parent_path = ""
                parent_file_name = f"{file_slug_no_date}.md"
                for key_path in flat_map.keys():
                    if key_path.endswith(f"/{parent_file_name}") or key_path == parent_file_name:
                        calculated_parent_path = key_path
                        break

                node = {}
                node['title'] = data.get('title', file_slug_no_date)

                # А. Пост хроники С пермалинком
                if ready_permalink:
                    node['url'] = ready_permalink
                    permalink_clean = ready_permalink.strip('/')
                    first_word = permalink_clean.split('/')[0] if permalink_clean else ''
                    
                    has_clean_dir = first_word in root_dirs_present
                    has_under_dir = f"_{first_word}" in root_dirs_present
                    
                    if calculated_parent_path:
                        node['relatedpages'] = calculated_parent_path
                    
                    if has_clean_dir and has_under_dir:
                        pass
                    elif has_under_dir:
                        node['relatedcollection'] = first_word
                    elif has_clean_dir:
                        node['relatedsection'] = first_word

                # Б. Пост хроники БЕЗ пермалинка
                else:
                    fallback_type = post_page_type if post_page_type else "journal"
                    node['url'] = f"/{fallback_type}/{file_slug_no_date}/{post_date.replace('-', '/')}/{file_name_clean}.html"
                    if calculated_parent_path:
                        node['relatedpages'] = calculated_parent_path

                # Синхронизация Front Matter самого файла
                if has_post_page_property and post_page_type:
                    data['categories'] = [post_page_type, file_slug_no_date]
                    data['post-page'] = post_page_type
                if calculated_parent_path:
                    parent_node_list = flat_map[calculated_parent_path]
                    if isinstance(parent_node_list, list) and len(parent_node_list) > 0:
                        p_node = parent_node_list[0]
                        data['section'] = p_node.get('relatedsection', p_node.get('section', 'faire'))

                        log_artifact(f"[NAV-DEBUG] Файл: {relative_file_key} | Записано section: {data['section']}")

                write_yaml_front_matter(file_path, data, body)

                # 🔥 ПОДКЛЮЧЕНИЕ МОДУЛЯ НОВОСТЕЙ: Расширение паспорта строго в оперативной памяти сервера
                node = navigation_news_properties(data, node)

                flat_map[relative_file_key] = [node]

    # СОБИРАЕМ ИТОГОВЫЙ СЛОВАРЬ С СЕРВЕРНЫМ СПИСКОМ ПАПОК НА ПЕРВОЙ СТРОКЕ
    final_output_map = {}
    final_output_map['detected_root_folders'] = sorted(list(root_dirs_present))
    for k, v in flat_map.items():
        final_output_map[k] = v

    # Запись плоской карты на диск без значков *id
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(final_output_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации: {e}")

    try:
        log_file_path = os.path.join(debug_dir, 'navigation-md-properties.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print("[NAV-SUCCESS] Лог изменений свойств успешно сохранен.")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось сохранить лог: {e}")

if __name__ == '__main__':
    build_navigation_tree()
