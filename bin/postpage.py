#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module post-page
@about Изолированный автономный генератор физических md-страниц архивов проектов.
@purpose Автоматическая штамповка страниц под кнопку "0" с динамическим объединением
         минимальных свойств во Front Matter, каноничными русскими заголовками проектов 
         напрямую из navigation.yml и вызовом внешнего инклуда с параметрами.
@author TechLab
@version 16.0.0-restored-stable
"""

import os
import sys
import yaml

def generate_project_posts_pages():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    navigation_file = os.path.join(root_dir, '_data', 'navigation.yml')
    log_file_path = os.path.join(root_dir, '_content_files', 'posts-page-generator.log')
    
    log_buffer = []
    
    if not os.path.exists(navigation_file):
        print(f"[POST-ERROR] Карта навигации navigation.yml не найдена: {navigation_file}")
        return

    # Шаг 0: Загружаем Единственный Источник Правды в оперативную память
    try:
        with open(navigation_file, 'r', encoding='utf-8') as f:
            navigation_map = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[POST-ERROR] Сбой чтения конфигурационного файла YAML: {e}")
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

    # Сканируем карту навигации, находим родительские проекты и штампуем для них страницы-оболочки
    for nav_key, nav_nodes in navigation_map.items():
        if (not nav_key.startswith('_posts/') and 
            nav_key != 'detected_root_folders' and 
            isinstance(nav_nodes, list) and len(nav_nodes) > 0):
            
            project_passport = nav_nodes
            if isinstance(project_passport, dict) and 'title' in project_passport:
                
                # Извлекаем слаг проекта и его русский заголовок
                p_slug = nav_key.split('/')[-2] if '/' in nav_key else nav_key.replace('.md', '')
                parent_title = project_passport['title'].strip()
                
                # Генерируем страницы СТРОГО для двух типов лент: journal и media
                for loop_type in ['journal', 'media']:
                    target_folder_path = os.path.join(root_dir, loop_type)
                    os.makedirs(target_folder_path, exist_ok=True)
                    target_md_file = os.path.join(target_folder_path, f"{p_slug}.md")
                    
                    # Индивидуальный Front Matter страницы проекта (mathjax: true на месте)
                    base_front_matter = {
                        "layout": "page",
                        "title": f"{parent_title}: лента постов",
                        "permalink": f"/{loop_type}/{p_slug}/",
                        "mathjax": True
                    }
                    front_matter_string = yaml.dump(base_front_matter, allow_unicode=True, default_flow_style=False, sort_keys=False)
                    
                    # Впечатываем чистый вызов инклуда с передачей параметров связи
                    body_content_string = f'{{% include posts-page-open.liquid category="{loop_type}" project_file="{nav_key}" %}}'
                    file_content = f"---\n{front_matter_string}---\n\n{body_content_string}".strip()
                    
                    try:
                        with open(target_md_file, 'w', encoding='utf-8') as f:
                            f.write(file_content)
                        log_msg = f"[POST-GENERATOR] Создан файл: {loop_type}/{p_slug}.md | Заголовок: {parent_title}: лента постов"
                        print(log_msg)
                        log_buffer.append(log_msg)
                    except Exception as e:
                        print(f"[POST-ERROR] Не удалось записать файл архива {target_md_file}: {e}")

    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
    except:
        pass

if __name__ == '__main__':
    generate_project_posts_pages()
