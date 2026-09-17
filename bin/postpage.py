#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module post-page
@about Изолированный автономный генератор физических md-страниц архивов проектов.
@purpose Автоматическая штамповка страниц под кнопку "0" с динамическим объединением
         свойств во Front Matter, mathjax, чистокровной серверной фильтрацией 
         и автоматической зачисткой пустых строк бэкенда.
@author TechLab
@version 8.0.0-dynamic-frontmatter
"""

import os
import sys
import yaml

def generate_project_posts_pages():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    feed_file = os.path.join(root_dir, '_data', 'feed.yml')
    navigation_file = os.path.join(root_dir, '_data', 'navigation.yml')
    log_file_path = os.path.join(root_dir, '_post_page_files', 'posts-page-generator.log')
    
    log_buffer = []
    
    # Проверяем наличие Источников Правды контура
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

    created_pages_registry = set()

    # Шаг 2: Сканирование универсальной ленты и генерация изолированных страниц
    for item in feed_source:
        p_related = item.get('related')
        p_type = item.get('posttype')
        is_post_valid = item.get('is_post') == 'true' or item.get('is_post') is True
        
        if p_related and p_type and is_post_valid:
            page_uid = f"{p_type}::{p_related}"
            if page_uid in created_pages_registry:
                continue
                
            # ИСПРАВЛЕНИЕ ТРАНСЛИТА: Ищем красивое русское имя родительского проекта в navigation.yml
            parent_title = p_related.replace('-', ' ').capitalize() # Резервный вариант
            
            for file_key, nodes in navigation_map.items():
                if isinstance(nodes, list) and len(nodes) > 0:
                    card = nodes
                    # ЖЁСТКИЙ ПРЕДОХРАНИТЕЛЬ: обрабатываем только словари паспортов проектов, отсекая root-строки
                    if isinstance(card, dict):
                        card_url = card.get('url', '').strip('/')
                        if card_url and card_url.split('/')[-1] == p_related:
                            if card.get('title'):
                                parent_title = card['title'].strip()
                                break

            target_folder_path = os.path.join(root_dir, p_type)
            os.makedirs(target_folder_path, exist_ok=True)
            
            target_md_file = os.path.join(target_folder_path, f"{p_related}.md")
            
            # 🔥 ОБЩИЕ ПРАВИЛА: Базовый расширяемый словарь свойств индивидуальной страницы
            base_front_matter = {
                "layout": "page",
                "title": f"{parent_title}: лента постов",
                "permalink": f"/{p_type}/{p_related}/",
                "mathjax": True
                # Сюда в будущем можно добавлять любые свойства в один клик: "comments": True, и т.д.
            }
            
            # Превращаем структурированный словарь свойств в чистокровную YAML-шапку контура
            front_matter_string = yaml.dump(base_front_matter, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
            # Шаг 3: Формируем тело маркдаун-страницы с нативной фильтрацией
            body_lines = [
                '<!--1. HTML-СКЕЛЕТ ВЫВОДА ПОЛНОЦЕННЫХ ПУБЛИКАЦИЙ ПРОЕКТА ИЗ FEED.YML -->',
                '<div id="media-container" class="media-archive-list-wrapper">',
                '  {%- comment -%} Серверная фильтрация массива строго под текущий проект контура {%- endcomment -%}',
               f'  {{%- assign project_posts = site.data.feed.feed | where: "related", "{p_related}" | where: "posttype", "{p_type}" | where: "is_post", "true" -%}}',
                '  ',
                '  {%- for feed_item in project_posts -%}',
                '    {%- assign post = site.posts | where: "url", feed_item.url | first -%}',
                '    {%- if post == nil -%}',
                '      {%- assign post = site.pages | where: "url", feed_item.url | first -%}',
                '    {%- endif -%}',
                '    ',
                '    {%- if post -%}',
                '      <div class="media-entry">',
                '        <!-- Контейнер строки даты и заголовка -->',
                '        <div class="media-entry-title-row">',
                '          <span class="media-entry-date">{{ post.date | date: "%d.%m.%Y" }}</span>',
                '          <h3 class="media-entry-title">{{ post.title }}</h3>',
                '        </div>',
                '        ',
                '        <!-- Оболочка основного контента статьи (1 в 1 как на старом сайте) -->',
                '        <div class="media-content main-content">',
                '          {%- if post.description and post.description != "" -%}',
                '            <p class="page-description">{{ post.description }}</p>',
                '          {%- endif -%}',
                '          ',
                '          {{ post.content }}',
                '          ',
                '          {%- if post.author and post.author != "" -%}',
                '          <!-- А. БЛОК ВЫВОДА АВТОРА -->',
                '          <div class="author-inline">',
                '              <strong>Автор:</strong> ',
                '              <div class="sources-content">{{ post.author }}</div>',
                '          </div>',
                '          {%- endif -%}',
                '          ',
                '          {%- if post.sources and post.sources != "" -%}',
                '          <!-- Б. БЛОК ВЫВОДА ИСТОЧНИКОВ -->',
                '          <div class="sources-inline">',
                '              <strong>Источники:</strong>',
                '              <div class="sources-content">{{ post.sources | markdownify }}</div>',
                '          </div>',
                '          {%- endif -%}',
                '          ',
                '          {%- if post.tags.size > 0 -%}',
                '          <!-- В. БЛОК ВЫВОДА ТЕГОВ -->',
                '          <div class="tag-container">',
                '              {%- for tag in post.tags -%}',
                '                  {%- assign tag_clean = tag | replace: "#", "" | strip -%}',
                '                  <a href="{{ \'/tags.html\' | relative_url }}#{{ tag_clean | slugify }}" class="tag-item">{{ tag_clean }}</a>',
                '              {%- endfor -%}',
                '          </div>',
                '          {%- endif -%}',
                '        </div>',
                '        ',
                '        {%- comment -%} НАСТОЯЩАЯ СЕРВЕРНАЯ ЗАЧИСТКА: Линия создаётся только если впереди есть посты {%- endcomment -%}',
                '        {%- unless forloop.last -%}',
                '          <hr class="media-entry-hr">',
                '        {%- endunless -%}',
                '      </div>',
                '    {%- endif -%}',
                '  {%- endfor -%}',
                '</div>' # 🧼 Закрывающий тег прижат вплотную, предотвращая пустые строки Kramdown!
            ]
            
            body_content_string = "\n".join(body_lines)
            
            # Собираем файл воедино, зачищая концевые переносы методом .strip()
            file_content = f"---\n{front_matter_string}---\n\n{body_content_string}".strip()
            
            try:
                with open(target_md_file, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                log_msg = f"[POST-GENERATOR] Создан файл: {p_type}/{p_related}.md | Свойства объединены динамически."
                print(log_msg)
                log_buffer.append(log_msg)
                created_pages_registry.add(page_uid)
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
