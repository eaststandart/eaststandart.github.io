#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation_tree
@about Модуль автоматической сборки карты сайта и дерева навигации в _data/navigation.yml.
@purpose Обходит контентные разделы и папку _posts, парсит Front Matter, учитывает кастомные 
         пермалинки и генерирует актуальную карту ссылок для Liquid-шаблонов Jekyll.
@author TechLab
@version 1.0
"""

import os
import re

def build_navigation_tree():
    """Сканирует репозиторий и собирает карту навигации сайта."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    
    # Создаем папку _data, если её вдруг нет
    os.makedirs(data_dir, exist_ok=True)
    
    # Список папок для мониторинга
    target_folders = ['faire', 'projects', 'inspiration', 'tools', 'biblio', 'diary', '_posts']
    
    # Структура будущего YAML файла
    nav_tree = {folder: [] for folder in target_folders}
    
    print("\n[NAV-TREE] Начинаю сборку дерева навигации сайта...")
    
    for folder in target_folders:
        folder_path = os.path.join(root_dir, folder)
        if not os.path.exists(folder_path):
            continue
            
        for root, _, files in os.walk(folder_path):
            for file in files:
                if not file.endswith('.md'):
                    continue
                    
                full_path = os.path.join(root, file)
                
                # Читаем только Front Matter файла (первые 200 строк максимум для скорости)
                title = ""
                permalink = ""
                in_front_matter = False
                lines_read = 0
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            lines_read += 1
                            if lines_read > 200:
                                break
                                
                            line_strip = line.strip()
                            if line_strip == '---':
                                in_front_matter = not in_front_matter
                                if not in_front_matter and lines_read > 1:
                                    break # Вышли из Front Matter
                                continue
                                
                            if in_front_matter:
                                if line_strip.lower().startswith('title:'):
                                    title = re.sub(r'^title:\s*', '', line, flags=re.IGNORECASE).strip('\'" \n')
                                elif line_strip.lower().startswith('permalink:'):
                                    permalink = re.sub(r'^permalink:\s*', '', line, flags=re.IGNORECASE).strip('\'" \n')
                except Exception as e:
                    print(f"[NAV-TREE-WARN] Не удалось прочитать {file}: {e}")
                    continue
                
                # Если заголовка нет, берем красивое имя файла в качестве заглушки
                if not title:
                    title = os.path.splitext(file)[0].replace('-', ' ').capitalize()
                    
                # Вычисляем URL страницы
                if permalink:
                    # Приоритет №1: Кастомный пермалинк автора
                    final_url = permalink
                    if not final_url.startswith('/'):
                        final_url = '/' + final_url
                else:
                    # Приоритет №2: Нативный URL Jekyll
                    file_clean = os.path.splitext(file)[0]
                    
                    # Очистка даты для файлов из папки _posts (ГГГГ-ММ-ДД-имя -> имя)
                    if folder == '_posts':
                        file_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_clean)
                        final_url = f"/{file_clean}.html"
                    else:
                        final_url = f"/{folder}/{file_clean}.html"
                        
                # Добавляем элемент в массив ветки
                nav_tree[folder].append({
                    'title': title,
                    'url': final_url
                })
                
    # Сортируем списки статей по алфавиту для красоты в меню
    for folder in nav_tree:
        nav_tree[folder] = sorted(nav_tree[folder], key=lambda x: x['title'].lower())
        
    # Записываем дерево в файл _data/navigation.yml нативным методом (без сторонних библиотек yaml)
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        with open(output_file, 'w', encoding='utf-8') as yml:
            yml.write("# Автоматически сгенерированная карта навигации сайта. НЕ ПРАВИТЬ РУКАМИ!\n")
            for folder, items in nav_tree.items():
                # Убираем нижнее подчеркивание из имени ветки _posts для красоты Liquid селектора
                clean_folder_name = folder.replace('_', '')
                yml.write(f"{clean_folder_name}:\n")
                
                if not items:
                    yml.write("  []\n")
                    continue
                    
                for item in items:
                    # Экранируем кавычки в заголовках, чтобы YAML не ругался
                    safe_title = item['title'].replace('"', '\\"')
                    yml.write(f"  - title: \"{safe_title}\"\n")
                    yml.write(f"    url: \"{item['url']}\"\n")
                    
        print(f"[NAV-TREE-SUCCESS] Дерево навигации успешно собрано в: _data/navigation.yml (Найдено статей: {sum(len(v) for v in nav_tree.values())})")
    except Exception as e:
        print(f"[NAV-TREE-ERROR] Не удалось записать файл карты сайта: {e}")

if __name__ == '__main__':
    build_navigation_tree()