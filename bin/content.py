#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content
@about Главный изолированный конвейер предобработки и оформления контента.
@purpose Автоматически собирает маркеры оформления из Obsidian, сортирует контент
         и генерирует идеальные готовые ленты данных в _data/news_feed.yml.
@author TechLab
@version 1.2.0-pure-backend
"""

import os
import re
import yaml

# ==========================================================================
# СЕРВИСНЫЙ БЛОК: ИНСТРУМЕНТЫ РАБОТЫ С ДАННЫМИ (НЕ ИЗМЕНЯЮТСЯ)
# ==========================================================================

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

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства обратно в markdown-файл."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[CON-ERROR] Не удалось перезаписать файл {file_path}: {e}")


# ==========================================================================
# МОДУЛЬ А: СБОРКА И ЗАКРЕПЛЕНИЕ ЛЕНТЫ НОВОСТЕЙ (ПОЛНОСТЬЮ НА СЕРВЕРЕ)
# ==========================================================================

def build_pinned_news_list(root_dir, content_debug_dir, log_buffer):
    """Сканирует весь сайт, формирует готовую отсортированную ленту с закреплениями вверху."""
    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    
    pinned_posts = []
    regular_posts = []

    # 1. СБОР И КЛАССИФИКАЦИЯ АБСОЛЮТНО ВСЕХ ЗАМЕТОК НА САЙТЕ
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

            # Формируем чистый узел новости для вывода
            news_node = {
                'title': data.get('title', file),
                'url': item_url,
                'date': item_date,
                'is_post': is_post_flag,
                'path': rel_path,
                'pinned': False
            }

            # Фильтруем на закрепленные и обычные
            if data.get('pinnednews') is True:
                news_node['pinned'] = True
                pinned_posts.append(news_node)
            else:
                regular_posts.append(news_node)

    # 2. ОДНОВРЕМЕННАЯ СОРТИРОВКА ПО ДАТЕ ВНУТРИ КАЖДОЙ ГРУППЫ
    pinned_posts.sort(key=lambda x: x['date'], reverse=True)
    regular_posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Склеиваем монолит: сначала все закрепленные по дате, затем все обычные по дате!
    final_feed = pinned_posts + regular_posts
    
    # 3. ФИЗИЧЕСКАЯ ЗАПИСЬ ИДЕАЛЬНОЙ ГОТОВОЙ ЛЕНТЫ В _DATA/NEWS_FEED.YML
    data_dir = os.path.join(root_dir, '_data')
    output_feed_path = os.path.join(data_dir, 'news_feed.yml')
    
    try:
        with open(output_feed_path, 'w', encoding='utf-8') as f:
            yaml.dump({'feed': final_feed}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        log_buffer.append(f"[CON-SUCCESS] Готовая серверная лента успешно сохранена в _data/news_feed.yml. Всего постов: {len(final_feed)}")
        log_buffer.append(f"  [➔] Из них закреплено и отсортировано вверху: {len(pinned_posts)}")
    except Exception as e:
        log_buffer.append(f"[CON-ERROR] Не удалось записать файл данных ленты news_feed.yml: {e}")

    # Дублируем для контроля в наш новый архив контента
    processed_news_path = os.path.join(content_debug_dir, 'processed-news_feed.yml')
    with open(processed_news_path, 'w', encoding='utf-8') as pnf:
        yaml.dump({'feed': final_feed}, pnf, allow_unicode=True, default_flow_style=False, sort_keys=False)


# ==========================================================================
# ГЛАВНАЯ ТОЧКА ВХОДА И УПРАВЛЕНИЯ КОНВЕЙЕРОМ
# ==========================================================================

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    content_debug_dir = os.path.join(root_dir, '_content_files')
    os.makedirs(content_debug_dir, exist_ok=True)
    
    global_content_log = []
    
    # Запуск изолированного модуля А
    build_pinned_news_list(root_dir, content_debug_dir, global_content_log)
    
    for line in global_content_log:
        print(line)
        
    try:
        log_file_path = os.path.join(content_debug_dir, 'content_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(global_content_log))
        print(f"[CON-SUCCESS] Лог-отчет успешно упакован в архив content.")
    except Exception as e:
        print(f"[CON-ERROR] Не удалось сохранить итоговый файл лога: {e}")

if __name__ == '__main__':
    main()
