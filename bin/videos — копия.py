#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script videos.py
@about Модуль предобработки видео-ссылок для Obsidian -> Jekyll с поддержкой ленивой загрузки.
@purpose Автоматически вычисляет одиночные и групповые видеоролики в Маркдауне.
         Ключевое слово для центрирования и figure изменено с 'center' на 'fig'.
         Добавлена автоматическая генерация SEO-атрибута title для всех плееров.
"""

import re

def process_markdown_videos(markdown_content):
    """
    Ищет ссылки на видео и собирает их в HTML5-блоки с data-src для ленивой загрузки.
    Поддерживает одиночные и групповые журнальные видеосетки с подписями,
    а также собирает простые видео без ключей во флекс-ряды .video-row.
    """
    video_pattern = r'!\[(.*?)\]\((.*?\.(?:webm|mp4))\)'
    
    lines = markdown_content.split('\n')
    fig_line_indices = set()
    
    # Пасс 1: Заранее находим все строки, где ЯВНО запрошен журнальный ключ fig
    for i in range(len(lines)):
        current_line = lines[i].strip()
        if current_line and re.search(video_pattern, current_line, re.IGNORECASE):
            match = re.search(video_pattern, current_line, re.IGNORECASE)
            alt_text = match.group(1).strip()
            parts = [p.strip() for p in alt_text.split('|') if p.strip()]
            if parts and parts[0].lower() == 'fig':
                fig_line_indices.add(i)

    # Пасс 2: Построчная обработка контента с умной группировкой
    processed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # Если строка пустая — просто пропускаем её дальше
        if not line_stripped:
            processed_lines.append(line)
            i += 1
            continue
            
        # Проверяем, является ли строка видеороликом
        is_video = re.match(video_pattern, line_stripped, re.IGNORECASE)
        
        if is_video:
            # СИТУАЦИЯ А: Это журнальное видео с ключом fig
            if i in fig_line_indices:
                match = re.match(video_pattern, line_stripped, re.IGNORECASE)
                alt_text = match.group(1).strip()
                video_url = match.group(2).strip()
                parts = [p.strip() for p in alt_text.split('|') if p.strip()]
                
                classes = ['video-fig']
                parts.pop(0) # Удаляем 'fig'
                
                # Вложенная проверка на вертикалку ![fig | v]
                if parts and parts[0].lower() == 'v':
                    classes.append('video-v')
                    parts.pop(0)
                    
                # Отсекаем цифры размера Обсидиана в конце
                if parts and re.match(r'^\d+$', parts[-1]):
                    parts.pop()
                    
                clean_alt = " | ".join(parts) if parts else ""
                class_str = f' class="{" ".join(classes)}"'
                # Формируем title, если текст описания существует
                title_str = f' title="{clean_alt}"' if clean_alt else ''
                
                # Собираем плеер с атрибутом title контента
                video_html = f'<video{class_str}{title_str} data-src="{video_url}" controls muted playsinline preload="none"></video>'
                figcaption_html = f'<figcaption class="figcaption-video">{clean_alt}</figcaption>' if clean_alt else ''
                
                processed_lines.append(f'<figure class="figure-video">{video_html}{figcaption_html}</figure>')
                i += 1
                
            # СИТУАЦИЯ Б: Это простые видеоролики без ключа fig (Собираем в группу!)
            else:
                video_group = []
                while i < len(lines) and lines[i].strip() and re.match(video_pattern, lines[i].strip(), re.IGNORECASE) and (i not in fig_line_indices):
                    match = re.match(video_pattern, lines[i].strip(), re.IGNORECASE)
                    alt_text = match.group(1).strip()
                    video_url = match.group(2).strip()
                    parts = [p.strip() for p in alt_text.split('|') if p.strip()]
                    
                    classes = []
                    if parts and parts[0].lower() == 'v':
                        classes.append('video-v')
                        parts.pop(0)
                        
                    # Отсекаем цифры размера
                    if parts and re.match(r'^\d+$', parts[-1]):
                        parts.pop()
                        
                    clean_alt = " | ".join(parts) if parts else ""
                    class_str = f' class="{" ".join(classes)}"' if classes else ''
                    # Формируем title, если текст описания существует
                    title_str = f' title="{clean_alt}"' if clean_alt else ''
                    
                    # Собираем плеер с атрибутом title контента
                    video_html = f'<video{class_str}{title_str} data-src="{video_url}" controls muted playsinline preload="none"></video>'
                    video_group.append(video_html)
                    i += 1
                    
                if video_group:
                    processed_lines.append(f'<div class="video-row">{"".join(video_group)}</div>')
        else:
            # Обычный текст, заголовки, списки
            processed_lines.append(line)
            i += 1
            
    # === ФИНАЛЬНЫЙ ПАСС: Автоматическая группировка рядов figure-video ДЛЯ JEKYLL ===
    article_html = '\n'.join(processed_lines)
    
    def group_rows(match):
        content = match.group(1)
        if content.count('<figure class="figure-video"') > 1:
            return f'<div class="figure-video-row">{content}</div>' 
        return f'<div class="figure-video-single">{content}</div>' 

    article_html = re.sub(
        r'((?:<figure class="figure-video">.*?</figure>[ \t]*\n?)+)',
        group_rows,
        article_html
    )
        
    return article_html
