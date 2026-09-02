#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script pathlinks.py
@about Модуль глобальной очистки путей, конвертации Wiki-ссылок и текстовых связей Obsidian.
@purpose v3.3 🚀 АВТОПИЛОТ ПАПОК: Скрипт сам определяет, в какой папке лежит статья (как Jekyll),
         автоматически дописывает её к относительным путям картинок и выдаёт подробный лог в GitHub Actions.
@author TechLab
@version 3.3 (Часть 1)
"""

import re
import os

def process_markdown_paths(markdown_content, file_path=None):
    """
    Вычисляет имя текущей папки статьи, чистит пути и конвертирует Wiki-ссылки,
    выдавая подробные логи работы в консоль сборки.
    """
    # 🌟 АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ ПАПКИ (Как в Jekyll!)
    current_folder_prefix = "/"
    if file_path:
        # Извлекаем имя папки, в которой физически лежит обрабатываемый .md файл
        folder_name = os.path.basename(os.path.dirname(file_path))
        # Исключаем корень репозитория, берем только вложенные папки (например, 'test' или 'faire')
        if folder_name and folder_name not in ['', '.', '..']:
            current_folder_prefix = f"/{folder_name}/"

    # А. МАССИВ ИСКЛЮЧЕНИЙ
    ignored_patterns = [
        r'https?://',            
        r'mailto:',              
        r'telegram\.org',        
    ]

    # Б. ЗАМОРОЗКА БЛОКОВ КОДА (Железный сейф)
    code_vault = []
    
    def code_freezer(match):
        code_vault.append(match.group(0))
        return f'==CODE_BLOCK_{len(code_vault)-1}=='

    temporary_content = re.sub(r'```[\s\S]*?```', code_freezer, markdown_content)
    temporary_content = re.sub(r'`[\s\S]*?`', code_freezer, temporary_content)

    # В. УМНАЯ ЧИСТКА КЛАССИЧЕСКИХ МАРКДАУН-ПУТЕЙ С ЛОГИРОВАНИЕМ
    domain_pattern = r'(https?://)?github/eaststandart\.github\.io/'
    temporary_content = re.sub(domain_pattern, '/', temporary_content)

    classic_media_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))\)'
    
    def classic_path_cleaner(match):
        alt_text = match.group(1).strip()
        img_url = match.group(2).strip()
        original_url = img_url
        
        # Если путь изначально абсолютный (начинается с / или /faire/) — оставляем как есть
        if img_url.startswith('/'):
            pass
        # Если путь относительный с двоеточиями (../faire/) — сносим двоеточия, делая абсолютным корня
        elif img_url.startswith('../') or img_url.startswith('./'):
            img_url = re.sub(r'^[\s./]+', '', img_url)
            if not img_url.startswith('/'):
                img_url = '/' + img_url
        # 🔥 ЕСЛИ ПУТЬ СЫРОЙ ОТНОСИТЕЛЬНЫЙ (folder/img.webp) — РАБОТАЕМ КАК JEKYLL!
        else:
            img_url = (current_folder_prefix + img_url).replace('//', '/')

        # 📄 ЛОГИРОВАНИЕ ДЛЯ GITHUB ACTIONS: Выводим красивую строчку трансформации в консоль
        if original_url != img_url:
            print(f"[PATHLINKS-LOG] Путь изменен: {original_url} ➡️ {img_url}")
            
        return f'![{alt_text}]({img_url})'

    temporary_content = re.sub(classic_media_pattern, classic_path_cleaner, temporary_content, flags=re.IGNORECASE)
    wiki_media_pattern = r'!\[\[(.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))(?:\|(.*?))?\]\]'

    # 3. Функция-заменитель для пересборки медиа-ссылок Wiki в классический вид
    def wiki_media_replacer(match):
        img_url = match.group(1).strip()
        alt_content = match.group(2).strip() if match.group(2) else ""
        original_url = img_url
        
        # Если путь изначально абсолютный
        if img_url.startswith('/'):
            pass
        # Если путь относительный с двоеточиями (../faire/)
        elif img_url.startswith('../') or img_url.startswith('./'):
            img_url = re.sub(r'^[\s./]+', '', img_url)
            if not img_url.startswith('/'):
                img_url = '/' + img_url
        # 🔥 ЕСЛИ ПУТЬ СЫРОЙ ОТНОСИТЕЛЬНЫЙ (folder/img.webp) — ДОПИСЫВАЕМ ТЕКУЩУЮ ПАПКУ СТАТЬИ
        else:
            img_url = (current_folder_prefix + img_url).replace('//', '/')
            
        # Логирование для Wiki-медиа в GitHub Actions
        if original_url != img_url:
            print(f"[PATHLINKS-LOG] Wiki-путь изменен: {original_url} ➡️ {img_url}")
            
        return f'![{alt_content}]({img_url})'

    # Запускаем конвертацию всех МЕДИА Wiki-ссылок в тексте
    temporary_content = re.sub(wiki_media_pattern, wiki_media_replacer, temporary_content, flags=re.IGNORECASE)
    
    # Г. КОНВЕРТАЦИЯ ТЕКСТОВЫХ ССЫЛОК OBSIDIAN [[План|Текст]] -> Текст
    wiki_text_pattern = r'\[\[([^\]\n|]+)(?:\|([^\]\n]+))?\]\]'
    
    def wiki_text_replacer(match):
        link_target = match.group(1).strip()
        visible_text = match.group(2).strip() if match.group(2) else link_target
        return visible_text

    # Превращаем обсидиановые текстовые связи в чистые слова контента
    temporary_content = re.sub(wiki_text_pattern, wiki_text_replacer, temporary_content)

    # Ваша родная страховка от случайных двойных слэшей
    temporary_content = temporary_content.replace('//', '/')
    
    # Д. РАЗМОРОЗКА БЛОКОВ КОДА: Возвращаем примеры из сейфа в полной целости
    for idx, original_code in enumerate(code_vault):
        temporary_content = temporary_content.replace(f'==CODE_BLOCK_{idx}==', original_code)
        
    return temporary_content
