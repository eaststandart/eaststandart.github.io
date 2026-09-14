#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 2)
@about Универсальный плоский препроцессор метаданных контента.
@purpose Собирает строго 3 базовых параметра для работы хлебных крошек.
@author TechLab
@version 12.1.0-clean-monolith-part1
"""

import os
import re
import sys
import yaml

def parse_yaml_front_matter(file_path):
    """Извлекает блок Front Matter из markdown-файла контента."""
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
    """Выводит лог в консоль и буферизирует его для артефактов."""
    print(text)
    artifacts_log_buffer.append(text)

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства обратно в md-файл."""
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

    EXCLUDED_FOLDERS = {'_includes', '_layouts', '_pages', 'assets', 'bin', '.git', '.github'}
    
    flat_map = {}
    folders_with_index = set()
    
    # Шаг 1: Автоматическое определение Режима А по наличию index.md внутри папок
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.'):
            if name != '_posts':
                if os.path.exists(os.path.join(full_path, 'index.md')) or os.path.exists(os.path.join(full_path, 'index.html')):
                    folders_with_index.add(name)

    # Шаг 2: Плоский сбор файлов страниц контента и коллекций
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_')
            is_jekyll_collection = name.startswith('_')
            
            for root_walk, _, files in os.scandir(full_path) if hasattr(os, 'scandir') else os.walk(full_path):
                # Поддержка обхода для os.walk
                if not isinstance(files, list):
                    continue
                for file in files:
                    if not (file.endswith('.md') or file.endswith('.html')): continue
                    
                    file_path = os.path.join(root_walk, file)
                    data, front_text, body = parse_yaml_front_matter(file_path)
                    if data is None or data.get('published') is False: continue

                    file_slug, _ = os.path.splitext(file)
                    
                    # Расчёт URL Режимов А и Б
                    ready_permalink = data.get('permalink')
                    if ready_permalink:
                        final_url = ready_permalink
                    elif name in folders_with_index:
                        if file_slug == 'index':
                            final_url = f"/{clean_section_name}/"
                        else:
                            final_url = f"/{clean_section_name}/{file_slug}.html"
                    else:
                        if file_slug == 'index':
                            final_url = f"/{clean_section_name}/"
                        else:
                            final_url = f"/{clean_section_name}/{file_slug}/"

                    data['section'] = clean_section_name
                    write_yaml_front_matter(file_path, data, body)

                    # Формируем плоский паспорт страницы контента заметок
                    node = {}
                    node['title'] = data.get('title', file_slug)
                    node['url'] = final_url
                    
                    # 🔥 НОВАЯ СИНТАКСИЧЕСКАЯ ЛОГИКА РАЗДЕЛОВ И КОЛЛЕКЦИЙ ПО ВАШИМ ПРАВИЛАМ
                    if is_jekyll_collection:
                        node['collection'] = clean_section_name
                    elif name in folders_with_index:
                        if file_slug == 'index':
                            node['section'] = clean_section_name
                        else:
                            node['relatedsection'] = clean_section_name
                    else:
                        # Режим Б (нет индекса, например faire) -> они сами формируют раздел!
                        node['section'] = clean_section_name

                    relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')
                    flat_map[relative_file_key] = [node]

    # Шаг 3: Тотальный обход папки связанных постов хроники _posts/
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

                # 🔥 ИСПРАВЛЕНО НАВСЕГДА: Извлекаем строго первое строковое слово из сплита суффикса
                post_page_type = data.get('post-page', 'journal')
                for key in list(data.keys()):
                    if str(key).endswith('-post-page'):
                        post_page_type = str(key).split('-')[0]
                        break

                if data and data.get('date'):
                    post_date = str(data['date'])
                else:
                    match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                    post_date = match_date.group(1) if match_date else "2026-01-01"

                short_url = f"/{post_page_type}/{file_slug_no_date}/{post_date.replace('-', '/')}/{file_name_clean}.html"

                calculated_parent_section = "faire"
                parent_file_key = f"{file_slug_no_date}.md"
                
                for key_path, nodes_list in flat_map.items():
                    if key_path.endswith(f"/{parent_file_key}") or key_path == parent_file_key:
                        if isinstance(nodes_list, list) and len(nodes_list) > 0:
                            p_node = nodes_list[0]
                            calculated_parent_section = p_node.get('section', p_node.get('relatedsection', p_node.get('collection', 'faire')))
                            break

                data['categories'] = [post_page_type, file_slug_no_date]
                data['post-page'] = post_page_type
                data['section'] = calculated_parent_section
                write_yaml_front_matter(file_path, data, body)

                # Формируем плоский паспорт связанного поста
                node = {}
                node['title'] = data.get('title', file_slug_no_date)
                node['url'] = short_url
                node['relatedpages'] = file_slug_no_date

                relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')
                flat_map[relative_file_key] = [node]
                log_artifact(f"[NAV-DEBUG] Обработан файл: {relative_file_key} | relatedpages: {file_slug_no_date}")

    # Финишная запись чистой плоской карты на диск заметок без значков *id
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(flat_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
        log_artifact("[NAV-SUCCESS] Плоская навигационная карта успешно записана.")
    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации: {e}")

    try:
        log_file_path = os.path.join(debug_dir, 'navigation_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print("[NAV-SUCCESS] Отчёт успешно выгружен в артефакты.")
    except:
        pass

if __name__ == '__main__':
    build_navigation_tree()
