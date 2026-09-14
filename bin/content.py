#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module content
@about Главный изолированный диспетчер сквозного оформления свойств файлов сайта.
@purpose Автоматически генерирует теги (tags) и категории (categories) для markdown-файлов
         внутри Obsidian и выгружает дубликаты логов в артефакты Actions.
@author TechLab
@version 6.0.0-pure-formatter
"""

import os
import re
import yaml

def translit_title(text):
    """Очищает заголовок, превращая его в монолитный тег строчными буквами без пробелов."""
    if not text: return ""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9а-яё]', '', text)
    return text

def clean_tag(text):
    """Сжимает пробелы внутри тега, приводя его к нижнему регистру."""
    if not text: return ""
    return re.sub(r'\s+', '', str(text).lower().strip())

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

def write_yaml_front_matter(file_path, data, body_content, log_buffer, root_dir):
    """Записывает свойства в файл и дублирует их в папку серверных артефактов."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        f_name = os.path.basename(file_path)
        log_buffer.append(f"[CON-DEBUG] Оформлен файл: {f_name} | Теги: {data.get('tags', [])}")

        # ЗЕРКАЛЬНОЕ ДУБЛИРОВАНИЕ В АРТЕФАКТЫ (СОХРАНЕНО)
        debug_dir = os.path.join(root_dir, '_content_files')
        os.makedirs(debug_dir, exist_ok=True)
        
        debug_file_path = os.path.join(debug_dir, f"processed-{f_name}")
        with open(debug_file_path, 'w', encoding='utf-8') as df:
            df.write(f"---\n{front_text}---\n[Тело статьи успешно обработано контентом]")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[CON-ERROR] Не удалось перезаписать файл {file_path}: {e}")

def process_all_markdown_files():
    """Главная функция-оформитель: сканирует диск и штампует теги по канонам репозитория."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github', '_content_files'}
    log_buffer = []

    # Очистка старой папки артефактов перед новой сборкой
    debug_dir = os.path.join(root_dir, '_content_files')
    if os.path.exists(debug_dir):
        for f in os.listdir(debug_dir):
            try: os.remove(os.path.join(debug_dir, f))
            except: pass
    os.makedirs(debug_dir, exist_ok=True)

    # Тотальное сканирование репозитория контента
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS and not d.startswith('.')]
        for file in files:
            if not file.endswith('.md') or file == 'index.md': continue
                
            full_path = os.path.join(root, file)
            data, front_text, body = parse_yaml_front_matter(full_path)
            if data is None: continue

            # Сбор автоматических тегов на основе свойств карточки
            calculated_tags = []
            if data.get('direction'): calculated_tags.append(clean_tag(data['direction']))
            if data.get('entity'): calculated_tags.append(clean_tag(data['entity']))
            if data.get('level'): calculated_tags.append(f"{str(data['level']).strip()}класс")
            if data.get('title'): calculated_tags.append(translit_title(data['title']))
            if data.get('keywords'):
                if isinstance(data['keywords'], list):
                    for kw in data['keywords']: calculated_tags.append(clean_tag(kw))
                else: calculated_tags.append(clean_tag(data['keywords']))

            # Фильтрация дубликатов тегов
            final_tags = []
            for t in calculated_tags:
                if t and t not in final_tags: final_tags.append(t)

            data['tags'] = final_tags
            if 'keywords' in data: del data['keywords']

            # Перезапись файла с обновлёнными тегами
            write_yaml_front_matter(full_path, data, body, log_buffer, root_dir)

    log_buffer.append("[CON-SUCCESS] Модульный серверный конвейер оформления контента успешно выполнен.")
    
    for line in log_buffer:
        print(line)

    # Выгрузка общего отладочного лога в ZIP-архив
    try:
        log_file_path = os.path.join(debug_dir, 'content_debug.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
    except Exception as e:
        print(f"[CON-ERROR] Не удалось сохранить файл лога контента: {e}")

if __name__ == '__main__':
    process_all_markdown_files()
