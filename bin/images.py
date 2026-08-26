#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll.
@purpose Автоматически вычисляет одиночные и групповые картинки в Маркдауне.
         Для одиночных включает класс img-custom, ко всем добавляет loading="lazy".
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки всех форматов и превращает их в HTML-блоки с нативным лези-лоадом.
    """
    # Паттерн ловит картинки с расширениями webp, jpg, jpeg, png, gif, svg (регистронезависимо)
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    
    lines = markdown_content.split('\n')
    grouped_line_indices = set()
    
    # Пасс 1: Находим все групповые картинки (столбики без пустых строк)
    for i in range(len(lines)):
        current_line = lines[i].strip()
        if current_line and re.search(img_pattern, current_line, re.IGNORECASE):
            is_grouped = False
            
            if i > 0 and lines[i-1].strip() and re.search(img_pattern, lines[i-1].strip(), re.IGNORECASE):
                is_grouped = True
                grouped_line_indices.add(i-1)
                
            if i < len(lines) - 1 and lines[i+1].strip() and re.search(img_pattern, lines[i+1].strip(), re.IGNORECASE):
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
            
            if not alt_text:
                if not is_in_gallery:
                    return f'<img class="img-custom" loading="lazy" alt="" src="{img_url}">'
                return f'<img loading="lazy" alt="" src="{img_url}">'
                
            parts = [p.strip() for p in alt_text.split('|') if p.strip()]
            
            if not parts:
                if not is_in_gallery:
                    return f'<img class="img-custom" loading="lazy" alt="" src="{img_url}">'
                return f'<img loading="lazy" alt="" src="{img_url}">'
                
            classes = []
            custom_attrs = []
            is_centered = False
            
            if not is_in_gallery:
                classes.append('img-custom')
            
            first_part = parts[0]
            
            if first_part.lower() == 'v':
                if is_in_gallery:
                    classes.append('img-v')
                parts.pop(0)
                
            elif first_part.lower() == 'center':
                classes.append('img-center')
                is_centered = True
                if 'img-custom' in classes:
                    classes.remove('img-custom')
                parts.pop(0)
                
            elif re.match(r'^\d+[xх]\d+$', first_part, re.IGNORECASE):
                dimensions = re.split(r'[xх]', first_part, flags=re.IGNORECASE)
                width, height = dimensions[0], dimensions[1]
                
                custom_attrs.append(f'width="{width}"')
                custom_attrs.append(f'height="{height}"')
                
                # Автоматически рассчитываем и внедряем персональный aspect-ratio в HTML
                custom_attrs.append(f'style="aspect-ratio: {width} / {height} !important;"')
                
                if 'img-custom' not in classes:
                    classes.append('img-custom')
                parts.pop(0)

                
            if parts and re.match(r'^\d+$', parts[-1]):
                parts.pop()
                
            clean_alt = " | ".join(parts) if parts else ""
            
            class_str = f' class="{" ".join(classes)}"' if classes else ''
            attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
            
            # Добавляем нативный loading="lazy" прямо в сердце тега!
            img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{img_url}" loading="lazy">'
            
            if is_centered:
                # Берём текст подписи напрямую из готовой переменной clean_alt
                figcaption_html = f'<figcaption class="figcaption-center">{clean_alt}</figcaption>' if clean_alt else ''
                
                # Возвращаем чистую одиночную фигуру
                return f'<figure class="figure-center">{img_html}{figcaption_html}</figure>'


                # Собираем красивую HTML5 структуру figure
                return f'<figure class="figure-center">{img_html}{figcaption_html}</figure>'
                
            return img_html

        new_line = re.sub(img_pattern, replacer, line, flags=re.IGNORECASE)
        processed_lines.append(new_line)
        
    # Склеиваем все обработанные строки в один большой текст
    markdown_content = '\n'.join(processed_lines)
    
    # Автоматически оборачиваем одиночные и групповые figure в один общий div-ряд
    markdown_content = re.sub(
        r'((?:<figure class="figure-center">.*?</figure>\s*)+)',
        r'<div class="figure-center-row">\1</div>',
        markdown_content
    )
        
    return markdown_content
