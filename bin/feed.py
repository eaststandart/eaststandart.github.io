#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module feed
@about Динамический сборщик обособленных корзин обновлений из Источника Правды.
@purpose Автоматически собирает корзины на основе пермалинков карты навигации,
         нативно выжигает эмодзи-шум, независимо сортирует мультизакрепы
         и выгружает раздельные логи под каждую ленту сайта.
@author TechLab
@version 2.0.0-baskets-monolith
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

    # 🟢 ШАГ 1: ДИНАМИЧЕСКИЙ СБОР КОРЗИН И КЭША ЭМОДЗИ ПО ПЕРМАЛИНКАМ КЛЮЧЕЙ 'feed-'
    baskets = {}
    section_emojis = {}
    
    # Главная корзина новостей создается всегда по умолчанию
    baskets['news'] = []
    section_emojis['news'] = ""

    for key, items in nav_data.items():
        if key.startswith('feed-') and isinstance(items, list) and len(items) > 0:
            passport = items[0]
            if isinstance(passport, dict) and passport.get('url'):
                # Вырезаем чистое имя корзины из пермалинка (например, "/journal/" -> "journal")
                basket_name = passport['url'].strip('/')
                if basket_name:
                    baskets[basket_name] = []
                    # Запоминаем дефолтный эмодзи секции строго по принудительному ключу feed-имя
                    if passport.get('emoji'):
                        section_emojis[key] = passport['emoji']

    # 🟢 ШАГ 2: СКВОЗНОЙ СБОР ПОСТОВ И КАСКАДНОЕ РАСПРЕДЕЛЕНИЕ С ФИЛЬТРАЦИЕЙ ШУМА
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

        # Вырезаем тип контента и слаг проекта из адресов папки _posts
        if file_key.startswith('_posts/') and item_url:
            url_parts = item_url.split('/')
            if len(url_parts) >= 2:
                post_type = url_parts[0]
                project_slug = url_parts[1]
                is_post_flag = 'true'
        else:
            if item_url:
                project_slug = item_url.split('/')[-1]
            post_type = passport.get('relatedsection', '')
            if not post_type:
                post_type = passport.get('relatedcollection', '')

        # Нативно вычисляем дефолтный эмодзи, принудительно подставляя приставку feed-
        personal_emoji = passport.get('emoji', '')  # Ручной знак из Obsidian
        calculated_emoji = personal_emoji
        
        if not calculated_emoji and post_type:
            target_key = f"feed-{post_type}"
            calculated_emoji = section_emojis.get(target_key, "")

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

        current_posttype = str(post_type).strip().lower()

        # Базовая карточка-нода для Главной корзины news
        node_news = {
            'title': passport.get('title', 'Без названия'),
            'url': passport.get('url', ''),
            'date': item_date,
            'posttype': post_type,
            'related': project_slug,
            'is_post': is_post_flag,
            'emoji': calculated_emoji,
            'personal_emoji': personal_emoji,
            'pinned': 'news' in pinned_list
        }
        baskets['news'].append(node_news)

        # Если у поста есть целевая обособленная корзина — дублируем его туда
        if current_posttype in baskets:
            # Вычисляем дефолтный знак этого конкретного раздела контура
            default_section_emoji = section_emojis.get(f"feed-{current_posttype}", "")
            
            # Нативная бэкенд-очистка: если эмодзи унаследован — стираем его в пустоту. Личные знаки — оставляем!
            final_own_emoji = calculated_emoji
            if calculated_emoji == default_section_emoji and not personal_emoji:
                final_own_emoji = ""

            node_own = {
                'title': passport.get('title', 'Без названия'),
                'url': passport.get('url', ''),
                'date': item_date,
                'posttype': post_type,
                'related': project_slug,
                'is_post': is_post_flag,
                'emoji': final_own_emoji,
                'personal_emoji': personal_emoji,
                'pinned': current_posttype in pinned_list
            }
            baskets[current_posttype].append(node_own)

    # 🟢 ШАГ 3: НЕЗАВИСИМАЯ МУЛЬТИ-СОРТИРОВКА И ВЫГРУЗКА РАЗДЕЛЬНЫХ ЛОГОВ
    final_feed_data = {}
    os.makedirs(log_dir_path, exist_ok=True)

    for b_name, b_items in baskets.items():
        # Сортируем каждую корзину отдельно: сначала закрепы (pinned), внутри блоков — строго по датам хроники
        sorted_items = sorted(
            b_items,
            key=lambda x: (1 if x.get('pinned') else 0, x['date']),
            reverse=True
        )
        
        # Сохраняем готовую очищенную корзину для YAML
        final_feed_data[b_name] = sorted_items

        # Пишем индивидуальный, независимый текстовый лог для текущей ленты на диск
        log_buffer = []
        log_buffer.append("=========================================================================")
        log_buffer.append(f"РЕЕСТР ОБОСОБЛЕННОЙ ЛЕНТЫ ОБНОВЛЕНИЙ: {b_name.upper()}")
        log_buffer.append(f"[SUMMARY] Всего извлечено уникальных событий: {len(sorted_items)}")
        log_buffer.append("=========================================================================")
        
        for idx, f_item in enumerate(sorted_items, 1):
            p_status = "POST" if f_item['is_post'] == 'true' else "PAGE"
            pin_marker = "PIN" if f_item.get('pinned') else "   "
            log_buffer.append(
                f"{idx:03d}. [{p_status}] {f_item['date']} | {f_item['emoji']:2} | {pin_marker} | "
                f"{f_item['posttype']:8} | {f_item['related']:20} | {f_item['title']}"
            )
            
        try:
            individual_log_path = os.path.join(log_dir_path, f"{b_name}_debug.log")
            with open(individual_log_path, 'w', encoding='utf-8') as lf:
                lf.write("\n".join(log_buffer))
        except Exception as e:
            print(f"[FEED-ERROR] Не удалось сохранить изолированный лог {b_name}: {e}")

    # Записываем монолитную многопоточную базу готовых корзин контура на диск
    try:
        with open(output_feed_path, 'w', encoding='utf-8') as f:
            yaml.dump(final_feed_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[FEED-SUCCESS] Обособленные корзины созданы в feed.yml. Лент: {len(final_feed_data)}")
    except Exception as e:
        print(f"[FEED-ERROR] Ошибка записи многопоточного feed.yml: {e}")

if __name__ == '__main__':
    build_universal_feed()
