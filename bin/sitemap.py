#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module sitemap
@about Точка входа пакета sitemap. Координирует обмен данными конвейера в оперативной памяти.
"""

import os
import yaml

# Импортируем первый этап обхода структуры
from .sitemap_navigation import run_navigation_stage

def build_sitemap_tree():
    """Главный диспетчер пакета sitemap. Вызывается из preprocess.py."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Если sitemap.py лежит в подпапке sitemap/, поднимаемся на два уровня: к корню репозитория
    root_dir = os.path.abspath(os.path.join(current_dir, '..', '..')) if os.path.basename(current_dir) == 'sitemap' else os.path.abspath(os.path.join(current_dir, '..'))
    
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    debug_dir = os.path.join(root_dir, '_sitemap_files')
    os.makedirs(debug_dir, exist_ok=True)

    # Исключения корневых папок проекта
    EXCLUDED_FOLDERS = {
        '_includes', '_layouts', '_pages', 'assets', 'bin', 
        '.git', '.github', '_data', '_navigation_files', '_sitemap_files'
    }

    print("[SITEMAP] Запуск Конвейера в оперативной памяти. Шаг 1: Навигация...")
    
    # 1. Получаем расширенную сквозную карту из оперативной памяти без дисковых перезаписей
    sitemap_flat_map, root_dirs_present = run_navigation_stage(root_dir, EXCLUDED_FOLDERS)

    # 2. ТЕСТИРОВАНИЕ: Пересобираем сквозную карту в чистый словарь для выгрузки в sitemap.yml
    final_output_map = {}
    final_output_map['detected_root_folders'] = sorted(list(root_dirs_present))
    
    for key_file, items in sitemap_flat_map.items():
        # Извлекаем из паспорта только ноду структуры, отсекая технические данные текста и путей
        final_output_map[key_file] = [item['node'] for item in items]

    # 3. Выгружаем результат в sitemap.yml
    output_file = os.path.join(data_dir, 'sitemap.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(final_output_map, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"[SITEMAP-SUCCESS] Тестовая карта успешно сохранена на диск: _data/sitemap.yml")
    except Exception as e:
        print(f"[SITEMAP-ERROR] Ошибка записи тестовой карты sitemap.yml: {e}")

    # Возвращаем сквозную карту дальше по конвейеру для будущего Этажа 2 (модуля Feed)
    return sitemap_flat_map

if __name__ == '__main__':
    build_sitemap_tree()
