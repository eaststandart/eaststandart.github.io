#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module sitemap
@about Изолированный чистый препроцессор однотипной карты метаданных контента.
@purpose Полностью вычищен от модуля ленты новостей (feed), сохраняя 1-в-1
         все оригинальные функции проверки индексов, штамповки тегов и дат.
@author TechLab
@version 20.0.0-pure-monolith
"""

import os
import re
import sys
import yaml
import subprocess
import datetime

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

# Вспомогательные функции очистки текстовых свойств по вашему эталону
def clean_tag_local(text):
    if not text: return ""
    return re.sub(r'\s+', '', str(text).lower().strip())
    
    
def translit_title_local(text):
    if not text: return ""
    return re.sub(r'[^a-z0-9а-яё]', '', str(text).lower().strip())

# =====================================================================
# ЭТАЖ 3: ГЛАВНЫЙ УПРАВЛЯЮЩИЙ КОНВЕЙЕР (Диспетчер обхода)
# =====================================================================
def build_sitemap_tree():
    global artifacts_log_buffer
    artifacts_log_buffer.clear()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    debug_dir = os.path.join(root_dir, '_sitemap_files')
    os.makedirs(debug_dir, exist_ok=True)

    # Список жестких технических исключений корневых папок диска
    EXCLUDED_FOLDERS = {'_includes', '_layouts', '_pages', 'assets', 'bin', '.git', '.github', '_data', '_navigation_files', '_sitemap_files'}
    
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
            
            if front_data:
                node['title'] = front_data.get('title', clean_section_name.capitalize())
                if 'crumbtitle' in front_data:
                    node['crumbtitle'] = front_data['crumbtitle']
                if front_data.get('emoji'):
                    node['emoji'] = front_data['emoji']
                
                if front_data.get('permalink'):
                    node['url'] = front_data['permalink'].strip()
                else:
                    node['url'] = f"/{clean_section_name}/"
            else:
                node['title'] = clean_section_name.capitalize()
                node['url'] = f"/{clean_section_name}/"

            if is_under_dir:
                node['collection'] = clean_section_name
            else:
                node['section'] = clean_section_name
                
            flat_map[clean_section_name] = [node]

    # ФИНАЛЬНАЯ ПРОВЕРКА: Добор автономных файлов из папки _pages/
    pages_dir = os.path.join(root_dir, '_pages')
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md') and file != 'index.md':
                slug, _ = os.path.splitext(file)
                
                if slug not in flat_map:
                    p_data, _, _ = parse_yaml_front_matter(os.path.join(pages_dir, file))
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
                        flat_map[slug] = [node]

    # 🔥 ШАГ 2: ОБХОД ФИЗИЧЕСКИХ ФАЙЛОВ СТАТЕЙ И ПРОЕКТОВ (ИНДЕКСЫ ИГНОРИРУЮТСЯ)
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

                    # 1. Если у файла ЕСТЬ permalink во Front Matter
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

                    # 2. Если у файла НЕТ permalink — СТАРЫЙ ОРИГИНАЛЬНЫЙ КОНТУР
                    else:
                        clean_section_name = name.lstrip('_')
                        is_under_dir = name.startswith('_')
                        
                        node['url'] = f"/{clean_section_name}/{file_slug}/"

                        # 🛡️ ПРЕДОХРАНИТЕЛЬ: пишем permalink строго если в папке нет индексного файла!
                        if name not in folders_with_index and not name.startswith('_'):                        
                            data['permalink'] = node['url']
                            log_artifact(f"[NAV-DEBUG] Файл: {relative_file_key} | Записано permalink: {data['permalink']}")
                            # Перезаписываем только по факту реального добавления авто-пермалинка
                            write_yaml_front_matter(file_path, data, body)

                        if is_under_dir:
                            node['relatedcollection'] = clean_section_name
                        else:
                            node['relatedsection'] = clean_section_name

                    # АВТОНОМНАЯ ОБРАБОТКА ДАТЫ И ТЕГОВ СТРОГО В ПАМЯТИ ДЛЯ КАРТЫ СИТЕМЫ
                    if not data.get('date'):
                        match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_slug)
                        if match_date:
                            data['date'] = match_date.group(1)
                        else:
                            try:
                                cmd = ['git', 'log', '--diff-filter=A', '--format=%as', '--', file_path]
                                git_date = subprocess.check_output(cmd, text=True).strip().split('\n')[-1]
                                if git_date and re.match(r'^\d{4}-\d{2}-\d{2}$', git_date):
                                    data['date'] = git_date
                                else:
                                    mtime = os.path.getmtime(file_path)
                                    data['date'] = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                            except Exception:
                                mtime = os.path.getmtime(file_path)
                                data['date'] = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

                    node['date'] = str(data.get('date', ''))
                    for prop in ['direction', 'entity', 'level', 'emoji']:
                        if data.get(prop):
                            node[prop] = data[prop]

                    flat_map[relative_file_key] = [node]

    # 🔥 ШАГ 3: ОБРАБОТКА ПАПКИ СВЯЗАННЫХ ПОСТОВ ХРОНИКИ _POSTS/
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

                raw_post_type = str(data.get('posttype', '')).strip().lower() if data.get('posttype') else ""
                base_type_clean = raw_post_type.split('-')[0] if '-' in raw_post_type else raw_post_type

                calculated_parent_path = ""
                parent_file_name = f"{file_slug_no_date}.md"
                for key_path in flat_map.keys():
                    if key_path.endswith(f"/{parent_file_name}") or key_path == parent_file_name:
                        calculated_parent_path = key_path
                        break

                node = {}
                node['title'] = data.get('title', file_slug_no_date)
                node['date'] = post_date
                if raw_post_type:
                    node['posttype'] = raw_post_type

                if ready_permalink:
                    node['url'] = ready_permalink
                    permalink_clean = ready_permalink.strip('/')
                    first_word = permalink_clean.split('/')[0] if permalink_clean else ''
                    
                    if calculated_parent_path:
                        node['relatedpages'] = calculated_parent_path
                    
                    if f"_{first_word}" in root_dirs_present:
                        node['relatedcollection'] = first_word
                    elif first_word in root_dirs_present:
                        node['relatedsection'] = first_word
                else:
                    url_prefix = base_type_clean if base_type_clean else "post"
                    node['url'] = f"/{url_prefix}/{file_slug_no_date}/{post_date.replace('-', '/')}/{file_slug_no_date}.html"
                    if calculated_parent_path:
                        node['relatedpages'] = calculated_parent_path

                flat_map[relative_file_key] = [node]

    # СОБИРАЕМ ИТОГОВЫЙ СЛОВАРЬ КАРТЫ НАВИГАЦИИ С КОРНЕВЫМИ ПАПКАМИ
    final_output_map = {}
    final_output_map['detected_root_folders'] = sorted(list(root_dirs_present))
    for k, v in flat_map.items():
        final_output_map[k] = v

    output_file = os.path.join(data_dir, 'sitemap.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(final_output_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации: {e}")

    try:
        log_file_path = os.path.join(debug_dir, 'sitemap-md-properties.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print("[NAV-SUCCESS] Лог навигации успешно сохранен.")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось сохранить лог: {e}")

if __name__ == '__main__':
    build_sitemap_tree()
