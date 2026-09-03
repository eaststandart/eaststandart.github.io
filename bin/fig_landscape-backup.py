#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script fig_landscape.py
@about Построчный стабильный модуль для обработки одиночных журнальных блоков.
@purpose Находит новые ссылки вида ![{fig...}], за один шаг определяет ориентацию 
         и кастомные размеры кадра, разделяет скрытый SEO Alt и живую подпись.
         Работает строго построчно на основе синтаксиса и методов оригинального images.py.
@author TechLab
@version 2.5-final
"""

import re

def process_single_figure_landscape(markdown_content):
    """
    Обрабатывает контент строго построчно по аналогии с images.py.
    Реагирует только на новые ссылки, начинающиеся с ![{fig.
    """
    lines = markdown_content.split('\n')
    processed_lines = []
    
    # Строгий оригинальный паттерн из images.py для фильтрации картинок
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    for line in lines:
        line_stripped = line.strip()
        
        # СТРОГИЙ ФИЛЬТР: Реагируем только на те ссылки, которые содержат маркер ![{fig
        if '![{fig' not in line_stripped.lower():
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
        
        # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА ---
        alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
        
        # --- ШАГ 2: РАЗБИВКА НА ПЛОСКИЙ МАССИВ ПАРАМЕТРОВ ПО ПАЙПАМ ---
        # Сначала бьем исходную строку, сохраняя сырые элементы для проверки скобок
        raw_parts = [p.strip() for p in alt_content.split('|') if p.strip()]
        
        target_class = "img-single-figure-landscape"
        custom_attrs = ""
        
        # Проверяем и удаляем первый маркер 'fig'
        if raw_parts and raw_parts[0].strip('{} ').lower() == 'fig':
            raw_parts.pop(0)
            
        # Проверяем второй параметр (флаг вертикали 'v' или кастомные размеры)
        if raw_parts and raw_parts[0].strip('{} ').lower() == 'v':
            target_class = "img-single-figure-portrait"
            raw_parts.pop(0)
            
        elif raw_parts and re.match(r'^\d+[xх]\d+$', raw_parts[0].strip('{} '), re.IGNORECASE):
            size_clean = raw_parts[0].strip('{} ')
            size_match = re.split(r'[xх]', size_clean, flags=re.IGNORECASE)
            width, height = int(size_match[0]), int(size_match[1])
            if width > height:
                target_class = "img-single-figure-custom-landscape"
            else:
                target_class = "img-single-figure-custom-portrait"
            custom_attrs = f' width="{width}" height="{height}" style="aspect-ratio: {width} / {height} !important;"'
            raw_parts.pop(0)
            
        # --- ШАГ 3: РАЗДЕЛЕНИЕ СКРЫТОГО SEO ALT И ЧЕЛОВЕЧЕСКОЙ ПОДПИСИ ---
        clean_alt = ""
        clean_caption = ""
        
        # Сканируем оставшиеся текстовые элементы в массиве
        for part in raw_parts:
            # Если элемент содержит закрывающую скобку '}' — это скрытый SEO Alt из скобок
            if '}' in part:
                clean_alt = part.strip('{} ')
            # Если скобки нет — это внешняя человеческая подпись для людей
            else:
                clean_caption = part.strip('{} ')
                
        # --- ШАГ 4: КРИТИЧЕСКОЕ SEO-ПРАВИЛО ЗАЩИТЫ (ЗАКОН ДУБЛИРОВАНИЯ) ---
        # Если скрытая зона альта пуста, дублируем в неё внешнюю человеческую подпись
        if not clean_alt and clean_caption:
            clean_alt = clean_caption
            
        # --- ШАГ 5: СБОРКА СЕМАНТИЧЕСКОГО HTML-БЛОКА ---
        figcaption_html = ""
        if clean_caption:
            figcaption_html = f'\n        <figcaption class="img-figcaption">{clean_caption}</figcaption>'
            
        html_output = (
            f'<div class="img-single-figure">\n'
            f'    <figure class="img-figure">\n'
            f'        <img class="{target_class}"{custom_attrs} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
            f'{figcaption_html}\n'
            f'    </figure>\n'
            f'</div>'
        )
        
        # ЛОГ ВЫХОДА ГОТОВОГО HTML
        print(f"[FIG-CONVERT] ВЫХОД:\n{html_output}")
        
        processed_lines.append(html_output)
        
    return '\n'.join(processed_lines)
