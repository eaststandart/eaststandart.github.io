#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script preprocess.py
@about Главный менеджер автоматической предобработки контента Obsidian перед сборкой Jekyll.
@purpose Читает markdown-файлы заметок, последовательно пропускает их через изолированные
         модули (картинки, видео и т.д.) и перезаписывает результат.
"""

import sys
import os

# ФИКС ДЛЯ GITHUB ACTIONS: Автоматически находим папку, в которой лежит preprocess.py,
# и принудительно добавляем её в пути поиска, чтобы Python железно увидел соседний файл images.py
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Теперь импорт гарантированно сработает и на сервере GitHub, и у тебя на ПК
from images import process_markdown_images

def main():
    if len(sys.argv) < 2:
        print("Ошибка: Не указан путь к файлу для обработки.")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    if not os.path.isfile(file_path):
        print(f"Ошибка: Файл не найден по пути {file_path}")
        sys.exit(1)
        
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
        
    # Шаг А: Обработка картинок через изолированный модуль images.py
    markdown_content = process_markdown_images(markdown_content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == '__main__':
    main()
