#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 2)
@about Универсальный плоский препроцессор однотипной карты метаданных контента.
@purpose Собирает строго 3 базовых параметра для работы хлебных крошек по полным путям.
@author TechLab
@version 13.0.0-flat-pure-paths
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
    """Выводит лог в консоль сервера Actions и буферизирует его для артефактов."""
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

    # Классический лаконичный набор исключений корневых папок диска
    EXCLUDED_FOLDERS = {'_includes', '_layouts', '_pages', 'assets', 'bin', '.git', '.github'}
    
    flat_map = {}
    folders_with_index = set()
    
    # Сначала собираем имена всех физических папок в корне диска для фильтра коллизий
    root_dirs_present = set()
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and not name.startswith('.'):
            root_dirs_present.add(name)
    
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
            
            for root_walk, _, files in os.walk(full_path):
                for file in files:
                    if not (file.endswith('.md') or file.endswith('.html')): continue
                    
                    file_path = os.path.join(root_walk, file)
                    data, front_text, body = parse_yaml_front_matter(file_path)
                    if data is None or data.get('published') is False: continue

                    file_slug, _ = os.path.splitext(file)
                    ready_permalink = data.get('permalink', '')
                    if not ready_permalink: continue

                    # Универсальный разбор первого слова структуры permalink
                    permalink_clean = ready_permalink.strip('/')
                    first_word = permalink_clean.split('/')[0] if permalink_clean else ''
                    
                    # Проверка коллизий корня диска по вашему правилу
                    has_clean_dir = first_word in root_dirs_present
                    has_under_dir = f"_{first_word}" in root_dirs_present
                    
                    # Записываем секцию в сам md-файл
                    data['section'] = name.lstrip('_')
                    write_yaml_front_matter(file_path, data, body)

                    # Сбор паспорта страницы контента заметок
                    node = {}
                    node['title'] = data.get('title', file_slug)
                    node['url'] = ready_permalink
                    
                    # Расстановка свойств по правилам Режимов А/Б и коллекций
                    if has_clean_dir and has_under_dir:
                        # Коллизия: папки дублируются в корне диска -> ничего не пишем
                        pass
                    elif has_under_dir:
                        if file_slug == 'index':
                            node['collection'] = first_word
                        else:
                            node['relatedcollection'] = first_word
                    elif has_clean_dir:
                        if name in folders_with_index:
                            if file_slug == 'index':
                                node['section'] = first_word
                            else:
                                node['relatedsection'] = first_word
                        else:
                            # Режим Б (нет индекса, например faire) -> сами формируют раздел!
                            node['section'] = first_word

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

                ready_permalink = data.get('permalink', '')
                if not ready_permalink: continue

                # Разбор первого слова структуры permalink поста хроники
                permalink_clean = ready_permalink.strip('/')
                first_word = permalink_clean.split('/')[0] if permalink_clean else ''
                
                has_clean_dir = first_word in root_dirs_present
                has_under_dir = f"_{first_word}" in root_dirs_present

                # 🔥 ИСПРАВЛЕНО: Поиск физического файла-родителя и запись полного пути в relatedpages
                calculated_parent_path = ""
                parent_file_name = f"{file_slug_no_date}.md"
                
                for key_path in flat_map.keys():
                    if key_path.endswith(f"/{parent_file_name}") or key_path == parent_file_name:
                        calculated_parent_path = key_path
                        break

                # Синхронизация Front Matter самого поста хроники
                post_page_type = data.get('post-page', 'journal')
                for key in list(data.keys()):
                    if str(key).endswith('-post-page'):
                        post_page_type = str(key).split('-')[0]
                        break

                data['categories'] = [post_page_type, file_slug_no_date]
                data['post-page'] = post_page_type
                write_yaml_front_matter(file_path, data, body)

                # Сбор паспорта связанного или автономного поста
                node = {}
                node['title'] = data.get('title', file_slug_no_date)
                node['url'] = ready_permalink
                
                # Записываем relatedpages только если физический родитель реально найден на диске
                if calculated_parent_path:
                    node['relatedpages'] = calculated_parent_path
                
                # Расстановка связей с корневыми разделами
                if has_clean_dir and has_under_dir:
                    pass
                elif has_under_dir:
                    node['relatedcollection'] = first_word
                elif has_clean_dir:
                    node['relatedsection'] = first_word

                relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')
                flat_map[relative_file_key] = [node]
                log_artifact(f"[NAV-DEBUG] Обработан файл: {relative_file_key} | parent: {calculated_parent_path}")

    # Запись чистой плоской карты контента заметок без значков *id
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
        print("[NAV-SUCCESS] Отчёт успешно выгружен в артефакты.")
    except:
        pass

if __name__ == '__main__':
    build_navigation_tree()
