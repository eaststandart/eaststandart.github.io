#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll с поддержкой JS ленивой загрузки.
@purpose Автоматически изолирует класс img-custom и выстраивает правильный HTML-порядок атрибутов.
         Внедряет прозрачный 1x1 GIF в src для полного уничтожения системной рамки Chrome.
@author TechLab
@version 3.1
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки всех форматов и превращает их в HTML-блоки с data-src.
    """
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    lines = markdown_content.split('\n')
    processed_lines = []

    for line in lines:
        def replacer(match):
            alt_content = match.group(1).strip()
            img_url = match.group(2).strip()
            
            # Очистка обсидиановских хвостов размеров
            alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
            
            # 🔥 ИСПРАВЛЕНИЕ ЛОВУШКИ 1: Если alt пустой, сразу отдаем чистый БЭМ-класс
            if not alt_content:
                return f'<img class="img-base" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                
            parts = [p.strip() for p in alt_content.split('|') if p.strip()]
            
            if not parts:
                return f'<img class="img-base" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                
            classes = []
            custom_attrs = []
            is_centered = False
            custom_width = None # Запоминаем ширину для безопасного коридора подписи
            
            # --- РАЗБОР СЛУЖЕБНЫХ КЛЮЧЕЙ (Слева направо) ---
            if parts[0].lower() == 'fig':
                classes.append('img-fig')
                is_centered = True
                parts.pop(0)
                
                if parts and parts[0].lower() == 'v':
                    classes.append('img-v')
                    parts.pop(0)
                    
                elif parts and re.match(r'^\d+[xх]\d+$', parts[0], re.IGNORECASE):
                    classes.append('img-custom')
                    dimensions = re.split(r'[xх]', parts[0], flags=re.IGNORECASE)
                    custom_width, height = dimensions[0], dimensions[1]
                    
                    custom_attrs.append(f'width="{custom_width}"')
                    custom_attrs.append(f'height="{height}"')
                    custom_attrs.append(f'style="aspect-ratio: {custom_width} / {height} !important;"')
                    parts.pop(0)
                
            elif parts[0].lower() == 'v':
                classes.append('img-v')
                parts.pop(0)
                
            elif re.match(r'^\d+[xх]\d+$', parts[0], re.IGNORECASE):
                classes.append('img-custom')
                dimensions = re.split(r'[xх]', parts[0], flags=re.IGNORECASE)
                custom_width, height = dimensions[0], dimensions[1]
                
                custom_attrs.append(f'width="{custom_width}"')
                custom_attrs.append(f'height="{height}"')
                custom_attrs.append(f'style="aspect-ratio: {custom_width} / {height} !important;"')
                parts.pop(0)
                
            # --- 🔥 АВТОМАТИЧЕСКИЙ ФИКСАТОР БАЗОВОГО КЛАССА ---
            # Если массив классов пуст, картинка гарантированно базовая горизонтальная
            if not classes:
                classes.append('img-base')
                
            clean_alt = " | ".join(parts) if parts else ""
            
            class_str = f' class="{" ".join(classes)}"' if classes else ''
            attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
            
            img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
            
            if is_centered:
                if custom_width:
                    figcaption_html = f'<figcaption class="figcaption-img" style="max-width: {custom_width}px !important; min-width: 371px;">{clean_alt}</figcaption>' if clean_alt else ''
                else:
                    figcaption_html = f'<figcaption class="figcaption-img">{clean_alt}</figcaption>' if clean_alt else ''
                    
                return f'<figure class="figure-img">{img_html}{figcaption_html}</figure>'
           
            return img_html

        new_line = re.sub(img_pattern, replacer, line, flags=re.IGNORECASE)
        processed_lines.append(new_line)
        
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
