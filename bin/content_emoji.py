#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content_emoji
@about Подмодуль контента №2: Автомат значков.
@purpose Собирает эмодзи строго из первоисточников папки _pages/ и файлов-вывесок.
@author TechLab
"""

import os
import re
import yaml

def load_pages_emoji_map(root_dir):
    """Сканирует папку _pages/ и собирает карту эмодзи для разделов и типов постов."""
    pages_dir = os.path.join(root_dir, '_pages')
    emoji_map = {}
    
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if not file.endswith('.md'): continue
            
            full_path = os.path.join(pages_dir, file)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if match:
                    data = yaml.safe_load(match.group(1))
                    if data and data.get('emoji'):
                        p_slug, _ = os.path.splitext(file)
                        emoji_map[p_slug] = data['emoji']
            except Exception as e:
                print(f"[CON-ERROR] Не удалось прочитать эмодзи из вывески {file}: {e}")
                
    return emoji_map

def calculate_item_emoji(data, folder_parts, pages_emoji_map):
    """Определяет идеальный эмодзи для строки ленты новостей по вашему жесткому закону."""
    # Очередь 1: Посты хроники из папки _posts — берут эмодзи строго из вывесок journal.md или media.md
    if folder_parts == '_posts':
        post_type = data.get('post-page', 'journal')
        return pages_emoji_map.get(post_type, "")
        
    # Очередь 2 и 3: Любые другие страницы разделов — нативно берут эмодзи из файла своего раздела в _pages/
    section_name = data.get('section', folder_parts.lstrip('_'))
    return pages_emoji_map.get(section_name, "")
