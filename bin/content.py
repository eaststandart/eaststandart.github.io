#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content
@about Изолированный препроцессор для автоматического управления свойствами контента.
@purpose Находит маркеры pinnednews: true в файлах, сортирует их по дате и автоматически
         прописывает отсортированный массив pinned_urls в _pages/news.md.
@author TechLab
@version 1.0.0-multi-pin
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

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства обратно в markdown-файл."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[CON-ERROR] Не удалось перезаписать файл {file_path}: {e}")

def build_pinned_news_list():
    """Сканирует сайт на наличие pinnednews: true, формирует отсортированный список URL."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    
    pinned_items = []

    # 1. СКАНИРОВАНИЕ ВСЕХ ФАЙЛОВ КОНТЕНТА НА САЙТЕ
    for root, dirs, files in os.walk(root_dir):
        # Исключаем системные каталоги на лету
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS and not d.startswith('.')]
        
        for file in files:
            if not file.endswith('.md'):
                continue
                
            full_path = os.path.join(root, file)
            data, front_text, body = parse_yaml_front_matter(full_path)
            if data is None:
                continue

            # Находим маркер, который вы прописали в Obsidian
            if data.get('pinnednews') is True:
                rel_path = os.path.relpath(full_path, root_dir)
                folder_parts = rel_path.split(os.sep)
                
                # Забираем пермалинк, если он уже прописан жестко
                item_url = data.get('permalink')
                
                if not item_url:
                    # Если файл лежит в коллекции (например, _people/fran-blanche.md)
                    if folder_parts[0].startswith('_'):
                        coll_name = folder_parts[0].lstrip('_')
                        file_clean, _ = os.path.splitext(file)
                        item_url = f"/{coll_name}/{file_clean}/"
                    else:
                        # Если это обычная статичная страница
                        dir_url = "/".join(folder_parts[:-1])
                        file_clean, _ = os.path.splitext(file)
                        if file_clean == 'index':
                            item_url = f"/{dir_url}/" if dir_url else "/"
                        else:
                            item_url = f"/{dir_url}/{file_clean}/" if dir_url else f"/{file_clean}/"
                
                # Приводим URL к единому чистому стандарту Jekyll
                item_url = "/" + item_url.strip("/") + "/"
                
                # Забираем дату для сортировки (если даты нет, ставим дефолтную)
                item_date = str(data.get('date', '1970-01-01'))
                
                pinned_items.append({
                    'url': item_url,
                    'date': item_date
                })

    # 2. АВТОМАТИЧЕСКАЯ СОРТИРОВКА МАССИВА ПО ДАТЕ (ОТ СВЕЖИХ К СТАРЫМ)
    pinned_items.sort(key=lambda x: x['date'], reverse=True)
    
    # Собираем чистый список отсортированных URL-адресов
    final_urls = [item['url'] for item in pinned_items]
    
    # 3. ТОЧЕЧНАЯ ЗАПИСЬ МАССИВА В СТРАНИЦУ НОВОСТЕЙ
    news_page_path = os.path.join(root_dir, '_pages', 'news.md')
    content_log_buffer = []
    
    def log_content_action(text):
        print(text)
        content_log_buffer.append(text)

    # СОЗДАЕМ ОТДЕЛЬНУЮ СЕРВЕРНУЮ ПАПКУ ДЛЯ НОВОГО АРХИВА CONTENT
    content_debug_dir = os.path.join(root_dir, '_content_files')
    os.makedirs(content_debug_dir, exist_ok=True)

    if os.path.exists(news_page_path):
        news_data, n_front, n_body = parse_yaml_front_matter(news_page_path)
        if news_data is not None:
            news_data['pinned_urls'] = final_urls
            if 'pinned_url' in news_data:
                del news_data['pinned_url']
                
            write_yaml_front_matter(news_page_path, news_data, n_body)
            log_content_action(f"[CON-SUCCESS] В _pages/news.md успешно прописан массив из {len(final_urls)} закреплённых URL.")
            for idx, url in enumerate(final_urls, 1):
                log_content_action(f"  [{idx}] Закреплен адрес: {url}")
                
            # Дублируем обработанную страницу новостей в новый архив для контроля
            processed_news_path = os.path.join(content_debug_dir, 'processed-news.md')
            with open(processed_news_path, 'w', encoding='utf-8') as pnf:
                processed_news_front = yaml.dump(news_data, allow_unicode=True, default_flow_style=False, sort_keys=False)
                pnf.write(f"---\n{processed_news_front}---\n[Контент страницы новостей подготовлен]")
    else:
        log_content_action(f"[CON-ERROR] Файл _pages/news.md не найден на диске!")

    # Физически записываем отладочный лог в изолированную папку нового архива
    try:
        log_file_path = os.path.join(content_debug_dir, 'content_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(content_log_buffer))
        print(f"[CON-SUCCESS] Файлы модуля успешно направлены в новый архив: _content_files/content_debug.log")
    except Exception as e:
        print(f"[CON-ERROR] Не удалось сохранить файл лога в папку нового архива: {e}")

if __name__ == '__main__':
    build_pinned_news_list()
