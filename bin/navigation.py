#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module navigation (Часть 1 из 3)
@about Универсальный статический препроцессор метаданных и карт.
@purpose Инициализирует буферы логов и вшивает автомат эмодзи Tracy.
@author TechLab
@version 10.1.0-flat-registry-part1
"""

import os
import re
import sys
import yaml

def translit_title(text):
    if not text: return ""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9а-яё]', '', text)
    return text

def clean_tag(text):
    if not text: return ""
    return re.sub(r'\s+', '', str(text).lower().strip())

def parse_yaml_front_matter(file_path):
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
    print(text)
    artifacts_log_buffer.append(text)

def write_yaml_front_matter(file_path, data, body_content):
    try:
        front_text = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{front_text}---\n{body_content}")
    except Exception as e:
        print(f"[NAV-ERROR] Не удалось перезаписать файл {file_path}: {e}")

def load_emoji_sources(root_dir):
    pages_dir = os.path.join(root_dir, '_pages')
    page_types_emoji = {}
    section_index_emoji = {}

    if os.path.exists(pages_dir):
        for file in os.listdir(pages_dir):
            if file.endswith('.md'):
                p_data, _, _ = parse_yaml_front_matter(os.path.join(pages_dir, file))
                if p_data and p_data.get('emoji'):
                    p_slug, _ = os.path.splitext(file)
                    page_types_emoji[p_slug] = p_data['emoji']

    EXCLUDED = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)) and name not in EXCLUDED and not name.startswith('.'):
            idx_path = os.path.join(root_dir, name, 'index.md')
            if os.path.exists(idx_path):
                i_data, _, _ = parse_yaml_front_matter(idx_path)
                if i_data and i_data.get('emoji'):
                    section_index_emoji[name.lstrip('_')] = i_data['emoji']

    return page_types_emoji, section_index_emoji

def calculate_item_emoji(data, folder_parts, page_types_emoji, root_dir):
    # Извлекаем строго текстовую строку из массива папок, полностью убирая ошибку 'unhashable list'
    if isinstance(folder_parts, list) and len(folder_parts) > 0:
        first_folder = str(folder_parts[0])
    else:
        first_folder = str(folder_parts)
        
    clean_folder_name = first_folder.lstrip('_')

    if first_folder == '_posts':
        post_type = data.get('post-page')
        return page_types_emoji.get(post_type, "")

    section_dir = os.path.join(root_dir, first_folder)
    has_index = os.path.exists(os.path.join(section_dir, 'index.md')) or os.path.exists(os.path.join(section_dir, 'index.html'))

    if has_index:
        idx_path = os.path.join(section_dir, 'index.md')
        if not os.path.exists(idx_path):
            idx_path = os.path.join(section_dir, 'index.html')
        try:
            i_data, _, _ = parse_yaml_front_matter(idx_path)
            if i_data and i_data.get('emoji'):
                return i_data['emoji']
        except:
            pass
        return ""
    else:
        return page_types_emoji.get(clean_folder_name, "")

def build_navigation_tree():
    global artifacts_log_buffer
    artifacts_log_buffer.clear()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(root_dir, '_data')
    os.makedirs(data_dir, exist_ok=True)

    debug_dir = os.path.join(root_dir, '_processed_files')
    os.makedirs(debug_dir, exist_ok=True)

    EXCLUDED_FOLDERS = {'_includes', '_data', '_layouts', '_processed_files', '_pages', 'assets', 'bin', '.git', '.github'}
    RESOURCE_FOLDERS = {'img', 'images', 'files', 'res', 'resources', 'video', 'photo'}
    
    supported_sections = []
    valid_slugs = set()
    slug_to_section_map = {}
    sections_with_index = set()
    parent_properties_map = {}
    
    page_types_emoji, section_index_emoji = load_emoji_sources(root_dir)

    # 1. Анализ корневой структуры папок
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            if not name.startswith('.') and name != '_posts' and name not in EXCLUDED_FOLDERS:
                clean_section_name = name.lstrip('_')
                supported_sections.append(clean_section_name)
                
                section_dir = os.path.join(root_dir, name)
                if os.path.exists(os.path.join(section_dir, 'index.md')) or os.path.exists(os.path.join(section_dir, 'index.html')):
                    sections_with_index.add(clean_section_name)
                
                for entry in os.scandir(section_dir):
                    if entry.is_dir() and not entry.name.startswith('.') and entry.name not in RESOURCE_FOLDERS:
                        valid_slugs.add(entry.name)
                        slug_to_section_map[entry.name] = clean_section_name

    nav_tree = {
        'sections': {section: [] for section in supported_sections}
    }
    chronicle_registry = []
    seen_urls = set()

    # 2. Обход физических директорий контента
    for name in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, name)):
            if not name.startswith('.') and name != '_posts' and name not in EXCLUDED_FOLDERS:
                clean_section_name = name.lstrip('_')
                section_dir = os.path.join(root_dir, name)
                
                for root_walk, _, files in os.walk(section_dir):
                    for file in files:
                        if not file.endswith('.md'): continue
                        if os.path.basename(root_walk) in RESOURCE_FOLDERS: continue
                        
                        full_path = os.path.join(root_walk, file)
                        data, front_text, body = parse_yaml_front_matter(full_path)
                        if data is None or data.get('published') is False: continue

                        relative_path = os.path.relpath(root_walk, section_dir)
                        if relative_path == '.':
                            project_slug, _ = os.path.splitext(file)
                        else:
                            project_slug = relative_path.replace(os.sep, '-')

                        ready_permalink = data.get('permalink')
                        if ready_permalink:
                            final_url = ready_permalink
                        elif clean_section_name in sections_with_index:
                            if project_slug == 'index':
                                final_url = f"/{clean_section_name}/"
                            else:
                                final_url = f"/{clean_section_name}/{project_slug}.html"
                        else:
                            base_parent_url = f"/{clean_section_name}/"
                            if project_slug == 'index':
                                final_url = base_parent_url
                            else:
                                final_url = f"{base_parent_url}{project_slug}/"

                        data['section'] = clean_section_name
                        write_yaml_front_matter(full_path, data, body)

                        if project_slug != 'index':
                            parent_properties_map[project_slug] = {
                                'direction': data.get('direction', ''),
                                'level': data.get('level', ''),
                                'section': clean_section_name
                            }

                        # Чистая карточка витрины БЕЗ вложенных постов хроники
                        project_node = {
                            'title': data.get('title', project_slug),
                            'slug': project_slug,
                            'url': final_url,
                            'direction': data.get('direction', ''),
                            'level': data.get('level', ''),
                            'date': str(data.get('date', '')) if data.get('date') else ''
                        }
                        
                        if data.get('pinnednews') is True:
                            project_node['pinnednews'] = True

                        if clean_section_name not in nav_tree['sections']:
                            nav_tree['sections'][clean_section_name] = []
                        nav_tree['sections'][clean_section_name].append(project_node)

                        # Набиваем плоский реестр chronicle_registry самостоятельными страницами
                        item_date = str(data.get('date', '')).strip()
                        if item_date and final_url not in seen_urls and project_slug != 'index':
                            seen_urls.add(final_url)
                            item_emoji = calculate_item_emoji({}, [clean_section_name], page_types_emoji, root_dir)
                            
                            # 🔥 ПАСПОРТ СТРОГО В ВАШЕМ ПОРЯДКЕ СВОЙСТВ
                            node = {}
                            node['title'] = data.get('title', project_slug)
                            node['url'] = final_url
                            if data.get('navtitle'):
                                node['navtitle'] = data['navtitle']
                            node['section'] = clean_section_name
                            node['parentslug'] = ""
                            node['posttype'] = "page"
                            node['pinnednews'] = data.get('pinnednews', False)
                            node['emoji'] = item_emoji
                            node['date'] = item_date
                            node['direction'] = data.get('direction', '')
                            node['level'] = str(data.get('level', '')) if data.get('level') else ''
                            chronicle_registry.append(node)

    # 3. Обход папки связанных постов хроники проекта _posts/
    posts_dir = os.path.join(root_dir, '_posts')
    if os.path.exists(posts_dir):
        for root, _, files in os.walk(posts_dir):
            for file in files:
                if not file.endswith('.md'): continue
                
                full_path = os.path.join(root, file)
                data, front_text, body = parse_yaml_front_matter(full_path)
                if data is None or data.get('published') is False: continue

                file_name_clean, _ = os.path.splitext(file)
                file_name_clean_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', file_name_clean)

                post_slug = None
                post_page_type = None

                for key in list(data.keys()):
                    if str(key).endswith('-post-page'):
                        post_slug = file_name_clean_no_date if file_name_clean_no_date in valid_slugs else None
                        # 🔥 ИСПРАВЛЕНО: Берем строго первый элемент как строку, убирая list dict key error
                        post_page_type = str(key).split('-')[0]
                        break

                if not post_slug and file_name_clean_no_date in valid_slugs:
                    post_slug = file_name_clean_no_date
                    post_page_type = data.get('post-page', 'journal')

                if data and data.get('date'):
                    post_date = str(data['date'])
                else:
                    match_date = re.match(r'^(\d{4}-\d{2}-\d{2})', file_name_clean)
                    post_date = match_date.group(1) if match_date else "2026-01-01"

                short_url = f"/{post_page_type}/{post_slug}/{post_date.replace('-', '/')}/{file_name_clean_no_date}.html"

                if post_slug and short_url not in seen_urls:
                    seen_urls.add(short_url)
                    
                    parent_meta = parent_properties_map.get(post_slug, {'direction': '', 'level': '', 'section': 'faire'})
                    item_emoji = calculate_item_emoji({'post-page': post_page_type}, ['_posts'], page_types_emoji, root_dir)

                    data['categories'] = [post_page_type, post_slug]
                    data['post-page'] = post_page_type
                    data['section'] = parent_meta['section']
                    write_yaml_front_matter(full_path, data, body)

                    # 🔥 ПАСПОРТ СВЯЗАННОГО ПОСТА СТРОГО В ВАШЕМ ПОРЯДКЕ СВОЙСТВ
                    node = {}
                    node['title'] = data.get('title', file_name_clean_no_date)
                    node['url'] = short_url
                    if data.get('navtitle'):
                        node['navtitle'] = data['navtitle']
                    node['section'] = parent_meta['section']
                    node['parentslug'] = post_slug
                    node['posttype'] = post_page_type
                    node['pinnednews'] = data.get('pinnednews', False)
                    node['emoji'] = item_emoji
                    node['date'] = post_date
                    node['direction'] = parent_meta['direction']
                    node['level'] = str(parent_meta['level']) if parent_meta['level'] else ''
                    chronicle_registry.append(node)

    chronicle_registry.sort(key=lambda x: x['date'], reverse=True)
    nav_tree['chronicle_registry'] = chronicle_registry

    for section_name in list(nav_tree['sections'].keys()):
        nav_tree['sections'][section_name] = sorted(
            nav_tree['sections'][section_name], 
            key=lambda x: x['title'].lower()
        )

    nav_tree['post_types'] = ['journal', 'media']

    # 🔥 ЧИСТАЯ ПЛОСКАЯ ВЫГРУЗКА БЕЗ ЗНАЧКОВ *ID И &ID ЧЕРЕЗ SAFEDUMPER
    output_file = os.path.join(data_dir, 'navigation.yml')
    try:
        yaml.SafeDumper.ignore_aliases = lambda self, data: True
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(nav_tree, f, Dumper=yaml.SafeDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
        log_artifact("[NAV-SUCCESS] Плоская база метаданных 'navigation.yml' успешно обновлена.")
    except Exception as e:
        print(f"[NAV-ERROR] Ошибка записи карты навигации: {e}")

    for p_slug, p_meta in parent_properties_map.items():
        for p_type in ['journal', 'media']:
            dir_path = os.path.join(root_dir, p_type, p_slug)
            os.makedirs(dir_path, exist_ok=True)
            with open(os.path.join(dir_path, 'index.md'), 'w', encoding='utf-8') as pf:
                pf.write(f"---\nlayout: page\ntitle: \"Публикации проекта {p_slug}\"\nslug: {p_slug}\nsection: {p_meta['section']}\npost-page: {p_type}\nmathjax: true\n---\n\n{{% include posts-page-open.liquid type='{p_type}' %}}\n")

    try:
        with open(os.path.join(debug_dir, 'navigation_debug.log'), 'w', encoding='utf-8') as lf:
            lf.write("\n".join(artifacts_log_buffer))
    except:
        pass

if __name__ == '__main__':
    build_navigation_tree()
