#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module feed
@about Изолированный монолитный сборщик единой ленты обновлений из Источника Правды.
@purpose Автоматически вычисляет типы, проекты и наследует эмодзи на основе URL карты навигации,
         выгружая универсальный файл данных _data/feed.yml для нужд Jekyll и Liquid.
@author TechLab
@version 1.1.0-url-fixed
"""

import os
import sys
import yaml

def build_universal_feed():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'navigation.yml')
    output_feed_path = os.path.join(root_dir, '_data', 'feed.yml')
    log_file_path = os.path.join(root_dir, '_feed_files', 'feed_debug.log')
    
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

    regular_posts = []

    # 🟢 ШАГ 1: КЭШИРУЕМ ЗНАЧКИ ЭМОДЗИ ИЗ ГОЛОВНЫХ РАЗДЕЛОВ КАРТЫ НАВИГАЦИИ
    section_emojis = {}
    for key, items in nav_data.items():
        if key == 'detected_root_folders':
            continue
        if '/' not in key and isinstance(items, list) and len(items) > 0:
            section_card = items[0]
            if isinstance(section_card, dict) and section_card.get('emoji'):
                section_emojis[key] = section_card['emoji']

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

        # УНИВЕРСАЛЬНЫЙ ОЧИСТИТЕЛЬ: Намертво выжигает скобки и нарезает элементы по запятым
        raw_pinned = passport.get('pinnedfeed', False)
        pinned_list = []
        
        if isinstance(raw_pinned, list):
            pinned_list = [str(x).strip().lower() for x in raw_pinned]
        elif isinstance(raw_pinned, str):
            # Стираем технические скобки [ ] и кавычки, после чего режем по запятой
            clean_str = raw_pinned.replace('[', '').replace(']', '').replace("'", "").replace('"', '')
            pinned_list = [x.strip().lower() for x in clean_str.split(',') if x.strip()]
        elif raw_pinned is True:
            pinned_list = ['news', str(post_type).strip().lower()]

        # Вычисляем динамические маркеры закрепов без привязки к именам папок
        current_posttype = str(post_type).strip().lower()
        is_pinned_news = 'news' in pinned_list
        is_pinned_own = current_posttype in pinned_list if current_posttype else False

        node = {
            'title': passport.get('title', 'Без названия'),
            'url': passport.get('url', ''),
            'date': item_date,
            'posttype': post_type,
            'related': project_slug,
            'is_post': is_post_flag,
            'emoji': calculated_emoji,
            'pinnedfeed': raw_pinned,
            'pinned_news': is_pinned_news,  # Флаг закрепа на Главной
            'pinned_own': is_pinned_own     # Динамический флаг закрепа в своей ленте
        }

        # Складываем в общую базу regular_posts. Глобальную сортировку по блокам сделаем на Шаге 3!
        regular_posts.append(node)

    # 🟢 ШАГ 3: СОРТИРОВКА И ОБЪЕДИНЕНИЕ ПОТОКОВ
    # Универсальная каскадная сортировка: 
    # Приоритет 1: Любые закрепы (news или own) идут первыми. Приоритет 2: Внутри блоков всё строго по датам!
    final_feed = sorted(
        regular_posts,
        key=lambda x: (
            1 if (x.get('pinned_news') or x.get('pinned_own')) else 0,
            x['date']
        ),
        reverse=True
    )

    log_buffer.append(f"[SUMMARY] Всего извлечено уникальных событий: {len(final_feed)}")
    log_buffer.append("-------------------------------------------------------------------------")
    log_buffer.append("ПОСТРОЧНЫЙ ХРОНОЛОГИЧЕСКИЙ REEСТР УНИВЕРСАЛЬНОЙ ЛЕНТЫ FEED.YML:")
    log_buffer.append("-------------------------------------------------------------------------")
    
    for idx, f_item in enumerate(final_feed, 1):
        p_status = "POST" if f_item['is_post'] == 'true' else "PAGE"
        
        # Калибровка лога: наглядно показываем тип мультизакрепления
        if f_item.get('pinned_news') and f_item.get('pinned_own'):
            pin_marker = "N/O"
        elif f_item.get('pinned_news'):
            pin_marker = " N "
        elif f_item.get('pinned_own'):
            pin_marker = " O "
        else:
            pin_marker = "   "

        log_buffer.append(f"{idx:03d}. [{p_status}] {f_item['date']} | {f_item['emoji']:2} | {pin_marker} | {f_item['posttype']:8} | {f_item['related']:20} | {f_item['title']}")

    try:
        with open(output_feed_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[FEED-SUCCESS] Универсальная лента создана. Элементов: {len(final_feed)}")
    except Exception as e:
        print(f"[FEED-ERROR] Ошибка записи feed.yml: {e}")
        return

    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[FEED-SUCCESS] Отчёт успешно сохранён.")
    except Exception as e:
        print(f"[FEED-ERROR] Не удалось сохранить лог: {e}")

if __name__ == '__main__':
    build_universal_feed()
