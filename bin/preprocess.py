#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script preprocess.py
@about Главный менеджер автоматической предобработки контента Obsidian перед сборкой Jekyll.
@purpose Запускает сквозной глобальный сейф исключений с наглядным логированием,
         освобождая изолированные модули от избыточной локальной заморозки.
@author TechLab
@version 2.0
"""

import sys
import os
import re

# ФИКС ПУТЕЙ ДЛЯ GITHUB ACTIONS: Добавляем папку скрипта в системные пути поиска
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Импортируем все наши изолированные модули конвейера
from pathlinks import process_markdown_paths
from fig_landscape import process_single_figure_landscape
from videos import process_markdown_videos
from images import process_markdown_images

def global_freeze_content(markdown_content, file_rel_path):
    """
    Находит все блоки исключений, выводит наглядный лог с содержимым
    и заменяет их на безопасные глобальные маркеры.
    """
    global_vault = []
    
    def freezer(match, block_type):
        raw_text = match.group(0)
        global_vault.append(raw_text)
        
        # Подготавливаем наглядное превью содержимого (первые 70 символов в одну строку)
        preview = raw_text.replace('\n', ' ')
        if len(preview) > 70:
            preview = preview[:67] + "..."
            
        print(f"  📦 [GLOBAL-FREEZE-LOG] Изолирован {block_type}: `{preview}` | Файл: {file_rel_path}")
        return f'==GLOBAL_VAULT_BLOCK_{len(global_vault)-1}=='

    # 1. Многострочные блоки кода ``` ... ```
    temporary_content = re.sub(
        r'```[\s\S]*?```', 
        lambda m: freezer(m, "блок кода (multi)"), 
        markdown_content
    )
    
    # 2. Liquid-комментарии {% comment %} ... {% endcomment %}
    temporary_content = re.sub(
        r'{%\s*comment\s*%}[\s\S]*?{%\s*endcomment\s*%}', 
        lambda m: freezer(m, "Liquid-коммент  "), 
        temporary_content
    )
    
    # 3. HTML-комментарии <!-- ... -->
    temporary_content = re.sub(
        r'<!--[\s\S]*?-->', 
        lambda m: freezer(m, "HTML-коммент    "), 
        temporary_content
    )
    
    # 4. Строчный код ` ... ` (от 1 до 3 бэктиков)
    temporary_content = re.sub(
        r'`{1,3}[^`\n]+?`{1,3}', 
        lambda m: freezer(m, "строчный код    "), 
        temporary_content
    )

    return temporary_content, global_vault

def global_unfreeze_content(markdown_content, global_vault, file_rel_path):
    """
    Возвращает все изолированные блоки из глобального сейфа на свои места,
    выводя прозрачный отчет о восстановлении.
    """
    temporary_content = markdown_content
    
    # Разворачиваем в обратном порядке, чтобы избежать смещения индексов
    for idx in reversed(range(len(global_vault))):
        raw_text = global_vault[idx]
        marker = f'==GLOBAL_VAULT_BLOCK_{idx}=='
        
        if marker in temporary_content:
            preview = raw_text.replace('\n', ' ')
            if len(preview) > 70:
                preview = preview[:67] + "..."
                
            print(f"  🔓 [GLOBAL-UNFREEZE-LOG] Восстановлен {marker}: `{preview}` | Файл: {file_rel_path}")
            temporary_content = temporary_content.replace(marker, raw_text)
            
    return temporary_content

def process_single_file(file_path, root_dir):
    """Открывает, пропускает через сквозной сейф и последовательно обрабатывает через модули один .md файл."""
    file_rel_path = os.path.relpath(file_path, root_dir)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
            
        print(f"\n[PREPROCESS] >>> Начало обработки файла: {file_rel_path}")
            
        # ШАГ 0: АКТИВАЦИЯ СКВОЗНОГО ГЛОБАЛЬНОГО СЕЙФА
        markdown_content, global_vault = global_freeze_content(markdown_content, file_rel_path)
            
        # ЭТАП 1: Глобальная очистка путей домена Obsidian через pathlinks.py
        markdown_content = process_markdown_paths(markdown_content, file_path)
        
        # ЭТАП 1.5: Обработка одиночных журнальных блоков через fig_landscape.py
        markdown_content = process_single_figure_landscape(markdown_content)
            
        # ЭТАП 2: Конвертация видео-ссылок (.webm/.mp4) в нативные флекс-ряды через videos.py
        markdown_content = process_markdown_videos(markdown_content)
            
        # ЭТАП 3: Обработка геометрии оставшихся картинок через images.py
        markdown_content = process_markdown_images(markdown_content)
        
        # ШАГ 4: ДЕАКТИВАЦИЯ СКВОЗНОГО ГЛОБАЛЬНОГО СЕЙФА
        if global_vault:
            markdown_content = global_unfreeze_content(markdown_content, global_vault, file_rel_path)
            print(f"[PREPROCESS] Успешно синхронизировано блоков в сейфе: {len(global_vault)}")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"[SUCCESS] Файл полностью сохранен на диск: {file_rel_path}")
    except Exception as e:
        print(f"[ERROR] Не удалось обработать файл {file_rel_path}: {e}")

def main():
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            process_single_file(file_path, root_dir)
        else:
            print(f"[ERROR] Указанный файл не найден: {file_path}")
        return

    print("[PREPROCESS] Аргументы не переданы. Запускаю полный обход репозитория...")
    exclude_dirs = {'_site', '.sass-cache', '.git', '.github', 'bin'}
    
    md_count = 0
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                process_single_file(full_path, root_dir)
                md_count += 1
                
    print(f"\n[PREPROCESS] Полный обход завершен. Всего обработано файлов: {md_count}")

if __name__ == '__main__':
    main()
