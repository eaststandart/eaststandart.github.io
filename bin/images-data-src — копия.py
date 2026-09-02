#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll с поддержкой JS ленивой загрузки.
@purpose Заменяет нативный src на data-src для жесткого контроля трафика через JavaScript,
         реализует строгое левостороннее чтение служебных ключей (fig, v, 320x405),
         автоматически отсекает обсидиановские хвосты размеров |400, изолирует
         класс img-custom и выстраивает правильный HTML-порядок атрибутов alt -> data-src.
@author TechLab
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки всех форматов и превращает их в HTML-блоки с data-src.
    Гарантирует порядок атрибутов alt перед data-src для последующей ленивой загрузки.
    """
    # Паттерн ловит картинки с расширениями webp, jpg, jpeg, png, gif, svg (регистронезависимо)
    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    
    lines = markdown_content.split('\n')
    processed_lines = []

    for line in lines:
        def replacer(match):
            alt_content = match.group(1).strip()
            img_url = match.group(2).strip()
            
            # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА ---
            alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
            
            # Если после очистки скобки оказались пустыми — отдаем чистую базовую картинку с data-src
            if not alt_content:
                return f'<img alt="" data-src="{img_url}">'
                
            # Разбиваем содержимое по вертикальной палочке
            parts = [p.strip() for p in alt_content.split('|') if p.strip()]
            
            # Если массив частей пуст — отдаем чистую базовую картинку с data-src
            if not parts:
                return f'<img alt="" data-src="{img_url}">'
                
            classes = []
            custom_attrs = []
            is_centered = False
            
            # --- ШАГ 2: ЛЕВOСТОРОННИЙ РАЗБОР СЛУЖЕБНЫХ КЛЮЧЕЙ (Слева направо) ---
            
            # Проверяем Ключ 1: Журнальная сетка 'fig'
            if parts[0].lower() == 'fig':
                classes.append('img-fig')
                is_centered = True
                parts.pop(0) # Удаляем отработанный ключ fig
                
                # Проверяем вложенный Ключ 2: Вертикальный модификатор 'v' внутри fig
                if parts and parts[0].lower() == 'v':
                    classes.append('img-v')
                    parts.pop(0)
                    
            # Проверяем Ключ 1: Одиночная вертикалка в тексте 'v' (без fig)
            elif parts[0].lower() == 'v':
                classes.append('img-v')
                parts.pop(0)
                
            # Проверяем Ключ 1: Ручной кастомный размер сторон '320x405'
            elif re.match(r'^\d+[xх]\d+$', parts[0], re.IGNORECASE):
                classes.append('img-custom')
                dimensions = re.split(r'[xх]', parts[0], flags=re.IGNORECASE)
                width, height = dimensions[0], dimensions[1]
                
                # Записываем точные физические атрибуты сторон
                custom_attrs.append(f'width="{width}"')
                custom_attrs.append(f'height="{height}"')
                # Включаем жесткую защиту CLS и инлайновые пропорции соотношения сторон
                custom_attrs.append(f'style="aspect-ratio: {width} / {height} !important;"')
                parts.pop(0) # Удаляем отработанный ключ размера
                
            # --- ШАГ 3: СБОРКА ОЧИЩЕННОГО SEO-ТЕКСТА ALT ---
            clean_alt = " | ".join(parts) if parts else ""
            
            # Формируем строки атрибутов
            class_str = f' class="{" ".join(classes)}"' if classes else ''
            attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
            
            # --- ШАГ 4: СБОРКА ИТОГОВОГО HTML С ПРАВИЛЬНЫМ ПОРЯДКОМ (alt перед data-src) ---
            img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" data-src="{img_url}">'
            
            # Если был запрошен журнальный режим, упаковываем в семантическую коробку figure
            if is_centered:
                figcaption_html = f'<figcaption class="figcaption-img">{clean_alt}</figcaption>' if clean_alt else ''
                return f'<figure class="figure-img">{img_html}{figcaption_html}</figure>'
                
            return img_html

        new_line = re.sub(img_pattern, replacer, line, flags=re.IGNORECASE)
        processed_lines.append(new_line)
        
    # === ФИНАЛЬНАЯ СКЛЕЙКА И АВТОМАТИЧЕСКАЯ ГРУППИРОВКА РЯДОВ ДЛЯ JEKYLL ===
    article_html = '\n'.join(processed_lines)
    
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
