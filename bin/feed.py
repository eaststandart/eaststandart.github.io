#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module feed
@about Изолированный монолитный сборщик единой ленты обновлений из Источника Правды.
@purpose Собирает все посты хроники из плоской карты navigation.yml, упорядочивает их 
         и выгружает универсальный файл данных _data/feed.yml для нужд Jekyll и Liquid.
@author TechLab
@version 1.0.0
"""

import os
import sys
import yaml

def build_universal_feed():
    # Настройка базовых путей диска сервера Actions
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'navigation.yml')
    output_feed_path = os.path.join(root_dir, '_data', 'feed.yml')
    log_file_path = os.path.join(root_dir, '_feed_files', 'feed_debug.log')
    
    # Проверка: если карты навигации ещё нет на диске, останавливаем контур
    if not os.path.exists(nav_file_path):
        print(f"[FEED-ERROR] Единый Источник Правды не найден по пути: {nav_file_path}")
        return

    # Читаем карту навигации в память как плоский словарь
    try:
        with open(nav_file_path, 'r', encoding='utf-8') as f:
            nav_data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[FEED-ERROR] Сбой YAML при чтении карты сайта: {e}")
        return

    # Буфер для вывода scannable-строк в лог артефактов
    log_buffer = []
    log_buffer.append("=========================================================================")
    log_buffer.append("СТАРТ СЕРВЕРНОГО АУДИТА ЕДИНОЙ ЛЕНТЫ ОБНОВЛЕНИЙ FEED.YML")
    log_buffer.append("=========================================================================\n")

    pinned_posts = []
    regular_posts = []

    # 🟢 ШАГ 1: КЭШИРУЕМ ЗНАЧКИ ЭМОДЗИ ИЗ ГОЛОВНЫХ РАЗДЕЛОВ КАРТЫ НАВИГАЦИИ
    section_emojis = {}
    for key, items in nav_data.items():
        # Ищем только плоские корневые разделы (длина ключа короткая, без слэшей файлов)
        if '/' not in key and isinstance(items, list) and len(items) > 0:
            section_card = items[0]
            if isinstance(section_card, dict) and section_card.get('emoji'):
                section_emojis[key] = section_card['emoji']

    # 🟢 ШАГ 2: СКВОЗНОЙ СБОР ПОСТОВ ХРОНИКИ ИЗ ПЛОСКОЙ КАРТЫ НАВИГАЦИИ
    for file_key, nodes in nav_data.items():
        # Игнорируем технические служебные заголовки карты
        if file_key == 'detected_root_folders' or file_key.endswith('.html'):
            continue
            
        if not isinstance(nodes, list) or len(nodes) == 0:
            continue
            
        # 🟢 НАШ ЗАКОН: Безопасно распаковываем плоский словарь метаданных из массива карты
        passport = nodes[0] if isinstance(nodes, list) and len(nodes) > 0 else nodes
        
        if not isinstance(passport, dict):
            continue

        # Наш жесткий предохранитель: собираем только файлы, у которых есть дата
        item_date = str(passport.get('date', '')).strip()
        if not item_date or item_date == 'None':
            continue

        # Проверяем, является ли текущий файл постом хроники (наличие posttype и relatedpages)
        post_type = passport.get('posttype')
        related_page = passport.get('relatedpages')

        # Извлекаем слаг родительского проекта для нужд фильтрации кнопки "0"
        project_slug = ""
        if related_page:
            rel_parts = related_page.split('/')
            if len(rel_parts) > 1:
                # Отрезаем имя файла проекта, оставляя имя его папки (слаг)
                project_slug = rel_parts[-2]

        # 🟢 НАШ ЗРЯЧИЙ КАН दोषियों ЗАКОН: Наследуем эмодзи строго из кэша головного раздела карты!
        calculated_emoji = passport.get('emoji', '')
        if not calculated_emoji and post_type:
            calculated_emoji = section_emojis.get(post_type, "")

        # Сборка универсального узла обновления
        node = {
            'title': passport.get('title', 'Без названия'),
            'url': passport.get('url', ''),
            'date': item_date,
            'posttype': post_type if post_type else "",
            'project': project_slug,
            'is_post': 'true' if post_type else 'false',
            'emoji': calculated_emoji,
            'pinned': False
        }

        # Проверка оригинального флага закрепления pinnednews (из шапки файлов проектов)
        if passport.get('pinnednews') is True:
            node['pinned'] = True
            pinned_posts.append(node)
        else:
            regular_posts.append(node)

    # 🟢 ШАГ 3: СОРТИРОВКА И ОБЪЕДИНЕНИЕ ПОТОКОВ
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    final_feed = pinned_posts + regular_posts

    # Наполнение построчного реестра для лога артефактов
    log_buffer.append(f"[SUMMARY] Всего извлечено уникальных событий: {len(final_feed)}")
    log_buffer.append(f"[SUMMARY] Из них закреплённых (pinnednews): {len(pinned_posts)}\n")
    log_buffer.append("-------------------------------------------------------------------------")
    log_buffer.append("ПОСТРОЧНЫЙ ХРОНОЛОГИЧЕСКИЙ РЕЕСТР УНИВЕРСАЛЬНОЙ ЛЕНТЫ FEED.YML:")
    log_buffer.append("-------------------------------------------------------------------------")
    
    for idx, f_item in enumerate(final_feed, 1):
        p_status = "ЗАКРЕП" if f_item['pinned'] else "ПОСТ  " if f_item['is_post'] == 'true' else "КРТОЧКА"
        log_buffer.append(f"{idx:03d}. [{p_status}] Дата: {f_item['date']} | Значок: {f_item['emoji']} | Тип: {f_item['posttype']:8} | Проект: {f_item['project']:20} | Заголовок: {f_item['title']}")

    log_buffer.append("\n=========================================================================")
    log_buffer.append("КОНВЕЙЕР УСПЕШНО ЗАВЕРШЕН. СБОИ НЕ ОБНАРУЖЕНЫ.")
    log_buffer.append("=========================================================================")

    # Физически сохраняем единую ленту feed.yml на диск сервера
    try:
        with open(output_feed_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[FEED-SUCCESS] Единая универсальная лента создана. Всего элементов: {len(final_feed)}")
    except Exception as e:
        print(f"[FEED-ERROR] Ошибка записи feed.yml: {e}")
        return

    # Сохраняем изолированный человеческий лог в папку артефактов _feed_files/
    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[FEED-SUCCESS] Человеческий отчёт успешно сохранён в папку _feed_files/.")
    except Exception as e:
        print(f"[FEED-ERROR] Не удалось сохранить лог: {e}")

if __name__ == '__main__':
    build_universal_feed()
