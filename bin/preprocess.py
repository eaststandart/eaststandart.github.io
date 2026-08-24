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

# ФИКС ПУТЕЙ ДЛЯ GITHUB ACTIONS: Явно добавляем папку скрипта в системные пути поиска
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from images import process_markdown_images

def process_single_file(file_path):
    """Открывает, обрабатывает через модули и перезаписывает один .md файл."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
            
        # Шаг А: Обработка картинок через images.py (классы img-v, img-center и p-center)
        markdown_content = process_markdown_images(markdown_content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"[SUCCESS] Обработан файл: {file_path}")
    except Exception as e:
        print(f"[ERROR] Не удалось обработать файл {file_path}: {e}")

def main():
    # ЛОГИКА АРГУМЕНТОВ: Если передан аргумент (локальный тест конкретной статьи)
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            process_single_file(file_path)
        else:
            print(f"[ERROR] Указанный файл не найден: {file_path}")
        return

    # ЕСЛИ АРГУМЕНТОВ НЕТ (Автоматический запуск на сервере GitHub Actions):
    print("[PREPROCESS] Аргументы не переданы. Запускаю полный обход репозитория...")
    
    # Начинаем сканирование с корня проекта (на уровень выше папки bin)
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    # Папки, в которые скрипту заходить категорически запрещено
    exclude_dirs = {'_site', '.sass-cache', '.git', '.github', 'bin'}
    
    md_count = 0
    for root, dirs, files in os.walk(root_dir):
        # Вырезаем системные папки на лету
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                process_single_file(full_path)
                md_count += 1
                
    print(f"[PREPROCESS] Полный обход завершен. Всего обработано файлов: {md_count}")

if __name__ == '__main__':
    main()
