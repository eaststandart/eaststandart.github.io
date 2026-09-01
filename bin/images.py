#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll с поддержкой JS ленивой загрузки.
@purpose Автоматически разделяет одиночки и ряды, присваивая БЭМ-классы стандарта v4.0.
         Внедряет прозрачный 1x1 GIF в src для уничтожения системной рамки Chrome.
@author TechLab
@version 4.0
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки всех форматов и превращает их в HTML-блоки с БЭМ-классами v4.0.
    """
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    lines = markdown_content.split('\n')
    processed_lines = []

    for line in lines:
        # Находим все совпадения картинок в текущей строке абзаца
        matches = list(re.finditer(img_pattern, line, flags=re.IGNORECASE))
        
        if not matches:
            processed_lines.append(line)
            continue
            
        # Определяем режим размещения: одиночка или групповой ряд
        is_row_mode = len(matches) > 1
        
        # Будем заменять картинки по очереди слева направо
        current_line = line
        
        for match in matches:
            raw_match = match.group(0)
            alt_content = match.group(1).strip()
            img_url = match.group(2).strip()
            
            # Очистка обсидиановских хвостов размеров
            alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
            
            classes = []
            custom_attrs = []
            is_centered = False
            custom_width = None
            
            # Разбираем внутренние ключи (v, fig, размеры)
            parts = [p.strip() for p in alt_content.split('|') if p.strip()]
            
            if parts:
                if parts[0].lower() == 'fig':
                    classes.append('img-fig')
                    is_centered = True
                    parts.pop(0)
                    
                    if parts and parts[0].lower() == 'v':
                        classes.append('img-row-portrait' if is_row_mode else 'img-single-portrait')
                        parts.pop(0)
                    elif parts and re.match(r'^\d+[xх]\d+$', parts[0], re.IGNORECASE):
                        classes.append('img-single-custom') # Кастомные всегда изолированы
                        dimensions = re.split(r'[xх]', parts[0], flags=re.IGNORECASE)
                        custom_width, height = dimensions[0], dimensions[1]
                        custom_attrs.append(f'width="{custom_width}"')
                        custom_attrs.append(f'height="{height}"')
                        custom_attrs.append(f'style="aspect-ratio: {custom_width} / {height} !important;"')
                        parts.pop(0)
                        
                elif parts[0].lower() == 'v':
                    classes.append('img-row-portrait' if is_row_mode else 'img-single-portrait')
                    parts.pop(0)
                    
                elif re.match(r'^\d+[xх]\d+$', parts[0], re.IGNORECASE):
                    classes.append('img-single-custom')
                    dimensions = re.split(r'[xх]', parts[0], flags=re.IGNORECASE)
                    custom_width, height = dimensions[0], dimensions[1]
                    custom_attrs.append(f'width="{custom_width}"')
                    custom_attrs.append(f'height="{height}"')
                    custom_attrs.append(f'style="aspect-ratio: {custom_width} / {height} !important;"')
                    parts.pop(0)

            # Если после всех проверок специфичный класс формы не назначен
            if not any(c in classes for c in ['img-single-portrait', 'img-row-portrait', 'img-single-custom']):
                if 'img-fig' not in classes:
                    classes.append('img-row-landscape' if is_row_mode else 'img-single-landscape')
            
            clean_alt = " | ".join(parts) if parts else ""
            class_str = f' class="{" ".join(classes)}"' if classes else ''
            attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
            
            img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
            
            if is_centered:
                if custom_width:
                    figcaption_html = f'<figcaption class="figcaption-img" style="max-width: {custom_width}px !important; min-width: 371px;">{clean_alt}</figcaption>' if clean_alt else ''
                else:
                    figcaption_html = f'<figcaption class="figcaption-img">{clean_alt}</figcaption>' if clean_alt else ''
                img_html = f'<figure class="figure-img">{img_html}{figcaption_html}</figure>'
            
            # Заменяем маркдаун-шаблон на готовый HTML-код
            current_line = current_line.replace(raw_match, img_html, 1)
            
        processed_lines.append(current_line)
        
    article_html = '\n'.join(processed_lines)
    return article_html
