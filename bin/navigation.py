#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 2)
@about Универсальный плоский препроцессор однотипной карты метаданных контента.
@purpose Шаг 1: Изолированная функция build_navigation_crumbs для хлебных крошек.
@author TechLab
@version 15.1.0-clean-names
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

# 🔥 ИЗОЛИРОВАННЫЙ МОДУЛЬ НАВИГАЦИИ С ИСПРАВЛЕННЫМ ПОНЯТНЫМ ИМЕНЕМ
def build_navigation_crumbs(data, file_slug, ready_permalink, name, is_under_dir, root_dirs_present):
    """Принимает сырые данные из памяти и собирает строго базовый паспорт хлебных крошек.
    Никаких повторных открытий файлов с диска!"""
    crumbs = {}
    
    # 1. Свойство title
    crumbs['title'] = data.get('title', file_slug)
    
    # 2. Свойство url (Строго нативный permalink из файла или плоский автомат папки)
    if ready_permalink:
        crumbs['url'] = ready_permalink
    else:
        clean_section_name = name.lstrip('_')
        crumbs['url'] = f"/{clean_section_name}/{file_slug}/"

    # 3. Вычисление свойств связей по пермалинком и проверке корня диска контента
    if ready_permalink:
        permalink_clean = ready_permalink.strip('/')
        first_word = permalink_clean.split('/') if permalink_clean else ''
        
        has_clean_dir = first_word in root_dirs_present
        has_under_dir = f"_{first_word}" in root_dirs_present
        
        # Защита от коллизий: если папки дублируются или их нет — свойства связей отсутствуют
        if not (has_clean_dir and has_under_dir):
            if has_under_dir:
                crumbs['relatedcollection'] = first_word
            elif has_clean_dir:
                crumbs['relatedsection'] = first_word
    else:
        # Автоматический плоский расчёт связей по физической папке
        clean_section_name = name.lstrip('_')
        if is_under_dir:
            crumbs['relatedcollection'] = clean_section_name
        else:
            crumbs['relatedsection'] = clean_section_name
            
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

    # 🔥 ИСПРАВЛЕНО: Служебные технические директории внесены в список жестких исключений
    EXCLUDED_FOLDERS = {'_includes', '_layouts', '_pages', 'assets', 'bin', '.git', '.github', '_data', '_processed_files', '_content_files'}
    
    flat_map = {}
    root_dirs_present = set()
    
    # Собираем имена всех физических папок в корне диска для фильтра коллизий
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and not name.startswith('.'):
            root_dirs_present.add(name)

    # ШАГ 1: ОБРАБОТКА КОРНЕВЫХ ПАПОК (БЕЗ ФАЙЛОВ И ИНДЕКСОВ) ПО НАШЕМУ ПРАВИЛУ
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_')
            is_under_dir = name.startswith('_')
            
            node = {}
            node['title'] = clean_section_name.capitalize()
            node['url'] = f"/{clean_section_name}/"
            
            if is_under_dir:
                node['collection'] = clean_section_name
            else:
                node['section'] = clean_section_name
                
            flat_map[clean_section_name] = [node]
            log_artifact(f"[NAV-DEBUG] Шаг 1 (Папки): Зафиксирован узел корневой папки '{name}' -> {node['url']}")

    # ШАГ 2 И ШАГ 3: ОБХОД ФИЗИЧЕСКИХ ФАЙЛОВ СТАТЕЙ (ИНДЕКСЫ ПОЛНОСТЬЮ ИГНОРИРУЮТСЯ)
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_')
            is_under_dir = name.startswith('_')
            
            for root_walk, _, files in os.walk(full_path):
                for file in files:
                    if not (file.endswith('.md') or file.endswith('.html')): continue
                    
                    file_slug, _ = os.path.splitext(file)
                    if file_slug == 'index': continue
                    
                    file_path = os.path.join(root_walk, file)
                    # 🔥 Файл открывается с диска СТРОГО один раз!
                    data, front_text, body = parse_yaml_front_matter(file_path)
                    if data is None or data.get('published') is False: continue

                    ready_permalink = data.get('permalink', '').strip()
                    relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')

                    # 🔥 ВЫЗОВ ИЗОЛИРОВАННОЙ ФАБРИКИ КРОШЕК ИЗ ОПЕРАТИВНОЙ ПАМЯТИ
                    passport = build_navigation_crumbs(data, file_slug, ready_permalink, name, is_under_dir, root_dirs_present)

                    # Синхронизируем Front Matter самого md-файла на диске
                    data['section'] = clean_section_name
                    write_yaml_front_matter(file_path, data, body)

                    flat_map[relative_file_key] = [passport]

    # ОБРАБОТКА ПАПКИ СВЯЗАННЫХ ПОСТОВ ХРОНИКИ _POSTS/
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not (file.endswith('.md') or file.endswith('.html')): continue
                
                file_path = os.path.join(root, file)
                # 🔥 Пост открывается с диска СТРОГО один раз!
                data, front_text, body = parse_yaml_front_matter(file_path)
                if data is None or data.get('published') is False: continue

                file_name_clean, _ = os.path.splitext(file)
                file_slug_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)
                ready_permalink = data.get('permalink', '').strip()
                relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')

                match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                post_date = match_date.group(1) if match_date else "2026-01-01"

                # Вычисляем полный физический путь к родителю контента
                calculated_parent_path = ""
                parent_file_name = f"{file_slug_no_date}.md"
                for key_path in flat_map.keys():
                    if key_path.endswith(f"/{parent_file_name}") or key_path == parent_file_name:
                        calculated_parent_path = key_path
                        break

                # 🔥 ВЫЗОВ ИЗОЛИРОВАННОЙ ФАБРИКИ КРОШЕК ИЗ ОПЕРАТИВНОЙ ПАМЯТИ ДЛЯ ПОСТА ХРОНИКИ
                passport = build_navigation_crumbs(data, file_slug_no_date, ready_permalink, '_posts', False, root_dirs_present)

                # Дописываем к паспорту поста relatedpages по вашему правилу полных путей
                if calculated_parent_path:
                    passport['relatedpages'] = calculated_parent_path
                    
                # Доработка автомата URL для постов без пермалинка
                if not ready_permalink:
                    post_page_type = data.get('post-page', 'journal')
                    for key in list(data.keys()):
                        if str(key).endswith('-post-page'):
                            post_page_type = str(key).split('-')[0]
                            break
                    passport['url'] = f"/{post_page_type}/{file_slug_no_date}/{post_date.replace('-', '/')}/{file_name_clean}.html"

                # Синхронизация Front Matter самого файла поста
                if calculated_parent_path:
                    parent_node = flat_map[calculated_parent_path]
                    data['section'] = parent_node.get('relatedsection', parent_node.get('section', 'faire'))
                write_yaml_front_matter(file_path, data, body)

                flat_map[relative_file_key] = [passport]
                log_artifact(f"[NAV-DEBUG] Пост хроники: {relative_file_key} | parent: {calculated_parent_path}")

    # ФИНИШНАЯ НАЧИСТАЯ ЗАПИСЬ ПЛОСКОЙ КАРТЫ НА ДИСК
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
