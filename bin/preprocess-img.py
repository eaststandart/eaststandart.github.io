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

# Импортируем функцию обработки картинок из нашего нового модуля images.py
from images import process_markdown_images

def main():
    # Проверяем, передан ли путь к файлу в качестве аргумента скрипту
    if len(sys.argv) < 2:
        print("Ошибка: Не указан путь к файлу для обработки.")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    # Защитная проверка: существует ли файл физически
    if not os.path.isfile(file_path):
        print(f"Ошибка: Файл не найден по пути {file_path}")
        sys.exit(1)
        
    # 1. ЧИТАЕМ ИСХОДНЫЙ КОНТЕНТ ЗАМЕТКИ
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
        
    # 2. ПОСЛЕДОВАТЕЛЬНО ПРОПУСКАЕМ ЧЕРЕЗ МОДУЛИ-МОДИФИКАТОРЫ
    
    # Шаг А: Обработка картинок (убираем alt-мусор, вешаем классы .img-v, .img-center и .p-center)
    markdown_content = process_markdown_images(markdown_content)
    
    # Шаг Б: Сюда мы в один клик добавим модуль обработки видео-ссылок, когда напишем его:
    # from videos import process_videos
    # markdown_content = process_videos(markdown_content)
    
    # 3. ЗАПИСЫВАЕМ ОЧИЩЕННЫЙ И ПРЕОБРАЗОВАННЫЙ ТЕКСТ ОБРАТНО В ФАЙЛ
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == '__main__':
    main()
