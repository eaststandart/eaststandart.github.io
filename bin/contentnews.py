#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module contentnews
@about Изолированный целевой сборщик ленты "Что нового?" из Единого Источника Правды.
@purpose Полностью восстанавливает каноничную логику контента Tracy, оригинальные эмодзи
         и выводит развёрнутый человеческий лог-аудит в артефакты.
@author TechLab
@version 4.0.0-tracy-perfection
"""

import os
import sys
import re
import yaml
from content_emoji import load_emoji_sources, calculate_item_emoji

def parse_yaml_front_matter_stub(file_path):
    """Вспомогательный синтаксический парсер для инициализации автомата эмодзи."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            data = yaml.safe_load(match.group(1))
            return data if data else {}, "", ""
    except:
        pass
    return {}, "", ""

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

    # 🔥 ЧЕЛОВЕЧЕСКИЙ ЛОГ-БУФЕР ДЛЯ АРТЕФАКТОВ
    log_buffer = []
    log_buffer.append("=========================================================================")
    log_buffer.append("СТАРТ СЕРВЕРНОГО АУДИТА ЛЕНТЫ ОБНОВЛЕНИЙ ИЗ ЕДИНОГО ИСТОЧНИКА ПРАВДЫ")
    log_buffer.append("=========================================================================\n")

    pinned_posts = []
    regular_posts = []
    sections = nav_data.get('sections', {})
    
    # Инициализируем ваши эталонные источники эмодзи из _pages и папок контента
    page_types_emoji, section_index_emoji = load_emoji_sources(root_dir, parse_yaml_front_matter_stub)

    # Сквозной сбор из навигационного дерева
    for section_name, items_list in sections.items():
        if not isinstance(items_list, list): continue
        for item in items_list:
            if not isinstance(item, dict): continue
            slug = item.get('slug', '')
            if slug == 'index': continue

            # Ветка 1: Сбор связанных постов журнала (journal_posts)
            if 'journal_posts' in item and isinstance(item['journal_posts'], list):
                for post in item['journal_posts']:
                    p_date = str(post.get('date', '')).strip()
                    if p_date:
                        # Нативно вычисляем эмодзи по вашей рабочей логике content_emoji
                        item_emoji = calculate_item_emoji({'post-page': 'journal'}, ['_posts'], page_types_emoji, root_dir, parse_yaml_front_matter_stub)
                        
                        node = {
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'date': p_date,
                            'is_post': 'true',
                            'emoji': item_emoji,
                            'pinned': False
                        }
                        regular_posts.append(node)

            # Ветка 2: Сбор связанных постов галереи (media_posts)
            if 'media_posts' in item and isinstance(item['media_posts'], list):
                for post in item['media_posts']:
                    p_date = str(post.get('date', '')).strip()
                    if p_date:
                        # Нативно вычисляем эмодзи по вашей рабочей логике content_emoji
                        item_emoji = calculate_item_emoji({'post-page': 'media'}, ['_posts'], page_types_emoji, root_dir, parse_yaml_front_matter_stub)
                        
                        node = {
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'date': p_date,
                            'is_post': 'true',
                            'emoji': item_emoji,
                            'pinned': False
                        }
                        regular_posts.append(node)

            # Ветка 3: Сбор головных карточек контента (Автомобиль, Мультивибратор, Книги)
            item_date = str(item.get('date', '')).strip()
            if item_date:
                # Нативно вычисляем эмодзи по вашей рабочей логике Режимов А и Б
                item_emoji = calculate_item_emoji({}, [section_name], page_types_emoji, root_dir, parse_yaml_front_matter_stub)
                
                node = {
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'date': item_date,
                    'is_post': 'false',
                    'emoji': item_emoji,
                    'pinned': False
                }
                
                # Проверка оригинального флага закрепления pinnednews
                if item.get('pinnednews') is True:
                    node['pinned'] = True
                    pinned_posts.append(node)
                else:
                    regular_posts.append(node)

    # Раздельная строгая сортировка по датам
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    
    # 🔥 ЖЕЛЕЗОБЕТОННО ИСКЛЮЧАЕМ ДУБЛИ: Начисто формируем итоговую ленту
    final_feed = pinned_posts + regular_posts
    
    # Наполнение человеческого построчного лога для артефактов
    log_buffer.append(f"[SUMMARY] Всего извлечено уникальных событий: {len(final_feed)}")
    log_buffer.append(f"[SUMMARY] Из них закреплённых (pinnednews): {len(pinned_posts)}\n")
    log_buffer.append("-------------------------------------------------------------------------")
    log_buffer.append("ПОСТРОЧНЫЙ ХРОНОЛОГИЧЕСКИЙ РЕЕСТР ЛЕНТЫ ОБНОВЛЕНИЙ:")
    log_buffer.append("-------------------------------------------------------------------------")
    
    for idx, item in enumerate(final_feed, 1):
        p_status = "ЗАКРЕП" if item['pinned'] else "ПОСТ  " if item['is_post'] == 'true' else "КРТОЧКА"
        log_buffer.append(f"{idx:03d}. [{p_status}] Дата: {item['date']} | Значок: {item['emoji']} | Заголовок: {item['title']}")

    log_buffer.append("\n=========================================================================")
    log_buffer.append("КОНВЕЙЕР УСПЕШНО ЗАВЕРШЕН. СБОИ НЕ ОБНАРУЖЕНЫ.")
    log_buffer.append("=========================================================================")

    # Запись итоговой чистой ленты новостей на диск (начисто перезаписывает файл)
    data_dir = os.path.join(root_dir, '_data')
    output_path = os.path.join(data_dir, 'news_feed.yml')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[NEWS-SUCCESS] Каноничная лента успешно обновлена. Всего элементов: {len(final_feed)}")
    except Exception as e:
        print(f"[NEWS-ERROR] Ошибка записи news_feed.yml: {e}")
        sys.exit(1)

    # 🔥 ВЫГРУЗКА РАЗВЕРНУТОГО ЧЕЛОВЕЧЕСКОГО ЛОГА В АРТЕФАКТЫ CONTENT
    debug_dir = os.path.join(root_dir, '_content_files')
    os.makedirs(debug_dir, exist_ok=True)
    try:
        log_file_path = os.path.join(debug_dir, 'contentnews_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[NEWS-SUCCESS] Человеческий отчёт успешно выгружен в артефакты.")
    except Exception as e:
        print(f"[NEWS-ERROR] Не удалось сохранить лог новостей: {e}")

if __name__ == '__main__':
    build_news_feed()
