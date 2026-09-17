#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module post-page
@about Изолированный автономный генератор физических md-страниц архивов проектов.
@purpose Автоматическая штамповка страниц под кнопку "0" с динамическим объединением
         свойств во Front Matter (включая mathjax: true), каноничными русскими заголовками 
         проектов на основе связанных путей relatedpages и вызовом внешнего инклуда.
@author TechLab
@version 12.0.0-relatedpages-exact
"""

import os
import sys
import yaml

def generate_project_posts_pages():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    feed_file = os.path.join(root_dir, '_data', 'feed.yml')
    navigation_file = os.path.join(root_dir, '_data', 'navigation.yml')
    log_file_path = os.path.join(root_dir, '_post_page_files', 'posts-page-generator.log')
    
    log_buffer = []
    
    # Проверяем наличие Источников Правды контура
    if not os.path.exists(feed_file):
        print(f"[POST-ERROR] Источник Правды feed.yml не найден по пути: {feed_file}")
        return
    if not os.path.exists(navigation_file):
        print(f"[POST-ERROR] Карта навигации navigation.yml не найдена: {navigation_file}")
        return

    # Шаг 1: Загружаем данные в оперативную память
    try:
        with open(feed_file, 'r', encoding='utf-8') as f:
            feed_data = yaml.safe_load(f) or {}
        feed_source = feed_data.get('feed', [])
        
        with open(navigation_file, 'r', encoding='utf-8') as f:
            navigation_map = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[POST-ERROR] Сбой чтения конфигурационных файлов YAML: {e}")
        return

    # 🧼 САНИТАРНАЯ ЗАЧИСТКА ПАПОК ОТ СТРАНИЦ-ПРИЗРАКОВ
    print("[POST-CLEAN] Запуск санитарной зачистки целевых папок контура...")
    for target_folder in ['journal', 'media']:
        folder_path = os.path.join(root_dir, target_folder)
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.md') and 'index' not in file_name:
                    file_to_remove = os.path.join(folder_path, file_name)
                    try:
                        os.remove(file_to_remove)
                        log_buffer.append(f"[CLEAN] Удален устаревший файл: {target_folder}/{file_name}")
                    except Exception as e:
                        print(f"[POST-ERROR] Не удалось удалить файл {file_to_remove}: {e}")

    # Шаг 2: Группируем элементы фида по уникальным путям связанных проектов (relatedpages)
    # Нам нужно вытащить relatedpages из навигационной карты для каждого элемента фида
    projects_data = {}
    
    for item in feed_source:
        p_url = item.get('url', '')
        p_type = item.get('posttype')
        is_post_valid = item.get('is_post') == 'true' or item.get('is_post') is True
        
        if p_url and p_type and is_post_valid:
            # Ищем паспорт этого поста в navigation.yml, чтобы вытащить точный relatedpages
            related_page_path = None
            for nav_key, nav_nodes in navigation_map.items():
                if nav_key.startswith('_posts/') and isinstance(nav_nodes, list) and len(nav_nodes) > 0:
                    if nav_nodes[0].get('url') == p_url:
                        related_page_path = nav_nodes[0].get('relatedpages')
                        break
            
            if not related_page_path:
                continue
                
            if related_page_path not in projects_data:
                projects_data[related_page_path] = {
                    'project_file': related_page_path,
                    'type': p_type,
                    'slug': related_page_path.split('/')[-2] if '/' in related_page_path else related_page_path.replace('.md', '')
                }
            
    # Шаг 3: Генерация файлов страниц
    for rel_path, proj_info in projects_data.items():
        p_file = proj_info['project_file']
        p_type = proj_info['type']
        p_slug = proj_info['slug']
        
        # Находим чистокровный русский заголовок родительского проекта по прямому ключу
        parent_title = p_slug.replace('-', ' ').capitalize()
        parent_nodes = navigation_map.get(rel_path)
        if parent_nodes and isinstance(parent_nodes, list) and len(parent_nodes) > 0:
            if parent_nodes[0].get('title'):
                parent_title = parent_nodes[0]['title'].strip()

        target_folder_path = os.path.join(root_dir, p_type)
        os.makedirs(target_folder_path, exist_ok=True)
        target_md_file = os.path.join(target_folder_path, f"{p_slug}.md")
        
        # Базовый расширяемый словарь свойств индивидуальной страницы
        base_front_matter = {
            "layout": "page",
            "title": f"{parent_title}: лента постов",
            "permalink": f"/{p_type}/{p_slug}/",
            "mathjax": True
        }
        front_matter_string = yaml.dump(base_front_matter, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        # Формируем тело маркдаун-страницы с передачей точного пути к файлу проекта
        body_content_string = f'{{% include posts-page-open.liquid category="{p_type}" project_file="{p_file}" %}}'
        file_content = f"---\n{front_matter_string}---\n\n{body_content_string}".strip()
        
        try:
            with open(target_md_file, 'w', encoding='utf-8') as f:
                f.write(file_content)
            log_msg = f"[POST-GENERATOR] Создан файл: {p_type}/{p_slug}.md | Заголовок: {parent_title}: лента постов | Параметр project_file: {p_file}"
            print(log_msg)
            log_buffer.append(log_msg)
        except Exception as e:
            print(f"[POST-ERROR] Не удалось записать файл архива {target_md_file}: {e}")

    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[POST-SUCCESS] Изолированный лог генератора страниц успешно сохранён.")
    except Exception as e:
        print(f"[POST-ERROR] Не удалось сохранить файл лога: {e}")

if __name__ == '__main__':
    generate_project_posts_pages()
