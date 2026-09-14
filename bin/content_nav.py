#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content_nav
@about Подмодуль контента №1: Универсальный навигационный сопоставитель.
@purpose Забирает адреса строго по сквозному закону приоритетов: permalink -> карта сайта -> .html
@author TechLab
@version 2.0.0-universal-law
"""

def find_url_and_date_in_navigation(nav_data, project_slug, file_name_clean, folder_parts, data):
    """Возвращает кортеж (url, date) напрямую из глобальной карты навигации."""
    
    # Шаг 1: Если в самом файле руками прописан жесткий пермалинк
    if data and data.get('permalink'):
        return data['permalink'], str(data.get('date', ''))

    # Шаг 2: Поиск постов хроники в navigation.yml
    first_folder = folder_parts[0] if isinstance(folder_parts, list) and len(folder_parts) > 0 else str(folder_parts)
    
    if first_folder == '_posts':
        for section_name, projects in nav_data.get('sections', {}).items():
            for proj in projects:
                if proj.get('slug') == project_slug:
                    for key in ['journal_posts', 'media_posts']:
                        if key in proj:
                            for post in proj[key]:
                                # Сопоставляем по очищенному имени файла в URL
                                if file_name_clean in post.get('url', ''):
                                    # Возвращаем URL и эталонную дату, которую зафиксировал navigation.py
                                    return post.get('url'), post.get('date', '')

    # Шаг 3: Поиск обычных карточек контента внутри разделов
    else:
        for section_name, projects in nav_data.get('sections', {}).items():
            for proj in projects:
                if proj.get('slug') == project_slug:
                    return proj.get('url'), str(data.get('date', ''))
                    
    return None, None
