#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module feed.py
@about Изолированный монолитный сборщик единой ленты обновлений из Источника Правды.
@purpose Автоматически вычисляет типы, проекты и наследует эмодзи на основе URL карты навигации,
         квантует массивы по страницам со сквозными закрепами на основе свойства perpage,
         выгружает их в виде раздельных физических JSON-порций в открытую папку assets/feed/
         и полностью сохраняет ваши оригинальные постраничные логи контроля закрепов.
@author TechLab
@version 4.0.0-json-portions
"""

import os
import sys
import yaml
import json

def build_universal_feed():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'sitemap.yml')
    # Автоматический путь к новой открытой папке порций сетевой подкачки
    portions_dir_path = os.path.join(root_dir, 'assets', 'feed')
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

        if file_key.startswith('_posts/') and item_url:
            url_parts = item_url.split('/')
            if len(url_parts) >= 2:
                post_type = url_parts[0]
                project_slug = url_parts[1]
                is_post_flag = 'true'
        else:
            if item_url:
                project_slug = item_url.split('/')[-1]

        target_section = post_type
        if not target_section:
            target_section = passport.get('relatedsection', '')
        if not target_section:
            target_section = passport.get('relatedcollection', '')

        calculated_emoji = passport.get('emoji', '')
        if not calculated_emoji and target_section:
            calculated_emoji = section_emojis.get(target_section, "")

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
            'personal_emoji': passport.get('emoji', ''),
            'pinned_list': pinned_list
        }

        if 'news' in pinned_list or (str(post_type).strip().lower() in pinned_list if post_type else False):
            pinned_posts.append(node)
        else:
            regular_posts.append(node)

    # 🟢 ШАГ 3: СКВОЗНАЯ МУЛЬТИ-СОРТИРОВКА И ДИНАМИЧЕСКОЕ КВАНТОВАНИЕ ПО СТРАНИЦАМ
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    final_feed = pinned_posts + regular_posts

    # Динамически инициализируем корзины, значки и лимиты страниц по пермалинкам ключей feed-
    baskets = {'news': []}
    feed_section_emojis = {}
    feed_section_limits = {'news': 10}  # По умолчанию для Главной лимит равен 10

    # Извлекаем чистую ноду для правильного создания JSON-файлов пагинации
    for key, items in nav_data.items():
        if key.startswith('feed-') and isinstance(items, list) and len(items) > 0:
            sect_card = items[0] if isinstance(items, list) and len(items) > 0 else items
            
            # Если внутри структуры есть ключ 'node' — проваливаемся в него
            if isinstance(sect_card, dict) and 'node' in sect_card:
                sect_card = sect_card['node']
                
            if isinstance(sect_card, dict) and sect_card.get('url'):
                b_name = sect_card['url'].strip('/')

                if b_name:
                    baskets[b_name] = []
                    if sect_card.get('emoji'):
                        feed_section_emojis[b_name] = sect_card['emoji']
                    # Считываем свойство perpage напрямую из Source of Truth карты навигации
                    if sect_card.get('perpage'):
                        try:
                            feed_section_limits[b_name] = int(sect_card['perpage'])
                        except ValueError:
                            feed_section_limits[b_name] = 10

    # Наполняем временные плоские списки из готового массива final_feed
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

    # НАЧИНАЕМ СКВОЗНОЕ КВАНТОВАНИЕ МАССИВОВ С АВТОМАТИЧЕСКИМ СОЗДАНИЕМ ПАПКИ И JSON-ПОРЦИЙ
    os.makedirs(log_dir_path, exist_ok=True)
    # 🌟 АВТОМАТ ПАПКИ: Питон сам физически создаёт открытую папку на диске
    os.makedirs(portions_dir_path, exist_ok=True)

    for b_name, b_items in baskets.items():
        # Сортируем кучку: закрепы текущей ленты наверх, обычные — по датам вниз
        sorted_pool = sorted(b_items, key=lambda x: (1 if x['pinned'] else 0, x['date']), reverse=True)
        
        # Вычленяем закрепы и обычную хронику в изолированные очереди
        pinned_queue = [x for x in sorted_pool if x['pinned']]
        regular_queue = [x for x in sorted_pool if not x['pinned']]
        
        # Забираем динамический лимит perpage из карты навигации
        ITEMS_PER_PAGE = feed_section_limits.get(b_name, 10)
        
        # Рассчитываем, сколько обычных постов поместится на страницу под закрепами
        regular_step = ITEMS_PER_PAGE - len(pinned_queue)
        if regular_step < 1:
            regular_step = 1  # Защита от переполнения закрепами

        pages_dict = {}
        total_items = len(sorted_pool)
        
        if total_items > 0:
            page_num = 1
            # Если обычных постов нет, но есть закрепы — выводим одну страницу закрепов
            if not regular_queue and pinned_queue:
                pages_dict[page_num] = pinned_queue
            else:
                # Нарезаем обычные посты шагами regular_step и в начало каждой страницы дописываем закрепы!
                for i in range(0, len(regular_queue), regular_step):
                    chunk = regular_queue[i:i + regular_step]
                    # СКВОЗНАЯ МАТЕМАТИКА: закрепы жестко подмешиваются на абсолютно любую страницу контура
                    pages_dict[page_num] = pinned_queue + chunk
                    page_num += 1
        else:
            pages_dict = {}

        total_pages = len(pages_dict)

        # 🌟 ЧЕСТНАЯ СЕТЕВАЯ ПОДКАЧКА: Питон нарезает и сохраняет независимые файлы JSON под каждую страницу!
        for p_idx, p_items in pages_dict.items():
            portion_filename = f"{b_name}-page{p_idx}.json"
            portion_file_path = os.path.join(portions_dir_path, portion_filename)
            
            # Структура одного изолированного файла-порции для JavaScript
            portion_data = {
                'per_page': ITEMS_PER_PAGE,
                'total_pages': total_pages,
                'total_items': total_items,
                'current_page': p_idx,
                'items': p_items
            }
            
            try:
                with open(portion_file_path, 'w', encoding='utf-8') as jf:
                    json.dump(portion_data, jf, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"[FEED-ERROR] Не удалось сохранить JSON-порцию {portion_filename}: {e}")

        # ГЕНЕРАЦИЯ ОФИЦИАЛЬНОГО ПОСТРАНИЧНОГО ОТЧЕТА КОНТРОЛЯ ЗАКРЕПОВ (1-в-1 ВАШ СТАРЫЙ ЛОГ)
        log_buffer = []
        log_buffer.append("=========================================================================")
        log_buffer.append(f"РЕЕСТР ОБОСОБЛЕННОЙ ЛЕНТЫ ОБНОВЛЕНИЙ: {b_name.upper()}")
        log_buffer.append(f"[SUMMARY] Всего событий: {total_items} | Страниц пагинации: {total_pages} | Лимит: {ITEMS_PER_PAGE} на стр.")
        log_buffer.append("=========================================================================")
        
        global_idx = 1
        for p_idx in sorted(pages_dict.keys()):
            current_page_list = pages_dict[p_idx]
            log_buffer.append(f"\n[📑 СТРАНИЦА {p_idx}] (Закрепов: {len(pinned_queue)} | Хроники: {len(current_page_list) - len(pinned_queue)} | Всего строк: {len(current_page_list)})")
            log_buffer.append("-------------------------------------------------------------------------")
            
            for item in current_page_list:
                p_status = "POST" if item['is_post'] == 'true' else "PAGE"
                pin_marker = "PIN" if item['pinned'] else "   "
                log_buffer.append(
                    f"{global_idx:03d}. [{p_status}] {item['date']} | {item['emoji']:2} | {pin_marker} | "
                    f"{str(item['posttype']):8} | {item['related']:20} | {item['title']}"
                )
                global_idx += 1
            
        try:
            with open(os.path.join(log_dir_path, f"{b_name}_debug.log"), 'w', encoding='utf-8') as lf:
                lf.write("\n".join(log_buffer))
        except Exception as e:
            print(f"[FEED-ERROR] Не удалось сохранить изолированный лог {b_name}: {e}")

    # 🌟 ТОТАЛЬНАЯ ИНСПЕКЦИЯ: Питон детально рапортует обо всех созданных файлах порций
    print("\n=========================================================================")
    print("ФИЗИЧЕСКАЯ КАРТА СЕРВЕРНЫХ JSON-ПОРЦИЙ В ПАПКЕ assets/feed/:")
    print("=========================================================================")
    
    try:
        generated_files = sorted(os.listdir(portions_dir_path))
        if not generated_files:
            print("[FEED-WARNING] Папка assets/feed/ пуста! Файлы не создались.")
        else:
            for file_name in generated_files:
                if file_name.endswith('.json'):
                    full_p_path = os.path.join(portions_dir_path, file_name)
                    # Читаем вес и заглядываем внутрь для проверки количества постов
                    with open(full_p_path, 'r', encoding='utf-8') as j_check:
                        c_data = json.load(j_check)
                        p_items_count = len(c_data.get('items', []))
                        p_total_pages = c_data.get('total_pages', 1)
                    
                    print(f" 📂 [FILE] {file_name:<25} | Постов в порции: {p_items_count:<3} | Всего страниц ленты: {p_total_pages}")
    except Exception as e:
        print(f"[FEED-ERROR] Не удалось провести инспекцию папки порций: {e}")
        
    print("=========================================================================\n")
    print(f"[FEED-SUCCESS] Честный порционный контур JSON создан в assets/feed/. Лент: {len(baskets)}")

if __name__ == '__main__':
    build_universal_feed()

