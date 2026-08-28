#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script videos.py
@about Модуль предобработки видео-ссылок для Obsidian -> Jekyll с поддержкой ленивой загрузки.
"""

import re

def process_markdown_videos(markdown_content):
    """
    Ищет ссылки на видео и собирает их в блоки с data-src для ленивой загрузки.
    """
    video_pattern = r'!\[(.*?)\]\((.*?\.(?:webm|mp4))\)'
    
    lines = markdown_content.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        if line_stripped and re.match(video_pattern, line_stripped, re.IGNORECASE):
            video_group = []
            
            while i < len(lines) and lines[i].strip() and re.match(video_pattern, lines[i].strip(), re.IGNORECASE):
                match = re.match(video_pattern, lines[i].strip(), re.IGNORECASE)
                video_url = match.group(2).strip()
                
                # ТВОЯ ЛОГИКА: Пишем data-src вместо src, чтобы JS активировал плеер за 200px до экрана!
                video_html = (
                    f'<video data-src="{video_url}" controls muted playsinline preload="none">'
                    f'</video>'
                )
                video_group.append(video_html)
                i += 1
                
            if video_group:
                processed_lines.append(f'<div class="video-test-row">{"".join(video_group)}</div>')
            continue
        else:
            processed_lines.append(line)
            i += 1
            
    return '\n'.join(processed_lines)
