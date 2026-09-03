#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script fig_landscape.py
@about Построчный стабильный модуль для обработки одиночных журнальных блоков.
@purpose Находит новые ссылки вида ![{fig...}], за один шаг определяет ориентацию 
         и кастомные размеры кадра, дублирует подпись в пустой alt и собирает HTML.
         Работает строго построчно по аналогии с оригинальным images.py.
@author TechLab
@version 1.8
"""

import re

def process_single_figure_landscape(markdown_content):
    """
    Обрабатывает контент строго построчно, исключая видеофайлы
    по аналогии с оригинальным images.py.
    """
    lines = markdown_content.split('\n')
    processed_lines = []
    
    # СТРОГО ОРИГИНАЛЬНЫЙ ПАТТЕРН ИЗ IMAGES.PY (Фильтрация только картинок)
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    for line in lines:
        line_stripped = line.strip()
        
        # Если в строке нет маркера fig, пропускаем её без изменений
        if 'fig' not in line_stripped.lower():
            processed_lines.append(line)
            continue
            
        # Проверяем строку на соответствие паттерну картинок из images.py
        match = re.search(img_pattern, line_stripped)
        if not match:
            processed_lines.append(line)
            continue
            
        alt_content = match.group(1).strip()
        img_url = match.group(2).strip()
        
        # ЛОГ ВХОДА СТРОКИ ПОСЛЕ PATHLINKS.PY
        print(f"\n[FIG-CONVERT] ВХОД: {line_stripped}")
        
        # 1. Очистка хвоста
        alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
        
        # 2. Разбивка по пайпам с очисткой от скобок {} и пробелов
        parts = [p.strip('{} ') for p in alt_content.split('|') if p.strip()]
        
        target_class = "img-single-figure-landscape"
        custom_attrs = ""
        
        if parts and parts[0].lower() == 'fig':
            parts.pop(0)
            
        if parts and parts[0].lower() == 'v':
            target_class = "img-single-figure-portrait"
            parts.pop(0)
            
        elif parts and re.match(r'^\d+[xх]\d+$', parts[0], re.IGNORECASE):
            size_match = re.split(r'[xх]', parts[0], flags=re.IGNORECASE)
            width, height = int(size_match[0]), int(size_match[1])
            if width > height:
                target_class = "img-single-figure-custom-landscape"
            else:
                target_class = "img-single-figure-custom-portrait"
            custom_attrs = f' width="{width}" height="{height}" style="aspect-ratio: {width} / {height} !important;"'
            parts.pop(0)
            
        clean_text = " | ".join(parts) if parts else ""
        
        figcaption_html = ""
        if clean_text:
            figcaption_html = f'\n        <figcaption class="img-figcaption">{clean_text}</figcaption>'
            
        html_output = (
            f'<div class="img-single-figure">\n'
            f'    <figure class="img-figure">\n'
            f'        <img class="{target_class}"{custom_attrs} alt="{clean_text}" src="{transparent_pixel}" data-src="{img_url}">'
            f'{figcaption_html}\n'
            f'    </figure>\n'
            f'</div>'
        )
        
        # ЛОГ ВЫХОДА ГОТОВОГО HTML
        print(f"[FIG-CONVERT] ВЫХОД:\n{html_output}")
        
        processed_lines.append(html_output)
        
    return '\n'.join(processed_lines)
