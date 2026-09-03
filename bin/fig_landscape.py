#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script fig_landscape.py
@about Построчный стабильный модуль для обработки одиночных журнальных блоков.
@purpose Находит новые ссылки вида ![{fig...}], изолирует скрытую зону параметров {} 
         от внешней живой подписи, дублирует подпись в пустой alt и собирает HTML.
@author TechLab
@version 2.1
"""

import re

def process_single_figure_landscape(markdown_content, file_rel_path):
    """
    Обрабатывает контент строго построчно по аналогии с images.py.
    Изолирует внутренние параметры фигурных скобок от внешней подписи.
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
        
        # ЛОГ ПУТИ К ФАЙЛУ И ВХОДЯЩЕЙ СТРОКИ ПОСЛЕ PATHLINKS.PY
        print(f"\n[FIG-CONVERT] ФАЙЛ: {file_rel_path}")
        print(f"[FIG-CONVERT] ВХОД: {line_stripped}")
        
        # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА (|400) ---
        alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
        
        # --- ШАГ 2: ИЗОЛЯЦИЯ ЖИВОЙ ЗОНЫ ЧЕЛОВЕЧЕСКОЙ ПОДПИСИ (СНАРУЖИ СКОБОК {}) ---
        # Вырезаем полностью блок фигурных скобок вместе с возможным пайпом после него
        outside_content = re.sub(r'\{\s*fig[^}]*\}\s*\|?', '', alt_content).strip()
        clean_caption = outside_content  # Это чистая подпись для людей
        
        # --- ШАГ 3: ИЗОЛЯЦИЯ СКРЫТОЙ ЗОНЫ ПАРАМЕТРОВ РОБОТОВ (ВНУТРИ СКОБОК {}) ---
        inner_match = re.search(r'\{\s*(fig[^}]+)\}', alt_content)
        inner_bracket = inner_match.group(1).strip() if inner_match else ""
        
        # Разрезаем скрытые параметры по пайпам
        inner_parts = [p.strip() for p in inner_bracket.split('|') if p.strip()]
        
        target_class = "img-single-figure-landscape"
        custom_attrs = ""
        
        # А. Первым параметром всегда идет и удаляется 'fig'
        if inner_parts and inner_parts[0].lower() == 'fig':
            inner_parts.pop(0)
            
        # Б. Проверяем второй параметр (флаг вертикали 'v' или размеры)
        if inner_parts and inner_parts[0].lower() == 'v':
            target_class = "img-single-figure-portrait"
            inner_parts.pop(0)
            
        elif inner_parts and re.match(r'^\d+[xх]\d+$', inner_parts[0], re.IGNORECASE):
            size_match = re.split(r'[xх]', inner_parts[0], flags=re.IGNORECASE)
            width, height = int(size_match[0]), int(size_match[1])
            if width > height:
                target_class = "img-single-figure-custom-landscape"
            else:
                target_class = "img-single-figure-custom-portrait"
            custom_attrs = f' width="{width}" height="{height}" style="aspect-ratio: {width} / {height} !important;"'
            inner_parts.pop(0)
            
        # Всё, что осталось внутри скобок после удаления маркеров — это чистый скрытый alt
        clean_alt = " | ".join(inner_parts) if inner_parts else ""
        
        # --- ШАГ 4: КРИТИЧЕСКОЕ SEO-ПРАВИЛО ЗАЩИТЫ (ДУБЛИРОВАНИЕ) ---
        # Подпись копируется в alt ТОЛЬКО если скрытый alt изначально пуст
        if not clean_alt and clean_caption:
            clean_alt = clean_caption
            
        # --- ШАГ 5: СБОРКА СЕМАНТИЧЕСКОГО HTML ---
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
