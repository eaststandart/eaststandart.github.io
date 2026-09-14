#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module contentnews
@about Изолированный целевой сборщик ленты "Что нового?" из Единого Источника Правды.
@purpose Собирает новости строго из navigation.yml по прямым ключам массивов.
@version 2.0.0-pure-arrays-verified
"""

import os
import sys
import yaml

def build_news_feed():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'navigation.yml')
    if not os.path.exists(nav_file_path):
        print(f"[NEWS-ERROR] Карта навигации не найдена: {nav_file_path}")
        sys.exit(1)

    with open(nav_file_path, 'r', encoding='utf-8') as nf:
        nav_data = yaml.safe_load(nf) or {}

    flat_news = []
    sections = nav_data.get('sections', {})

    # 🔥 ПРЯМОЙ СТРОГИЙ ОБХОД КАРТЫ НАВИГАЦИИ БЕЗ ВЛОЖЕННЫХ ЦИКЛОВ КЛЮЧЕЙ
    for section_name, items_list in sections.items():
        if not isinstance(items_list, list): continue
        for item in items_list:
            if not isinstance(item, dict): continue
            if item.get('slug') == 'index': continue

            # Ветка 1: Извлекаем посты журнала (journal_posts)
            if 'journal_posts' in item and isinstance(item['journal_posts'], list):
                for post in item['journal_posts']:
                    p_date = str(post.get('date', '')).strip()
                    if p_date:
                        flat_news.append({
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'date': p_date,
                            'is_post': 'true',
                            'emoji': '✍\u200d🏻',
                            'pinned': False
                        })

            # Ветка 2: Извлекаем посты галереи (media_posts)
            if 'media_posts' in item and isinstance(item['media_posts'], list):
                for post in item['media_posts']:
                    p_date = str(post.get('date', '')).strip()
                    if p_date:
                        flat_news.append({
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'date': p_date,
                            'is_post': 'true',
                            'emoji': '👀',
                            'pinned': False
                        })

            # Ветка 3: Извлекаем головные карточки проектов (Автомобиль, Мультивибратор)
            item_date = str(item.get('date', '')).strip()
            if item_date:
                # Назначаем эмодзи по умолчанию в зависимости от раздела карточки
                default_emoji = '📚' if section_name == 'biblio' else ('🧍‍♂️' if section_name == 'people' else '🛠')
                flat_news.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'date': item_date,
                    'is_post': 'false',
                    'emoji': default_emoji,
                    'pinned': False
                })

    # Сортировка от самых свежих к самым старым
    flat_news.sort(key=lambda x: x['date'], reverse=True)
    
    # Запись итоговой ленты новостей
    data_dir = os.path.join(root_dir, '_data')
    output_path = os.path.join(data_dir, 'news_feed.yml')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed if 'final_feed' in locals() else flat_news}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[NEWS-SUCCESS] Лента успешно собрана! Обработано событий: {len(flat_news)}")
    except Exception as e:
        print(f"[NEWS-ERROR] Ошибка записи news_feed.yml: {e}")
        sys.exit(1)

    # ВЫГРУЗКА ЛОГА В КОРЕНЬ РЕПОЗИТОРИЯ БЕЗ КОНФЛИКТОВ ПРАВ ДОСТУПА
    try:
        with open(os.path.join(root_dir, 'contentnews_debug.log'), 'w', encoding='utf-8') as lf:
            lf.write(f"[NEWS-SUCCESS] Сборка завершена. Всего элементов в ленте: {len(flat_news)}")
    except:
        pass

if __name__ == '__main__':
    build_news_feed()
