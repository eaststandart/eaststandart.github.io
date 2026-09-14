#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module contentnews
@about Изолированный целевой сборщик ленты "Что нового?" из Единого Источника Правды.
@purpose Полностью исключает повторное сканирование диска и коллизии дат/пермалинков,
         собирая новости напрямую из готовой глобальной карты navigation.yml.
@author TechLab
@version 1.0.0-pure-source
"""

import os
import sys
import yaml

def extract_flat_feed_from_navigation():
    """Сквозной сбор абсолютно всех страниц и постов из глобальной карты навигации."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'navigation.yml')
    if not os.path.exists(nav_file_path):
        print(f"[NEWS-ERROR] Единый Источник Правды не найден по адресу: {nav_file_path}")
        sys.exit(1)

    with open(nav_file_path, 'r', encoding='utf-8') as nf:
        try:
            nav_data = yaml.safe_load(nf) or {}
        except Exception as e:
            print(f"[NEWS-ERROR] Сбой синтаксиса YAML при чтении карты сайта: {e}")
            sys.exit(1)

    flat_news = []
    sections = nav_data.get('sections', {})

    # Обходим все секции глобальной карты сайта
    for section_name, items_list in sections.items():
        for item in items_list:
            slug = item.get('slug', '')
            if slug == 'index': continue # Пропускаем заглавные вывески разделов

            # 1. Сбор связанных постов хроники проекта (массивы journal_posts, media_posts и т.д.)
            for key, val in item.items():
                if isinstance(val, list) and key.endswith('_posts'):
                    for post in val:
                        # Динамически вычисляем тип публикации по имени массива
                        post_type = key.replace('_posts', '')
                        
                        # Автомат значков: подтягиваем эмодзи строго из вывески типа в _pages/
                        # (Например, если post_type == 'journal', то рука ✍🏻, если 'media' — глаза 👀)
                        # Так как они уже обработаны navigation.py, мы можем безопасно доверять структуре
                        flat_news.append({
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'date': str(post.get('date', '')),
                            'is_post': 'true',
                            'section': section_name,
                            'type': post_type
                        })

            # 2. Сбор самостоятельных карточек контента (книги, проекты, автономные посты вроде Мультивибратора)
            # Если у узла есть дата, значит это самостоятельное событие для ленты новостей
            if item.get('date') or (section_name == 'reference' and not item.get('date')):
                # Восстанавливаем дату автономного поста, если она была извлечена navigation.py
                item_date = str(item.get('date', ''))
                if not item_date and 'date' in item:
                    item_date = str(item['date'])
                
                flat_news.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'date': item_date if item_date else '2026-01-01',
                    'is_post': 'false',
                    'section': section_name,
                    'type': 'page'
                })

    return flat_news, root_dir

def load_emoji_map(root_dir):
    """Считывает эталонные эмодзи напрямую из первоисточников папки _pages/."""
    pages_dir = os.path.join(root_dir, '_pages')
    emoji_map = {}
    
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                file_path = os.path.join(pages_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    if match:
                        data = yaml.safe_load(match.group(1))
                        if data and data.get('emoji'):
                            p_slug, _ = os.path.splitext(file)
                            emoji_map[p_slug] = data['emoji']
                except:
                    pass
    return emoji_map

def build_news_feed():
    """Диспетчер сборщика: упаковывает, сортирует и выгружает ленту 'Что нового?'."""
    # Шаг 1: Извлекаем плоский список публикаций из Единого Источника Правды
    flat_items, root_dir = extract_flat_feed_from_navigation()
    
    # Шаг 2: Загружаем карту эталонных эмодзи из _pages/
    emoji_map = load_emoji_map(root_dir)
    
    # Шаг 3: Навешиваем эмодзи на каждую новость строго по первоисточникам
    final_feed = []
    for item in flat_items:
        # По умолчанию берем эмодзи по типу поста (journal -> ✍🏻, media -> 👀)
        # Если это самостоятельная карточка (page) — берем эмодзи по имени её секции (biblio -> 📚, people -> 🧍‍♂️)
        lookup_key = item['type'] if item['is_post'] == 'true' else item['section']
        detected_emoji = emoji_map.get(lookup_key, "")
        
        final_feed.append({
            'title': item['title'],
            'url': item['url'],
            'date': item['date'],
            'is_post': item['is_post'],
            'emoji': detected_emoji,
            'pinned': False # Базовый флаг закрепления новостей
        })
        
    # Шаг 4: Железная хронологическая сортировка от самых свежих к самым старым
    final_feed.sort(key=lambda x: x['date'], reverse=True)
    
    # Запись готовой ленты для движка Jekyll
    data_dir = os.path.join(root_dir, '_data')
    output_path = os.path.join(data_dir, 'news_feed.yml')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[NEWS-SUCCESS] Лента новостей 'What's New' успешно собрана напрямую из карты навигации!")
        print(f"[NEWS-SUCCESS] Всего обработано событий в ленту: {len(final_feed)}")
    except Exception as e:
        print(f"[NEWS-ERROR] Не удалось записать файл news_feed.yml: {e}")
        sys.exit(1)

    # Выгрузка серверного лога контента в артефакты
    content_debug_dir = os.path.join(root_dir, '_content_files')
    os.makedirs(content_debug_dir, exist_ok=True)
    
    try:
        with open(os.path.join(content_debug_dir, 'content_debug.log'), 'w', encoding='utf-8') as lf:
            lf.write(f"[NEWS-SUCCESS] Лента новостей сформирована на чистом автомате.\nКоличество записей: {len(final_feed)}")
    except:
        pass

if __name__ == '__main__':
    import re
    build_news_feed()
