#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content_nav
@about Подмодуль контента №1: Навигационный сопоставитель.
@purpose Ищет идеальные интернет-адреса страниц внутри карты navigation.yml.
@author TechLab
@version 1.0.0-pure-navigation
"""

def find_url_in_navigation(nav_data, project_slug, file_name_clean, folder_parts, data):
    """Ищет идеальный, готовый интернет-адрес страницы внутри карты navigation.yml."""
    # Если это пост хроники из папки _posts
    if folder_parts[0] == '_posts':
        post_date = str(data.get('date', ''))
        # Проверяем все разделы карты навигации
        for section_name, projects in nav_data.get('sections', {}).items():
            for proj in projects:
                if proj.get('slug') == project_slug:
                    # Ищем пост во вкладках journal или media данного проекта
                    for key in ['journal_posts', 'media_posts']:
                        if key in proj:
                            for post in proj[key]:
                                if post.get('date') == post_date and file_name_clean in post.get('url', ''):
                                    return post.get('url')

    # Если это обычная карточка контента внутри разделов
    else:
        for section_name, projects in nav_data.get('sections', {}).items():
            for proj in projects:
                if proj.get('slug') == project_slug:
                    return proj.get('url')
                    
    return None
