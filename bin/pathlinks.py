#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script pathlinks.py
@about Модуль глобальной очистки путей и предварительной конвертации Wiki-ссылок для Jekyll.
@purpose v2.0 🚀 Находит упоминания домена github, зачищает относительные переходы (../),
         и на лету пересобирает любые Wiki-ссылки Obsidian ![[...]] в классический Markdown,
         приводя все возможные варианты написания к единому абсолютному стандарту /faire/...
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
    
    # 2. Глобальная чистка относительных путей маркдауна (убираем двоеточия ../ в путях)
    # Ищет конструкции вида (../faire/...) за пределами скобок и внутри них
    cleaned_content = re.sub(re.escape('../faire/'), '/faire/', cleaned_content)
    
    # Регулярный паттерн для Wiki-ссылок Obsidian
    # Ловит: ![[путь.webp]] или ![[путь.jpg|{параметры}]]
    wiki_pattern = r'!\[\[(.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))(?:\|(.*?))?\]\]'

    # 3. Функция-заменитель для пересборки Wiki-ссылок в классический вид
    def wiki_replacer(match):
        img_url = match.group(1).strip()
        alt_content = match.group(2).strip() if match.group(2) else ""
        
        # Гарантируем, что путь начинается с одиночного абсолютного слэша
        if not img_url.startswith('/'):
            img_url = '/' + img_url
            
        # Возвращаем стандартный классический маркдаун для следующего этапа
        return f'![{alt_content}]({img_url})'

    # Запускаем конвертацию всех Wiki-ссылок в тексте
    cleaned_content = re.sub(wiki_pattern, wiki_replacer, cleaned_content, flags=re.IGNORECASE)
    
    # 4. Ваша родная страховка от случайных двойных слэшей
    cleaned_content = cleaned_content.replace('//', '/')
    
    return cleaned_content
