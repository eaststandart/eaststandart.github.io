#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script videos.py
@about Модуль предобработки видео-ссылок для Obsidian -> Jekyll.
@purpose Находит маркдаун-ссылки на .webm и .mp4, определяет одиночные и
         групповые видео (в столбиках) и оборачивает их в контейнер .video-test-row.
"""

import re

def process_markdown_videos(markdown_content):
    """
    Ищет ссылки на видео-файлы и собирает их в блоки <div class="video-test-row">.
    """
    # Паттерн ищет стандартный маркдаун картинок, но строго с расширениями видео: .webm или .mp4
    video_pattern = r'!\[(.*?)\]\((.*?\.(?:webm|mp4))\)'
    
    # Разбиваем текст статьи на строки
    lines = markdown_content.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # Если строка является видео-ссылкой
        if line_stripped and re.match(video_pattern, line_stripped):
            video_group = []
            
            # Начинаем собирать "столбик" — все видео-ссылки, идущие подряд без пустых строк
            while i < len(lines) and lines[i].strip() and re.match(video_pattern, lines[i].strip()):
                match = re.match(video_pattern, lines[i].strip())
                alt_text = match.group(1).strip()
                video_url = match.group(2).strip()
                
                # Формируем нативный, экономичный тег плеера
                video_html = (
                    f'<video src="{video_url}" controls muted playsinline preload="none">'
                    f'</video>'
                )
                video_group.append(video_html)
                i += 1
                
            # Упаковываем всю собранную группу (или одно одиночное видео) в единый контейнер темы
            if video_group:
                container_open = '<div class="video-test-row">'
                container_close = '</div>'
                # Объединяем плееры в одну строку внутри контейнера
                full_video_block = f'{container_open}{"".join(video_group)}{container_close}'
                processed_lines.append(full_video_block)
                
            # Переходим к следующей строке, так как индекс i уже сдвинут циклом сбора группы
            continue
            
        else:
            # Если строка — обычный текст или картинка, просто оставляем её как есть
            processed_lines.append(line)
            i += 1
            
    return '\n'.join(processed_lines)
