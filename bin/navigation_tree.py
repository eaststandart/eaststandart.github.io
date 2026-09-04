#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation_tree
@about Глубокий монолитный парсер метаданных и сборщик дерева навигации сайта.
@purpose Извлекает title, permalink, date, categories и tags из Front Matter статей,
         учитывает хронологию _posts и собирает расширенную карту в _data/navigation.yml.
@author TechLab
@version 2.0-smart
"""

import os
import re

def parse_yaml_list(line_content):
    """Вспомогательная функция для парсинга инлайновых списков вида [item1, item2]"""
    clean = line_content.strip('[] \n\'"')
    if not clean:
        return []
    return [item.strip(' \'"') for item in clean.split(',') if item.strip()]

def build_navigation_tree():
    """Сканирует репозиторий и собирает расширенную карту метаданных сайта."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    
    os.makedirs(data_dir, exist_ok=True)
    
    target_folders = ['faire', 'projects', 'inspiration', 'tools', 'biblio', 'diary', '_posts']
    nav_tree = {folder: [] for folder in target_folders}
    
    print("\n[NAV-TREE] Запуск глубокого анализа метаданных из Front Matter...")
    
    for folder in target_folders:
        folder_path = os.path.join(root_dir, folder)
        if not os.path.exists(folder_path):
            continue
            
        for root, _, files in os.walk(folder_path):
            for file in files:
                if not file.endswith('.md'):
                    continue
                    
                full_path = os.path.join(root, file)
                
                # Инициализируем переменные метаданных для каждой статьи
                title = ""
                permalink = ""
                doc_date = ""
                categories = []
                tags = []
                
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
                                    break
                                continue
                                
                            if in_front_matter:
                                # Точечный сбор метаданных
                                if line_strip.lower().startswith('title:'):
                                    title = re.sub(r'^title:\s*', '', line, flags=re.IGNORECASE).strip('\'" \n')
                                elif line_strip.lower().startswith('permalink:'):
                                    permalink = re.sub(r'^permalink:\s*', '', line, flags=re.IGNORECASE).strip('\'" \n')
                                elif line_strip.lower().startswith('date:'):
                                    doc_date = re.sub(r'^date:\s*', '', line, flags=re.IGNORECASE).strip('\'" \n')
                                elif line_strip.lower().startswith('categories:'):
                                    cat_content = re.sub(r'^categories:\s*', '', line, flags=re.IGNORECASE)
                                    categories = parse_yaml_list(cat_content)
                                elif line_strip.lower().startswith('tags:'):
                                    tags_content = re.sub(r'^tags:\s*', '', line, flags=re.IGNORECASE)
                                    tags = parse_yaml_list(tags_content)
                except Exception as e:
                    print(f"[NAV-TREE-WARN] Пропуск файла {file}: {e}")
                    continue
                
                if not title:
                    title = os.path.splitext(file)[0].replace('-', ' ').capitalize()
                    
                # Хронологическая очистка даты из имени файла для папки _posts
                file_name_clean = os.path.splitext(file)[0]
                file_date_prefix = ""
                date_match = re.match(r'^(\d{4}-\d{2}-\d{2})-(.*)$', file_name_clean)
                if date_match:
                    file_date_prefix = date_match.group(1)
                    file_name_clean = date_match.group(2)
                
                # Если в самом файле даты не было, но она есть в имени (_posts), берём её
                if not doc_date and file_date_prefix:
                    doc_date = file_date_prefix
                
                # Интеллектуальное вычисление URL страницы
                if permalink:
                    final_url = permalink if permalink.startswith('/') else '/' + permalink
                else:
                    if folder == '_posts':
                        final_url = f"/{file_name_clean}.html"
                    else:
                        final_url = f"/{folder}/{file_name_clean}.html"
                        
                # Упаковываем все собранные метаданные в карточку статьи
                nav_tree[folder].append({
                    'title': title,
                    'url': final_url,
                    'date': doc_date if doc_date else "0000-00-00",
                    'categories': categories,
                    'tags': tags
                })
                
    # Правило сортировки: Обычные папки сортируем по Алфавиту, а _posts — строго по Дате (от новых к старым)
    for folder in nav_tree:
        if folder == '_posts':
            nav_tree[folder] = sorted(nav_tree[folder], key=lambda x: x['date'], reverse=True)
        else:
            nav_tree[folder] = sorted(nav_tree[folder], key=lambda x: x['title'].lower())
            
    # Запись структурированного расширенного YAML без внешних библиотек
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        with open(output_file, 'w', encoding='utf-8') as yml:
            yml.write("# Умная автоматическая карта метаданных сайта Jekyll. НЕ ПРАВИТЬ РУКАМИ!\n")
            for folder, items in nav_tree.items():
                clean_folder_name = folder.replace('_', '')
                yml.write(f"{clean_folder_name}:\n")
                
                if not items:
                    yml.write("  []\n")
                    continue
                    
                for item in items:
                    safe_title = item['title'].replace('"', '\\"')
                    yml.write(f"  - title: \"{safe_title}\"\n")
                    yml.write(f"    url: \"{item['url']}\"\n")
                    yml.write(f"    date: \"{item['date']}\"\n")
                    
                    # Записываем массив категорий, если они есть
                    if item['categories']:
                        yml.write("    categories: [")
                        yml.write(", ".join(f'"{c}"' for f, c in enumerate(item['categories'])))
                        yml.write("]\n")
                    else:
                        yml.write("    categories: []\n")
                        
                    # Записываем массив тегов
                    if item['tags']:
                        yml.write("    tags: [")
                        yml.write(", ".join(f'"{t}"' for f, t in enumerate(item['tags'])))
                        yml.write("]\n")
                    else:
                        yml.write("    tags: []\n")
                        
        print(f"[NAV-TREE-SUCCESS] Глубокий анализ завершён! Карта метаданных собрана в _data/navigation.yml")
    except Exception as e:
        print(f"[NAV-TREE-ERROR] Ошибка записи карты метаданных: {e}")

if __name__ == '__main__':
    build_navigation_tree()