"""
@about Модуль предобработки разметки изображений на этапе GitHub Actions (до запуска Jekyll).
@purpose Находит стандартный Markdown-синтаксис картинок, считывает параметры и на лету переписывает 
         их в чистый HTML-код. Извлекает технические маркеры (v, center) и преобразует их в CSS-классы 
         родительского абзаца (img-vertical, img-center, img-vertical-center). Очищает атрибут alt от мусора, 
         оставляя только чистый человеческий текст для SEO, и нативно внедряет loading="lazy". Полностью 
         исключает ложные срабатывания, если ключевые слова встречаются внутри предложений или в путях файлов.
@author TechLab
"""

import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Вспомогательная функция для разбора параметров ОДНОЙ картинки
    def parse_alt_and_url(alt_part, url_part):
        valid_extensions = ('.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg')
        url_low = url_part.lower()
        if not any(ext in url_low for ext in valid_extensions):
            return None

        if 'github/eaststandart.github.io' in url_part:
            url_part = url_part.split('github/eaststandart.github.io')[-1]
        if not url_part.startswith('/'):
            url_part = '/' + url_part

        has_v = False
        has_center = False
        caption_text = ""

        if '|' not in alt_part:
            alt_low = alt_part.lower()
            if alt_low == 'v':
                has_v = True
            elif alt_low == 'center':
                has_center = True
            else:
                caption_text = alt_part
        else:
            parts = [p.strip() for p in alt_part.split('|')]
            first_part_low = parts[0].lower() if len(parts) > 0 else ""
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

            if len(remaining_parts) > 0:
                next_part_low = remaining_parts[0].lower()
                if next_part_low == 'v' and not has_v:
                    has_v = True
                    remaining_parts = remaining_parts[1:]
                elif next_part_low == 'center' and not has_center:
                    has_center = True
                    remaining_parts = remaining_parts[1:]

            for part in remaining_parts:
                if part.isdigit():
                    continue  # Игнорируем и стираем размер из Obsidian
                elif part != "":
                    caption_text = f"{caption_text} {part}".strip() if caption_text else part

        if not caption_text:
            if has_v and has_center: caption_text = "vertical centered image"
            elif has_v: caption_text = "vertical image"
            elif has_center: caption_text = "centered image"

        return {
            'has_v': has_v,
            'has_center': has_center,
            'caption': caption_text,
            'url': url_part
        }

    replacements_count = 0

    # Функция обрабатывает целую строку (абзац), если в ней найдены картинки
    def process_line(line_content):
        nonlocal replacements_count
        
        # Находим все маркдаун-картинки внутри текущей строки
        md_images = re.findall(r'!\[(.*?)\]\((.*?)\)', line_content)
        if not md_images:
            return line_content

        parsed_images = []
        is_pure_gallery = True

        for alt_p, url_p in md_images:
            res = parse_alt_and_url(alt_p, url_p)
            if res is None:
                is_pure_gallery = False
                break
            parsed_images.append(res)

        if not parsed_images or not is_pure_gallery:
            return line_content

        # Вычисляем общий класс выравнивания для всего ряда на основе картинок в нем
        any_v = any(img['has_v'] for img in parsed_images)
        any_center = any(img['has_center'] for img in parsed_images)

        p_class = ""
        if any_v and any_center: p_class = ' class="img-vertical-center"'
        elif any_v: p_class = ' class="img-vertical"'
        elif any_center: p_class = ' class="img-center"'

        # Собираем чистые HTML теги картинок без width
        html_images = []
        for img in parsed_images:
            html_images.append(f'<img loading="lazy" alt="{img["caption"]}" src="{img["url"]}">')

        replacements_count += 1
        
        # Склеиваем ВСЕ картинки строки внутрь ОДНОГО тега <p>, возвращая сетку ряда!
        return f'<p{p_class}>{" ".join(html_images)}</p>'

    # Разбиваем контент на строки и обрабатываем каждую индивидуально
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.strip().startswith('![') or '![' in line:
            # Ищем и заменяем группу картинок в пределах текущей строки
            # Регулярка захватывает всю строку от первой до последней картинки
            processed_line = re.sub(r'(!\[.*?\].*?\))', lambda m: process_line(m.group(0)), line)
            new_lines.append(processed_line)
        else:
            new_lines.append(line)

    new_content = '\n'.join(new_lines)

    if replacements_count > 0:
        print(f"[ИЗМЕНЕН]: {file_path} — успешно собрано галерейных рядов: {replacements_count}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Сканируем репозиторий на сервере GitHub
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', '.github', '_site', '.jekyll-cache', 'bin']):
        continue
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(root, file))
