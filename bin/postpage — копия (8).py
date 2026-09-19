#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module post-page
@about Изолированный автономный генератор физических md-страниц архивов проектов.
@purpose 100% бэкенд-фильтрация постов по карте навигации navigation.yml. 
         Python на Шаге 0 находит проекты, на Шаге 1 собирает посты по relatedpages, 
         проверяет наличие posttype и передаёт в Jekyll готовый массив URL-адресов.
@author TechLab
@version 15.0.0-pure-url-backend
"""

import os
import sys
import yaml

def generate_posts_pages():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    navigation_file = os.path.join(root_dir, '_data', 'navigation.yml')
    # 🧼 ЗАЧИСТКА ВАРНИНГОВ: Переносим лог в каноничную папку артефактов контента
    log_file_path = os.path.join(root_dir, '_post_page_files', 'posts-page-generator.log')
    
    log_buffer = []
    
    if not os.path.exists(navigation_file):
        print(f"[POST-ERROR] Карта навигации navigation.yml не найдена: {navigation_file}")
        return

    # Загружаем Единственный Источник Правды в оперативную память
    try:
        with open(navigation_file, 'r', encoding='utf-8') as f:
            navigation_map = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[POST-ERROR] Сбой чтения конфигурационного файла YAML: {e}")
        return

    # 🧼 САНИТАРНАЯ ЗАЧИСТКА ПАПОК ОТ СТРАНИЦ-ПРИЗРАКОВ
    print("[POST-CLEAN] Запуск санитарной зачистки целевых папок контура...")
    for target_folder in ['journal', 'media']:
        folder_path = os.path.join(root_dir, target_folder)
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.md') and 'index' not in file_name:
                    file_to_remove = os.path.join(folder_path, file_name)
                    try:
                        os.remove(file_to_remove)
                        log_buffer.append(f"[CLEAN] Удален устаревший файл: {target_folder}/{file_name}")
                    except Exception as e:
                        print(f"[POST-ERROR] Не удалось удалить файл {file_to_remove}: {e}")

    # ➡️ ШАГ 0: Находим все живые родительские проекты в карте сайта
    parent_projects = {}
    for nav_key, nav_nodes in navigation_map.items():
        if (not nav_key.startswith('_posts/') and 
            nav_key != 'detected_root_folders' and 
            isinstance(nav_nodes, list) and len(nav_nodes) > 0):
            
            project_passport = nav_nodes[0]
            if isinstance(project_passport, dict) and 'title' in project_passport:
                p_slug = nav_key.split('/')[-2] if '/' in nav_key else nav_key.replace('.md', '')
                parent_projects[nav_key] = {
                    'project_file': nav_key,
                    'title': project_passport['title'].strip(),
                    'slug': p_slug,
                    'journal_urls': [],
                    'media_urls': []
                }

    # ➡️ ШАГ 1: Сбор и фильтрация связанных постов строго по URL на основе связанных проектов
    for nav_key, nav_nodes in navigation_map.items():
        if nav_key.startswith('_posts/') and isinstance(nav_nodes, list) and len(nav_nodes) > 0:
            post_passport = nav_nodes[0]
            if isinstance(post_passport, dict):
                related_page_path = post_passport.get('relatedpages')
                
                if related_page_path in parent_projects:
                    # ЖЕСТКИЙ ПРОПУСК ПИТОНА: Проверяем физическое наличие свойства 'posttype'
                    p_type = post_passport.get('posttype')
                    post_url = post_passport.get('url')
                    
                    if not p_type or not post_url:
                        continue
                        
                    post_data = {
                        'url': post_url,
                        'date': str(post_passport.get('date', '0000-00-00'))
                    }
                    
                    # УНИВЕРСАЛЬНЫЙ АВТОМАТ: В большую ленту кнопки 0 летит всё, кроме маркеров-запретов *-close
                    if 'journal' in p_type and p_type != 'journal-close':
                        parent_projects[related_page_path]['journal_urls'].append(post_data)
                    elif 'media' in p_type and p_type != 'media-close':
                        parent_projects[related_page_path]['media_urls'].append(post_data)

    # ➡️ ШАГ 2: Сортировка хронологии, штамповка вложенных страниц и сбор паспортов навигации
    append_nodes = {}

    for rel_path, proj in parent_projects.items():
        for loop_type in ['journal', 'media']:
            urls_list = proj['journal_urls'] if loop_type == 'journal' else proj['media_urls']
            
            if not urls_list:
                continue
                
            urls_list.sort(key=lambda x: x['date'], reverse=True)
            sorted_urls = [u['url'] for u in urls_list]
            
            p_slug = proj['slug']
            parent_title = proj['title']
            
            # Универсально вычисляем имя родительской папки (раздела) на основе пути ключа проекта
            p_section = rel_path.split('/')[0] if '/' in rel_path else 'faire'
            
            # ЗЕРКАЛЬНАЯ ЗАЩИТА: создаем вложенную структуру папок разделов контура
            target_folder_path = os.path.join(root_dir, loop_type, p_section)
            os.makedirs(target_folder_path, exist_ok=True)
            target_md_file = os.path.join(target_folder_path, f"{p_slug}.md")
            
            # Глубокие физические и виртуальные интернет-адреса для Jekyll
            jekyll_page_path = f"{loop_type}/{p_section}/{p_slug}.md"
            jekyll_permalink = f"/{loop_type}/{p_section}/{p_slug}/"
            
            base_front_matter = {
                "layout": "page",
                "title": f"{parent_title}: лента постов",
                "permalink": jekyll_permalink,
                "mathjax": True
            }
            front_matter_string = yaml.dump(base_front_matter, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
            urls_string = ", ".join(sorted_urls)
            
            body_lines = [
                '<!--1. ПОЛНОСТЬЮ ОТФИЛЬТРОВАННЫЙ НА БЭКЕНДЕ МАССИВ URL-АДРЕСОВ ПРОЕКТА -->',
               f'{{%- assign project_post_urls = "{urls_string}" | split: ", " -%}}',
                '',
                '{% include posts-page-open.liquid urls=project_post_urls %}'
            ]
            file_content = f"---\n{front_matter_string}---\n\n" + "\n".join(body_lines).strip()
            
            try:
                with open(target_md_file, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                log_msg = f"[POST-GENERATOR] Создан файл: {jekyll_page_path} | Заголовок: {parent_title}: лента постов | Передано URL: {len(sorted_urls)}"
                print(log_msg)
                log_buffer.append(log_msg)
                
                # Запоминаем паспорт для последующей дозаписи в navigation.yml
                append_nodes[jekyll_page_path] = [{
                    'title': f"{parent_title}: лента постов",
                    'url': jekyll_permalink,
                    'posttype': 'post-page-open',
                    'relatedpages': rel_path
                }]
            except Exception as e:
                print(f"[POST-ERROR] Не удалось записать файл архива {target_md_file}: {e}")

    # ➡️ ШАГ 3: ДОЗАПИСЬ ПАСПОРТОВ В НАВИГАЦИЮ И ВЫВОД КАРТЫ В ЛОГ АУДИТА
    if append_nodes:
        try:
            # Обновляем навигационную карту в памяти для полного лога
            navigation_map.update(append_nodes)
            
            # Физически дописываем паспорта в самый конец файла navigation.yml
            with open(navigation_file, 'a', encoding='utf-8') as f:
                f.write("\n# =========================================================================\n")
                f.write("# АВТОГЕНЕРИРУЕМЫЕ СТРАНИЦЫ ПОСТОВ ПРОЕКТОВ (POST-PAGE-OPEN)\n")
                f.write("# =========================================================================\n")
                yaml.dump(append_nodes, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            log_buffer.append(f"[APPEND-SUCCESS] В хвост navigation.yml добавлено паспортов: {len(append_nodes)}")
        except Exception as e:
            print(f"[POST-ERROR] Не удалось дозаписать паспорта в navigation.yml: {e}")

    # Сохраняем изолированный слепок полной карты навигации в отдельный файл лога для ручного аудита
    try:
        nav_log_file_path = os.path.join(root_dir, '_post_page_files', 'navigation_after_postpage.log')
        os.makedirs(os.path.dirname(nav_log_file_path), exist_ok=True)
        with open(nav_log_file_path, 'w', encoding='utf-8') as nlf:
            yaml.dump(navigation_map, nlf, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except:
        pass

    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as lf:
            lf.write("\n".join(log_buffer))
        print("[POST-SUCCESS] Лог генератора страниц успешно зафиксирован в артефактах.")
    except Exception as e:
        print(f"[POST-ERROR] Не удалось сохранить файл лога: {e}")

if __name__ == '__main__':
    generate_posts_pages()
