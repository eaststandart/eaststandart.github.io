#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll.
@purpose ОПТИМИЗИРОВАННАЯ СБОРКА v5.6: Из кода полностью удалён дублирующий узел очистки путей.
         Скрипт принимает идеально чистые абсолютные пути от pathlinks.py.
@author TechLab
@version 5.6 🚀 (Часть 1)
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки всех форматов и превращает их в HTML-блоки с data-src.
    """
    # Ваша родная, проверенная регулярка классического маркдауна
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    lines = markdown_content.split('\n')
    processed_lines = []

    for line in lines:
        def replacer(match):
            alt_content = match.group(1).strip()
            img_url = match.group(2).strip() # Путь уже идеально чистый благодаря pathlinks.py!
            
            # --- ШАГ 1: ВАШ РОДНОЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА ---
            alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
            
            if not alt_content:
                return f'<img class="img-single-landscape" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                
            # Разбиваем содержимое по вертикальной палочке
            parts = [p.strip() for p in alt_content.split('|') if p.strip()]
            
            if not parts:
                return f'<img class="img-single-landscape" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                
            classes = []
            custom_attrs = []
            is_centered = False
            
            # Извлекаем первый ключ и очищаем его от фигурных скобок Обсидиана
            first_key = parts[0].strip('{} ')
            
            # --- ШАГ 2: ВАШ СЛУЖЕБНЫЙ РАЗБОР КЛЮЧЕЙ (Слева направо) ---
            if first_key.lower() == 'fig':
                classes.append('img-fig')
                is_centered = True
                parts.pop(0)
                
                # Проверяем вложенный вертикальный ключ внутри fig
                if parts and parts[0].strip('{} ').lower() == 'v':
                    classes.append('img-v')
                    parts.pop(0)
            # Проверяем Ключ 1: Текстовая вертикалка 'v' (без fig)
            elif first_key.lower() == 'v':
                classes.append('img-single-portrait') # Наш новый изолированный класс
                parts.pop(0)
                
            # Проверяем Ключ 1: Ручной кастомный размер сторон '320x405'
            elif re.match(r'^\d+[xх]\d+$', first_key, re.IGNORECASE):
                classes.append('img-single-custom') # Наш новый изолированный класс
                dimensions = re.split(r'[xх]', first_key, flags=re.IGNORECASE)
                width, height = dimensions[0], dimensions[1]
                
                custom_attrs.append(f'width="{width}"')
                custom_attrs.append(f'height="{height}"')
                custom_attrs.append(f'style="aspect-ratio: {width} / {height} !important;"')
                parts.pop(0)
                
            # Если специфичные классы формы не назначены, вешаем дефолтные горизонтальные
            if not classes:
                classes.append('img-single-landscape')
                
            # --- ШАГ 3: СБОРКА ОЧИЩЕННОГО SEO-ТЕКСТА ALT ---
            clean_parts = [p.strip('{} ') for p in parts if p.strip()]
            clean_alt = " | ".join(clean_parts) if clean_parts else ""
            
            class_str = f' class="{" ".join(classes)}"' if classes else ''
            attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
            
            # --- ШАГ 4: СБОРКА HTML С КРИСТАЛЬНЫМ LAZY-LOAD ---
            img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
            
            # Если журнальный режим fig, упаковываем в семантическую коробку figure
            if is_centered:
                figcaption_html = f'<figcaption class="figcaption-img">{clean_alt}</figcaption>' if clean_alt else ''
                return f'<figure class="figure-img">{img_html}{figcaption_html}</figure>'
                
            return img_html

        new_line = re.sub(img_pattern, replacer, line, flags=re.IGNORECASE)
        processed_lines.append(new_line)
        
    # === ВАША РОДНАЯ СКЛЕЙКА И АВТОМАТИЧЕСКАЯ ГРУППИРОВКА РЯДОВ ДЛЯ JEKYLL ===
    article_html = '\n'.join(processed_lines)
    
    def group_rows(match):
        content = match.group(1)
        if content.count('<figure class="figure-img"') > 1:
            return f'<div class="figure-img-row">{content}</div>' 
        return f'<div class="figure-img-single">{content}</div>' 

    article_html = re.sub(
        r'((?:<figure class="figure-img">.*?</figure>[ \t]*\n?)+)',
        group_rows,
        article_html
    )
        
    return article_html
