#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content
@about Главный изолированный конвейер предобработки и оформления контента.
@purpose Автоматически собирает маркеры pinnednews, сортирует контент по дате
         и генерирует готовую ленту данных в файл _data/news_feed.yml.
@author TechLab
@version 1.4.0-pure-backend-fixed
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

def build_pinned_news_list():
    """Главная функция: сканирует сайт, сортирует по дате и пишет готовую ленту в yml-данные."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    
    pinned_posts = []
    regular_posts = []
    log_buffer = []

    # 1. СКАНИРОВАНИЕ И СБОР ВСЕХ ЗАМЕТОК
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS and not d.startswith('.')]
        for file in files:
            if not file.endswith('.md'): continue
                
            full_path = os.path.join(root, file)
            data, front_text, body = parse_yaml_front_matter(full_path)
            if data is None or not data.get('date'): continue

            rel_path = os.path.relpath(full_path, root_dir)
            folder_parts = rel_path.split(os.sep)
            
            # Вычисляем URL
            item_url = data.get('permalink')
            if not item_url:
                if folder_parts[0].startswith('_'):
                    coll_name = folder_parts[0].lstrip('_')
                    file_clean, _ = os.path.splitext(file)
                    item_url = f"/{coll_name}/{file_clean}/"
                else:
                    dir_url = "/".join(folder_parts[:-1])
                    file_clean, _ = os.path.splitext(file)
                    if file_clean == 'index':
                        item_url = f"/{dir_url}/" if dir_url else "/"
                    else:
                        item_url = f"/{dir_url}/{file_clean}/" if dir_url else f"/{file_clean}/"
            
            item_url = "/" + item_url.strip("/") + "/"
            item_date = str(data.get('date', '1970-01-01'))
            is_post_flag = "true" if '_posts' in full_path else "false"

            news_node = {
                'title': data.get('title', file),
                'url': item_url,
                'date': item_date,
                'is_post': is_post_flag,
                'path': rel_path,
                'pinned': False
            }

            if data.get('pinnednews') is True:
                news_node['pinned'] = True
                pinned_posts.append(news_node)
            else:
                regular_posts.append(news_node)

    # 2. АВТОМАТИЧЕСКАЯ СОРТИРОВКА ПО ХРОНОЛОГИИ (ОТ СВЕЖИХ К СТАРЫМ)
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    
    final_feed = pinned_posts + regular_posts
    
    # Сборка красивого текстового лога для артефактов
    log_buffer.append("[CON-SUCCESS] Сборка ленты _data/news_feed.yml завершена успешно.")
    log_buffer.append(f"Всего обработано и отсортировано публикаций: {len(final_feed)}")
    log_buffer.append("\n==========================================================================")
    log_buffer.append(f"ЭТАП 1: ЗАКРЕПЛЕННЫЕ ПОСТЫ ПО МАРКЕРУ pinnednews (Всего: {len(pinned_posts)}):")
    log_buffer.append("==========================================================================")
    for idx, item in enumerate(pinned_posts, 1):
        log_buffer.append(f"  [{idx}] Дата: {item['date']} | Заголовок: {item['title']} | Путь: {item['path']}")
        
    log_buffer.append("\n==========================================================================")
    log_buffer.append(f"ЭТАП 2: ОБЫЧНЫЕ ПОСТЫ ХРОНИКИ И ОБНОВЛЕНИЙ (Всего: {len(regular_posts)}):")
    log_buffer.append("==========================================================================")
    for idx, item in enumerate(regular_posts, 1):
        if idx <= 15:
            log_buffer.append(f"  [{idx}] Дата: {item['date']} | Заголовок: {item['title']} | Путь: {item['path']}")
    if len(regular_posts) > 15:
        log_buffer.append(f"  ... и остальные {len(regular_posts) - 15} обычных заметок списка.")

    # 3. ЗАПИСЬ ГОТОВОЙ СТРУКТУРЫ В _DATA/NEWS_FEED.YML
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)
    output_feed_path = os.path.join(data_dir, 'news_feed.yml')
    try:
        with open(output_feed_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except Exception as e:
        log_buffer.append(f"[CON-ERROR] Не удалось записать файл данных ленты news_feed.yml: {e}")

    # 4. ФИЗИЧЕСКИЙ ВЫВОД И КУПИРОВАНИЕ ЛОГОВ В АРХИВ CONTENT
    content_debug_dir = os.path.join(root_dir, '_content_files')
    os.makedirs(content_debug_dir, exist_ok=True)

    # Записываем контрольный yml в папку нового архива
    processed_news_path = os.path.join(content_debug_dir, 'processed-news_feed.yml')
    with open(processed_news_path, 'w', encoding='utf-8') as pnf:
        yaml.dump({'feed': final_feed}, pnf, allow_unicode=True, default_flow_style=False, sort_keys=False)

    for line in log_buffer:
        print(line)

    try:
        log_file_path = os.path.join(content_debug_dir, 'content_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print(f"[CON-SUCCESS] Лог-отчет успешно упакован в архив content.")
    except Exception as e:
        print(f"[CON-ERROR] Не удалось сохранить итоговый файл лога: {e}")

if __name__ == '__main__':
    build_pinned_news_list()
