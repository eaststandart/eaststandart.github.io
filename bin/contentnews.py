#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module contentnews
@about Изолированный целевой сборщик ленты "Что нового?" из Единого Источника Правды.
@purpose Восстанавливает каноничную логику Tracy: закрепления pinnednews, эмодзи из _pages/
         и полностью ликвидирует дублирование постов хроники.
@author TechLab
@version 3.0.0-tracy-restored
"""

import os
import sys
import re
import yaml

def load_emoji_map(root_dir):
    """Считывает эталонные эмодзи напрямую из первоисточников папки _pages/."""
    pages_dir = os.path.join(root_dir, '_pages')
    emoji_map = {}
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                try:
                    with open(os.path.join(pages_dir, file), 'r', encoding='utf-8') as f:
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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'navigation.yml')
    if not os.path.exists(nav_file_path):
        print(f"[NEWS-ERROR] Карта навигации не найдена: {nav_file_path}")
        sys.exit(1)

    with open(nav_file_path, 'r', encoding='utf-8') as nf:
        try:
            nav_data = yaml.safe_load(nf) or {}
        except Exception as e:
            print(f"[NEWS-ERROR] Сбой YAML при чтении карты сайта: {e}")
            sys.exit(1)

    pinned_posts = []
    regular_posts = []
    sections = nav_data.get('sections', {})
    
    # Загружаем карту эталонных смайликов из _pages/
    emoji_map = load_emoji_map(root_dir)

    # 🔥 ЧИСТЫЙ СБОРОЧНЫЙ ЦИКЛ БЕЗ ДУБЛИРОВАНИЯ
    for section_name, items_list in sections.items():
        if not isinstance(items_list, list): continue
        for item in items_list:
            if not isinstance(item, dict): continue
            if item.get('slug') == 'index': continue

            # Ветка 1: Сбор связанных постов журнала (journal_posts)
            if 'journal_posts' in item and isinstance(item['journal_posts'], list):
                for post in item['journal_posts']:
                    p_date = str(post.get('date', '')).strip()
                    if p_date:
                        node = {
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'date': p_date,
                            'is_post': 'true',
                            'emoji': emoji_map.get('journal', '✍\u200d🏻'),
                            'pinned': False
                        }
                        regular_posts.append(node)

            # Ветка 2: Сбор связанных постов галереи (media_posts)
            if 'media_posts' in item and isinstance(item['media_posts'], list):
                for post in item['media_posts']:
                    p_date = str(post.get('date', '')).strip()
                    if p_date:
                        node = {
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'date': p_date,
                            'is_post': 'true',
                            'emoji': emoji_map.get('media', '👀'),
                            'pinned': False
                        }
                        regular_posts.append(node)

            # Ветка 3: Сбор головных карточек контента (Автомобиль, Мультивибратор, Книги)
            item_date = str(item.get('date', '')).strip()
            if item_date:
                # Навешиваем эмодзи строго по имени раздела карточки (biblio -> 📚, faire -> 🛠)
                detected_emoji = emoji_map.get(section_name, '🛠')
                
                node = {
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'date': item_date,
                    'is_post': 'false',
                    'emoji': detected_emoji,
                    'pinned': False
                }
                
                # 🔥 КАНОНИЧЕСКОЕ ВОССТАНОВЛЕНИЕ ЗАКРЕПЛЕНИЙ PINNEDNEWS
                # Если в оригинальном md-файле стояло pinnednews: true, навигация сохраняет это свойство
                if item.get('pinnednews') is True:
                    node['pinned'] = True
                    pinned_posts.append(node)
                else:
                    regular_posts.append(node)

    # Раздельная строгая хронологическая сортировка
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Склеиваем итоговую чистую ленту: закреплённые всегда идут первыми!
    final_feed = pinned_posts + regular_posts
    
    # Запись итоговой чистой ленты новостей
    data_dir = os.path.join(root_dir, '_data')
    output_path = os.path.join(data_dir, 'news_feed.yml')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[NEWS-SUCCESS] Каноничная лента успешно собрана! Элементов в ленте: {len(final_feed)}")
    except Exception as e:
        print(f"[NEWS-ERROR] Ошибка записи news_feed.yml: {e}")
        sys.exit(1)

    # Направляем лог новостей в отслеживаемую папку артефактов _processed_files
    try:
        debug_dir = os.path.join(root_dir, '_content_files')
        os.makedirs(debug_dir, exist_ok=True)
        with open(os.path.join(debug_dir, 'contentnews_debug.log'), 'w', encoding='utf-8') as lf:
            lf.write(f"[NEWS-SUCCESS] Сборка завершена.\nВсего уникальных элементов в ленте: {len(final_feed)}\nЗакреплённых: {len(pinned_posts)}")
    except Exception as e:
        print(f"[NEWS-ERROR] Не удалось сохранить лог новостей: {e}")

if __name__ == '__main__':
    build_news_feed()
