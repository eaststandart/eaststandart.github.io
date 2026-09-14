#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content
@about Главный изолированный диспетчер конвейера предобработки контента.
@purpose Связывает Модуль 1 (навигация) и Модуль 2 (эмодзи), выполняет сортировку
         закреплений по дате и выгружает лог-отчеты в артефакты Actions.
@author TechLab
@version 5.1.0-final-clean
"""

import os
import sys
import re
import yaml

# Фиксация системных путей импорта для сервера Actions
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from content_nav import find_url_and_date_in_navigation
from content_emoji import load_emoji_sources, calculate_item_emoji

def parse_yaml_front_matter(file_path):
    """Извлекает и безопасно парсит блок Front Matter из markdown-файла."""
    content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[CON-ERROR] Не удалось прочитать файл {file_path}: {e}")
        return None, None, content

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match: return None, None, content

    front_text = match.group(1)
    body_content = content[match.end():]

    try:
        data = yaml.safe_load(front_text)
        return data if data else {}, front_text, body_content
    except Exception as e:
        print(f"[CON-ERROR] Сбой синтаксиса YAML во Front Matter {file_path}: {e}")
        return None, None, content

def build_pinned_news_list():
    """Главная функция-диспетчер: собирает ленту новостей на основе карты навигации."""
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    nav_file_path = os.path.join(root_dir, '_data', 'navigation.yml')
    if not os.path.exists(nav_file_path):
        print("[CON-ERROR] Карта навигации _data/navigation.yml не найдена!")
        return

    with open(nav_file_path, 'r', encoding='utf-8') as nf:
        nav_data = yaml.safe_load(nf)

    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    pinned_posts = []
    regular_posts = []
    log_buffer = []

    page_types_emoji, section_index_emoji = load_emoji_sources(root_dir, parse_yaml_front_matter)

    # Сканирование репозитория
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS and not d.startswith('.')]
        for file in files:
            if not file.endswith('.md') or file == 'index.md': continue
                
            full_path = os.path.join(root, file)
            data, front_text, body = parse_yaml_front_matter(full_path)

            if data is None: continue

            rel_path = os.path.relpath(full_path, root_dir)
            folder_parts = rel_path.split(os.sep)
            
            file_name_clean, _ = os.path.splitext(file)
            file_name_clean_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)
            
            # 🔥 ИСПРАВЛЕНО: Строго и нативно берем имя первой папки из списка
            first_folder = folder_parts[0] if (isinstance(folder_parts, list) and len(folder_parts) > 0) else str(folder_parts)
            
            if first_folder == '_posts':
                project_slug = file_name_clean_no_date
                current_folder_type = '_posts'
            else:
                project_slug = file_name_clean
                current_folder_type = first_folder

            # 🔥 ЧИТАЕМ ДАННЫЕ СТРОГО ИЗ ЕДИНОГО ИСТОЧНИКА КАРТЫ
            item_url, item_date = find_url_and_date_in_navigation(nav_data, project_slug, file_name_clean_no_date, current_folder_type, data)

            # Резервные правила, если файла по какой-то причине не оказалось в карте навигации
            if not item_url:
                fallback_section = data.get('section', first_folder.lstrip('_'))
                item_url = f"/{fallback_section}/{project_slug}.html"
            
            if not item_date:
                if data.get('date'):
                    item_date = str(data['date'])
                else:
                    # Если даты нет вообще нигде, пропускаем узел во избежание 1970 года
                    continue

            # 🔥 ИСПРАВЛЕНО: Безопасная проверка строкового флага
            is_post_flag = "true" if current_folder_type == '_posts' else "false"
            section_emoji = calculate_item_emoji(data, folder_parts, page_types_emoji, root_dir, parse_yaml_front_matter)

            news_node = {
                'title': data.get('title', file),
                'url': item_url,
                'date': item_date,
                'is_post': is_post_flag,
                'path': rel_path,
                'emoji': section_emoji,
                'pinned': False
            }

            if data.get('pinnednews') is True:
                news_node['pinned'] = True
                pinned_posts.append(news_node)
            else:
                regular_posts.append(news_node)

    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    final_feed = pinned_posts + regular_posts
    
    log_buffer.append("[CON-SUCCESS] Модульный серверный конвейер новостей успешно выполнен.")
    log_buffer.append(f"Всего собрано публикаций в ленту: {len(final_feed)}")

    # Запись готовой ленты в систему Jekyll
    data_dir = os.path.join(root_dir, '_data')
    output_feed_path = os.path.join(data_dir, 'news_feed.yml')
    try:
        with open(output_feed_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except Exception as e:
        log_buffer.append(f"[CON-ERROR] Не удалось записать файл news_feed.yml: {e}")

    # Выгрузка отчетов в папку артефактов content
    content_debug_dir = os.path.join(root_dir, '_content_files')
    os.makedirs(content_debug_dir, exist_ok=True)

    processed_news_path = os.path.join(content_debug_dir, 'processed-news_feed.yml')
    with open(processed_news_path, 'w', encoding='utf-8') as pnf:
        yaml.dump({'feed': final_feed}, pnf, allow_unicode=True, default_flow_style=False, sort_keys=False)

    for line in log_buffer:
        print(line)

    try:
        log_file_path = os.path.join(content_debug_dir, 'content_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
    except Exception as e:
        print(f"[CON-ERROR] Не удалось сохранить файл лога контента: {e}")

if __name__ == '__main__':
    build_pinned_news_list()
