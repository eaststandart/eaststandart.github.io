#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module sitemap.py
@about Главный диспетчер и общий купол конвейера
@purpose Координирует последовательный обмен сквозной картой памяти между подмодулями этапов и выгружает итоговый sitemap.yml.
@author TechLab
@version 1.0.0
"""

import os
import yaml

def write_yaml_front_matter(file_path, data, body_content):
    """Записывает обновленные свойства обратно в md-файл на диске."""
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[SITEMAP-ERROR] Не удалось перезаписать файл {file_path}: {e}")

# =====================================================================
# УПРАВЛЯЮЩАЯ ТОЧКА ВХОДА СБОРЩИКА
# =====================================================================
# Импортируем первый этап обхода структуры без точек
import smLinks

def build_sitemap_tree():
    """Главный диспетчер пакета sitemap. Вызывается из preprocess.py."""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    debug_dir = os.path.join(root_dir, '_sitemap_files')
    os.makedirs(debug_dir, exist_ok=True)

    # Исключения корневых папок проекта
    EXCLUDED_FOLDERS = {
        '_includes', '_layouts', '_pages', 'assets', 'bin', 
        '.git', '.github', '_data', '_sitemap_files'
    }

    print("[SITEMAP] Запуск Конвейера в оперативной памяти. Шаг 1: Навигация (smLinks)...")
    
    # 1. Получаем расширенную сквозную карту из оперативной памяти нового модуля smLinks
    sitemap_flat_map, root_dirs_present = smLinks.run_navigation_stage(root_dir, EXCLUDED_FOLDERS)

    print("[SITEMAP] Подключение конвейера. Шаг 2: Обогащение свойств карты (smPropsIn)...")
    import smPropsIn
    sitemap_flat_map = smPropsIn.enrich_sitemap_properties(sitemap_flat_map)

    print("[SITEMAP] Подключение конвейера. Шаг 3: Расчет тегов, категорий и запись на диск (smPropsOut)...")
    import smPropsOut
    sitemap_flat_map = smPropsOut.process_files_metadata_and_save(sitemap_flat_map, root_dir, root_dirs_present)

    # 2. ТЕСТИРОВАНИЕ: Пересобираем сквозную карту в чистый словарь для выгрузки в sitemap.yml
    final_output_map = {}
    final_output_map['detected_root_folders'] = sorted(list(root_dirs_present))
    
    for key_file, item in sitemap_flat_map.items():
        # Прямое извлечение ноды каркаса из плоского паспорта памяти
        final_output_map[key_file] = [item['node']]

    # 3. Выгружаем результат в sitemap.yml
    output_file = os.path.join(data_dir, 'sitemap.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(final_output_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[SITEMAP-SUCCESS] Тестовая карта каркаса успешно сохранена на диск: _data/sitemap.yml")
    except Exception as e:
        print(f"[SITEMAP-ERROR] Ошибка записи карты sitemap.yml: {e}")

    print(f"[SITEMAP-SUCCESS] Всего обнаружено и проиндексировано объектов структуры: {len(sitemap_flat_map)}")

    # Возвращаем сквозную карту дальше по конвейеру
    return sitemap_flat_map

if __name__ == '__main__':
    build_sitemap_tree()
