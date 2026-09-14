#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content
@about Главный изолированный диспетчер сквозного оформления свойств файлов сайта.
@purpose Автоматически генерирует теги (tags) для markdown-файлов репозитория.
@version 7.1.0-global-buffer-stable
"""

import os
import re
import yaml
from navigation import build_navigation_tree
from contentnews import build_news_feed

# 🔥 УСПЕШНЫЙ СТАНДАРТ NAVIGATION: Глобальный буфер отчётов для артефактов
content_log_buffer = []

def log_content_artifact(text):
    """Выводит строку лога в консоль Actions и параллельно буферизирует её."""
    print(text)
    content_log_buffer.append(text)

def translit_title(text):
    if not text: return ""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9а-яё]', '', text)
    return text

def clean_tag(text):
    if not text: return ""
    return re.sub(r'\s+', '', str(text).lower().strip())

def parse_yaml_front_matter(file_path):
    content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None, None, content

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match: return None, None, content

    front_text = match.group(1)
    body_content = content[match.end():]

    try:
        data = yaml.safe_load(front_text)
        return data if data else {}, front_text, body_content
    except Exception as e:
        return None, None, content

def write_yaml_front_matter(file_path, data, body_content):
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        f_name = os.path.basename(file_path)
        
        # Запись строки лога напрямую в глобальный массив буфера
        log_content_artifact(f"[CON-DEBUG] Оформлен файл: {f_name} | Теги: {data.get('tags', [])}")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[CON-ERROR] Не удалось перезаписать файл {file_path}: {e}")

def process_all_markdown_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    
    # Очищаем буфер перед началом новой сквозной сборки
    global content_log_buffer
    content_log_buffer.clear()

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS and not d.startswith('.')]
        for file in files:
            if not file.endswith('.md') or file == 'index.md': continue
                
            full_path = os.path.join(root, file)
            data, front_text, body = parse_yaml_front_matter(full_path)
            if data is None: continue

            calculated_tags = []
            if data.get('direction'): calculated_tags.append(clean_tag(data['direction']))
            if data.get('entity'): calculated_tags.append(clean_tag(data['entity']))
            if data.get('level'): calculated_tags.append(f"{str(data['level']).strip()}класс")
            if data.get('title'): calculated_tags.append(translit_title(data['title']))
            if data.get('keywords'):
                if isinstance(data['keywords'], list):
                    for kw in data['keywords']: calculated_tags.append(clean_tag(kw))
                else: calculated_tags.append(clean_tag(data['keywords']))

            final_tags = []
            for t in calculated_tags:
                if t and t not in final_tags: final_tags.append(t)

            data['tags'] = final_tags
            if 'keywords' in data: del data['keywords']

            write_yaml_front_matter(full_path, data, body)

    log_content_artifact("[CON-SUCCESS] Модульный серверный конвейер оформления контента успешно выполнен.")
    log_content_artifact(f"Всего успешно оформлено markdown-файлов на диске: {len(content_log_buffer) - 1}")

    # 🔥 ЗАПИСЬ ИЗ ГЛОБАЛЬНОГО БУФЕРА ПО ОБРАЗУ NAVIGATION.PY
    try:
        debug_dir = os.path.join(root_dir, '_processed_files')
        os.makedirs(debug_dir, exist_ok=True)
        log_file_path = os.path.join(debug_dir, 'content_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(content_log_buffer))
        print("[CON-SUCCESS] Лог контента успешно зафиксирован в артефактах.")
    except Exception as e:
        print(f"[CON-ERROR] Не удалось сохранить файл лога: {e}")

    # 🔥 СКВОЗНОЙ КАСКАДНЫЙ ЗАПУСК КОНВЕЙЕРА: Карта сайта -> Лента новостей
    try:
        print("[CON-CONVEYER] Запуск автоматического дерева навигации...")
        build_navigation_tree()
    except Exception as e:
        print(f"[CON-CONVEYER-ERROR] Ошибка вызова navigation.py: {e}")

    try:
        print("[CON-CONVEYER] Запуск изолированного сборщика ленты новостей...")
        build_news_feed()
    except Exception as e:
        print(f"[CON-CONVEYER-ERROR] Ошибка вызова contentnews.py: {e}")

if __name__ == '__main__':
    process_all_markdown_files()
