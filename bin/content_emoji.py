#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content_emoji
@about Подмодуль контента №2: Автомат значков по первоисточникам.
@purpose Собирает эмодзи строго из файлов-вывесок _pages/ и родительских index.md.
@author TechLab
@version 1.0.0-pure-emoji
"""

import os
import re
import yaml

def load_emoji_sources(root_dir, parse_yaml_fn):
    """Сканирует вывески _pages и заглавные файлы разделов для сбора эталонных эмодзи."""
    pages_dir = os.path.join(root_dir, '_pages')
    page_types_emoji = {}
    section_index_emoji = {}

    # Сбор эмодзи типов постов из _pages/
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                p_data, _, _ = parse_yaml_fn(os.path.join(pages_dir, file))
                if p_data and p_data.get('emoji'):
                    p_slug, _ = os.path.splitext(file)
                    page_types_emoji[p_slug] = p_data['emoji']

    # Сбор родительских эмодзи из index.md корневых папок контента
    EXCLUDED = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and name not in EXCLUDED and not name.startswith('.'):
            idx_path = os.path.join(root_dir, name, 'index.md')
            if os.path.exists(idx_path):
                i_data, _, _ = parse_yaml_fn(idx_path)
                if i_data and i_data.get('emoji'):
                    section_index_emoji[name.lstrip('_')] = i_data['emoji']

    return page_types_emoji, section_index_emoji

def calculate_item_emoji(data, folder_parts, page_types_emoji, section_index_emoji):
    """Определяет идеальный эмодзи строки ленты строго по закону Tracy."""
    section_name = data.get('section', folder_parts.lstrip('_'))
    
    if folder_parts == '_posts':
        # Очередь 1: Посты хроники — берут эмодзи из вывесок типов в _pages/ (👀 или ✍🏻)
        post_type = data.get('post-page', 'journal')
        return page_types_emoji.get(post_type, "")
        
    elif section_name in section_index_emoji:
        # Очередь 3: Книги/статьи Режима А — нативно наследуют эмодзи родительской вывески раздела (📚)
        return section_index_emoji.get(section_name, "")
        
    else:
        # Очередь 2: Карточки проектов Режима Б — берут свой родной эмодзи из Front Matter страницы
        return data.get('emoji', "")
