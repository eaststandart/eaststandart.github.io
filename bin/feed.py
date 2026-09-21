#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module feed
@about Изолированный монолитный сборщик единой ленты обновлений из Источника Правды.
@purpose Автоматически вычисляет типы, проекты и наследует эмодзи на основе URL карты навигации,
         выгружая универсальный файл данных _data/feed.yml для нужд Jekyll и Liquid.
@author TechLab
@version 2.1.0-safe-baskets
"""

import os
import sys
import yaml

def build_universal_feed():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'navigation.yml')
    output_feed_path = os.path.join(root_dir, '_data', 'feed.yml')
    log_dir_path = os.path.join(root_dir, '_feed_files')
    
    if not os.path.exists(nav_file_path):
        print(f"[FEED-ERROR] Единый Источник Правды не найден по пути: {nav_file_path}")
        return

    try:
        with open(nav_file_path, 'r', encoding='utf-8') as f:
            nav_data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[FEED-ERROR] Сбой YAML при чтении карты сайта: {e}")
        return

    log_buffer = []
    log_buffer.append("=========================================================================")
    log_buffer.append("СТАРТ СЕРВЕРНОГО АУДИТА ЕДИНОЙ ЛЕНТЫ ОБНОВЛЕНИЙ FEED.YML")
    log_buffer.append("=========================================================================\n")

    pinned_posts = []
    regular_posts = []

    # 🟢 ШАГ 1: КЭШИРУЕМ ЗНАЧКИ ЭМОДЗИ ИЗ ГОЛОВНЫХ РАЗДЕЛОВ КАРТЫ НАВИГАЦИИ
    section_emojis = {}
    for key, items in nav_data.items():
        if key == 'detected_root_folders':
            continue
        if '/' not in key and isinstance(items, list) and len(items) > 0:
            section_card = items[0]
            if isinstance(section_card, dict) and section_card.get('emoji'):
                # Очищаем имя ключа от приставки feed- для 100% совместимости с Шагом 2
                clean_key = key.replace('feed-', '').strip().lower()
                section_emojis[clean_key] = section_card['emoji']

    # 🟢 ШАГ 2: СКВОЗНОЙ СБОР И НАЙТИВНОЕ РАСПОЗНАВАНИЕ ТИПОВ ИЗ URL
    for file_key, nodes in nav_data.items():
        if file_key == 'detected_root_folders':
            continue
            
        if not isinstance(nodes, list) or len(nodes) == 0:
            continue
            
        passport = nodes[0] if isinstance(nodes, list) and len(nodes) > 0 else nodes
        if not isinstance(passport, dict):
            continue

        item_date = str(passport.get('date', '')).strip()
        if not item_date or item_date == 'None':
            continue

        item_url = passport.get('url', '').strip('/')
        
        post_type = ""
        project_slug = ""
        is_post_flag = 'false'

        # Если файл лежит в папке _posts или его URL содержит структуру постов хроники
        if file_key.startswith('_posts/') and item_url:
            url_parts = item_url.split('/')
            if len(url_parts) >= 2:
                # Нативно вырезаем тип контента сайта (journal/media) и слаг проекта из адреса!
                post_type = url_parts[0]
                project_slug = url_parts[1]
                is_post_flag = 'true'
        else:
            # Для обычных карточек проектов определяем слаг по финалу URL
            if item_url:
                project_slug = item_url.split('/')[-1]

        # Вычисляем имя родителя строго по полям связи карты
        target_section = post_type
        if not target_section:
            target_section = passport.get('relatedsection', '')
        if not target_section:
            target_section = passport.get('relatedcollection', '')

        # Нативно наследуем эмодзи из кэша разделов по вычисленному родителю
        calculated_emoji = passport.get('emoji', '')
        if not calculated_emoji and target_section:
            calculated_emoji = section_emojis.get(target_section, "")

        # Всеядный очиститель синтаксиса pinnedfeed
        raw_pinned = passport.get('pinnedfeed', False)
        pinned_list = []
        if isinstance(raw_pinned, list):
            pinned_list = [str(x).strip().lower() for x in raw_pinned]
        elif isinstance(raw_pinned, str):
            clean_str = raw_pinned.replace('[', '').replace(']', '').replace("'", "").replace('"', '')
            pinned_list = [x.strip().lower() for x in clean_str.split(',') if x.strip()]
        elif raw_pinned is True:
            pinned_list = ['news', str(post_type).strip().lower()]

        node = {
            'title': passport.get('title', 'Без названия'),
            'url': passport.get('url', ''),
            'date': item_date,
            'posttype': post_type,
            'related': project_slug,
            'is_post': is_post_flag,
            'emoji': calculated_emoji,
            'personal_emoji': passport.get('emoji', ''),  # Сохраняем чистый знак из Obsidian
            'pinned_list': pinned_list
        }

        # Первичное разделение по оригинальной схеме для сохранения закрепов
        if 'news' in pinned_list or (str(post_type).strip().lower() in pinned_list if post_type else False):
            pinned_posts.append(node)
        else:
            regular_posts.append(node)

    # 🟢 ШАГ 3: УНИВЕРСАЛЬНАЯ СОРТИРОВКА И ПЕРЕНОС В ОБОСОБЛЕННЫЕ КОРЗИНЫ
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    final_feed = pinned_posts + regular_posts

    # Динамически инициализируем корзины и дефолтные значки по пермалинкам ключей feed-
    baskets = {'news': []}
    feed_section_emojis = {}

    for key, items in nav_data.items():
        if key.startswith('feed-') and isinstance(items, list) and len(items) > 0:
            sect_card = items[0]
            if isinstance(sect_card, dict) and sect_card.get('url'):
                b_name = sect_card['url'].strip('/')
                if b_name:
                    baskets[b_name] = []
                    if sect_card.get('emoji'):
                        feed_section_emojis[b_name] = sect_card['emoji']

    # Наполняем изолированные корзины из готового массива final_feed
    for f_item in final_feed:
        c_posttype = str(f_item['posttype']).strip().lower()

        # А. Наполнение Главной корзины news (сохраняем абсолютно все эмодзи)
        is_pinned_news = 'news' in f_item['pinned_list']
        node_news = {
            'title': f_item['title'],
            'url': f_item['url'],
            'date': f_item['date'],
            'posttype': f_item['posttype'],
            'related': f_item['related'],
            'is_post': f_item['is_post'],
            'emoji': f_item['emoji'],
            'personal_emoji': f_item['personal_emoji'],
            'pinned': is_pinned_news
        }
        baskets['news'].append(node_news)

        # Б. Наполнение частной корзины текущего раздела
        if c_posttype in baskets:
            is_pinned_own = c_posttype in f_item['pinned_list']
            default_section_emoji = feed_section_emojis.get(c_posttype, "")
            
            # Бэкенд-очистка шума: убираем эмодзи, только если он унаследован, а ручного в Obsidian нет
            final_own_emoji = f_item['emoji']
            if f_item['emoji'] == default_section_emoji and not f_item['personal_emoji']:
                final_own_emoji = ""

            node_own = {
                'title': f_item['title'],
                'url': f_item['url'],
                'date': f_item['date'],
                'posttype': f_item['posttype'],
                'related': f_item['related'],
                'is_post': f_item['is_post'],
                'emoji': final_own_emoji,
                'personal_emoji': f_item['personal_emoji'],
                'pinned': is_pinned_own
            }
            baskets[c_posttype].append(node_own)

    # ВЫГРУЗКА РАЗДЕЛЬНЫХ СОРТИРОВАННЫХ ЛОГОВ ПО КАЖДОЙ КОРЗИНЕ НА ДИСК
    final_feed_data = {}
    os.makedirs(log_dir_path, exist_ok=True)

    for b_name, b_items in baskets.items():
        # Сортируем каждую корзину отдельно: сначала закрепы этой ленты, затем по датам
        sorted_basket = sorted(b_items, key=lambda x: (1 if x['pinned'] else 0, x['date']), reverse=True)
        final_feed_data[b_name] = sorted_basket

        # Запись изолированного лога для текущей корзины
        log_buffer = []
        log_buffer.append("=========================================================================")
        log_buffer.append(f"РЕЕСТР ОБОСОБЛЕННОЙ ЛЕНТЫ ОБНОВЛЕНИЙ: {b_name.upper()}")
        log_buffer.append(f"[SUMMARY] Всего извлечено уникальных событий: {len(sorted_basket)}")
        log_buffer.append("=========================================================================")
        
        for idx, item in enumerate(sorted_basket, 1):
            p_status = "POST" if item['is_post'] == 'true' else "PAGE"
            pin_marker = "PIN" if item['pinned'] else "   "
            log_buffer.append(
                f"{idx:03d}. [{p_status}] {item['date']} | {item['emoji']:2} | {pin_marker} | "
                f"{item['posttype']:8} | {item['related']:20} | {item['title']}"
            )
            
        try:
            with open(os.path.join(log_dir_path, f"{b_name}_debug.log"), 'w', encoding='utf-8') as lf:
                lf.write("\n".join(log_buffer))
        except Exception as e:
            print(f"[FEED-ERROR] Не удалось сохранить изолированный лог {b_name}: {e}")

    # Запись монолитной многопоточной базы готовых корзин контура на диск
    try:
        with open(output_feed_path, 'w', encoding='utf-8') as f:
            yaml.dump(final_feed_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[FEED-SUCCESS] Обособленные корзины созданы в feed.yml. Лент: {len(final_feed_data)}")
    except Exception as e:
        print(f"[FEED-ERROR] Ошибка записи многопоточного feed.yml: {e}")

if __name__ == '__main__':
    build_universal_feed()
