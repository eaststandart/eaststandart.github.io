#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script pathlinks.py
@about Модуль глобальной очистки путей и предварительной конвертации Wiki-ссылок для Jekyll.
@purpose Зачищает относительные переходы (../), вырезает домены гитхаба 
         и пересобирает любые Wiki-ссылки Obsidian ![[...]] в классический Markdown.
@version 2.0
"""

import re

def process_markdown_paths(markdown_content):
    """
    Вырезает домены гитхаба, чистит относительные двоеточия и конвертирует Wiki-ссылки.
    """
    # 1. Ваша родная регулярка для очистки доменов гитхаба
    domain_pattern = r'(https?://)?github/eaststandart\.github\.io/'
    cleaned_content = re.sub(domain_pattern, '/', markdown_content)
    
    # 2. Глобальная чистка относительных путей маркдауна
    cleaned_content = re.sub(re.escape('../faire/'), '/faire/', cleaned_content)
    
    # 3. Регулярный паттерн для Wiki-ссылок Obsidian (картинки и видео)
    wiki_pattern = r'!\[\[(.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))(?:\|(.*?))?\]\]'
    
    def wiki_replacer(match):
        img_url = match.group(1).strip()
        alt_content = match.group(2).strip() if match.group(2) else ""
        
        # Гарантируем, что путь начинается с одиночного абсолютного слэша
        if not img_url.startswith('/'):
            img_url = '/' + img_url
            
        # Возвращаем стандартный классический маркдаун для следующих скриптов
        return f'![{alt_content}]({img_url})'

    # Запускаем конвертацию всех Wiki-ссылок в тексте заметки
    cleaned_content = re.sub(wiki_pattern, wiki_replacer, cleaned_content, flags=re.IGNORECASE)
    
    # 4. Ваша родная страховка от случайных двойных слэшей
    cleaned_content = cleaned_content.replace('//', '/')
    
    return cleaned_content
