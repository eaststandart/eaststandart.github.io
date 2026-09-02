#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll.
@purpose ИСПРАВЛЕНО: Полная поддержка фигурных скобок {...} в ОБОИХ форматах ссылок.
         Восстановлен ленивый JS-слой (data-src) во всех режимах.
@author TechLab
@version 5.2 🚀 (Часть 1)
"""

import re

def process_markdown_images(markdown_content):
    """
    Парсит маркдаун-изображения двух стандартов и превращает их в валидный HTML v5.2.
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
        # 🌟 ВЕТКА А: ПАРСИНГ WIKI-ССЫЛОК OBSIDIAN ![[...]]
        # ==========================================================================
        if wiki_matches:
            for match in wiki_matches:
                raw_match = match.group(0)
                inner_content = match.group(1).strip()
                inner_content = re.sub(r'\|\s*\d+\s*$', '', inner_content).strip()
                
                wiki_parts = [p.strip() for p in inner_content.split('|') if p.strip()]
                if not wiki_parts:
                    continue
                    
                img_url = wiki_parts.pop(0)
                img_url = re.sub(r'^\.\.\/', '/', img_url)
                
                classes = []
                custom_attrs = []
                is_centered = False
                custom_width = None
                alt_text = ""
                figcaption_text = ""
                
                params_str = ""
                for index, part in enumerate(wiki_parts):
                    if part.startswith('{') and part.endswith('}'):
                        params_str = wiki_parts.pop(index)
                        break
                
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
                
                if wiki_parts:
                    figcaption_text = " | ".join(wiki_parts)
                
                if not classes:
                    classes.append('img-row-landscape' if is_row_mode else 'img-single-landscape')
                    
                class_str = f' class="{" ".join(classes)}"' if classes else ''
                attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
                
                img_html = f'<img{class_str}{attr_str} alt="{alt_text}" src="{transparent_pixel}" data-src="{img_url}">'
                
                if is_centered:
                    if custom_width:
                        figcaption_html = f'<figcaption class="figcaption-img" style="max-width: {custom_width}px !important; min-width: 371px;">{figcaption_text}</figcaption>' if figcaption_text else ''
                    else:
                        figcaption_html = f'<figcaption class="figcaption-img">{figcaption_text}</figcaption>' if figcaption_text else ''
                    img_html = f'<figure class="figure-img">{img_html}{figcaption_html}</figure>'
                    
                current_line = current_line.replace(raw_match, img_html, 1)

        # ==========================================================================
        # 🌅 ВЕТКА Б: КЛАССИЧЕСКИЙ МАРКДАУН ![](url) С ПОДДЕРЖКОЙ {ПАРАМЕТРОВ}
        # ==========================================================================
        classic_matches = list(re.finditer(classic_pattern, current_line, flags=re.IGNORECASE))
        if classic_matches:
            def replacer(match):
                alt_content = match.group(1).strip()
                img_url = match.group(2).strip()
                
                # Вырезаем обсидиановские хвосты размеров
                alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()
                
                # Если alt пустой, сразу отдаем дефолтный ландшафтный класс
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
                alt_text = ""
                figcaption_text = ""
                
                # Ищем контейнер параметров {...} среди частей классического альта
                params_str = ""
                for index, part in enumerate(parts):
                    if part.startswith('{') and part.endswith('}'):
                        params_str = parts.pop(index)
                        break
                        
                # Если нашли фигурные скобки, вскрываем параметры и достаем ключи
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
                            # Внутренний текст в скобках уходит в alt-тег
                            alt_text = " | ".join(param_parts)
                            break
                            
                # Всё, что осталось за пределами скобок — распределяем
                if parts:
                    external_text = " | ".join(parts)
                    # Если был fig — пускаем в figcaption, если нет — в alt
                    if is_centered:
                        figcaption_text = external_text
                    else:
                        alt_text = external_text if not alt_text else f"{alt_text} | {external_text}"
                
                # Если специфичные классы формы не назначены
                if not classes:
                    classes.append('img-row-landscape' if is_row_mode else 'img-single-landscape')
                    
                clean_alt = alt_text if alt_text else ""
                class_str = f' class="{" ".join(classes)}"' if classes else ''
                attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
                
                # Ленивая загрузка зафиксирована для классической ветки
                img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
                
                if is_centered:
                    if custom_width:
                        figcaption_html = f'<figcaption class="figcaption-img" style="max-width: {custom_width}px !important; min-width: 371px;">{figcaption_text}</figcaption>' if figcaption_text else ''
                    else:
                        figcaption_html = f'<figcaption class="figcaption-img">{figcaption_text}</figcaption>' if figcaption_text else ''
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

