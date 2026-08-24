#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script preprocess.py
@about Главный менеджер автоматической предобработки контента Obsidian перед сборкой Jekyll.
@purpose Автоматически находит ВСЕ markdown-файлы в репозитории и последовательно 
         пропускает их через изолированные модули (картинки, видео и т.д.).
"""

import sys
import os

# ФИКС ПУТЕЙ ДЛЯ GITHUB ACTIONS: Добавляем папку скрипта в системные пути
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from images import process_markdown_images

def process_single_file(file_path):
    """Обрабатывает один конкретный файл заметки."""
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
        
    # Шаг А: Обработка картинок через images.py
    markdown_content = process_markdown_images(markdown_content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

def main():
    # Если аргумент передан (например, при локальном тесте одной статьи)
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            process_single_file(file_path)
        return

    # ЕСЛИ АРГУМЕНТОВ НЕТ (Запуск на GitHub Actions):
    # Автоматически обходим ВЕСЬ репозиторий и находим каждый .md файл!
    # Исключаем системные папки (например, скомпилированный сайт _site или кэш)
    exclude_dirs = {'_site', '.sass-cache', '.git', '.github', 'bin'}
    
    # Начинаем поиск с корня проекта (на одну папочку выше, чем папка bin)
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    for root, dirs, files in os.walk(root_dir):
        # Удаляем исключаемые папки на лету, чтобы скрипт в них не залезал
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                process_single_file(full_path)

if __name__ == '__main__':
    main()
