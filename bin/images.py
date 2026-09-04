#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Монолитный объединенный модуль предобработки изображений для Obsidian -> Jekyll.
@purpose За один проход каскадно обрабатывает сначала тяжелую журнальную графику {fig},
         а затем утилизирует все базовые одиночные картинки и галереи сайта.
@author TechLab
@version 4.0-monolith
"""

import re

def process_markdown_images(markdown_content):
    """
    Каскадный построчный диспетчер обработки всей графики репозитория.
    """
    # Общие константы и паттерны для обоих подмодулей
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    lines = markdown_content.split('\n')
    processed_lines = []
    
    # =========================================================================
    # 🌅 ШАГ 1: МОДУЛЬ ТЯЖЕЛОЙ ЖУРНАЛЬНОЙ ГРАФИКИ (БЫВШИЙ img_figure.py)
    # =========================================================================
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # Фильтруем и собираем только журнальные блоки, содержащие маркер {fig
        if not line_stripped or '![{fig' not in line_stripped.lower():
            processed_lines.append(line)
            i += 1
            continue
            
        is_image = re.search(img_pattern, line_stripped)
        if not is_image:
            processed_lines.append(line)
            i += 1
            continue
            
        # Сборщик плотной группы журнальных строк (Галерея блоков)
        group_lines = []
        while i < len(lines) and lines[i].strip() and '![{fig' in lines[i].strip().lower() and re.search(img_pattern, lines[i].strip()):
            group_lines.append(lines[i].strip())
            i += 1
            
        is_row_mode = len(group_lines) > 1
        div_class = "img-row-figure" if is_row_mode else "img-single-figure"
        img_prefix = "img-row-figure-" if is_row_mode else "img-single-figure-"
        
        figures_html = []
        
        for group_line in group_lines:
            match = re.search(img_pattern, group_line)
            alt_content = match.group(1).strip()
            img_url = match.group(2).strip()
            
            print(f"\n[FIG-CONVERT] ВХОД ({'РЯД' if is_row_mode else 'ОДИНОЧКА'}): {group_line}")
            
            # Очистка обсидианового хвоста ширины
            alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
            raw_parts = [p.strip() for p in alt_content.split('|') if p.strip()]
            
            geometry_class = "landscape"
            custom_attrs = ""
            
            if raw_parts and raw_parts[0].strip('{} ').lower() == 'fig':
                raw_parts.pop(0)
                
            if raw_parts and raw_parts[0].strip('{} ').lower() == 'v':
                geometry_class = "portrait"
                raw_parts.pop(0)
                
            elif raw_parts and re.match(r'^\d+[xх]\d+$', raw_parts[0].strip('{} '), re.IGNORECASE):
                size_clean = raw_parts[0].strip('{} ')
                size_match = re.split(r'[xх]', size_clean, flags=re.IGNORECASE)
                width, height = int(size_match[0]), int(size_match[1])
                
                if width > height:
                    geometry_class = "custom-landscape"
                else:
                    geometry_class = "custom-portrait"
                    
                custom_attrs = f' width="{width}" height="{height}" style="aspect-ratio: {width} / {height} !important;"'
                raw_parts.pop(0)
                
            target_img_class = f"{img_prefix}{geometry_class}"
            
            clean_alt = ""
            clean_caption = ""
            for part in raw_parts:
                if '}' in part:
                    clean_alt = part.strip('{} ')
                else:
                    clean_caption = part.strip('{} ')
                    
            if not clean_alt and clean_caption:
                clean_alt = clean_caption
                
            figcaption_html = ""
            if clean_caption:
                figcaption_html = f'\n        <figcaption class="img-figcaption">{clean_caption}</figcaption>'
                
            item_html = (
                f'    <figure class="img-figure">\n'
                f'        <img class="{target_img_class}"{custom_attrs} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
                f'{figcaption_html}\n'
                f'    </figure>'
            )
            figures_html.append(item_html)
            
        figures_joined = "\n".join(figures_html)
        html_output = f'<div class="{div_class}">\n{figures_joined}\n</div>'
        
        print(f"[FIG-CONVERT] ВЫХОД:\n{html_output}")
        processed_lines.append(html_output)

    # =========================================================================
    # 🖼️ ШАГ 2: БАЗОВЫЙ УТИЛИЗАТОР ГРАФИКИ (БЫВШИЙ img_base.py)
    # =========================================================================
    # Пересобираем промежуточный контент после первого шага обратно в строки
    intermediate_content = '\n'.join(processed_lines)
    base_lines = intermediate_content.split('\n')
    final_processed_lines = []
    
    j = 0
    while j < len(base_lines):
        line = base_lines[j]
        line_stripped = line.strip()
        
        if not line_stripped:
            final_processed_lines.append(line)
            j += 1
            continue
            
        is_image = re.match(img_pattern, line_stripped, re.IGNORECASE)
        
        if is_image:
            # Сборщик плотной группы базовых картинок, идущих друг под другом (Галереи)
            image_group_lines = []
            while j < len(base_lines) and base_lines[j].strip() and re.match(img_pattern, base_lines[j].strip(), re.IGNORECASE):
                image_group_lines.append(base_lines[j].strip())
                j += 1
                
            is_row_mode = len(image_group_lines) > 1
            
            for group_line in image_group_lines:
                match = re.match(img_pattern, group_line, re.IGNORECASE)
                alt_content = match.group(1).strip()
                img_url = match.group(2).strip()
                
                print(f"\n[IMAGES-BASE] ВХОД: {group_line}")
                
                # Очистка обсидианового хвоста ширины
                alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
                
                if not alt_content:
                    final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                    img_html_simple = f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                    print(f"[IMAGES-BASE] ВЫХОД:\n{img_html_simple}")
                    final_processed_lines.append(img_html_simple)
                    continue
                    
                parts = [p.strip() for p in alt_content.split('|') if p.strip()]
                
                if not parts:
                    final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                    img_html_simple = f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                    print(f"[IMAGES-BASE] ВЫХОД:\n{img_html_simple}")
                    final_processed_lines.append(img_html_simple)
                    continue
                    
                classes = []
                custom_attrs = []
                
                first_key = parts[0].strip('{} ')

                # ЛЕВОСТОРОННИЙ РАЗБОР СЛУЖЕБНЫХ КЛЮЧЕЙ БАЗОВЫХ КАРТИНОК
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
                    
                # СБОРКА ОЧИЩЕННОГО SEO ALT ТЕКСТА БАЗОВОЙ КАРТИНКИ
                clean_parts = [p.strip('{} ') for p in parts if p.strip()]
                clean_alt = " | ".join(clean_parts) if clean_parts else ""
                
                class_str = f' class="{" ".join(classes)}"' if classes else ''
                attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
                
                img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
                
                print(f"[IMAGES-BASE] ВЫХОД:\n{img_html}")
                final_processed_lines.append(img_html)
                    
        else:
            final_processed_lines.append(line)
            j += 1
            
    article_html = '\n'.join(final_processed_lines)
    
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
