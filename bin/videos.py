#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script videos.py
@about Модуль предобработки видео-ссылок для Obsidian -> Jekyll с поддержкой ленивой загрузки.
@purpose Автоматически вычисляет одиночные и групповые видеоролики в Маркдауне.
"""

import re

def process_markdown_videos(markdown_content):
    """
    Ищет ссылки на видео и собирает их в HTML5-блоки с data-src для ленивой загрузки.
    Поддерживает одиночные и групповые журнальные видеосетки с подписями.
    """
    video_pattern = r'!\[(.*?)\]\((.*?\.(?:webm|mp4))\)'
    
    lines = markdown_content.split('\n')
    grouped_line_indices = set()
    
    # Пасс 1: Находим все групповые видео (столбики ссылок без пустых строк)
    for i in range(len(lines)):
        current_line = lines[i].strip()
        if current_line and re.search(video_pattern, current_line, re.IGNORECASE):
            is_grouped = False
            
            if i > 0 and lines[i-1].strip() and re.search(video_pattern, lines[i-1].strip(), re.IGNORECASE):
                is_grouped = True
                grouped_line_indices.add(i-1)
                
            if i < len(lines) - 1 and lines[i+1].strip() and re.search(video_pattern, lines[i+1].strip(), re.IGNORECASE):
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
            video_url = match.group(2).strip()
            
            # Базовый плеер для простых видео без alt-текста
            if not alt_text:
                return f'<video data-src="{video_url}" controls muted playsinline preload="none"></video>'
                
            parts = [p.strip() for p in alt_text.split('|') if p.strip()]
            
            # Базовый плеер, если после очистки палочек ничего не осталось
            if not parts:
                return f'<video data-src="{video_url}" controls muted playsinline preload="none"></video>'
                
            classes = []
            is_centered = False
            first_part = parts[0]
            
            if first_part.lower() == 'fig':
                classes.append('video-fig') # Наш новый класс для плееров внутри figure
                is_centered = True
                parts.pop(0)
                
                # Вложенная проверка на случай вертикального видео ![fig | v]
                if parts and parts[0].lower() == 'v':
                    classes.append('video-v')
                    parts.pop(0)
            
            # Если просто одиночное вертикальное видео без fig (например, ![v](url))
            elif first_part.lower() == 'v':
                classes.append('video-v')
                parts.pop(0)
                
            clean_alt = " | ".join(parts) if parts else ""
            class_str = f' class="{" ".join(classes)}"' if classes else ''
            
            # Собираем плеер (управляющие атрибуты железно прижаты к концу тега)
            video_html = f'<video{class_str} data-src="{video_url}" controls muted playsinline preload="none"></video>'
            
            if is_centered:
                figcaption_html = f'<figcaption class="figcaption-video">{clean_alt}</figcaption>' if clean_alt else ''
                return f'<figure class="figure-video">{video_html}{figcaption_html}</figure>'
                
            return video_html

        new_line = re.sub(video_pattern, replacer, line, flags=re.IGNORECASE)
        processed_lines.append(new_line)
        
    # === ФИНАЛЬНАЯ СКЛЕЙКА И АВТОМАТИЧЕСКАЯ ГРУППИРОВКА РЯДОВ ДЛЯ JEKYLL ===
    article_html = '\n'.join(processed_lines)
    
    def group_rows(match):
        content = match.group(1)
        if content.count('<figure class="figure-video"') > 1:
            return f'<div class="figure-video-row">{content}</div>' # Многоколоночная галерея видео
        return f'<div class="figure-video-single">{content}</div>' # Одиночное центрированное видео

    article_html = re.sub(
        r'((?:<figure class="figure-video">.*?</figure>[ \t]*\n?)+)',
        group_rows,
        article_html
    )
        
    return article_html
