#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll с поддержкой JS ленивой загрузки.
@purpose v6.0 🚀 ИСПРАВЛЕНО: Устранены критические ошибки AttributeError (parts.strip) и распаковки размеров, ломавшие обработку страниц.
@author TechLab
@version 6.0 (Часть 1)
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки и собирает их в HTML-блоки с ленивой загрузкой.
    Использует логику группировки плотных строк из videos.py.
    """
    # 🌟 Б. ЗАМОРОЗКА БЛОКОВ КОДА (Железный сейф для картинок)
    code_vault = []
    
    def code_freezer(match):
        code_vault.append(match.group(0))
        return f'==CODE_BLOCK_{len(code_vault)-1}=='

    # Прячем код, чтобы этот модуль не лез внутрь бэктиков
    temporary_content = re.sub(r'```[\s\S]*?```', code_freezer, markdown_content)
    temporary_content = re.sub(r'`{1,3}[^`\n]+?`{1,3}', code_freezer, temporary_content)

    # 🔍 ДИАГНОСТИЧЕСКИЙ ЛОГ: Проверяем, как файл зашел в сейф картинок
    if "test-v.webp" in markdown_content:
        print(f"[IMAGES-VAULT-LOG] Вход в images. Сейф заполнен: {code_vault}")

    img_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    # Режем на строки уже ЗАМОРОЖЕННЫЙ контент
    lines = temporary_content.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        if not line_stripped:
            processed_lines.append(line)
            i += 1
            continue
            
        is_image = re.match(img_pattern, line_stripped, re.IGNORECASE)
        
        if is_image:
            # Запускаем сборщик плотной группы картинок, идущих друг под другом
            image_group_lines = []
            
            while i < len(lines) and lines[i].strip() and re.match(img_pattern, lines[i].strip(), re.IGNORECASE):
                image_group_lines.append(lines[i].strip())
                i += 1
                
            # Переменная флага ряда: если в группе больше одной картинки подряд — это ГАЛЕРЕЯ!
            is_row_mode = len(image_group_lines) > 1
            
            # Теперь обрабатываем каждую собранную строку внутри этой группы
            for group_line in image_group_lines:
                match = re.match(img_pattern, group_line, re.IGNORECASE)
                alt_content = match.group(1).strip()
                img_url = match.group(2).strip()
                
                # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА ---
                alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
                
                if not alt_content:
                    final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                    processed_lines.append(f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">')
                    continue
                    
                parts = [p.strip() for p in alt_content.split('|') if p.strip()]
                
                if not parts:
                    final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                    processed_lines.append(f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">')
                    continue
                    
                classes = []
                custom_attrs = []
                is_centered = False
                
                # 🔥 ИСПРАВЛЕНО: strip() применяется строго к строке-элементу, а не к списку parts
                first_key = parts[0].strip('{} ')

                # --- ШАГ 2: ЛЕВOСТОРОННИЙ РАЗБОР СЛУЖЕБНЫХ КЛЮЧЕЙ ---
                if first_key.lower() == 'fig':
                    classes.append('img-fig')
                    is_centered = True
                    parts.pop(0) # Удаляем отработанный ключ fig
                    
                    if parts and parts[0].strip('{} ').lower() == 'v':
                        classes.append('img-v')
                        parts.pop(0)
                        
                elif first_key.lower() == 'v':
                    # Выдаем точный класс формы в зависимости от режима одиночки/галереи
                    classes.append('img-row-portrait' if is_row_mode else 'img-single-portrait')
                    parts.pop(0)
                    
                elif re.match(r'^\d+[xх]\d+$', first_key, re.IGNORECASE):
                    classes.append('img-single-custom')
                    dimensions = re.split(r'[xх]', first_key, flags=re.IGNORECASE)
                    # 🔥 ИСПРАВЛЕНО: Извлекаем конкретные элементы строк из массива размеров
                    width, height = dimensions[0].strip(), dimensions[1].strip()
                    
                    custom_attrs.append(f'width="{width}"')
                    custom_attrs.append(f'height="{height}"')
                    custom_attrs.append(f'style="aspect-ratio: {width} / {height} !important;"')
                    parts.pop(0)
                    
                if not classes:
                    # Выдаем точный базовый класс формы
                    classes.append('img-row-landscape' if is_row_mode else 'img-single-landscape')
                    
                # --- ШАГ 3: СБОРКА ОЧИЩЕННОГО SEO-ТЕКСТА ALT ---
                clean_parts = [p.strip('{} ') for p in parts if p.strip()]
                clean_alt = " | ".join(clean_parts) if clean_parts else ""
                
                class_str = f' class="{" ".join(classes)}"' if classes else ''
                attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
                
                # --- ШАГ 4: СБОРКА ИТОГОВОГО HTML С ЛЕНИВОЙ ЗАГРУЗКОЙ ---
                img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
                
                if is_centered:
                    figcaption_html = f'<figcaption class="figcaption-img">{clean_alt}</figcaption>' if clean_alt else ''
                    processed_lines.append(f'<figure class="figure-img">{img_html}{figcaption_html}</figure>')
                else:
                    processed_lines.append(img_html)
                    
        else:
            processed_lines.append(line)
            i += 1
            
    # === ВАША РОДНАЯ СКЛЕЙКА И АВТОМАТИЧЕСКАЯ ГРУППИРОВКА РЯДОВ ДЛЯ JEKYLL ===
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
        
    # 🌟 РАЗМОРОЗКА БЛОКОВ КОДА (Возвращаем код на место в целости)
    for idx, original_code in enumerate(code_vault):
        article_html = article_html.replace(f'==CODE_BLOCK_{idx}==', original_code)
        
    return article_html
