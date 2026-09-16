#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module contentnews
@about Изолированный монолитный сборщик ленты "Что нового?" из Единого Источника Правды.
@purpose Собирает новости строго из navigation.yml, используя вашу родную логику эмодзи,
         и выгружает развёрнутый человеческий лог строго в верную папку _content_files/.
@author TechLab
@version 4.2.0-monolith-tracy-pure
"""

import os
import sys
import re
import yaml

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

# 🔥 ВШИТО НА ТИВНО: Ваша оригинальная рабочая функция сбора эмодзи из первоисточников
def load_emoji_sources(root_dir):
    pages_dir = os.path.join(root_dir, '_pages')
    page_types_emoji = {}
    section_index_emoji = {}

    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                p_data, _, _ = parse_yaml_front_matter_stub(os.path.join(pages_dir, file))
                if p_data and p_data.get('emoji'):
                    p_slug, _ = os.path.splitext(file)
                    page_types_emoji[p_slug] = p_data['emoji']

    EXCLUDED = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and name not in EXCLUDED and not name.startswith('.'):
            idx_path = os.path.join(root_dir, name, 'index.md')
            if os.path.exists(idx_path):
                i_data, _, _ = parse_yaml_front_matter_stub(idx_path)
                if i_data and i_data.get('emoji'):
                    section_index_emoji[name.lstrip('_')] = i_data['emoji']

    return page_types_emoji, section_index_emoji

# 🔥 ВШИТО НА ТИВНО: Ваш оригинальный калькулятор эмодзи по folder_parts[0]
def calculate_item_emoji(data, folder_parts, page_types_emoji, root_dir):
    first_folder = folder_parts[0] if isinstance(folder_parts, list) and len(folder_parts) > 0 else str(folder_parts)
    clean_folder_name = first_folder.lstrip('_')

    if first_folder == '_posts':
        post_type = data.get('post-page')
        return page_types_emoji.get(post_type, "")

    section_dir = os.path.join(root_dir, first_folder)
    has_index = os.path.exists(os.path.join(section_dir, 'index.md')) or os.path.exists(os.path.join(section_dir, 'index.html'))

    if has_index:
        idx_path = os.path.join(section_dir, 'index.md')
        if not os.path.exists(idx_path):
            idx_path = os.path.join(section_dir, 'index.html')
        try:
            i_data, _, _ = parse_yaml_front_matter_stub(idx_path)
            if i_data and i_data.get('emoji'):
                return i_data['emoji']
        except:
            pass
        return ""
    else:
        return page_types_emoji.get(clean_folder_name, "")

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

    # ПОЛНЫЙ ЧЕЛОВЕЧЕСКИЙ ЛОГ-БУФЕР ДЛЯ АРТЕФАКТОВ
    log_buffer = []
    log_buffer.append("=========================================================================")
    log_buffer.append("СТАРТ СЕРВЕРНОГО АУДИТА ЛЕНТЫ ОБНОВЛЕНИЙ ИЗ ЕДИНОГО ИСТОЧНИКА ПРАВДЫ")
    log_buffer.append("=========================================================================\n")

    pinned_posts = []
    regular_posts = []
    sections = nav_data.get('sections', {})
    
    # Загружаем карты эмодзи напрямую через вашу логику
    page_types_emoji, section_index_emoji = load_emoji_sources(root_dir)

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
                        item_emoji = calculate_item_emoji({'post-page': 'journal'}, ['_posts'], page_types_emoji, root_dir)
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
                        item_emoji = calculate_item_emoji({'post-page': 'media'}, ['_posts'], page_types_emoji, root_dir)
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
                item_emoji = calculate_item_emoji({}, [section_name], page_types_emoji, root_dir)
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

    # Сортировка по датам
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    final_feed = pinned_posts + regular_posts
    
    # Наполнение построчного человеческого реестра
    log_buffer.append(f"[SUMMARY] Всего извлечено уникальных событий: {len(final_feed)}")
    log_buffer.append(f"[SUMMARY] Из них закреплённых (pinnednews): {len(pinned_posts)}\n")
    log_buffer.append("-------------------------------------------------------------------------")
    log_buffer.append("ПОСТРОЧНЫЙ ХРОНОЛОГИЧЕСКИЙ РЕЕСТР ЛЕНТЫ ОБНОВЛЕНИЙ:")
    log_buffer.append("-------------------------------------------------------------------------")
    
    for idx, f_item in enumerate(final_feed, 1):
        p_status = "ЗАКРЕП" if f_item['pinned'] else "ПОСТ  " if f_item['is_post'] == 'true' else "КРТОЧКА"
        log_buffer.append(f"{idx:03d}. [{p_status}] Дата: {f_item['date']} | Значок: {f_item['emoji']} | Заголовок: {f_item['title']}")

    log_buffer.append("\n=========================================================================")
    log_buffer.append("КОНВЕЙЕР УСПЕШНО ЗАВЕРШЕН. СБОИ НЕ ОБНАРУЖЕНЫ.")
    log_buffer.append("=========================================================================")

    # Запись чистой ленты новостей news_feed.yml
    data_dir = os.path.join(root_dir, '_data')
    output_path = os.path.join(data_dir, 'news_feed.yml')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[NEWS-SUCCESS] Каноничная лента успешно обновлена. Всего элементов: {len(final_feed)}")
    except Exception as e:
        print(f"[NEWS-ERROR] Ошибка записи news_feed.yml: {e}")
        sys.exit(1)

    # 🔥 СТРОГО В ТРЕБУЕМУЮ ВАМИ И СЕРВЕРОМ ПАПКУ АРТЕФАКТОВ CONTENT
    debug_dir = os.path.join(root_dir, '_content_files')
    os.makedirs(debug_dir, exist_ok=True)
    try:
        log_file_path = os.path.join(debug_dir, 'contentnews_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[NEWS-SUCCESS] Человеческий отчёт успешно сохранён в верную папку _content_files/.")
    except Exception as e:
        print(f"[NEWS-ERROR] Не удалось сохранить лог новостей: {e}")

if __name__ == '__main__':
    build_news_feed()
