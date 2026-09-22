#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module sitemap_navigation (Шаг 1 из пакета sitemap)
@about Подмодуль Этажа 3. Собирает базовую структуру, связи контента и URL в память.
"""

import os
import re
from .sitemap_utils import parse_yaml_front_matter  # Системная утилита чтения

def run_navigation_stage(root_dir, EXCLUDED_FOLDERS):
    """Скан репозитория, расчет базовых URL/связей и сборка сквозного словаря в памяти."""
    sitemap_flat_map = {}
    root_dirs_present = set()
    folders_with_index = set()
    
    # Собираем имена всех физических папок в корне диска строго с фильтром исключений
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and not name.startswith('.') and name not in EXCLUDED_FOLDERS:
            root_dirs_present.add(name)

    # 🔥 ШАГ 1: ОБРАБОТКА КОРНЕВЫХ ПАПОК (БЕЗ ФАЙЛОВ И ИНДЕКСОВ) СТРОГО ПО КАСКАДНОЙ ТАБЛИЦЕ
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_')
            is_under_dir = name.startswith('_')
            
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
            
            # Вычисление title, crumbtitle, emoji в папках разделов (Приоритет 1 и 2)
            if front_data:
                node['title'] = front_data.get('title', clean_section_name.capitalize())
                if 'crumbtitle' in front_data:
                    node['crumbtitle'] = front_data['crumbtitle']
                if front_data.get('emoji'):
                    node['emoji'] = front_data['emoji']
                
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
                
            sitemap_flat_map[clean_section_name] = [{
                'node': node,
                'front_matter': front_data if front_data else {},
                'body_content': '',
                'file_path': index_file_path
            }]

    # ФИНАЛЬНАЯ ПРОВЕРКА ШАГА 1: Добор автономных файлов из папки _pages/
    pages_dir = os.path.join(root_dir, '_pages')
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md') and file != 'index.md':
                slug, _ = os.path.splitext(file)
                
                if slug not in sitemap_flat_map:
                    p_data, p_front, p_body = parse_yaml_front_matter(os.path.join(pages_dir, file))
                    if p_data:
                        node = {
                            'title': p_data.get('title', slug.capitalize()),
                            'url': p_data.get('permalink', f"/{slug}/").strip()
                        }
                        if p_data.get('crumbtitle'):
                            node['crumbtitle'] = p_data['crumbtitle']
                        if p_data.get('emoji'):
                            node['emoji'] = p_data['emoji']
                            
                        node['section'] = slug
                        
                        sitemap_flat_map[slug] = [{
                            'node': node,
                            'front_matter': p_data,
                            'body_content': p_body,
                            'file_path': os.path.join(pages_dir, file)
                        }]

    # 🔥 ШАГ 2: ОБХОД ФИЗИЧЕСКИХ ФАЙЛОВ СТАТЕЙ И ПРОЕКТОВ (ИНДЕКСЫ ПОЛНОСТЬЮ ИГНОРИРУЮТСЯ)
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

                    # 2. Если у файла НЕТ permalink (с вашим точечным исправлением по индексам папок)
                    else:
                        clean_section_name = name.lstrip('_')
                        is_under_dir = name.startswith('_')
                        
                        # А. Если в родительской папке ЕСТЬ индексный файл (index.md / index.html)
                        if name in folders_with_index:
                            node['url'] = f"/{clean_section_name}/{file_slug}.html"
                        # Б. Если в родительской папке НЕТ индексного файла
                        else:
                            node['url'] = f"/{clean_section_name}/{file_slug}/"

                        if is_under_dir:
                            node['relatedcollection'] = clean_section_name
                        else:
                            node['relatedsection'] = clean_section_name

                    data['section'] = name.lstrip('_')

                    # Вместо физической записи на диск мы пока просто упаковываем всё в сквозной паспорт в памяти
                    sitemap_flat_map[relative_file_key] = [{
                        'node': node,
                        'front_matter': data,
                        'body_content': body,
                        'file_path': file_path
                    }]

    return sitemap_flat_map, root_dirs_present
