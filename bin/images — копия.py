#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll с поддержкой JS ленивой загрузки.
@purpose Автоматически разделяет одиночки и плотные группы (галереи), написанные в Obsidian столбцом.
         Полностью изолирует классы форм img-row-landscape и img-row-portrait внутри рядов.
         Внедряет прозрачный 1x1 GIF в src для уничтожения системной рамки Chrome.
         Автоматически рассчитывает безопасный коридор max-width и min-width для подписи figcaption.
@author TechLab
@version 4.5
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки всех форматов и превращает их в HTML-блоки с БЭМ-классами v4.5.
    Разделение одиночек и групп происходит на основе анализа пустых строк (\n\n).
    """
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    # 🔥 ШАГ v4.5: Разбираем контент блоками (абзацами) между пустыми строками!
    blocks = markdown_content.split('\n\n')
    processed_blocks = []

    for block in blocks:
        # Находим все картинки внутри текущего плотного блока контента
        matches = list(re.finditer(img_pattern, block, flags=re.IGNORECASE))
        
        if not matches:
            processed_blocks.append(block)
            continue
            
        # Если картинок в блоке больше одной — это ГРУППА (ряд), иначе — ОДИНОЧКА!
        is_row_mode = len(matches) > 1
        current_block = block
        
        for match in matches:
            raw_match = match.group(0)
            alt_content = match.group(1).strip()
            img_url = match.group(2).strip()
            
            # Очистка обсидиановских хвостов размеров
            alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
            
            if not alt_content:
                # Если подпись пустая, вешаем базовый горизонтальный класс одиночки или ряда
                final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                img_html = f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                current_block = current_block.replace(raw_match, img_html, 1)
                continue
                
            parts = [p.strip() for p in alt_content.split('|') if p.strip()]
            
            if not parts:
                final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                img_html = f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                current_block = current_block.replace(raw_match, img_html, 1)
                continue
                
            classes = []
            custom_attrs = []
            is_centered = False
            custom_width = None # Запоминаем ширину для безопасного коридора подписи
            
            # --- РАЗБОР СЛУЖЕБНЫХ КЛЮЧЕЙ (Слева направо) ---
            if parts[0].lower() == 'fig':
                classes.append('img-fig')
                is_centered = True
                parts.pop(0)
                
                # ❄️ ЗАМОРОЖЕНО: Блок fig работает строго по вашей старой схеме
                if parts and parts[0].lower() == 'v':
                    classes.append('img-v')
                    parts.pop(0)
                    
                elif parts and re.match(r'^\d+[xх]\d+$', parts[0], re.IGNORECASE):
                    classes.append('img-single-custom')
                    dimensions = re.split(r'[xх]', parts[0], flags=re.IGNORECASE)
                    custom_width, height = dimensions[0], dimensions[1]
                    
                    custom_attrs.append(f'width="{custom_width}"')
                    custom_attrs.append(f'height="{height}"')
                    custom_attrs.append(f'style="aspect-ratio: {custom_width} / {height} !important;"')
                    parts.pop(0)
                
            # 🔥 ВАЖНО: Разделение классов форм для текстовых картинок (Сингл vs Ряд)
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
                
            # Если специфичные классы формы не назначены, вешаем дефолтные горизонтальные
            if not classes:
                horiz_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                classes.append(horiz_class)
                
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
           
            # Заменяем текущий маркдаун-шаблон на готовый HTML-код
            current_block = current_block.replace(raw_match, img_html, 1)
            
        processed_blocks.append(current_block)
        
    article_html = '\n\n'.join(processed_blocks)
    
    # Наша оригинальная финальная группировка строк figure-img блоков
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
