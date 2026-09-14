#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 2)
@about Универсальный плоский препроцессор однотипной карты метаданных контента.
@purpose Шаг 1: Инициализация корневых папок и разделов строго по вашей логике.
@author TechLab
@version 14.0.0-pure-step1
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

    # Жесткий лаконичный набор исключений корневых папок диска контента
    EXCLUDED_FOLDERS = {'_includes', '_layouts', '_pages', 'assets', 'bin', '.git', '.github'}
    
    flat_map = {}
    root_dirs_present = set()
    
    # Собираем имена всех физических папок в корне диска контента для фильтра коллизий
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and not name.startswith('.'):
            root_dirs_present.add(name)

    # 🔥 ШАГ 1: ОБРАБОТКА КОРНЕВЫХ ПАПОК (БЕЗ ФАЙЛОВ И ИНДЕКСОВ) СТРОГО ПО ВАШЕМУ ПРАВИЛУ
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_')
            is_under_dir = name.startswith('_')
            
            node = {}
            # Делаем красивое имя заголовка по умолчанию из названия папки
            node['title'] = clean_section_name.capitalize()
            node['url'] = f"/{clean_section_name}/"
            
            # Присваиваем свойства строго в зависимости от наличия подчёркивания _
            if is_under_dir:
                node['collection'] = clean_section_name
            else:
                node['section'] = clean_section_name
                
            # Ключом в карте на Шаге 1 становится чистое имя самой корневой папки
            flat_map[clean_section_name] = [node]
            log_artifact(f"[NAV-DEBUG] Шаг 1 (Папки): Зафиксирован узел корневой папки '{name}' -> {node['url']}")

    # 🔥 ШАГ 2 И ШАГ 3: ОБХОД ФИЗИЧЕСКИХ ФАЙЛОВ СТАТЕЙ И ПРОЕКТОВ (ИНДЕКСЫ ПОЛНОСТЬЮ ИГНОРИРУЮТСЯ)
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            for root_walk, _, files in os.walk(full_path):
                for file in files:
                    if not (file.endswith('.md') or file.endswith('.html')): continue
                    
                    # 🔥 ИГНОРИРУЕМ ИНДЕКСНЫЕ ФАЙЛЫ: их адреса и вывески разделов созданы на Шаге 1
                    file_slug, _ = os.path.splitext(file)
                    if file_slug == 'index': continue
                    
                    file_path = os.path.join(root_walk, file)
                    data, front_text, body = parse_yaml_front_matter(file_path)
                    if data is None or data.get('published') is False: continue

                    ready_permalink = data.get('permalink', '').strip()
                    relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')

                    node = {}
                    node['title'] = data.get('title', file_slug)

                    # 1. Если у файла ЕСТЬ permalink (Шаг 2)
                    if ready_permalink:
                        node['url'] = ready_permalink
                        
                        # Вырезаем первое слово структуры пермалинка контента сайта
                        permalink_clean = ready_permalink.strip('/')
                        first_word = permalink_clean.split('/')[0] if permalink_clean else ''
                        
                        # Проверка корня диска на дубли и коллизии папок по вашему правилу
                        has_clean_dir = first_word in root_dirs_present
                        has_under_dir = f"_{first_word}" in root_dirs_present
                        
                        if has_clean_dir and has_under_dir:
                            # Коллизия: в корне есть обе папки -> свойства связи вообще НЕ пишем
                            pass
                        elif has_under_dir:
                            node['relatedcollection'] = first_word
                        elif has_clean_dir:
                            node['relatedsection'] = first_word

                    # 2. Если у файла НЕТ permalink (Шаг 3 - Усовершенствованный автомат по вашей логике)
                    else:
                        clean_section_name = name.lstrip('_')
                        is_under_dir = name.startswith('_')
                        
                        node['url'] = f"/{clean_section_name}/{file_slug}/"
                        if is_under_dir:
                            node['relatedcollection'] = clean_section_name
                        else:
                            node['relatedsection'] = clean_section_name

                    # Синхронизируем Front Matter самого md-файла на диске
                    data['section'] = name.lstrip('_')
                    write_yaml_front_matter(file_path, data, body)

                    flat_map[relative_file_key] = [node]

    # 🔥 ОБРАБОТКА ПАПКИ СВЯЗАННЫХ ПОСТОВ ХРОНИКИ _POSTS/ СТРОГО ПО ВАШИМ ПРАВИЛАМ
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

                # Синхронизация Front Matter самого поста хроники
                post_page_type = data.get('post-page', 'journal')
                for key in list(data.keys()):
                    if str(key).endswith('-post-page'):
                        # 🔥 ИСПРАВЛЕНО НАВСЕГДА: Строгий индекс [0] исключает массивы заметок
                        post_page_type = str(key).split('-')[0]
                        break

                if data and data.get('date'):
                    post_date = str(data['date'])
                else:
                    match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                    post_date = match_date.group(1) if match_date else "2026-01-01"

                # Вычисляем полный физический путь к родителю по очищенному имени файла
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

                # Б. Пост хроники БЕЗ пермалинка (Вычисляем канонически по родителю)
                else:
                    node['url'] = f"/{post_page_type}/{file_slug_no_date}/{post_date.replace('-', '/')}/{file_name_clean}.html"
                    if calculated_parent_path:
                        node['relatedpages'] = calculated_parent_path
                        # Копируем свойства связи у найденного родителя
                        parent_node = flat_map[calculated_parent_path][0]
                        if 'relatedsection' in parent_node:
                            node['relatedsection'] = parent_node['relatedsection']
                        if 'relatedcollection' in parent_node:
                            node['relatedcollection'] = parent_node['relatedcollection']

                # Записываем вычисленные свойства обратно в исходный файл поста хроники
                data['categories'] = [post_page_type, file_slug_no_date]
                data['post-page'] = post_page_type
                if calculated_parent_path:
                    parent_node = flat_map[calculated_parent_path][0]
                    data['section'] = parent_node.get('relatedsection', parent_node.get('section', 'faire'))
                write_yaml_front_matter(file_path, data, body)

                flat_map[relative_file_key] = [node]
                log_artifact(f"[NAV-DEBUG] Обработан файл: {relative_file_key} | parent: {calculated_parent_path}")

    # ФИНИШНАЯ НАЧИСТАЯ ЗАПИСЬ ПЛОСКОЙ КАРТЫ НА ДИСК БЕЗ ЗНАЧКОВ *ID
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(flat_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
        log_artifact("[NAV-SUCCESS] Плоская универсальная навигационная карта успешно записана.")
    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации: {e}")

    try:
        log_file_path = os.path.join(debug_dir, 'navigation_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print("[NAV-SUCCESS] Технический отчёт успешно сохранен.")
    except:
        pass

if __name__ == '__main__':
    build_navigation_tree()
