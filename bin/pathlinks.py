#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script pathlinks.py
@about Модуль глобальной очистки путей, конвертации Wiki-ссылок и текстовых связей Obsidian.
@purpose 
@author TechLab
@version 1.0
"""

import re
import os

def process_markdown_paths(markdown_content, file_path=None):
    """
    Вычисляет имя папки статьи, чистит любые пути и конвертирует Wiki-ссылки,
    исключая ложную приставку папок для известных корней.
    """
    known_root_folders = ['faire', 'assets', 'biblio', 'diary', 'inspiration', 'projects', 'tools']

    current_folder_prefix = "/"
    if file_path:
        folder_name = os.path.basename(os.path.dirname(file_path))
        if folder_name and folder_name not in ['', '.', '..']:
            current_folder_prefix = f"/{folder_name}/"

    # А. МАССИВ ИСКЛЮЧЕНИЙ ДЛЯ ВНЕШНИХ ССЫЛОК
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
    temporary_content = re.sub(r'`{1,3}[^`\n]+?`{1,3}', code_freezer, temporary_content)

    # В. УЛЬТИМАТИВНАЯ ЧИСТКА КЛАССИЧЕСКИХ МАРКДАУН-ПУТЕЙ
    domain_pattern = r'(https?://)?github/eaststandart\.github\.io/'
    temporary_content = re.sub(domain_pattern, '/', temporary_content)

    classic_media_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))\)'
    
    def classic_path_cleaner(match):
        alt_text = match.group(1).strip()
        img_url = match.group(2).strip()
        original_url = img_url
        
        first_segment = img_url.split('/').strip()
        
        if img_url.startswith('/'):
            pass
        elif img_url.startswith('../') or img_url.startswith('./'):
            img_url = re.sub(r'^[\s./]+', '', img_url)
            if not img_url.startswith('/'):
                img_url = '/' + img_url
        elif first_segment in known_root_folders:
            img_url = '/' + img_url
        else:
            img_url = (current_folder_prefix + img_url).replace('//', '/')
            
        return f'![{alt_text}]({img_url})'

    temporary_content = re.sub(classic_media_pattern, classic_path_cleaner, temporary_content, flags=re.IGNORECASE)
    wiki_media_pattern = r'!\[\[(.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))(?:\|(.*?))?\]\]'

    def wiki_media_replacer(match):
        img_url = match.group(1).strip()
        alt_content = match.group(2).strip() if match.group(2) else ""
        
        first_segment = img_url.split('/').strip()
        
        if img_url.startswith('/'):
            pass
        elif img_url.startswith('../') or img_url.startswith('./'):
            img_url = re.sub(r'^[\s./]+', '', img_url)
            if not img_url.startswith('/'):
                img_url = '/' + img_url
        elif first_segment in known_root_folders:
            img_url = '/' + img_url
        else:
            img_url = (current_folder_prefix + img_url).replace('//', '/')
            
        return f'![{alt_content}]({img_url})'

    temporary_content = re.sub(wiki_media_pattern, wiki_media_replacer, temporary_content, flags=re.IGNORECASE)
    
    # Г. КОНВЕРТАЦИЯ ТЕКСТОВЫХ ССЫЛОК OBSIDIAN [[План|Текст]] -> Текст
    wiki_text_pattern = r'\[\[([^\]\n|]+)(?:\|([^\]\n]+))?\]\]'
    
    def wiki_text_replacer(match):
        link_target = match.group(1).strip()
        visible_text = match.group(2).strip() if match.group(2) else link_target
        return visible_text

    temporary_content = re.sub(wiki_text_pattern, wiki_text_replacer, temporary_content)
    temporary_content = temporary_content.replace('//', '/')
    
    # Д. РАЗМОРОЗКА БЛОКОВ КОДА
    for idx, original_code in enumerate(code_vault):
        temporary_content = temporary_content.replace(f'==CODE_BLOCK_{idx}==', original_code)
        
    return temporary_content
