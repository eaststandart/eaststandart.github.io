#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script preprocess.py
@about Главный менеджер автоматической предобработки контента Obsidian перед сборкой Jekyll.
@purpose Запускает СКВOЗНОЙ ТОЧЕЧНЫЙ сейф исключений с наглядным логированием.
         Строго восстановлены оригинальные имена функций и все этапы конвейера.
@author TechLab
@version 2.4
"""

import sys
import os
import re

# Добавляем папку скрипта в системные пути поиска
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# СТРОГО ОРИГИНАЛЬНЫЕ ИМЕНА ИМПОРТА (Без изменений)
from pathlinks import process_markdown_paths
from fig_landscape import process_single_figure_landscape
from videos import process_markdown_videos
from images import process_markdown_images

def global_freeze_content(markdown_content, file_rel_path):
    """
    Сканирует кодовые блоки и любые комментарии, точечно замораживая только те элементы,
    внутри которых обнаружен маркер fig или медиа-расширения.
    """
    global_vault = []
    
    def freezer(match, block_type):
        raw_text = match.group(0)
        
        # Строгий точечный фильтр для всех типов исключений
        has_fig = 'fig' in raw_text.lower()
        has_media = re.search(r'\.(webp|jpg|jpeg|png|gif|svg|webm|mp4)\b', raw_text, re.IGNORECASE)
        
        if not (has_fig or has_media):
            return raw_text

        global_vault.append(raw_text)
        
        preview = raw_text.replace('\n', ' ')
        if len(preview) > 70:
            preview = preview[:67] + "..."
            
        print(f"  📦 [GLOBAL-FREEZE-LOG] Изолирован {block_type}: `{preview}` | Файл: {file_rel_path}")
        return f'==GLOBAL_VAULT_BLOCK_{len(global_vault)-1}=='

    # Последовательная точечная заморозка
    temporary_content = re.sub(r'{%\s*comment\s*%}[\s\S]*?{%\s*endcomment\s*%}', lambda m: freezer(m, "Liquid-коммент  "), markdown_content)
    temporary_content = re.sub(r'<!--[\s\S]*?-->', lambda m: freezer(m, "HTML-коммент    "), temporary_content)
    temporary_content = re.sub(r'```[\s\S]*?```', lambda m: freezer(m, "блок кода (multi)"), temporary_content)
    temporary_content = re.sub(r'`{1,3}[^`\n]+?`{1,3}', lambda m: freezer(m, "строчный код    "), temporary_content)

    return temporary_content, global_vault

def global_unfreeze_content(markdown_content, global_vault, file_rel_path):
    """Возвращает все изолированные точечные блоки из глобального сейфа на свои места."""
    temporary_content = markdown_content
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
    """Открывает, пропускает через точечный сейф и последовательно обрабатывает через модули один .md файл."""
    file_rel_path = os.path.relpath(file_path, root_dir)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
            
        markdown_content, global_vault = global_freeze_content(markdown_content, file_rel_path)
            
        if global_vault:
            print(f"\n[PREPROCESS] >>> Начало обработки файла: {file_rel_path}")
            
        # СТРОГО ОРИГИНАЛЬНАЯ НАТИВНАЯ ЦЕПОЧКА ВЫЗOВОВ (Без изменений и комментариев)
        markdown_content = process_markdown_paths(markdown_content, file_path)
        markdown_content = process_single_figure_landscape(markdown_content)
        #markdown_content = process_markdown_videos(markdown_content)
        #markdown_content = process_markdown_images(markdown_content)
        
        if global_vault:
            markdown_content = global_unfreeze_content(markdown_content, global_vault, file_rel_path)
            print(f"[PREPROCESS] Успешно восстановлено блоков из сейфа: {len(global_vault)}")
            print(f"[SUCCESS] Файл полностью сохранен на диск: {file_rel_path}")
            
    except Exception as e:
        print(f"[ERROR] Не удалось обработать файл {file_rel_path}: {e}")

def main():
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    if len(sys.argv) > 1:
        file_path = sys.argv
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
