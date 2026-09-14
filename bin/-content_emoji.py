#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content_emoji
@about Подмодуль контента №2: Автомат значков по первоисточникам.
@purpose Собирает эмодзи строго из файлов-вывесок _pages/ и родительских index.md.
@author TechLab
@version 2.1.0-perfect-match
"""

import os
import re
import yaml

def load_emoji_sources(root_dir, parse_yaml_fn):
    """Сканирует вывески _pages и заглавные файлы разделов для сбора эталонных эмодзи."""
    pages_dir = os.path.join(root_dir, '_pages')
    page_types_emoji = {}
    section_index_emoji = {}

    # 1. Сбор эмодзи абсолютно всех вывесок из _pages/
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                p_data, _, _ = parse_yaml_fn(os.path.join(pages_dir, file))
                if p_data and p_data.get('emoji'):
                    p_slug, _ = os.path.splitext(file)
                    page_types_emoji[p_slug] = p_data['emoji']

    # 2. Сбор родительских эмодзи из index.md корневых папок контента
    EXCLUDED = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and name not in EXCLUDED and not name.startswith('.'):
            idx_path = os.path.join(root_dir, name, 'index.md')
            if os.path.exists(idx_path):
                i_data, _, _ = parse_yaml_fn(idx_path)
                if i_data and i_data.get('emoji'):
                    section_index_emoji[name.lstrip('_')] = i_data['emoji']

    return page_types_emoji, section_index_emoji

def calculate_item_emoji(data, folder_parts, page_types_emoji, root_dir, parse_yaml_fn):
    """Определяет эмодзи строки ленты строго по вашему правилу folder_parts[0]."""
    # Извлекаем чистую строку первой папки, как это сделано в вашем content.py
    first_folder = folder_parts[0] if isinstance(folder_parts, list) and len(folder_parts) > 0 else str(folder_parts)
    clean_folder_name = first_folder.lstrip('_')

    # Очередь 1: Посты хроники — берут эмодзи из вывесок типов в _pages/ (👀 или ✍🏻)
    if first_folder == '_posts':
        post_type = data.get('post-page')
        return page_types_emoji.get(post_type, "")

    # Очередь 2 и 3: Проверяем наличие файла index.md в корне папки контента на диске
    section_dir = os.path.join(root_dir, first_folder)
    has_index = os.path.exists(os.path.join(section_dir, 'index.md')) or os.path.exists(os.path.join(section_dir, 'index.html'))

    if has_index:
        # Режим А: Индекс есть (как в biblio) — нативно считываем эмодзи прямо из этого файла index.md
        idx_path = os.path.join(section_dir, 'index.md')
        if not os.path.exists(idx_path):
            idx_path = os.path.join(section_dir, 'index.html')
        
        try:
            i_data, _, _ = parse_yaml_fn(idx_path)
            if i_data and i_data.get('emoji'):
                return i_data['emoji']
        except:
            pass
        return ""
    else:
        # Режим Б: Индекса нет (как в faire или people) — берем эмодзи из файла-вывески в _pages/
        return page_types_emoji.get(clean_folder_name, "")
