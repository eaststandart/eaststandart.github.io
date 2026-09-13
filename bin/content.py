#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content
@about Главный изолированный конвейер предобработки и оформления контента.
@purpose Сортирует новости по дате и собирает эмодзи строго из файлов-вывесок
         и родительских разделов по канонам гибридного автомата Tracy.
@author TechLab
@version 3.0.0-emoji-perfection
"""

import os
import re
import yaml

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

def find_url_in_navigation(nav_data, project_slug, file_name_clean, folder_parts, data):
    """Ищет идеальный интернет-адрес страницы внутри карты navigation.yml."""
    if folder_parts == '_posts':
        post_date = str(data.get('date', ''))
        for section_name, projects in nav_data.get('sections', {}).items():
            for proj in projects:
                if proj.get('slug') == project_slug:
                    for key in ['journal_posts', 'media_posts']:
                        if key in proj:
                            for post in proj[key]:
                                if post.get('date') == post_date and file_name_clean in post.get('url', ''):
                                    return post.get('url')
    else:
        for section_name, projects in nav_data.get('sections', {}).items():
            for proj in projects:
                if proj.get('slug') == project_slug:
                    return proj.get('url')
    return None

def build_pinned_news_list():
    """Главная функция: собирает ленту новостей на основе первоисточников свойств."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
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

    # 🔥 ШАГ А: СБОР ЭТАЛОННЫХ ЭМОДЗИ ТИПОВ ПОСТОВ ИЗ ПАПКИ _PAGES
    pages_dir = os.path.join(root_dir, '_pages')
    page_types_emoji = {}
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                p_data, _, _ = parse_yaml_front_matter(os.path.join(pages_dir, file))
                if p_data and p_data.get('emoji'):
                    p_slug, _ = os.path.splitext(file)
                    page_types_emoji[p_slug] = p_data['emoji']

    # 🔥 ШАГ Б: СБОР РОДИТЕЛЬСКИХ ЭМОДЗИ ДЛЯ СТАРЫХ РАЗДЕЛОВ (РЕЖИМ А)
    section_index_emoji = {}
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and name not in EXCLUDED_FOLDERS and not name.startswith('.'):
            idx_path = os.path.join(root_dir, name, 'index.md')
            if os.path.exists(idx_path):
                i_data, _, _ = parse_yaml_front_matter(idx_path)
                if i_data and i_data.get('emoji'):
                    section_index_emoji[name.lstrip('_')] = i_data['emoji']

    # 2. СКАНИРОВАНИЕ И СБОР ЛЕНТЫ
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS and not d.startswith('.')]
        for file in files:
            if not file.endswith('.md') or file == 'index.md': continue
                
            full_path = os.path.join(root, file)
            data, front_text, body = parse_yaml_front_matter(full_path)
            if data is None or not data.get('date'): continue

            rel_path = os.path.relpath(full_path, root_dir)
            folder_parts = rel_path.split(os.sep)
            
            file_name_clean, _ = os.path.splitext(file)
            file_name_clean_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)
            
            if folder_parts == '_posts':
                project_slug = file_name_clean_no_date
                current_folder_type = '_posts'
            else:
                project_slug = file_name_clean
                current_folder_type = folder_parts

            item_url = find_url_in_navigation(nav_data, project_slug, file_name_clean_no_date, current_folder_type, data)
            if not item_url:
                item_url = f"/{folder_parts.lstrip('_')}/{project_slug}.html"

            item_date = str(data.get('date', '1970-01-01'))
            is_post_flag = "true" if folder_parts == '_posts' else "false"

            # 🔥 ФИНАЛЬНЫЙ АВТОМАТ ВЫЧИСЛЕНИЯ ЭМОДЗИ СТРОГО ПО ПЕРВОИСТОЧНИКАМ
            section_name = data.get('section', folder_parts.lstrip('_'))
            
            if folder_parts == '_posts':
                # Очередь 1: Посты хроники - берут эмодзи из вывесок типов постов в _pages/
                post_type = data.get('post-page', 'journal')
                section_emoji = page_types_emoji.get(post_type, "")
            elif section_name in section_index_emoji:
                # Очередь 3: Книги/статьи Режима А - нативно считывают эмодзи родительской вывески раздела
                section_emoji = section_index_emoji.get(section_name, "")
            else:
                # Очередь 2: Карточки проектов Режима Б - берут свой родной эмодзи из Front Matter
                section_emoji = data.get('emoji', "")

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

    # 3. АВТОМАТИЧЕСКАЯ СОРТИРОВКА ЗАКРЕПЛЕНИЙ ПО ДАТЕ
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    final_feed = pinned_posts + regular_posts
    
    log_buffer.append("[CON-SUCCESS] Серверный конвейер новостей успешно интегрирован с навигацией.")
    log_buffer.append(f"Всего собрано публикаций в ленту: {len(final_feed)}")

    # 4. ЗАПИСЬ ГОТОВОЙ ЛЕНТЫ В СИСТЕМУ JEKYLL
    data_dir = os.path.join(root_dir, '_data')
    output_feed_path = os.path.join(data_dir, 'news_feed.yml')
    try:
        with open(output_feed_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except Exception as e:
        log_buffer.append(f"[CON-ERROR] Не удалось записать файл news_feed.yml: {e}")

    # 📂 ВЫГРУЗКА ОТЧЕТОВ В АРХИВ АРТЕФАКТОВ CONTENT
    content_debug_dir = os.path.join(root_dir, '_content_files')
    os.makedirs(content_debug_dir, exist_ok=True)

    processed_news_path = os.path.join(content_debug_dir, 'processed-news_feed.yml')
    with open(processed_news_path, 'w', encoding='utf-8') as pnf:
        yaml.dump({'feed': final_feed}, pnf, allow_unicode=True, default_flow_style=False, sort_keys=False)

    try:
        log_file_path = os.path.join(content_debug_dir, 'content_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
    except Exception as e:
        print(f"[CON-ERROR] Не удалось сохранить файл лога контента: {e}")

if __name__ == '__main__':
    build_pinned_news_list()
