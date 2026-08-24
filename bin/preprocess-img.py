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

    replacements_count = 0

    def replace_to_pure_html(match):
        nonlocal replacements_count
        alt_part = match.group(1).strip()
        url_part = match.group(2).strip()

        # ФИКС ПУНКТА 2: Проверяем, что это точно картинка. Если видео — возвращаем исходную строку маркдауна без изменений!
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

            # Проверяем второй элемент: вдруг там второй маркер
            if len(remaining_parts) > 0:
                next_part_low = remaining_parts[0].lower()
                if next_part_low == 'v' and not has_v:
                    has_v = True
                    remaining_parts = remaining_parts[1:]
                elif next_part_low == 'center' and not has_center:
                    has_center = True
                    remaining_parts = remaining_parts[1:]

            # Все остальные элементы сканируем. ИГНОРИРУЕМ ЦИФРЫ РАЗМЕРОВ (вырезаем их)
            for part in remaining_parts:
                if part.isdigit():
                    continue # Просто пропускаем размер, в HTML-код сайта он не пойдет!
                elif part != "":
                    caption_text = f"{caption_text} {part}".strip() if caption_text else part

        # Сборка комбинированного класса на основе найденных маркеров
        p_class = ""
        if has_v and has_center:
            p_class = ' class="img-vertical-center"'
        elif has_v:
            p_class = ' class="img-vertical"'
        elif has_center:
            p_class = ' class="img-center"'

        # Защита от пустого alt
        if not caption_text:
            if has_v and has_center:
                caption_text = "vertical centered image"
            elif has_v:
                caption_text = "vertical image"
            elif has_center:
                caption_text = "centered image"

        alt_attr = f' alt="{caption_text}"'

        replacements_count += 1
        # ФИКС ПУНКТА 1: Полностью убрали width="" из сборки. HTML теперь кристально чистый
        return f'<p{p_class}><img loading="lazy"{alt_attr} src="{url_part}"></p>'

    # Перехватываем стандартные Markdown-картинки ![alt](url)
    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_to_pure_html, content)

    if replacements_count > 0:
        print(f"[ИЗМЕНЕН]: {file_path} — сгенерирован чистый HTML с классами: {replacements_count}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Сканируем рабочую директорию репозитория на сервере GitHub
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', '.github', '_site', '.jekyll-cache', 'bin']):
        continue
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(root, file))
