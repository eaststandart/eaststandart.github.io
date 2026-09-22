#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module smPropsIn
@about Затягивание свойств Obsidian в карту сайта
@purpose Пробегает по готовому каркасу ссылок конвейера в оперативной памяти и обогащает ноды кастомными метаданными Front Matter заметок.
@author TechLab
@version 1.0.0
"""

def enrich_sitemap_properties(sitemap_flat_map):
    """Принимает сквозную карту памяти конвейера и затягивает в ноды свойства Obsidian."""
    if not sitemap_flat_map:
        return sitemap_flat_map

    # Список кастомных текстовых свойств Obsidian, которые строго должны попасть в sitemap.yml
    SITEMAP_PROPERTIES = ['crumbtitle', 'emoji', 'posttype']

    for file_key, passport in sitemap_flat_map.items():
        # Технический ключ списка папок игнорируем
        if file_key == 'detected_root_folders': 
            continue

        node = passport.get('node', {})
        front_data = passport.get('front_matter', {})

        if not node or not front_data:
            continue

        # Сквозной нативный перенос свойств Obsidian внутрь ноды памяти карты сайта
        for prop in SITEMAP_PROPERTIES:
            if front_data.get(prop):
                val_clean = str(front_data[prop]).strip()
                if val_clean:
                    node[prop] = front_data[prop]

    return sitemap_flat_map
