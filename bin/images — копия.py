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
            
            # Перенесли loading="lazy" в самый конец пустых тегов
            if not alt_text:
                if not is_in_gallery:
                    return f'<img class="img-custom" alt="" src="{img_url}" loading="lazy">'
                return f'<img alt="" src="{img_url}" loading="lazy">'
                
            parts = [p.strip() for p in alt_text.split('|') if p.strip()]
            
            # Перенесли loading="lazy" в самый конец пустых отфильтрованных тегов
            if not parts:
                if not is_in_gallery:
                    return f'<img class="img-custom" alt="" src="{img_url}" loading="lazy">'
                return f'<img alt="" src="{img_url}" loading="lazy">'
                
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
                
                # Повторная проверка на случай конструкции ![v | fig | Текст]
                if parts and parts[0].lower() == 'fig':
                    # 🔥 ПЕРЕИМЕНОВАНО: Заменили img-center на img-fig
                    classes.append('img-fig')
                    is_centered = True
                    if 'img-custom' in classes:
                        classes.remove('img-custom')
                    parts.pop(0)
                
            # Строгое точное совпадение с 'fig'. Любые 'fig.', 'figure 1' и т.д. пойдут в текст подписи
            elif first_part.lower() == 'fig':
                # 🔥 ПЕРЕИМЕНОВАНО: Заменили img-center на img-fig
                classes.append('img-fig')
                is_centered = True
                if 'img-custom' in classes:
                    classes.remove('img-custom')
                parts.pop(0)
                
            elif re.match(r'^\d+[xх]\d+$', first_part, re.IGNORECASE):
                dimensions = re.split(r'[xх]', first_part, flags=re.IGNORECASE)
                width, height = dimensions[0], dimensions[1]
                
                custom_attrs.append(f'width="{width}"')
                custom_attrs.append(f'height="{height}"')
                
                custom_attrs.append(f'style="aspect-ratio: {width} / {height} !important;"')
                
                if 'img-custom' not in classes:
                    classes.append('img-custom')
                parts.pop(0)

                
            if parts and re.match(r'^\d+$', parts[-1]):
                parts.pop()
                
            clean_alt = " | ".join(parts) if parts else ""
            
            class_str = f' class="{" ".join(classes)}"' if classes else ''
            attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
            
            # loading="lazy" гарантированно замыкает основной тег img
            img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{img_url}" loading="lazy">'
            
            if is_centered:
                figcaption_html = f'<figcaption class="figcaption-center">{clean_alt}</figcaption>' if clean_alt else ''
                return f'<figure class="figure-center">{img_html}{figcaption_html}</figure>'
                
            return img_html

        new_line = re.sub(img_pattern, replacer, line, flags=re.IGNORECASE)
        processed_lines.append(new_line)
        
    # === ФИНАЛЬНАЯ СКЛЕЙКА И АВТОМАТИЧЕСКАЯ ГРУППИРОВКА РЯДОВ ДЛЯ JEKYLL ===
    article_html = '\n'.join(processed_lines)
    
    def group_rows(match):
        content = match.group(1)
        if content.count('<figure') > 1:
            return f'<div class="figure-center-row">{content}</div>' 
        return f'<div class="figure-center-single">{content}</div>' 

    article_html = re.sub(
        r'((?:<figure class="figure-center">.*?</figure>[ \t]*\n?)+)',
        group_rows,
        article_html
    )
        
    return article_html
