#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module smPropsIn.py
@about Обогащение карты и расчет инвариантных дат
@purpose Затягивает из Front Matter свойства Obsidian в карту сайта и вычисляет недостающие даты через каскад Git/mtime в оперативной памяти.
@author TechLab
@version 2.0.0
"""

import os
import re
import datetime
import subprocess

import os

def write_local_log(text):
    """Локально дописывает строку в изолированный лог второго модуля smPropsIn."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(current_dir, '..', '_sitemap_files')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'smPropsIn-md-properties.log')
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(text + "\n")
    except Exception as e:
        print(f"[SITEMAP-ERROR] Не удалось записать лог smPropsIn: {e}")

def enrich_sitemap_properties(sitemap_flat_map):
    """Принимает сквозную карту памяти конвейера, затягивает свойства Obsidian и рассчитывает даты."""
    if not sitemap_flat_map:
        return sitemap_flat_map

    # Список кастомных текстовых свойств Obsidian, которые строго должны попасть в sitemap.yml
    SITEMAP_PROPERTIES = ['crumbtitle', 'emoji', 'posttype', 'pinnedfeed']

    for file_key, passport in sitemap_flat_map.items():
        # Технический ключ списка папок игнорируем
        if file_key == 'detected_root_folders': 
            continue

        node = passport.get('node', {})
        front_data = passport.get('front_matter', {})
        file_path = passport.get('file_path', '')

        if not node or not front_data:
            continue

        # 1. Сквозной нативный перенос свойств Obsidian внутрь ноды памяти карты сайта
        for prop in SITEMAP_PROPERTIES:
            if front_data.get(prop):
                val_clean = str(front_data[prop]).strip()
                if val_clean:
                    node[prop] = front_data[prop]

        # 2. ОРИГИНАЛЬНЫЙ КАСКАД ВЫЧИСЛЕНИЯ ДАТЫ В ОПЕРАТИВНОЙ ПАМЯТИ (БЛОК А)
        # Инициализируем флаг-сигнал для Этапа 3
        passport['stamp_date_to_disk'] = False

        # А. Если дата изначально задана автором в Obsidian Front Matter
        if front_data.get('date'):
            node['date'] = str(front_data['date']).strip()

        # Б. Если даты в файле нет — включаем каскад оригинальных вычислений контура
        else:
            calculated_date = ""
            
            # Приоритет 1: Для постов хроники вырезаем дату из имени файла
            file_name = os.path.basename(file_path) if file_path else ""
            match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name)
            
            if match_date:
                calculated_date = match_date.group(1)
            
            # Приоритет 2: Для обычных файлов вызываем системную команду Git log
            else:
                if file_path and os.path.exists(file_path):
                    try:
                        cmd = ['git', 'log', '--diff-filter=A', '--format=%as', '--', file_path]
                        git_date = subprocess.check_output(cmd, text=True).strip().split('\n')[-1]
                        if git_date and re.match(r'^\d{4}-\d{2}-\d{2}$', git_date):
                            calculated_date = git_date
                        else:
                            # Приоритет 3: Если Гит молчит — берём системное mtime диска
                            mtime = os.path.getmtime(file_path)
                            calculated_date = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                    except Exception:
                        # Защитный fallback на mtime диска при сбое команды Git
                        mtime = os.path.getmtime(file_path)
                        calculated_date = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

            # Если дата успешно вычислена, фиксируем её в памяти конвейера
            if calculated_date:
                node['date'] = calculated_date
                front_data['date'] = calculated_date  # Обновляем словарь Front Matter в памяти для Этапа 3
                
                # Включаем зеленый свет для физической записи на диск на Этапе 3
                passport['stamp_date_to_disk'] = True

    return sitemap_flat_map
