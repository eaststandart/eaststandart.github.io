#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll.
@purpose Автоматически вычисляет одиночные и групповые (в столбиках) картинки в Маркдауне.
         Для одиночных картинок включает класс img-custom, убирая серые уши в CSS.
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки и превращает их в HTML-блоки на основе их окружения.
    """
    # Шаблон для поиска стандартной разметки картинки: ![параметры](ссылка)
    img_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    # Сначала разбиваем весь текст статьи на отдельные строки
    lines = markdown_content.split('\n')
    
    # Массив, где мы отметим индексы строк, которые являются частью "столбика-галереи"
    grouped_line_indices = set()
    
    # Пасс 1: Находим все групповые картинки (используем search вместо капризного match)
    for i in range(len(lines)):
        current_line = lines[i].strip()
        if current_line and re.search(img_pattern, current_line):
            is_grouped = False
            
            # Проверяем строку ВЫШЕ: если она тоже картинка, то это столбик!
            if i > 0 and lines[i-1].strip() and re.search(img_pattern, lines[i-1].strip()):
                is_grouped = True
                grouped_line_indices.add(i-1)
                
            # Проверяем строку НИЖЕ: если она тоже картинка, то это столбик!
            if i < len(lines) - 1 and lines[i+1].strip() and re.search(img_pattern, lines[i+1].strip()):
                is_grouped = True
                grouped_line_indices.add(i+1)
                
            if is_grouped:
                grouped_line_indices.add(i)

    # Пасс 2: Построчно обрабатываем контент
    processed_lines = []
    for i, line in enumerate(lines):
        is_in_gallery = i in grouped_line_indices
        
        def replacer(match):
            alt_text = match.group(1).strip()
            img_url = match.group(2).strip()
            
            # Если скобки пустые и картинка одиночная — делаем её кастомной
            if not alt_text:
                if not is_in_gallery:
                    return f'<img class="img-custom" alt="" src="{img_url}">'
                return f'<img alt="" src="{img_url}">'
                
            # Разбиваем параметры строго по палочке, убирая пустые элементы
            parts = [p.strip() for p in alt_text.split('|') if p.strip()]
            
            if not parts:
                if not is_in_gallery:
                    return f'<img class="img-custom" alt="" src="{img_url}">'
                return f'<img alt="" src="{img_url}">'
                
            classes = []
            custom_attrs = []
            is_centered = False
            
            # Если картинка одиночная — принудительно вешаем на неё img-custom,
            # чтобы сбросить для неё ложные горизонтальные рамки 16:9
            if not is_in_gallery:
                classes.append('img-custom')
            
            # ИСПРАВЛЕНИЕ: Строго берём первый элемент списка по индексу!
            first_part = parts[0]
            
            # РАЗБОР МАРКЕРА ВЕРТИКАЛИ 'v'
            if first_part.lower() == 'v':
                if is_in_gallery:
                    classes.append('img-v')
                parts.pop(0)
                
            # РАЗБОР МАРКЕРА ЦЕНТРА 'center'
            elif first_part.lower() == 'center':
                classes.append('img-center')
                is_centered = True
                if 'img-custom' in classes:
                    classes.remove('img-custom')
                parts.pop(0)
                
            # РАЗБОР ФИЗИЧЕСКОГО РАЗРЕШЕНИЯ (например, 320x405)
            elif re.match(r'^\d+[xх]\d+$', first_part, re.IGNORECASE):
                dimensions = re.split(r'[xх]', first_part, flags=re.IGNORECASE)
                width, height = dimensions[0], dimensions[1]
                
                custom_attrs.append(f'width="{width}"')
                custom_attrs.append(f'height="{height}"')
                if 'img-custom' not in classes:
                    classes.append('img-custom')
                parts.pop(0)
                
            # ПРОВЕРКА ХВОСТА: отрезаем мусорный размер Obsidian (например, |400)
            if parts and re.match(r'^\d+$', parts[-1]):
                parts.pop()
                
            # Собираем чистый SEO-текст
            clean_alt = " | ".join(parts) if parts else ""
            
            class_str = f' class="{" ".join(classes)}"' if classes else ''
            attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
            
            img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{img_url}">'
            
            if is_centered:
                return f'<p class="p-center">{img_html}</p>'
                
            return img_html

        new_line = re.sub(img_pattern, replacer, line)
        processed_lines.append(new_line)
        
    return '\n'.join(processed_lines)
