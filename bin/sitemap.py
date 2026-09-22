#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module sitemap
@about Главный диспетчер пакета sitemap со встроенными утилитами парсинга.
"""

import os
import re
import yaml

# =====================================================================
# СИСТЕМНЫЕ УТИЛИТЫ ОБРАБОТКИ ФАЙЛОВ (Встроенный Этаж 1)
# =====================================================================
def parse_yaml_front_matter(file_path):
    """Извлекает блок Front Matter из markdown-файла контента сайта."""
    content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[SITEMAP-ERROR] Не удалось прочитать файл {file_path}: {e}")
        return None, None, content

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match: return None, None, content

    front_matter_text = match.group(1)
    body_content = content[match.end():]

    try:
        data = yaml.safe_load(front_matter_text)
        return data if data else {}, front_matter_text, body_content
    except Exception as e:
        print(f"[SITEMAP-ERROR] Сбой синтаксиса YAML во Front Matter в {file_path}: {e}")
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
        print(f"[SITEMAP-ERROR] Не удалось перезаписать файл {file_path}: {e}")


# =====================================================================
# УПРАВЛЯЮЩАЯ ТОЧКА ВХОДА СБОРЩИКА (Бывший Этаж 3)
# =====================================================================
# Импортируем первый этап обхода структуры прямо из папки bin/ БЕЗ точек
import sitemap_navigation

def build_sitemap_tree():
    """Главный диспетчер пакета sitemap. Вызывается из preprocess.py."""
    global artifacts_log_buffer
    artifacts_log_buffer.clear()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
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
    
    # 1. Получаем расширенную сквозную карту из оперативной памяти
    sitemap_flat_map, root_dirs_present = sitemap_navigation.run_navigation_stage(root_dir, EXCLUDED_FOLDERS)

    # 2. ТЕСТИРОВАНИЕ: Пересобираем сквозную карту в чистый словарь для выгрузки в sitemap.yml
    final_output_map = {}
    final_output_map['detected_root_folders'] = sorted(list(root_dirs_present))
    
    for key_file, items in sitemap_flat_map.items():
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

    # Запись пустого базового лога для прохождения шага в GitHub Actions
    try:
        log_file_path = os.path.join(debug_dir, 'sitemap-md-properties.log')
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("[SITEMAP] Инициализация пустого лога этапа навигации.")
    except Exception:
        pass

    # Возвращаем сквозную карту дальше по конвейеру
    return sitemap_flat_map

if __name__ == '__main__':
    build_sitemap_tree()
