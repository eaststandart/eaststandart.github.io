#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content_nav
@about Подмодуль контента №1: Универсальный навигационный сопоставитель.
@purpose Забирает адреса строго по сквозному закону приоритетов: permalink -> карта сайта -> .html
@author TechLab
@version 2.0.0-universal-law
"""

def find_url_in_navigation(nav_data, project_slug, file_name_clean, folder_parts, data):
    """Вычисляет идеальный интернет-адрес по общему сквозному правилу приоритетов."""
    
    # 🔥 ШАГ 1 (АБСОЛЮТНЫЙ ПРИОРИТЕТ): Если в самом файле руками прописан permalink — берем его!
    if data and data.get('permalink'):
        return data['permalink']

    # ШАГ 2 (ПОИСК ПО КАРТЕ): Если ручного пермалинка нет, ищем совпадение в navigation.yml
    if folder_parts == '_posts':
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
