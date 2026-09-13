#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content_nav
@about Подмодуль контента №1: Навигационный сопоставитель.
@purpose Ищет идеальные интернет-адреса страниц внутри карты navigation.yml.
@author TechLab
"""

import re

def find_url_in_navigation(nav_data, project_slug, file_name_clean, folder_parts, data):
    """Сопоставляет файл на диске с его точным URL из верховной карты навигации."""
    # Очередь А: Если это пост хроники из папки _posts
    if folder_parts == '_posts':
        post_date = str(data.get('date', ''))
        for section_name, projects in nav_data.get('sections', {}).items():
            for proj in projects:
                if proj.get('slug') == project_slug:
                    for key in ['journal_posts', 'media_posts']:
                        if key in proj:
                            for post in proj[key]:
                                if post.get('date') == post_date and file_name_clean in post.get('url', ''):
                                    return post.get('url')

    # Очередь Б: Если это обычная карточка проекта или книга внутри разделов
    else:
        for section_name, projects in nav_data.get('sections', {}).items():
            for proj in projects:
                if proj.get('slug') == project_slug:
                    return proj.get('url')
                    
    return None
