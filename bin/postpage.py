#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module post-page
@about Изолированный автономный генератор физических md-страниц архивов проектов.
@purpose Автоматическая штамповка лент под кнопку "0" на основе плоской карты Питона 
         с автоматической санитарной зачисткой папок от устаревшего контента.
@author TechLab
@version 2.0.0
"""

import os
import re
import yaml

def generate_project_posts_pages():
    # Настройка базовых путей диска сервера Actions
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    navigation_file = os.path.join(root_dir, '_data', 'navigation.yml')
    log_file_path = os.path.join(root_dir, '_post_page_files', 'posts-page-generator.log')
    
    # Буфер для вывода scannable-строк в лог артефактов
    log_buffer = []
    
    # Проверка: если карты навигации ещё нет на диске, останавливаем контур
    if not os.path.exists(navigation_file):
        print(f"[POST-ERROR] Источник Правды navigation.yml не найден по пути: {navigation_file}")
        return

    # Шаг 1: Читаем Источник Правды в память как плоский словарь
    try:
        with open(navigation_file, 'r', encoding='utf-8') as f:
            navigation_map = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[POST-ERROR] Сбой чтения файла карты навигации: {e}")
        return

    # 🧼 ЭТАП САНИТАРНОЙ ЗАЧИСТКИ: Удаляем старые сгенерированные файлы, чтобы избежать страниц-призраков
    print("[POST-CLEAN] Запуск санитарной зачистки целевых папок контура...")
    for target_folder in ['journal', 'media']:
        folder_path = os.path.join(root_dir, target_folder)
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                # Удаляем только .md файлы проектов, не трогая главные индексы папок
                if file_name.endswith('.md') and 'index' not in file_name:
                    file_to_remove = os.path.join(folder_path, file_name)
                    try:
                        os.remove(file_to_remove)
                        log_buffer.append(f"[CLEAN] Удален устаревший файл: {target_folder}/{file_name}")
                    except Exception as e:
                        print(f"[POST-ERROR] Не удалось удалить файл {file_to_remove}: {e}")

    # Буфер в оперативной памяти для защиты от дублирования одинаковых страниц
    created_pages_registry = set()

    # Шаг 2: Сквозное сканирование карты навигации
    for file_key, nodes in navigation_map.items():
        # Игнорируем заголовок со списком корневых папок
        if file_key == 'detected_root_folders':
            continue
            
        if not isinstance(nodes, list) or len(nodes) == 0:
            continue
            
        passport = nodes[0]
        
        # Наш жесткий предохранитель: ищем только посты хроники с posttype и relatedpages
        post_type = passport.get('posttype')
        related_page_path = passport.get('relatedpages')
        
        if post_type and related_page_path:
            # Шаг 3: Переходим по ключу relatedpages к карточке родительского проекта
            parent_nodes = navigation_map.get(related_page_path)
            if not parent_nodes or not isinstance(parent_nodes, list) or len(parent_nodes) == 0:
                continue
                
            parent_card = parent_nodes[0]
            
            # Извлекаем чистый заголовок родителя
            parent_title = parent_card.get('title', '').strip()
            
            # Извлекаем канонический слаг родителя из его готового интернет-адреса URL
            parent_url = parent_card.get('url', '').strip('/')
            parent_slug = parent_url.split('/')[-1] if parent_url else ""
            
            if not parent_slug or not parent_title:
                continue

            # Формируем уникальный идентификатор будущей страницы, чтобы не перезаписывать её дважды
            page_uid = f"{post_type}::{parent_slug}"
            if page_uid in created_pages_registry:
                continue

            # Шаг 4: Разметка жёсткого диска сервера Actions
            target_folder_path = os.path.join(root_dir, post_type)
            os.makedirs(target_folder_path, exist_ok=True)
            
            # Строим точный физический путь к .md файлу страницы проекта
            target_md_file = os.path.join(target_folder_path, f"{parent_slug}.md")
            
            # Шаг 5: Сборка текстового содержимого строго по вашему паспорту контура (layout: news)
            front_matter_lines = [
                "---",
                "layout: news",
                f'title: "{parent_title}: лента проекта"',
                f'project: "{parent_slug}"',
                f'posttype: "{post_type}"',
                f"permalink: /{post_type}/{parent_slug}/",
                "---",
                "",
                f'{{% include posts-page-open.liquid project="{parent_slug}" type="{post_type}" %}}'
            ]
            file_content = "\n".join(front_matter_lines)
            
            # Физически сохраняем файл страницы проекта на диск сервера
            try:
                with open(target_md_file, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                
                relative_log_path = f"{post_type}/{parent_slug}.md"
                log_msg = f"[POST-GENERATOR] Файл: {relative_log_path} | Записана лента проекта: {parent_title}\n--- ШАПКА НА ДИСКЕ ---\n{file_content}\n----------------------------"
                print(log_msg)
                log_buffer.append(log_msg)
                
                # Добавляем страницу в реестр выполненных задач
                created_pages_registry.add(page_uid)
            except Exception as e:
                print(f"[POST-ERROR] Не удалось записать файл архива {target_md_file}: {e}")

    # Запись изолированного лога артефактов на жёсткий диск
    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[POST-SUCCESS] Изолированный лог генератора страниц успешно сохранён.")
    except Exception as e:
        print(f"[POST-ERROR] Не удалось сохранить файл лога: {e}")

if __name__ == '__main__':
    generate_project_posts_pages()
