#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module img_base
@about Модуль предобработки базовых изображений для Obsidian -> Jekyll с поддержкой JS ленивой загрузки.
@purpose Обрабатывает стандартные одиночные картинки и галереи в теге <p>.
@author TechLab
@version 1.0-clean
"""

import re

def process_markdown_images_base(markdown_content):
    """
    Ищет стандартные маркдаун-картинки и собирает их в HTML-блоки с ленивой загрузкой.
    Полностью очищен от журнальной логики {fig}.
    """
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    lines = markdown_content.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        if not line_stripped:
            processed_lines.append(line)
            i += 1
            continue
            
        is_image = re.match(img_pattern, line_stripped, re.IGNORECASE)
        
        if is_image:
            # Запускаем сборщик плотной группы картинок, идущих друг под другом
            image_group_lines = []
            
            while i < len(lines) and lines[i].strip() and re.match(img_pattern, lines[i].strip(), re.IGNORECASE):
                image_group_lines.append(lines[i].strip())
                i += 1
                
            is_row_mode = len(image_group_lines) > 1
            
            for group_line in image_group_lines:
                match = re.match(img_pattern, group_line, re.IGNORECASE)
                alt_content = match.group(1).strip()
                img_url = match.group(2).strip()
                
                print(f"\n[IMAGES-BASE] ВХОД: {group_line}")
                
                # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА ---
                alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
                
                if not alt_content:
                    final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                    img_html_simple = f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                    print(f"[IMAGES-BASE] ВЫХОД:\n{img_html_simple}")
                    processed_lines.append(img_html_simple)
                    continue
                    
                parts = [p.strip() for p in alt_content.split('|') if p.strip()]
                
                if not parts:
                    final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                    img_html_simple = f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                    print(f"[IMAGES-BASE] ВЫХОД:\n{img_html_simple}")
                    processed_lines.append(img_html_simple)
                    continue
                    
                classes = []
                custom_attrs = []
                
                first_key = parts[0].strip('{} ')

                # --- ШАГ 2: ЛЕВОСТОРОННИЙ РАЗБОР СЛУЖЕБНЫХ КЛЮЧЕЙ (БЕЗ FIG) ---
                if first_key.lower() == 'v':
                    classes.append('img-row-portrait' if is_row_mode else 'img-single-portrait')
                    parts.pop(0)
                    
                elif re.match(r'^\d+[xх]\d+$', first_key, re.IGNORECASE):
                    dimensions = re.split(r'[xх]', first_key, flags=re.IGNORECASE)
                    width, height = dimensions[0], dimensions[1]
                    
                    if int(width) > int(height):
                        classes.append('img-single-custom-landscape')
                    else:
                        classes.append('img-single-custom-portrait')
                    
                    custom_attrs.append(f'width="{width}"')
                    custom_attrs.append(f'height="{height}"')
                    custom_attrs.append(f'style="aspect-ratio: {width} / {height} !important;"')
                    parts.pop(0)
                    
                if not classes:
                    classes.append('img-row-landscape' if is_row_mode else 'img-single-landscape')
                    
                # --- ШАГ 3: СБОРКА ОЧИЩЕННОГО SEO-ТЕКСТА ALT ---
                clean_parts = [p.strip('{} ') for p in parts if p.strip()]
                clean_alt = " | ".join(clean_parts) if clean_parts else ""
                
                class_str = f' class="{" ".join(classes)}"' if classes else ''
                attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
                
                # --- ШАГ 4: СБОРКА ИТОГОВОГО HTML С ЛЕНИВОЙ ЗАГРУЗКОЙ ---
                img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
                
                print(f"[IMAGES-BASE] ВЫХОД:\n{img_html}")
                processed_lines.append(img_html)
                    
        else:
            processed_lines.append(line)
            i += 1
            
    article_html = '\n'.join(processed_lines)
    
    # === ВАША РОДНАЯ СКЛЕЙКА И АВТОМАТИЧЕСКАЯ ГРУППИРОВКА РЯДОВ ДЛЯ JEKYLL ===
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