#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll.
@purpose ОТЛАДОЧНЫЙ ВАРИАНТ: Полная изоляция от блока группировки figure. 
         Жесткий контроль сохранения lazy-load (data-src) в Wiki-ссылках.
@author TechLab
@version 5.3 🚀 (Часть 1)
"""

import re

def process_markdown_images(markdown_content):
    """
    Парсит маркдаун-изображения двух стандартов и превращает их в валидный HTML v5.3.
    """
    wiki_pattern = r'!\[\[(.*?)\]\]'
    classic_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg))\)'
    
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    lines = markdown_content.split('\n')
    processed_lines = []

    for line in lines:
        current_line = line
        
        # Счетчик картинок на строке
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
                inner_content = re.sub(r'\|\s*\d+\s*$', '', inner_content).strip()
                
                wiki_parts = [p.strip() for p in inner_content.split('|') if p.strip()]
                if not wiki_parts:
                    continue
                    
                # 1. Извлекаем и чистим путь
                img_url = wiki_parts.pop(0)
                img_url = re.sub(r'^\.\.\/', '/', img_url)
                
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
                
                # 3. Всё, что снаружи — это подпись figcaption
                if wiki_parts:
                    figcaption_text = " | ".join(wiki_parts)
                
                if not classes:
                    classes.append('img-row-landscape' if is_row_mode else 'img-single-landscape')
                    
                class_str = f' class="{" ".join(classes)}"' if classes else ''
                attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
                
                # Порядок запечатан железно: прозрачный пиксель в src, путь в data-src!
                img_html = f'<img{class_str}{attr_str} alt="{alt_text}" src="{transparent_pixel}" data-src="{img_url}">'
                
                if is_centered:
                    if custom_width:
                        figcaption_html = f'<figcaption class="figcaption-img" style="max-width: {custom_width}px !important; min-width: 371px;">{figcaption_text}</figcaption>' if figcaption_text else ''
                    else:
                        figcaption_html = f'<figcaption class="figcaption-img">{figcaption_text}</figcaption>' if figcaption_text else ''
                    img_html = f'<figure class="figure-img">{img_html}{figcaption_html}</figure>'
                    
                current_line = current_line.replace(raw_match, img_html, 1)
