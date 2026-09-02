#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll.
@purpose ИСПРАВЛЕНО: Полное сохранение Lazy-Load (data-src) для чистых ссылок без параметров.
@author TechLab
@version 5.1 🚀 (Часть 1)
"""

import re

def process_markdown_images(markdown_content):
    """
    Парсит маркдаун-изображения двух стандартов и превращает их в валидный HTML v5.1.
    """
    wiki_pattern = r'!\[\[(.*?)\]\]'
    classic_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    lines = markdown_content.split('\n')
    processed_lines = []

    for line in lines:
        current_line = line
        
        # Считаем количество картинок на строке
        wiki_matches = list(re.finditer(wiki_pattern, current_line, flags=re.IGNORECASE))
        classic_matches = list(re.finditer(classic_pattern, current_line, flags=re.IGNORECASE))
        is_row_mode = (len(wiki_matches) + len(classic_matches)) > 1

        # ==========================================================================
        # 🌟 ВЕТКА А: ПАРСИНГ НОВЫХ WIKI-ССЫЛОК OBSIDIAN ![[...]]
        # ==========================================================================
        if wiki_matches:
            for match in wiki_matches:
                raw_match = match.group(0)
                inner_content = match.group(1).strip()
                
                # Очистка обсидиановских хвостов размеров (|400 в конце)
                inner_content = re.sub(r'\|\s*\d+\s*$', '', inner_content).strip()
                
                # Дробим внутренности ссылки по палочкам
                wiki_parts = [p.strip() for p in inner_content.split('|') if p.strip()]
                if not wiki_parts:
                    continue
                    
                # 1. Первый элемент — всегда путь к файлу
                img_url = wiki_parts.pop(0)
                img_url = re.sub(r'^\.\.\/', '/', img_url) # Превращаем ../faire/ в /faire/
                
                # Инициализируем переменные сборки HTML
                classes = []
                custom_attrs = []
                is_centered = False
                custom_width = None
                alt_text = ""
                figcaption_text = ""
                
                # 2. Ищем контейнер скрытых параметров {...}
                params_str = ""
                for index, part in enumerate(wiki_parts):
                    if part.startswith('{') and part.endswith('}'):
                        params_str = wiki_parts.pop(index)
                        break
                
                # Разбираем скрытые параметры
                if params_str:
                    clean_params = params_str.strip('{}')
                    param_parts = [p.strip() for p in clean_params.split('|') if p.strip()]
                    
                    while param_parts:
                        current_param = param_parts[0]
                        if current_param.lower() == 'fig':
                            classes.append('img-fig')
                            is_centered = True
                            param_parts.pop(0)
                        elif current_param.lower() == 'v':
                            classes.append('img-v' if is_centered else ('img-row-portrait' if is_row_mode else 'img-single-portrait'))
                            param_parts.pop(0)
                        elif re.match(r'^\d+[xх]\d+$', current_param, re.IGNORECASE):
                            classes.append('img-single-custom')
                            dimensions = re.split(r'[xх]', current_param, flags=re.IGNORECASE)
                            custom_width, height = dimensions[0], dimensions[1]
                            custom_attrs.append(f'width="{custom_width}"')
                            custom_attrs.append(f'height="{height}"')
                            custom_attrs.append(f'style="aspect-ratio: {custom_width} / {height} !important;"')
                            param_parts.pop(0)
                        else:
                            alt_text = " | ".join(param_parts)
                            break
                
                # 3. Всё, что осталось снаружи — это чистый figcaption
                if wiki_parts:
                    figcaption_text = " | ".join(wiki_parts)
                
                # Фиксируем дефолтный базовый класс, если специфичные не назначены
                if not classes:
                    classes.append('img-row-landscape' if is_row_mode else 'img-single-landscape')
                    
                class_str = f' class="{" ".join(classes)}"' if classes else ''
                attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
                
                # 🔥 ИСПРАВЛЕНО ЖЕСТКО: Путь уходит СТРОГО в data-src, а в src встает прозрачный пиксель!
                img_html = f'<img{class_str}{attr_str} alt="{alt_text}" src="{transparent_pixel}" data-src="{img_url}">'
                
                if is_centered:
                    if custom_width:
                        figcaption_html = f'<figcaption class="figcaption-img" style="max-width: {custom_width}px !important; min-width: 371px;">{figcaption_text}</figcaption>' if figcaption_text else ''
                    else:
                        figcaption_html = f'<figcaption class="figcaption-img">{figcaption_text}</figcaption>' if figcaption_text else ''
                    img_html = f'<figure class="figure-img">{img_html}{figcaption_html}</figure>'
                    
                current_line = current_line.replace(raw_match, img_html, 1)

        # ==========================================================================
        # 🌅 ВЕТКА Б: КЛАССИЧЕСКИЙ МАРКДАУН ![](url) ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ
        # ==========================================================================
        classic_matches = list(re.finditer(classic_pattern, current_line, flags=re.IGNORECASE))
        if classic_matches:
            def replacer(match):
                alt_content = match.group(1).strip()
                img_url = match.group(2).strip()
                
                alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
                
                if not alt_content:
                    final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                    return f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                    
                parts = [p.strip() for p in alt_content.split('|') if p.strip()]
                if not parts:
                    final_class = 'img-row-landscape' if is_row_mode else 'img-single-landscape'
                    return f'<img class="{final_class}" alt="" src="{transparent_pixel}" data-src="{img_url}">'
                    
                classes = []
                custom_attrs = []
                is_centered = False
                custom_width = None
                
                if parts[0].lower() == 'fig':
                    classes.append('img-fig')
                    is_centered = True
                    parts.pop(0)
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
                elif parts[0].lower() == 'v':
                    classes.append('img-single-portrait')
                    parts.pop(0)
                elif re.match(r'^\d+[xх]\d+$', parts[0], re.IGNORECASE):
                    classes.append('img-single-custom')
                    dimensions = re.split(r'[xх]', parts[0], flags=re.IGNORECASE)
                    custom_width, height = dimensions[0], dimensions[1]
                    custom_attrs.append(f'width="{custom_width}"')
                    custom_attrs.append(f'height="{height}"')
                    custom_attrs.append(f'style="aspect-ratio: {custom_width} / {height} !important;"')
                    parts.pop(0)
                    
                if not classes:
                    classes.append('img-single-landscape')
                    
                clean_alt = " | ".join(parts) if parts else ""
                class_str = f' class="{" ".join(classes)}"' if classes else ''
                attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
                
                img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
                
                if is_centered:
                    if custom_width:
                        figcaption_html = f'<figcaption class="figcaption-img" style="max-width: {custom_width}px !important; min-width: 371px;">{clean_alt}</figcaption>' if clean_alt else ''
                    else:
                        figcaption_html = f'<figcaption class="figcaption-img">{clean_alt}</figcaption>' if clean_alt else ''
                    return f'<figure class="figure-img">{img_html}{figcaption_html}</figure>'
               
                return img_html

            current_line = re.sub(classic_pattern, replacer, current_line, flags=re.IGNORECASE)

        processed_lines.append(current_line)
        
    article_html = '\n'.join(processed_lines)
    
    # Сборка рядов блоков figure (Журнальная группировка строк)
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

