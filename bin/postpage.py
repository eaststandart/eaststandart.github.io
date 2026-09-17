#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module post-page
@about Изолированный автономный генератор физических md-страниц архивов проектов.
@purpose Полная монолитная сборка развёрнутых маркдаун-лент под кнопку "0" силами Python.
         Скрипт сам читает контент из _posts, вычисляет финальный пост, внедряет 
         индивидуальные стили и отдаёт Jekyll абсолютно чистый HTML/Markdown без Liquid-кода.
@author TechLab
@version 9.0.0-pure-python-compiler
"""

import os
import sys
import re
import yaml

def get_post_markdown_body(root_dir, url_path):
    """📖 МОДУЛЬ ЧТЕНИЯ: Находит оригинальный .md файл в _posts и извлекает тело без Front Matter."""
    url_clean = url_path.strip('/')
    posts_dir = os.path.join(root_dir, '_posts')
    if not os.path.exists(posts_dir) or not url_clean:
        return ""
        
    target_file_name = None
    # Ссылки в фиде имеют вид: /journal/muzykalnyj-karandash/2026/04/18/muzykalnyj-karandash.html
    # Имена файлов в _posts имеют вид: YYYY-MM-DD-slug.md
    for f in os.listdir(posts_dir):
        if f.endswith('.md'):
            f_base, _ = os.path.splitext(f)
            f_date = f_base[:10]  # Извлекаем дату YYYY-MM-DD
            f_slug = f_base[11:]  # Извлекаем чистый слаг
            if f_slug in url_clean and f_date.replace('-', '/') in url_clean:
                target_file_name = f
                break
                
    if not target_file_name:
        return ""
        
    full_post_path = os.path.join(posts_dir, target_file_name)
    try:
        with open(full_post_path, 'r', encoding='utf-8') as pf:
            p_content = pf.read()
        # Отсекаем шапку Front Matter
        match = re.match(r'^---\s*\n.*?\n---\s*\n', p_content, re.DOTALL)
        if match:
            return p_content[match.end():].strip()
        return p_content.strip()
    except:
        return ""

def generate_project_posts_pages():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    feed_file = os.path.join(root_dir, '_data', 'feed.yml')
    navigation_file = os.path.join(root_dir, '_data', 'navigation.yml')
    log_file_path = os.path.join(root_dir, '_post_page_files', 'posts-page-generator.log')
    
    log_buffer = []
    
    if not os.path.exists(feed_file):
        print(f"[POST-ERROR] Источник Правды feed.yml не найден по пути: {feed_file}")
        return
    if not os.path.exists(navigation_file):
        print(f"[POST-ERROR] Карта навигации navigation.yml не найдена: {navigation_file}")
        return

    # Шаг 1: Загружаем данные в оперативную память
    try:
        with open(feed_file, 'r', encoding='utf-8') as f:
            feed_data = yaml.safe_load(f) or {}
        feed_source = feed_data.get('feed', [])
        
        with open(navigation_file, 'r', encoding='utf-8') as f:
            navigation_map = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[POST-ERROR] Сбой чтения конфигурационных файлов YAML: {e}")
        return

    # 🧼 САНИТАРНАЯ ЗАЧИСТКА ПАПОК ОТ СТРАНИЦ-ПРИЗРАКОВ
    print("[POST-CLEAN] Запуск санитарной зачистки целевых папок контура...")
    for target_folder in ['journal', 'media']:
        folder_path = os.path.join(root_dir, target_folder)
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.md') and 'index' not in file_name:
                    file_to_remove = os.path.join(folder_path, file_name)
                    try:
                        os.remove(file_to_remove)
                        log_buffer.append(f"[CLEAN] Удален устаревший файл: {target_folder}/{file_name}")
                    except Exception as e:
                        print(f"[POST-ERROR] Не удалось удалить файл {file_to_remove}: {e}")

    # Шаг 2: Группируем элементы фида по уникальным проектам на сервере
    projects_data = {}
    for item in feed_source:
        p_related = item.get('related')
        p_type = item.get('posttype')
        is_post_valid = item.get('is_post') == 'true' or item.get('is_post') is True
        
        if p_related and p_type and is_post_valid:
            page_uid = f"{p_type}::{p_related}"
            if page_uid not in projects_data:
                projects_data[page_uid] = {
                    'project': p_related,
                    'type': p_type,
                    'items': []
                }
            projects_data[page_uid]['items'].append(item)

    # Шаг 3: Монолитная сборка страниц силами Python
    for page_uid, proj_info in projects_data.items():
        p_related = proj_info['project']
        p_type = proj_info['type']
        p_items = proj_info['items']
        
        # Вычисляем красивый русский заголовок родительского проекта
        parent_title = p_related.replace('-', ' ').capitalize()
        for file_key, nodes in navigation_map.items():
            if isinstance(nodes, list) and len(nodes) > 0:
                card = nodes
                if isinstance(card, dict):
                    card_url = card.get('url', '').strip('/')
                    if card_url and card_url.split('/')[-1] == p_related:
                        if card.get('title'):
                            parent_title = card['title'].strip()
                            break

        target_folder_path = os.path.join(root_dir, p_type)
        os.makedirs(target_folder_path, exist_ok=True)
        target_md_file = os.path.join(target_folder_path, f"{p_related}.md")
        
        # Динамическое объединение свойств Front Matter
        base_front_matter = {
            "layout": "page",
            "title": f"{parent_title}: лента постов",
            "permalink": f"/{p_type}/{p_related}/",
            "mathjax": True
        }
        front_matter_string = yaml.dump(base_front_matter, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        # Начинаем сборку тела HTML/Markdown-страницы контура
        body_lines = [
            '<!--1. ПОЛНОСТЬЮ СКОМПИЛИРОВАННЫЙ НА СЕРВЕРЕ HTML-СКЕЛЕТ ЛЕНТЫ ПРОЕКТА -->',
            '<div id="media-container" class="media-archive-list-wrapper">'
        ]
        
        # Бежим по отфильтрованным постам этого проекта
        for idx, item in enumerate(p_items):
            post_title = item.get('title', '')
            post_date_raw = item.get('date', '')
            post_url = item.get('url', '')
            
            # Приводим дату к красивому формату DD.MM.YYYY
            try:
                dt = post_date_raw.split('-')
                post_date_clean = f"{dt[2]}.{dt[1]}.{dt[0]}"
            except:
                post_date_clean = post_date_raw
                
            # Извлекаем живой маркдаун заметки напрямую из файла папки _posts/
            post_markdown_body = get_post_markdown_body(root_dir, post_url)
            
            # 🔥 ИНЖЕНЕРНАЯ ОПТИМИЗАЦИЯ: Вычисляем финальный пост контура средствами Python
            is_last_post = (idx == len(p_items) - 1)
            
            if is_last_post:
                # Впечатываем обнуление отступа для последнего поста
                body_lines.append('  <div class="media-entry" style="margin-bottom: 0px !important;">')
            else:
                body_lines.append('  <div class="media-entry">')
                
            body_lines.extend([
                '    <!-- Контейнер строки даты и заголовка -->',
                '    <div class="media-entry-title-row">',
                f'      <span class="media-entry-date">{post_date_clean}</span>',
                f'      <h3 class="media-entry-title">{post_title}</h3>',
                '    </div>',
                '    ',
                '    <!-- Оболочка основного контента статьи (1 в 1 как на старом сайте) -->',
                '    <div class="media-content main-content">',
                "",
                # Выливаем чистый оригинальный маркдаун поста вплотную к левому краю
                post_markdown_body,
                "",
                '    </div>'
            ])
            
            # Линию <hr> пишем только если это НЕ последний пост проекта!
            if not is_last_post:
                body_lines.extend([
                    '    <hr class="media-entry-hr">',
                    '  </div>'
                ])
            else:
                body_lines.append('  </div>')
                
        body_lines.append('</div>')
        body_content_string = "\n".join(body_lines)
        
        # Собираем файл воедино и зачищаем пустые концевые строки
        file_content = f"---\n{front_matter_string}---\n\n{body_content_string}".strip()
        
        try:
            with open(target_md_file, 'w', encoding='utf-8') as f:
                f.write(file_content)
            log_msg = f"[POST-GENERATOR] Создан файл: {p_type}/{p_related}.md | Сборка Варианта Б (Чистый бэкенд Питона)."
            print(log_msg)
            log_buffer.append(log_msg)
        except Exception as e:
            print(f"[POST-ERROR] Не удалось записать файл архива {target_md_file}: {e}")

    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[POST-SUCCESS] Изолированный лог генератора страниц успешно сохранён.")
    except Exception as e:
        print(f"[POST-ERROR] Не удалось сохранить файл лога: {e}")

if __name__ == '__main__':
    generate_project_posts_pages()
