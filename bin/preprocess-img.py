"""
@about Модуль предобработки разметки изображений на этапе GitHub Actions (до запуска Jekyll).
@purpose Находит стандартный Markdown-синтаксис картинок, считывает параметры и на лету преобразует 
         их в чистые HTML-теги <img> без вмешательства в структуру абзацев <p>. 
         Полностью сохраняет логику Obsidian: картинки, написанные в столбик без пустых строк, 
         Jekyll объединит в единый абзац-галерею, а изолированные через пустую строку — разделит.
         Переносит технические маркеры в точечные HTML-классы (img-v, img-center). 
         Если человеческого описания нет, alt остается строго пустым (alt="").
@author TechLab
@version 1.3.3
"""

import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements_count = 0

    def replace_to_pure_html(match):
        nonlocal replacements_count
        alt_part = match.group(1).strip()
        url_part = match.group(2).strip()

        # Защита видео: обрабатываем строго графические форматы
        valid_extensions = ('.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg')
        url_low = url_part.lower()
        if not any(ext in url_low for ext in valid_extensions):
            return match.group(0)

        # Чистим путь к картинке от мусорного префикса гитхаба
        if 'github/eaststandart.github.io' in url_part:
            url_part = url_part.split('github/eaststandart.github.io')[-1]
        if not url_part.startswith('/'):
            url_part = '/' + url_part

        has_v = False
        has_center = False
        caption_text = ""

        # СЦЕНАРИЙ 1: Внутри скобок только один элемент (нет палочек '|')
        if '|' not in alt_part:
            alt_low = alt_part.lower()
            if alt_low == 'v':
                has_v = True
            elif alt_low == 'center':
                has_center = True
            else:
                caption_text = alt_part
        
        # СЦЕНАРИЙ 2: Есть палочки '|', разбиваем параметры
        else:
            parts = [p.strip() for p in alt_part.split('|')]
            
            # СТРОГАЯ ПРОВЕРКА: Проверяем ТОЛЬКО самый первый элемент на маркеры
            if len(parts) > 0:
                first_part_low = parts[0].lower()
                remaining_parts = parts
                
                if first_part_low == 'v':
                    has_v = True
                    remaining_parts = parts[1:]
                elif first_part_low == 'center':
                    has_center = True
                    remaining_parts = parts[1:]
                elif first_part_low in ('v-center', 'center-v'):
                    has_v = True
                    has_center = True
                    remaining_parts = parts[1:]
            else:
                remaining_parts = parts

            # Проверяем второй элемент: вдруг там второй маркер (например, ![v|center|...])
            if len(remaining_parts) > 0:
                next_part_low = remaining_parts[0].lower()
                if next_part_low == 'v' and not has_v:
                    has_v = True
                    remaining_parts = remaining_parts[1:]
                elif next_part_low == 'center' and not has_center:
                    has_center = True
                    remaining_parts = remaining_parts[1:]

            # Все остальные элементы сканируем. Игнорируем размеры, собираем только текст
            for part in remaining_parts:
                if part.isdigit():
                    continue  # Полностью вырезаем мусорные размеры из Obsidian для сайта
                elif part != "":
                    caption_text = f"{caption_text} {part}".strip() if caption_text else part

        # Собираем классы СТРОГО на саму картинку, не трогая абзацы!
        classes = []
        if has_v: classes.append("img-v")
        if has_center: classes.append("img-center")
        
        img_class_attr = f' class="{" ".join(classes)}"' if classes else ""
        
        # ФИКС: Никаких системных подстановок текста. Если caption_text пустой, будет чистое alt=""
        alt_attr = f' alt="{caption_text}"'
        replacements_count += 1
        
        return f'<img loading="lazy"{img_class_attr}{alt_attr} src="{url_part}">'

    # Ювелирно перехватываем маркдаун-ссылки и меняем их на чистые теги <img>
    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_to_pure_html, content)

    if replacements_count > 0:
        print(f"[ИЗМЕНЕН]: {file_path} — успешно обработано картинок: {replacements_count}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Сканируем рабочую директорию репозитория на сервере GitHub
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', '.github', '_site', '.jekyll-cache', 'bin']):
        continue
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(root, file))
