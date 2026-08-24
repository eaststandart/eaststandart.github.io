#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll.
@purpose Вычищает технические маркеры (v, center) из alt, вешает чистые классы 
         на <img> и переносит центрирование сразу на родительский тег <p class="p-center">.
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки и превращает их в HTML-блоки с классами.
    """
    # Регулярное выражение ловит: ![маркеры|текст](ссылка)
    pattern = r'!\[(.*?)\]\((.*?)\)'
    
    def replacer(match):
        alt_text = match.group(1).strip()
        img_url = match.group(2).strip()
        
        # Разбиваем параметры по палочке
        parts = [p.strip() for p in alt_text.split('|')]
        
        classes = []
        is_centered = False
        clean_alt_parts = []
        
        # Разбираем маркеры
        for part in parts:
            if part.lower() == 'v':
                classes.append('img-v')
            elif part.lower() == 'center':
                classes.append('img-center')
                is_centered = True
            else:
                # Если это не маркер, значит это человеческий текст для SEO
                if part:
                    clean_alt_parts.append(part)
        
        # Собираем чистый текст для alt
        clean_alt = " | ".join(clean_alt_parts)
        
        # Собираем строку классов для картинки
        class_str = f' class="{" ".join(classes)}"' if classes else ''
        
        # Генерируем финальный HTML-тег картинки
        img_html = f'<img{class_str} alt="{clean_alt}" src="{img_url}">'
        
        # Если был маркер center — сразу формируем класс у родительского абзаца!
        if is_centered:
            return f'<p class="p-center">{img_html}</p>'
        
        # Для обычной картинки отдаем чистый тег (Jekyll сам обернет его в обычный <p>)
        return img_html

    # Запускаем замену по всему тексту файла
    return re.sub(pattern, replacer, markdown_content)
