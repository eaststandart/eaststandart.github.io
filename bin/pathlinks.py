#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module pathlinks
@about Модуль глобальной очистки путей, конвертации Wiki-ссылок и текстовых связей Obsidian.
@purpose Автоматически нормализует маркдаун-пути контента, делая их абсолютными от корня сайта.
         Полностью очищен от избыточных локальных сейфов кода, но сохраняет массив исключений.
@author TechLab
@version 1.6-final
"""

import re
import os

def process_markdown_paths(markdown_content, file_path=None):
    """
    Вычисляет имя папки статьи, чистит любые пути и конвертирует Wiki-ссылки,
    исключая ложную приставку папок для известных корней и внешних ресурсов.
    """
    # 🌟 Утвержденный список глобальных корневых разделов и папок медиа-ресурсов сайта
    known_root_folders = ['faire', 'assets', 'biblio', 'diary', 'inspiration', 'projects', 'tools']

    current_folder_prefix = "/"
    if file_path:
        folder_name = os.path.basename(os.path.dirname(file_path))
        if folder_name and folder_name not in ['', '.', '..']:
            current_folder_prefix = f"/{folder_name}/"

    # А. МАССИВ ИСКЛЮЧЕНИЙ ДЛЯ ВНЕШНИХ ССЫЛОК (Возвращен на место!)
    ignored_patterns = [
        r'https?://',            
        r'mailto:',              
        r'telegram\.org',        
    ]

    # Б. УЛЬТИМАТИВНАЯ ЧИСТКА КЛАССИЧЕСКИХ МАРКДАУН-ПУТЕЙ
    domain_pattern = r'(?<!https://)(?<!http://)github/eaststandart\.github\.io/'

    temporary_content = re.sub(domain_pattern, '/', markdown_content)

    classic_media_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))\)'
    
    def classic_path_cleaner(match):
        alt_text = match.group(1).strip()
        img_url = match.group(2).strip()
        original_url = img_url
        
        # Проверяем, не является ли ссылка внешней интернет-ссылкой из массива исключений
        if any(re.search(pat, img_url, re.IGNORECASE) for pat in ignored_patterns):
            return match.group(0)
        
        # Вычисляем первое слово в пути (имя корневой папки ссылки)
        first_segment = img_url.split('/')[0].strip()
        
        # 1. Если путь изначально абсолютный — не трогаем
        if img_url.startswith('/'):
            pass
        # 2. Если путь относительный с двоеточиями (../faire/) — делаем абсолютным от корня
        elif img_url.startswith('../') or img_url.startswith('./'):
            img_url = re.sub(r'^[\s./]+', '', img_url)
            if not img_url.startswith('/'):
                img_url = '/' + img_url
        # 3. Если путь начинается с известной контентной папки — просто ставим слэш /
        elif first_segment in known_root_folders:
            img_url = '/' + img_url
        # 4. Во всех остальных случаях (локальные папки статей) — дописываем префикс папки статьи
        else:
            img_url = (current_folder_prefix + img_url).replace('//', '/')

        if original_url != img_url:
            print(f"[PATHLINKS-LOG] Путь изменен: {original_url} ➡️ {img_url}")
            
        return f'![{alt_text}]({img_url})'

    temporary_content = re.sub(classic_media_pattern, classic_path_cleaner, temporary_content, flags=re.IGNORECASE)
    wiki_media_pattern = r'!\[\[(.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))(?:\|(.*?))?\]\]'

    # Функция-заменитель для пересборки медиа-ссылок Wiki в классический вид
    def wiki_media_replacer(match):
        img_url = match.group(1).strip()
        alt_content = match.group(2).strip() if match.group(2) else ""
        original_url = img_url
        
        # Проверяем внешние ссылки
        if any(re.search(pat, img_url, re.IGNORECASE) for pat in ignored_patterns):
            return match.group(0)
        
        # Вычисляем первое слово в пути (имя корневой папки ссылки)
        first_segment = img_url.split('/')[0].strip()
        
        # 1. Если путь изначально абсолютный
        if img_url.startswith('/'):
            pass
        # 2. Если путь относительный с двоеточиями (../faire/)
        elif img_url.startswith('../') or img_url.startswith('./'):
            img_url = re.sub(r'^[\s./]+', '', img_url)
            if not img_url.startswith('/'):
                img_url = '/' + img_url
        # 3. Если Wiki-путь начинается с известной контентной папки — просто ставим слэш /
        elif first_segment in known_root_folders:
            img_url = '/' + img_url
        # 4. Во всех остальных случаях — дописываем префикс текущей папки статьи
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

    # Страховка от случайных двойных слэшей
    temporary_content = re.sub(r'(?<!http:)(?<!https:)(?<!:)\/\/+', '/', temporary_content)
        
    return temporary_content