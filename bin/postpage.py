#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module post-page
@about Изолированный автономный генератор физических md-страниц архивов проектов.
@purpose Автоматическая сборка монолитных маркдаун-лент под кнопку "0" на основе 
         данных feed.yml, сквозного чтения _posts и санитарной зачистки диска.
@author TechLab
@version 3.1.0-split-stable
"""

import os
import sys
import re
import yaml

def clean_expired_project_pages(root_dir, log_buffer):
    """🧼 САНИТАРНАЯ ЗАЧИСТКА: Удаляет старые сгенерированные файлы, избегая страниц-призраков."""
    print("[POST-CLEAN] Запуск санитарной зачистки целевых папок контура...")
    for target_folder in ['journal', 'media']:
        folder_path = os.path.join(root_dir, target_folder)
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                # Удаляем только .md файлы проектов, не трогая главные индексы папок
                if file_name.endswith('.md') and 'index' not in file_name:
                    file_to_remove = os.path.join(folder_path, file_name)
                    try:
                        os.remove(file_to_remove)
                        log_buffer.append(f"[CLEAN] Удален устаревший файл: {target_folder}/{file_name}")
                    except Exception as e:
                        print(f"[POST-ERROR] Не удалось удалить файл {file_to_remove}: {e}")

def get_post_markdown_body(root_dir, url_path):
    """📖 МОДУЛЬ ЧТЕНИЯ: Находит оригинальный .md файл в _posts и извлекает тело без Front Matter."""
    url_clean = url_path.strip('/')
    posts_dir = os.path.join(root_dir, '_posts')
    if not os.path.exists(posts_dir) or not url_clean:
        return ""
        
    target_file_name = None
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
    """🚀 ГЛАВНЫЙ ДИСПЕТЧЕР: Сканирует feed.yml и штампует монолитные маркдаун-страницы проектов."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    feed_file = os.path.join(root_dir, '_data', 'feed.yml')
    log_file_path = os.path.join(root_dir, '_post_page_files', 'posts-page-generator.log')
    
    log_buffer = []
    
    if not os.path.exists(feed_file):
        print(f"[POST-ERROR] Источник Правды feed.yml не найден по пути: {feed_file}")
        return

    try:
        with open(feed_file, 'r', encoding='utf-8') as f:
            feed_data = yaml.safe_load(f) or {}
        feed_source = feed_data.get('feed', [])
    except Exception as e:
        print(f"[POST-ERROR] Сбой чтения файла универсальной ленты: {e}")
        return

    # Запускаем санитарную зачистку из Части 1
    clean_expired_project_pages(root_dir, log_buffer)

    # Группируем посты по проектам на основе feed.yml
    projects_to_generate = {}
    for item in feed_source:
        p_related = item.get('related')
        p_type = item.get('posttype')
        is_post_valid = item.get('is_post') == 'true' or item.get('is_post') is True
        
        if p_related and p_type and is_post_valid:
            page_uid = f"{p_type}::{p_related}"
            if page_uid not in projects_to_generate:
                projects_to_generate[page_uid] = {'project': p_related, 'type': p_type, 'items': []}
            projects_to_generate[page_uid]['items'].append(item)

    # Цикл склейки живых маркдаун-страниц под кнопку "0"
    for uid, proj_info in projects_to_generate.items():
        p_slug = proj_info['project']
        p_type = proj_info['type']
        p_items = proj_info['items']
        
        parent_title = p_slug.replace('-', ' ').capitalize()
        target_folder_path = os.path.join(root_dir, p_type)
        os.makedirs(target_folder_path, exist_ok=True)
        
        target_md_file = os.path.join(target_folder_path, f"{p_slug}.md")
        
        front_matter_lines = [
            "---",
            "layout: page",
            f'title: "{parent_title}: лента проекта"',
            f'project: "{p_slug}"',
            f'posttype: "{p_type}"',
            f"permalink: /{p_type}/{p_slug}/",
            "---",
            "",
            '<div id="media-container" class="media-archive-list-wrapper">',
            ""
        ]
        
        for idx, item in enumerate(p_items):
            post_title = item.get('title', '')
            post_date_raw = item.get('date', '')
            post_url = item.get('url', '')
            post_emoji = item.get('emoji', '')
            
            try:
                dt = post_date_raw.split('-')
                post_date_clean = f"{dt[2]}.{dt[1]}.{dt[0]}"
            except:
                post_date_clean = post_date_raw
                
            # Запрашиваем живое маркдаун-тело статьи из Части 1
            post_markdown_body = get_post_markdown_body(root_dir, post_url)
            emoji_str = f"{post_emoji} " if post_emoji else ""
            
            front_matter_lines.extend([
                '<div class="media-entry">',
                '  <div class="media-entry-title-row">',
                f'    <span class="media-entry-date">{post_date_clean}</span>',
                f'    <h3 class="media-entry-title">{emoji_str}{post_title}</h3>',
                '  </div>',
                '  <div class="media-content main-content">',
                "",
                post_markdown_body,
                "",
                '  </div>'
            ])
            
            if idx < len(p_items) - 1:
                front_matter_lines.extend(['  <hr class="media-entry-hr">', '</div>', ""])
            else:
                front_matter_lines.extend(['</div>', ""])
                
        front_matter_lines.extend([
            "</div>", "",
            f'<script src="/assets/js/media-archive-filter.js"></script>',
            "<script>",
            "  (function() {",
            "    if (typeof runMediaArchiveFilter === 'function') { runMediaArchiveFilter(); }",
            "  })();",
            "</script>"
        ])
        
        try:
            with open(target_md_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(front_matter_lines))
            log_msg = f"[POST-GENERATOR] Файл: {p_type}/{p_slug}.md | Монолитный Markdown успешно склеен ({len(p_items)} постов)."
            print(log_msg)
            log_buffer.append(log_msg)
        except Exception as e:
            print(f"[POST-ERROR] Не удалось записать файл архива {target_md_file}: {e}")

    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[POST-SUCCESS] Излированный лог генератора страниц успешно сохранён.")
    except Exception as e:
        print(f"[POST-ERROR] Не удалось сохранить файл лога: {e}")

if __name__ == '__main__':
    generate_project_posts_pages()
