#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module post-page
@about Изолированный автономный генератор физических md-страниц архивов проектов.
@purpose Автоматическая штамповка страниц под кнопку "0" с макетом layout: page,
         свойством mathjax: true и вызовом оригинального инклуда media-archive.liquid.
@author TechLab
@version 5.0.0-final-kanon
"""

import os
import sys
import yaml

def generate_project_posts_pages():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    feed_file = os.path.join(root_dir, '_data', 'feed.yml')
    log_file_path = os.path.join(root_dir, '_post_page_files', 'posts-page-generator.log')
    
    log_buffer = []
    
    if not os.path.exists(feed_file):
        print(f"[POST-ERROR] Источник Правды feed.yml не найден по пути: {feed_file}")
        return

    try:
        with open(feed_file, 'r', encoding='utf-8') as f:
            feed_data = yaml.safe_load(f) or {}
        feed_source = feed_data.get('feed', [])
    except Exception as e:
        print(f"[POST-ERROR] Сбой чтения файла универсальной ленты: {e}")
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

    created_pages_registry = set()

    # Сбор уникальных страниц проектов на основе feed.yml
    for item in feed_source:
        p_related = item.get('related')
        p_type = item.get('posttype')
        is_post_valid = item.get('is_post') == 'true' or item.get('is_post') is True
        
        if p_related and p_type and is_post_valid:
            page_uid = f"{p_type}::{p_related}"
            if page_uid in created_pages_registry:
                continue
                
            parent_title = p_related.replace('-', ' ').capitalize()
            target_folder_path = os.path.join(root_dir, p_type)
            os.makedirs(target_folder_path, exist_ok=True)
            
            target_md_file = os.path.join(target_folder_path, f"{p_related}.md")
            
            # Штампуем Front Matter 1 в 1 как на старом сайте, включая mathjax: true
            front_matter_lines = [
                "---",
                "layout: page",
                f'title: "{parent_title}: лента проекта"',
                f"permalink: /{p_type}/{p_related}/",
                "mathjax: true",
                "---",
                "",
                f'{{% include media-archive.liquid category="{p_type}" project="{p_related}" %}}'
            ]
            
            try:
                with open(target_md_file, 'w', encoding='utf-8') as f:
                    f.write("\n".join(front_matter_lines))
                log_msg = f"[POST-GENERATOR] Создан файл: {p_type}/{p_related}.md с вызовом media-archive.liquid."
                print(log_msg)
                log_buffer.append(log_msg)
                created_pages_registry.add(page_uid)
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
