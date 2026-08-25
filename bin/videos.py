#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script videos.py
@about Модуль предобработки видео-ссылок для Obsidian -> Jekyll.
@purpose Находит маркдаун-ссылки на видео (.webm, .mp4), определяет одиночные и
         групповые видео (в столбиках) и оборачивает их в контейнер .video-test-row.
"""

import re

def process_markdown_videos(markdown_content):
    """
    Ищет ссылки на видео-файлы и собирает их в блоки <div class="video-test-row">.
    """
    # Паттерн ищет стандартный маркдаун, но строго с расширениями видео: .webm или .mp4 (регистронезависимо)
    video_pattern = r'!\[(.*?)\]\((.*?\.(?:webm|mp4))\)'
    
    lines = markdown_content.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # Используем re.IGNORECASE, чтобы ловить и .WEBM, и .mp4
        if line_stripped and re.match(video_pattern, line_stripped, re.IGNORECASE):
            video_group = []
            
            # Собираем "столбик" — все видео-ссылки, идущие подряд без пустых строк
            while i < len(lines) and lines[i].strip() and re.match(video_pattern, lines[i].strip(), re.IGNORECASE):
                match = re.match(video_pattern, lines[i].strip(), re.IGNORECASE)
                alt_text = match.group(1).strip()
                video_url = match.group(2).strip()
                
                # Формируем нативный тег плеера
                video_html = (
                    f'<video src="{video_url}" controls muted playsinline preload="none">'
                    f'</video>'
                )
                video_group.append(video_html)
                i += 1
                
            if video_group:
                container_open = '<div class="video-test-row">'
                container_close = '</div>'
                full_video_block = f'{container_open}{"".join(video_group)}{container_close}'
                processed_lines.append(full_video_block)
                
            continue
            
        else:
            processed_lines.append(line)
            i += 1
            
    return '\n'.join(processed_lines)
