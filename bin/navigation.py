#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 3)
@about Универсальный плоский препроцессор однотипной карты метаданных контента.
@purpose Этаж 1, 2 и подготовка Диспетчера к каскадному Шагу 1.
@author TechLab
@version 19.0.0-split-cascade
"""

import os
import re
import sys
import yaml
import subprocess

# =====================================================================
# ЭТАЖ 1: СИСТЕМНЫЕ УТИЛИТЫ (Парсер Front Matter и перезапись на диск)
# =====================================================================
def parse_yaml_front_matter(file_path):
    """Извлекает блок Front Matter из markdown-файла контента сайта."""
    content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось прочитать файл {file_path}: {e}")
        return None, None, content

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match: return None, None, content

    front_matter_text = match.group(1)
    body_content = content[match.end():]

    try:
        data = yaml.safe_load(front_matter_text)
        return data if data else {}, front_matter_text, body_content
    except Exception as e:
        print(f"[NAV-ERROR] Сбой синтаксиса YAML во Front Matter в {file_path}: {e}")
        return None, None, content

artifacts_log_buffer = []

def log_artifact(text):
    """Выводит строку лога в консоль Actions и буферизирует её для архива артефактов."""
    print(text)
    artifacts_log_buffer.append(text)

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства обратно в md-файл на диске."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось перезаписать файл {file_path}: {e}")

# =====================================================================
# ЭТАЖ 2: ПОДКЛЮЧАЕМЫЙ МОДУЛЬ FEED
# =====================================================================
def navigation_feed_properties(data, passport, file_path=None):
    """Модуль ленты feed на Этаже 2. Рассчитывает, записывает свойства на диск 
    и выводит факты изменений в лог контура контроля."""
    import datetime
    
    date_was_written = False
    
    # Вспомогательные функции очистки текстовых свойств по вашему эталону
    def clean_tag_local(text):
        if not text: return ""
        return re.sub(r'\s+', '', str(text).lower().strip())
        
    def translit_title_local(text):
        if not text: return ""
        return re.sub(r'[^a-z0-9а-яё]', '', str(text).lower().strip())

    # А. БЛОК ОБРАБОТКИ ДАТЫ
    date_was_written = False
    if not data.get('date'):
        file_name = os.path.basename(file_path) if file_path else ""
        match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name)
        if match_date:
            data['date'] = match_date.group(1)
            date_was_written = True
        else:
            if file_path and os.path.exists(file_path):
                try:
                    cmd = ['git', 'log', '--diff-filter=A', '--format=%as', '--', file_path]
                    git_date = subprocess.check_output(cmd, text=True).strip().split('\n')[-1]
                    if git_date and re.match(r'^\d{4}-\d{2}-\d{2}$', git_date):
                        data['date'] = git_date
                    else:
                        mtime = os.path.getmtime(file_path)
                        data['date'] = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                except Exception:
                    mtime = os.path.getmtime(file_path)
                    data['date'] = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                date_was_written = True

    # Безопасно распаковываем паспорт: если это массив, берем его внутренний словарь
    target_dict = passport[0] if isinstance(passport, list) and len(passport) > 0 else passport

    if isinstance(target_dict, dict):
        # Записываем дату в карту навигации
        target_dict['date'] = str(data.get('date', ''))
        
        # Записываем эмодзи и свойства в карту навигации
        for prop in ['direction', 'entity', 'level', 'emoji']:
            if data.get(prop):
                target_dict[prop] = data[prop]

    # Б. АВТОМАТИЧЕСКАЯ СБОРКА И ЗАПИСИ ТЕГОВ НА ДИСК
    tags_were_written = False
    calculated_tags = []
    if data.get('direction'): calculated_tags.append(clean_tag_local(data['direction']))
    if data.get('entity'): calculated_tags.append(clean_tag_local(data['entity']))
    if data.get('level'): calculated_tags.append(f"{str(data['level']).strip()}класс")
    if data.get('title'): calculated_tags.append(translit_title_local(data['title']))
    
    if data.get('keywords'):
        if isinstance(data['keywords'], list):
            for kw in data['keywords']: calculated_tags.append(clean_tag_local(kw))
        else:
            calculated_tags.append(clean_tag_local(data['keywords']))

    final_tags = []
    for t in calculated_tags:
        if t and t not in final_tags: final_tags.append(t)

    if final_tags and data.get('tags') != final_tags:
        data['tags'] = final_tags
        if 'keywords' in data: 
            del data['keywords']
        tags_were_written = True

    # В. ЕДИНАЯ ФИЗИЧЕСКАЯ ПЕРЕЗАПИСЬ ФАЙЛА С ФИКСАЦИЕЙ ЧИСТОГО ЛОГА
    if (date_was_written or tags_were_written) and file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            body_content = content[match.end():] if match else content
            
            write_yaml_front_matter(file_path, data, body_content)
            
            root_dir_local = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
            f_rel = os.path.relpath(file_path, root_dir_local).replace(os.sep, '/')
            
            # Печатаем логи изменений строго по факту первой физической записи на диск
            if date_was_written:
                log_artifact(f"[NAV-DEBUG] Файл: {f_rel} | Записано date: {data['date']}")
            if tags_were_written:
                log_artifact(f"[NAV-DEBUG] Файл: {f_rel} | Записано tags: {data['tags']}")
        except Exception as e:
            print(f"[NAV-ERROR] Не удалось перезаписать свойства контента в {file_path}: {e}")

    # Г. БЛОК ОБРАБОТКИ PINNEDFEED (Если во Front Matter заметки обнаружен флаг pinnedfeed, записываем его в карту.)
    if data and data.get('pinnedfeed') is True:
        passport['pinnedfeed'] = True
            
    return passport

# =====================================================================
# ЭТАЖ 3: ГЛАВНЫЙ УПРАВЛЯЮЩИЙ КОНВЕЙЕР (Диспетчер обхода)
# =====================================================================
def build_navigation_tree():
    global artifacts_log_buffer
    artifacts_log_buffer.clear()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    debug_dir = os.path.join(root_dir, '_navigation_files')
    os.makedirs(debug_dir, exist_ok=True)

    # Список жестких технических исключений корневых папок диска
    EXCLUDED_FOLDERS = {'_includes', '_layouts', '_pages', 'assets', 'bin', '.git', '.github', '_data', '_navigation_files'}
    
    flat_map = {}
    root_dirs_present = set()
    folders_with_index = set()
    
    # Собираем имена всех физических папок в корне диска строго с фильтром исключений
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and not name.startswith('.') and name not in EXCLUDED_FOLDERS:
            root_dirs_present.add(name)

    # 🔥 ШАГ 1: ОБРАБОТКА КОРНЕВЫХ ПАПОК (БЕЗ ФАЙЛОВ И ИНДЕКСОВ) СТРОГО ПО ВАШЕЙ КАСКАДНОЙ ТАБЛИЦЕ
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            clean_section_name = name.lstrip('_')
            is_under_dir = name.startswith('_')
            
            # Локальные буферы каскада
            front_data = None
            index_file_path = ""
            
            # --- ПРИОРИТЕТ 1: Поиск физического индекса прямо внутри папки ---
            possible_index_md = os.path.join(full_path, 'index.md')
            possible_index_html = os.path.join(full_path, 'index.html')
            
            if os.path.exists(possible_index_md):
                index_file_path = possible_index_md
            elif os.path.exists(possible_index_html):
                index_file_path = possible_index_html
                
            if index_file_path:
                front_data, _, _ = parse_yaml_front_matter(index_file_path)
                folders_with_index.add(name)
                
            # --- ПРИОРИТЕТ 2: Поиск совпадения в папке _pages/ ---
            if not front_data:
                possible_page = os.path.join(root_dir, '_pages', f"{clean_section_name}.md")
                if os.path.exists(possible_page):
                    front_data, _, _ = parse_yaml_front_matter(possible_page)

            # Собираем паспорт раздела
            node = {}
            
            # Вычисление title, crumbtitle, emoji в папках разделов (Приоритет 1 и 2)
            if front_data:
                node['title'] = front_data.get('title', clean_section_name.capitalize())
                if 'crumbtitle' in front_data:
                    node['crumbtitle'] = front_data['crumbtitle']
                if front_data.get('emoji'):
                    node['emoji'] = front_data['emoji']
                
                # Вычисление URL по пермалинку
                if front_data.get('permalink'):
                    node['url'] = front_data['permalink'].strip()
                else:
                    # --- ПРИОРИТЕТ 3 (Сброс URL на автомат папки, если пермалинка в шапке не было) ---
                    node['url'] = f"/{clean_section_name}/"
            
            # --- ПРИОРИТЕТ 3: Полный автомат, если файлов на диске вообще не найдено ---
            else:
                node['title'] = clean_section_name.capitalize()
                node['url'] = f"/{clean_section_name}/"

            # Назначение прямых свойств связи в зависимости от наличия подчёркивания папки на диске
            if is_under_dir:
                node['collection'] = clean_section_name
            else:
                node['section'] = clean_section_name
                
            flat_map[clean_section_name] = [node]

            flat_map[clean_section_name] = [node]

    # ФИНАЛЬНАЯ ПРОВЕРКА: Добор автономных файлов из папки _pages/
    pages_dir = os.path.join(root_dir, '_pages')
    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md') and file != 'index.md':
                slug, _ = os.path.splitext(file)
                
                # Если файлу из _pages не сопоставлено ни одно корневое имя папки в flat_map
                if slug not in flat_map:
                    p_data, _, _ = parse_yaml_front_matter(os.path.join(pages_dir, file))
                    if p_data:
                        node = {
                            'title': p_data.get('title', slug.capitalize()),
                            'url': p_data.get('permalink', f"/{slug}/").strip()
                        }
                        if p_data.get('crumbtitle'):
                            node['crumbtitle'] = p_data['crumbtitle']
                        # Нативно забираем эмодзи для автономного раздела (Журнал, Медиа)
                        if p_data.get('emoji'):
                            node['emoji'] = p_data['emoji']
                            
                        # Прописываем системное свойство раздела Jekyll
                        node['section'] = slug
                        
                        flat_map[slug] = [node]

    # 🔥 ШАГ 2: ОБХОД ФИЗИЧЕСКИХ ФАЙЛОВ СТАТЕЙ И ПРОЕКТОВ (ИНДЕКСЫ ПОЛНОСТЬЮ ИГНОРИРУЮТСЯ) - 1 В 1 ВАШ ФАЙЛ
    for name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path) and name not in EXCLUDED_FOLDERS and not name.startswith('.') and name != '_posts':
            
            for root_walk, _, files in os.walk(full_path):
                for file in files:
                    if not (file.endswith('.md') or file.endswith('.html')): continue
                    
                    file_slug, _ = os.path.splitext(file)
                    if file_slug == 'index': continue
                    
                    file_path = os.path.join(root_walk, file)
                    data, front_text, body = parse_yaml_front_matter(file_path)
                    if data is None or data.get('published') is False: continue

                    ready_permalink = data.get('permalink', '').strip()
                    relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')

                    node = {}
                    node['title'] = data.get('title', file_slug)

                    # 1. Если у файла ЕСТЬ permalink
                    if ready_permalink:
                        node['url'] = ready_permalink
                        permalink_clean = ready_permalink.strip('/')
                        first_word = permalink_clean.split('/')[0] if permalink_clean else ''
                        
                        has_clean_dir = first_word in root_dirs_present
                        has_under_dir = f"_{first_word}" in root_dirs_present
                        
                        if has_clean_dir and has_under_dir:
                            pass
                        elif has_under_dir:
                            node['relatedcollection'] = first_word
                        elif has_clean_dir:
                            node['relatedsection'] = first_word

                    # 2. Если у файла НЕТ permalink
                    else:
                        clean_section_name = name.lstrip('_')
                        is_under_dir = name.startswith('_')
                        
                        node['url'] = f"/{clean_section_name}/{file_slug}/"

                        if name not in folders_with_index and not name.startswith('_'):                        
                            data['permalink'] = node['url']
                            log_artifact(f"[NAV-DEBUG] Файл: {relative_file_key} | Записано permalink: {data['permalink']}")

                        if is_under_dir:
                            node['relatedcollection'] = clean_section_name
                        else:
                            node['relatedsection'] = clean_section_name

                    data['section'] = name.lstrip('_')
                    write_yaml_front_matter(file_path, data, body)

                    node = navigation_feed_properties(data, node, file_path)

                    flat_map[relative_file_key] = [node]

    # 🔥 ШАГ 3: ОБРАБОТКА ПАПКИ СВЯЗАННЫХ ПОСТОВ ХРОНИКИ _POSTS/ (СТРОГО 1 В 1 ВАШ ФАЙЛ)
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not (file.endswith('.md') or file.endswith('.html')): continue
                
                file_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(file_path)
                if data is None or data.get('published') is False: continue

                file_name_clean, _ = os.path.splitext(file)
                file_slug_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)
                ready_permalink = data.get('permalink', '').strip()
                relative_file_key = os.path.relpath(file_path, root_dir).replace(os.sep, '/')

                match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                post_date = match_date.group(1) if match_date else "2026-01-01"

                # Нативно извлекаем наше новое универсальное свойство posttype из Front Matter заметки
                raw_post_type = str(data.get('posttype', '')).strip().lower() if data.get('posttype') else ""
                
                # ОБЩЕЕ УНИВЕРСАЛЬНОЕ ПРАВИЛО: Выделяем базовый тип контента (отсекаем приставку -close)
                base_type_clean = raw_post_type.split('-')[0] if '-' in raw_post_type else raw_post_type

                # Вычисляем полный физический путь к родителю (СТАРАЯ ЛОГИКА 1 в 1)
                calculated_parent_path = ""
                parent_file_name = f"{file_slug_no_date}.md"
                for key_path in flat_map.keys():
                    if key_path.endswith(f"/{parent_file_name}") or key_path == parent_file_name:
                        calculated_parent_path = key_path
                        break

                node = {}
                node['title'] = data.get('title', file_slug_no_date)
                
                # Записываем точное свойство posttype в карту навигации, только если оно физически есть в Obsidian
                if raw_post_type:
                    node['posttype'] = raw_post_type

                # А. Пост хроники С пермалинком (Адрес полностью в приоритете автора — СТАРАЯ ЛОГИКА)
                if ready_permalink:
                    node['url'] = ready_permalink
                    permalink_clean = ready_permalink.strip('/')
                    first_word = permalink_clean.split('/')[0] if permalink_clean else ''
                    
                    has_clean_dir = first_word in root_dirs_present
                    has_under_dir = f"_{first_word}" in root_dirs_present
                    
                    if calculated_parent_path:
                        node['relatedpages'] = calculated_parent_path
                    
                    if has_clean_dir and has_under_dir:
                        pass
                    elif has_under_dir:
                        node['relatedcollection'] = first_word
                    elif has_clean_dir:
                        node['relatedsection'] = first_word

                # Б. Пост хроники БЕЗ пермалинка (Динамическая сборка URL на основе вычисленного базового типа)
                else:
                    # Если свойства posttype в Obsidian нет — префиксом нативно становится универсальное слово "post"
                    url_prefix = base_type_clean if base_type_clean else "post"
                    node['url'] = f"/{url_prefix}/{file_slug_no_date}/{post_date.replace('-', '/')}/{file_slug_no_date}.html"
                    if calculated_parent_path:
                        node['relatedpages'] = calculated_parent_path

                # В. ЕДИНАЯ СКВОЗНАЯ ШТАМПОВКА КАТЕГОРИЙ [ТИП, ИМЯ] С ЖЕСТКОЙ СТАРОЙ ЗАЩИТОЙ ОТ ПЕРЕЗАПИСИ
                if not data.get('categories'):
                    # Извлекаем слаг родительского проекта по его готовому URL из flat_map (СТАРАЯ ЛОГИКА 1 в 1)
                    calculated_slug = ""
                    if calculated_parent_path and calculated_parent_path in flat_map:
                        parent_card = flat_map[calculated_parent_path]
                        if isinstance(parent_card, list) and len(parent_card) > 0:
                            parent_card = parent_card[0]
                        parent_url = parent_card.get('url', '').strip('/')
                        if parent_url:
                            calculated_slug = parent_url.split('/')[-1]

                    # Если есть родитель — берем его слаг, если пост автономный — слаг самого файла постов
                    final_topic_slug = calculated_slug if calculated_slug else file_slug_no_date
                    final_type_prefix = base_type_clean if base_type_clean else "post"

                    if final_type_prefix and final_topic_slug:
                        data['categories'] = [final_type_prefix, final_topic_slug]
                        log_artifact(f"[NAV-DEBUG] Файл: {relative_file_key} | Записано универсальные categories: {data['categories']}")

                # Сохраняем имя свойства для обратной совместимости со старым Jekyll-рендером
                if base_type_clean in ['journal', 'media']:
                    data['post-page'] = base_type_clean

                write_yaml_front_matter(file_path, data, body)

                # 🔥 ПОДКЛЮЧЕНИЕ МОДУЛЯ НОВОСТЕЙ: Расширение паспорта строго в оперативной памяти сервера
                node = navigation_feed_properties(data, node, file_path)

                flat_map[relative_file_key] = [node]

    # СОБИРАЕМ ИТОГОВЫЙ СЛОВАРЬ С СЕРВЕРНЫМ СПИСКОМ ПАПОК НА ПЕРВОЙ СТРОКЕ
    final_output_map = {}
    final_output_map['detected_root_folders'] = sorted(list(root_dirs_present))
    for k, v in flat_map.items():
        final_output_map[k] = v

    # Запись плоской карты на диск без значков *id
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(final_output_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации: {e}")

    try:
        log_file_path = os.path.join(debug_dir, 'navigation-md-properties.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
        print("[NAV-SUCCESS] Лог изменений свойств успешно сохранен.")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось сохранить лог: {e}")

if __name__ == '__main__':
    build_navigation_tree()
