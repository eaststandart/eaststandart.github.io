#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml

def extract_flat_feed_from_navigation():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'navigation.yml')
    if not os.path.exists(nav_file_path):
        print(f"[NEWS-ERROR] Единый Источник Правды не найден: {nav_file_path}")
        sys.exit(1)

    with open(nav_file_path, 'r', encoding='utf-8') as nf:
        try:
            nav_data = yaml.safe_load(nf) or {}
        except Exception as e:
            print(f"[NEWS-ERROR] Сбой YAML: {e}")
            sys.exit(1)

    flat_news = []
    sections = nav_data.get('sections', {})

    for section_name, items_list in sections.items():
        for item in items_list:
            slug = item.get('slug', '')
            if slug == 'index': continue

            # 1. Сбор связанных постов хроники проекта
            for key, val in item.items():
                if isinstance(val, list) and key.endswith('_posts'):
                    for post in val:
                        post_date = str(post.get('date', '')).strip()
                        if not post_date: continue
                        
                        post_type = key.replace('_posts', '')
                        flat_news.append({
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'date': post_date,
                            'is_post': 'true',
                            'section': section_name,
                            'type': post_type
                        })

            # 2. Сбор самостоятельных карточек контента (Мультивибратор, Автомобиль)
            item_date = str(item.get('date', '')).strip()
            # Пропускаем пустые кавычки, берем только реальные даты проектов
            if item_date:
                flat_news.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'date': item_date,
                    'is_post': 'false',
                    'section': section_name,
                    'type': 'page'
                })

    return flat_news, root_dir

def load_emoji_map(root_dir):
    pages_dir = os.path.join(root_dir, '_pages')
    emoji_map = {}
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                try:
                    with open(os.path.join(pages_dir, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                    import re
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
    flat_items, root_dir = extract_flat_feed_from_navigation()
    emoji_map = load_emoji_map(root_dir)
    
    final_feed = []
    for item in flat_items:
        lookup_key = item['type'] if item['is_post'] == 'true' else item['section']
        detected_emoji = emoji_map.get(lookup_key, "")
        
        final_feed.append({
            'title': item['title'],
            'url': item['url'],
            'date': item['date'],
            'is_post': item['is_post'],
            'emoji': detected_emoji,
            'pinned': False
        })
        
    final_feed.sort(key=lambda x: x['date'], reverse=True)
    
    data_dir = os.path.join(root_dir, '_data')
    output_path = os.path.join(data_dir, 'news_feed.yml')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[NEWS-SUCCESS] Всего обработано событий в ленту: {len(final_feed)}")
    except Exception as e:
        print(f"[NEWS-ERROR] Ошибка записи news_feed.yml: {e}")
        sys.exit(1)

    # НАПРАВЛЯЕМ ЛОГ СТРОГО В КАНОНИЧНУЮ ПАПКУ АРТЕФАКТОВ
    debug_dir = os.path.join(root_dir, '_processed_files')
    os.makedirs(debug_dir, exist_ok=True)
    try:
        with open(os.path.join(debug_dir, 'contentnews_debug.log'), 'w', encoding='utf-8') as lf:
            lf.write(f"[NEWS-SUCCESS] Лента новостей сформирована из карты навигации.\nКоличество записей: {len(final_feed)}")
    except:
        pass

if __name__ == '__main__':
    build_news_feed()
