#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 2)
@about Универсальный плоский препроцессор однотипной карты метаданных контента.
@purpose Шаг 1: Точный перенос рабочей логики в функцию build_navigation_crumbs.
@author TechLab
@version 16.0.0-exact-transfer
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

# 🔥 ТЕПЕРЬ СЮДА ЗАВЕДЕН ТОТ САМЫЙ РАБОЧИЙ КОД БЕЗ ИЗМЕНЕНИЙ ЛОГИКИ
def build_navigation_crumbs(data, file_slug, ready_permalink, name, folders_with_index, root_dirs_present, calculated_parent_path=""):
    """Сборка навигационного паспорта. Сюда перенесён стабильный рабочий алгоритм."""
    crumbs = {}
    crumbs['title'] = data.get('title', file_slug)
    
    # Режим А и Б для обычных страниц контента (Шаг 2)
    if name != '_posts':
        if ready_permalink:
            crumbs['url'] = ready_permalink
            permalink_clean = ready_permalink.strip('/')
            first_word = permalink_clean.split('/')[0] if permalink_clean else ''
            
            has_clean_dir = first_word in root_dirs_present
            has_under_dir = f"_{first_word}" in root_dirs_present
            
            if has_clean_dir and has_under_dir:
                pass
            elif has_under_dir:
                crumbs['relatedcollection'] = first_word
            elif has_clean_dir:
                crumbs['relatedsection'] = first_word
        else:
            clean_section_name = name.lstrip('_')
            is_under_dir = name.startswith('_')
            crumbs['url'] = f"/{clean_section_name}/{file_slug}/"
            if is_under_dir:
                crumbs['relatedcollection'] = clean_section_name
            else:
                crumbs['relatedsection'] = clean_section_name
                
    # Рабочая логика для постов хроники папки _posts/ (Шаг 3)
    else:
        if ready_permalink:
            crumbs['url'] = ready_permalink
            permalink_clean = ready_permalink.strip('/')
            first_word = permalink_clean.split('/')[0] if permalink_clean else ''
            
            has_clean_dir = first_word in root_dirs_present
            has_under_dir = f"_{first_word}" in root_dirs_present
            
            if calculated_parent_path:
                crumbs['relatedpages'] = calculated_parent_path
                
            if has_clean_dir and has_under_dir:
                pass
            elif has_under_dir:
                crumbs['relatedcollection'] = first_word
            elif has_clean_dir:
                # Вписываем связь только если это автономный пост без родительского пути
                if not calculated_parent_path:
                    crumbs['relatedsection'] = first_word
        else:
            # Ссылка соберется во внешней обертке конвейера по умолчанию
            if calculated_parent_path:
                crumbs['relatedpages'] = calculated_parent_path

    return crumbs

def build_navigation_tree():
    global artifacts_log_buffer
    artifacts_log_buffer.clear()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    debug_dir = os.path.join(root_dir, '_processed_files')
    os.makedirs(debug_dir, exist_ok=True)

    # Список жестких технических исключений корневых папок диска
    EXCLUDED_FOLDERS = {'_includes', '_layouts', '_pages', 'assets', 'bin', '.git', '.github', '_data', '_processed_files', '_content_files'}
    
    flat_map = {}
    root_dirs_present = set()
    folders_with_index = set()
    
    # 🔥 ИСПРАВЛЕНО: Собираем имена корневых папок СТРОГО с фильтром исключений, убирая мусор
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and not name.startswith('.') and name not in EXCLUDED_FOLDERS:
            root_dirs_present.add(name)

    # ШАГ 1: ОБРАБОТКА КОРНЕВЫХ ПАПОК (БЕЗ ФАЙЛОВ И ИНДЕКСОВ)
    for name in sorted(list(root_dirs_present)):
        full_path = os.path.join(root_dir, name)
        clean_section_name = name.lstrip('_')
        is_under_dir = name.startswith('_')
        
        # Определяем Режим А для Шага 2
        if os.path.exists(os.path.join(full_path, 'index.md')) or os.path.exists(os.path.join(full_path, 'index.html')):
            folders_with_index.add(name)
            
        node = {}
        node['title'] = clean_section_name.capitalize()
        node['url'] = f"/{clean_section_name}/"
        
        if is_under_dir:
            node['collection'] = clean_section_name
        else:
            node['section'] = clean_section_name
            
        flat_map[clean_section_name] = [node]
        log_artifact(f"[NAV-DEBUG] Шаг 1 (Папки): Инициализирован узел папки '{name}'")

    # ШАГ 2: ОБХОД ФИЗИЧЕСКИХ ФАЙЛОВ СТАТЕЙ (ИНДЕКСЫ ПОЛНОСТЬЮ ИГНОРИРУЮТСЯ)
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_')
            
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

                    # Вызов фабрики крошек из оперативной памяти сервера
                    passport = build_navigation_crumbs(data, file_slug, ready_permalink, name, folders_with_index, root_dirs_present)

                    data['section'] = clean_section_name
                    write_yaml_front_matter(file_path, data, body)

                    flat_map[relative_file_key] = [passport]

    # ШАГ 3: ОБРАБОТКА ПАПКИ СВЯЗАННЫХ ПОСТОВ ХРОНИКИ _POSTS/
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

                # Вычисляем полный физический путь к родителю по очищенной карте Шага 2
                calculated_parent_path = ""
                parent_file_name = f"{file_slug_no_date}.md"
                for key_path in flat_map.keys():
                    if key_path.endswith(f"/{parent_file_name}") or key_path == parent_file_name:
                        calculated_parent_path = key_path
                        break

                # Вызов фабрики крошек для постов хроники с передачей пути родителя
                passport = build_navigation_crumbs(data, file_slug_no_date, ready_permalink, '_posts', folders_with_index, root_dirs_present, calculated_parent_path)
                    
                # Обертка автомата URL для постов без пермалинка
                if not ready_permalink:
                    post_page_type = data.get('post-page', 'journal')
                    for key in list(data.keys()):
                        if str(key).endswith('-post-page'):
                            post_page_type = str(key).split('-')
                            break
                    passport['url'] = f"/{post_page_type}/{file_slug_no_date}/{post_date.replace('-', '/')}/{file_name_clean}.html"

                # Синхронизация Front Matter самого файла поста
                if calculated_parent_path:
                    parent_node_list = flat_map[calculated_parent_path]
                    if isinstance(parent_node_list, list) and len(parent_node_list) > 0:
                        parent_node = parent_node_list
                        data['section'] = parent_node.get('relatedsection', parent_node.get('section', 'faire'))
                write_yaml_front_matter(file_path, data, body)

                flat_map[relative_file_key] = [passport]
                log_artifact(f"[NAV-DEBUG] Пост хроники: {relative_file_key} | parent: {calculated_parent_path}")

    # Склеиваем итоговую чистую карту
    final_output_map = {}
    final_output_map['detected_root_folders'] = sorted(list(root_dirs_present))
    for k, v in flat_map.items():
        final_output_map[k] = v

    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(final_output_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
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
