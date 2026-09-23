#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module smPropsOut.py
@about Расчет тегов, категорий контура и сохранение файлов
@purpose Принимает из оперативной памяти обогащенную карту, вычисляет динамические метаданные и за один присест физически обновляет файлы на диске.
@author TechLab
@version 1.1.0
"""

import os
import re
from sitemap import write_yaml_front_matter

def write_local_log(text):
    """Локально дописывает строку в изолированный лог третьего модуля smPropsOut."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(current_dir, '..', '_sitemap_files')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'smPropsOut-md-properties.log')
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(text + "\n")
    except Exception as e:
        print(f"[SITEMAP-ERROR] Не удалось записать лог smPropsOut: {e}")

def process_files_metadata_and_save(sitemap_flat_map, root_dir, root_dirs_present):
    """Рассчитывает динамические свойства в памяти и за один проход сохраняет md-файлы на диск."""
    if not sitemap_flat_map:
        return sitemap_flat_map

    # Вспомогательные функции очистки текстовых свойств по вашему эталону
    def clean_tag_local(text):
        if not text: return ""
        return re.sub(r'\s+', '', str(text).lower().strip())
        
    def translit_title_local(text):
        if not text: return ""
        return re.sub(r'[^a-z0-9а-яё]', '', str(text).lower().strip())

    for file_key, passport in sitemap_flat_map.items():
        if file_key == 'detected_root_folders': 
            continue

        node = passport.get('node', {})
        data = passport.get('front_matter', {})
        body = passport.get('body_content', '')
        file_path = passport.get('file_path', '')

        # ИГНОРИРУЕМ КОРНЕВЫЕ РАЗДЕЛЫ САЙТА (УСТРАНЯЕМ АНОМАЛИЮ 3)
        # Корневые папки разделов из Шага 1 не имеют физического md-файла внутри своей папки, 
        # либо в их паспорте нативно взведен признак section/collection без related-приставок.
        if not file_path or not os.path.exists(file_path):
            continue
        if 'section' in node or 'collection' in node:
            continue

        # Состояния-триггеры для жесткого контроля избыточных дисковых операций
        tags_were_written = False
        categories_were_written = False
        date_was_written = passport.get('stamp_date_to_disk', False)
        permalink_was_written = passport.get('stamp_permalink_to_disk', False)

        # 1. 🔥 АВТОМАТИЧЕСКАЯ СБОРКА И ОБЪЕДИНЕНИЕ ТЕГОВ В ОПЕРАТИВНОЙ ПАМЯТИ
        calculated_tags = []
        if data.get('direction'): calculated_tags.append(clean_tag_local(data['direction']))
        if data.get('entity'): calculated_tags.append(clean_tag_local(data['entity']))
        if data.get('level'): calculated_tags.append(f"{str(data['level']).strip()}класс")
        
        # НАДЁЖНОЕ ИЗВЛЕЧЕНИЕ ЗАГОЛОВКА ДЛЯ СТАТЕЙ И ПОСТОВ ХРОНИКИ (УСТРАНЯЕМ АНОМАЛИЮ 1 И 2)
        # Если во front-matter пусто, забираем вычисленный title из оперативной памяти ноды каркаса
        title_text = str(data.get('title', node.get('title', ''))).strip()
        if title_text:
            if ':' in title_text:
                parts = title_text.split(':', 1)
                tag_before = translit_title_local(parts[0])
                tag_after = translit_title_local(parts[1])
                if tag_before: calculated_tags.append(tag_before)
                if tag_after: calculated_tags.append(tag_after)
            else:
                calculated_tags.append(translit_title_local(title_text))
        
        if data.get('keywords'):
            if isinstance(data['keywords'], list):
                for kw in data['keywords']: calculated_tags.append(clean_tag_local(kw))
            else:
                calculated_tags.append(clean_tag_local(data['keywords']))

        # Умное слияние: бережно сохраняем и подклеиваем старые теги из файла контента
        old_tags = data.get('tags', [])
        if isinstance(old_tags, list):
            for ot in old_tags: calculated_tags.append(clean_tag_local(ot))
        elif old_tags:
            calculated_tags.append(clean_tag_local(old_tags))

        # Очищаем итоговый объединенный список от дубликатов и пустых элементов
        final_tags = []
        for t in calculated_tags:
            if t and t not in final_tags: final_tags.append(t)

        if final_tags and data.get('tags') != final_tags:
            data['tags'] = final_tags
            if 'keywords' in data: 
                del data['keywords']
            tags_were_written = True

        # 2. 🔥 АВТОМАТИЧЕСКАЯ СБОРКА КАТЕГОРИЙ ДЛЯ ХРОНИКИ В ОПЕРАТИВНОЙ ПАМЯТИ
        # Срабатывает строго для постов из папки _posts без рудимента post-page
        if '_posts/' in file_key and not data.get('categories'):
            calculated_parent_path = node.get('relatedpages', '')
            file_name_clean, _ = os.path.splitext(os.path.basename(file_path))
            file_slug_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)

            calculated_slug = ""
            if calculated_parent_path and calculated_parent_path in sitemap_flat_map:
                parent_passport = sitemap_flat_map[calculated_parent_path]
                parent_url = parent_passport.get('node', {}).get('url', '').strip('/')
                if parent_url:
                    calculated_slug = parent_url.split('/')[-1]

            final_topic_slug = calculated_slug if calculated_slug else file_slug_no_date
            
            raw_post_type = str(node.get('posttype', '')).strip().lower()
            base_type_clean = raw_post_type.split('-')[0] if '-' in raw_post_type else raw_post_type
            final_type_prefix = base_type_clean if base_type_clean else "post"

            if final_type_prefix and final_topic_slug:
                data['categories'] = [final_type_prefix, final_topic_slug]
                categories_were_written = True

        # 3. 🔥 ЕДИНЫЙ ЗАЩИЩЕННЫЙ ПРИСЕСТ НА ДИСК (СТРОГО 1 ВЫЗОВ ЗАПИСИ НА ФАЙЛ)
        if permalink_was_written:
            data['permalink'] = node['url']

        if date_was_written:
            # Дата уже подложена во front_matter на Этапе 2, подтверждаем ее прописку на диск
            pass

        # Если хотя бы один триггер истинен — осуществляем физическую запись за 1 проход
        # ПРИМЕЧАНИЕ: Для тестирования симуляции вы можете временно закомментировать строку с write_yaml_front_matter
        if date_was_written or tags_were_written or categories_were_written or permalink_was_written:
            write_yaml_front_matter(file_path, data, body)
            
            # Печатаем логи изменений
            if permalink_was_written:
                write_local_log(f"[SITEMAP-DEBUG] Файл: {file_key} | Записано permalink: {data['permalink']}")
            if date_was_written:
                write_local_log(f"[SITEMAP-DEBUG] Файл: {file_key} | Записано date: {data['date']}")
            if tags_were_written:
                write_local_log(f"[SITEMAP-DEBUG] Файл: {file_key} | Записано tags: {data['tags']}")
            if categories_were_written:
                write_local_log(f"[SITEMAP-DEBUG] Файл: {file_key} | Записано categories: {data['categories']}")

    return sitemap_flat_map
