#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script fig_landscape.py
@about Построчный стабильный модуль для обработки одиночных и групповых журнальных блоков.
@purpose Находит новые ссылки вида ![{fig...}], группирует плотные строки в галереи,
         за один шаг определяет ориентацию и размеры, разделяет SEO Alt и подпись.
         Работает строго по логике и структуре циклов оригинального images.py.
@author TechLab
@version 3.0-final
"""

import re

def process_markdown_images_figure(markdown_content):
    """
    Обрабатывает контент построчно с использованием цикла while для автоматической
    группировки плотных журнальных строк в полноценные ряды (галереи).
    """
    # Строгий оригинальный паттерн из images.py для фильтрации картинок
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    lines = markdown_content.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # Проверяем, является ли строка началом нашего журнального блока
        if not line_stripped or '![{fig' not in line_stripped.lower():
            processed_lines.append(line)
            i += 1
            continue
            
        # Проверяем строку на соответствие паттерну картинок из images.py
        is_image = re.search(img_pattern, line_stripped)
        if not is_image:
            processed_lines.append(line)
            i += 1
            continue
            
        # 🏎️ НАЧАЛО СБОРКИ ПЛОТНОЙ ГРУППЫ СТРОК (ГАЛЕРЕИ)
        group_lines = []
        while i < len(lines) and lines[i].strip() and '![{fig' in lines[i].strip().lower() and re.search(img_pattern, lines[i].strip()):
            group_lines.append(lines[i].strip())
            i += 1
            
        # Определяем режим работы на основе количества собранных строк
        is_row_mode = len(group_lines) > 1
        
        # Задаем префиксы классов и обертки согласно таблице соответствий
        div_class = "img-row-figure" if is_row_mode else "img-single-figure"
        img_prefix = "img-row-figure-" if is_row_mode else "img-single-figure-"
        
        figures_html = []
        
        # Обрабатываем каждую строку внутри собранной группы
        for group_line in group_lines:
            match = re.search(img_pattern, group_line)
            alt_content = match.group(1).strip()
            img_url = match.group(2).strip()
            
            # ТЕХНИЧЕСКИЙ ЛОГ КОНВЕЙЕРА СБОРКИ
            print(f"\n[FIG-CONVERT] ВХОД ({'РЯД' if is_row_mode else 'ОДИНОЧКА'}): {group_line}")
            
            # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА ---
            alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
            
            # --- ШАГ 2: РАЗБИВКА НА ПЛОСКИЙ МАССИВ ПАРАМЕТРОВ ПО ПАЙПАМ ---
            raw_parts = [p.strip() for p in alt_content.split('|') if p.strip()]
            
            # Базовая геометрия по умолчанию
            geometry_class = "landscape"
            custom_attrs = ""
            
            # Проверяем и удаляем первый маркер 'fig'
            if raw_parts and raw_parts[0].strip('{} ').lower() == 'fig':
                raw_parts.pop(0)
                
            # Проверяем второй параметр (флаг вертикали 'v' или кастомные размеры)
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
                
            # Собираем итоговое имя класса для тега <img>
            target_img_class = f"{img_prefix}{geometry_class}"
            
            # --- ШАГ 3: РАЗДЕЛЕНИЕ СКРЫТОГО SEO ALT И ЧЕЛОВЕЧЕСКОЙ ПОДПИСИ ---
            clean_alt = ""
            clean_caption = ""
            
            for part in raw_parts:
                if '}' in part:
                    clean_alt = part.strip('{} ')
                else:
                    clean_caption = part.strip('{} ')
                    
            # --- ШАГ 4: КРИТИЧЕСКОЕ SEO-ПРАВИЛО ЗАЩИТЫ (ЗАКОН ДУБЛИРОВАНИЯ) ---
            if not clean_alt and clean_caption:
                clean_alt = clean_caption
                
            # --- ШАГ 5: СБОРКА СЕМАНТИЧЕСКОЙ СТРУКТУРЫ FIGURE ---
            figcaption_html = ""
            if clean_caption:
                figcaption_html = f'\n        <figcaption class="img-figcaption">{clean_caption}</figcaption>'
                
            item_html = (
                f'    <figure class="img-figure">\n'
                f'        <img class="{target_class_name(target_img_class)}"{custom_attrs} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
                f'{figcaption_html}\n'
                f'    </figure>'
            )
            figures_html.append(item_html)
            
        # --- ШАГ 6: СКЛЕЙКА И УПАКОВКА В ОБЩИЙ ДИСПЕТЧЕРСКИЙ DIV ---
        figures_joined = "\n".join(figures_html)
        html_output = f'<div class="{div_class}">\n{figures_joined}\n</div>'
        
        print(f"[FIG-CONVERT] ВЫХОД:\n{html_output}")
        processed_lines.append(html_output)
        
    return '\n'.join(processed_lines)

def target_class_name(class_str):
    """Вспомогательная функция для чистки двойных дефисов в именах классов"""
    return class_str.replace('--', '-')
