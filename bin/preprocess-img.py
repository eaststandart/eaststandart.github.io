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

        # Корректируем и чистим путь к картинке от мусорного префикса гитхаба
        if 'github/eaststandart.github.io' in url_part:
            url_part = url_part.split('github/eaststandart.github.io')[-1]
        if not url_part.startswith('/'):
            url_part = '/' + url_part

        # Если палочек нет — это простая картинка с чистым описанием (или пустая)
        if '|' not in alt_part:
            return f'<p><img loading="lazy" alt="{alt_part}" src="{url_part}"></p>'

        # Разбираем параметры по палочкам
        parts = [p.strip() for p in alt_part.split('|')]
        
        has_v = False
        has_center = False
        caption_text = ""
        img_width = ""

        # Сканируем все элементы внутри скобок
        for part in parts:
            part_low = part.lower()
            if part_low == 'v':
                has_v = True
            elif part_low == 'center':
                has_center = True
            elif part.isdigit():
                img_width = part
            elif part != "":
                caption_text = part

        # Магическая сборка комбинированного класса на основе найденных маркеров
        p_class = ""
        if has_v and has_center:
            p_class = ' class="img-vertical-center"'
        elif has_v:
            p_class = ' class="img-vertical"'
        elif has_center:
            p_class = ' class="img-center"'

        # Собираем атрибуты тега img
        width_attr = f' width="{img_width}"' if img_width else ''
        
        # Если текста для SEO нет, временно подставим имя класса, чтобы тег alt не был пустым
        if not caption_text:
            if has_v and has_center:
                caption_text = "vertical center image"
            elif has_v:
                caption_text = "vertical image"
            elif has_center:
                caption_text = "centered image"

        alt_attr = f' alt="{caption_text}"'

        replacements_count += 1
        
        # Генерируем идеальный, чистый HTML
        return f'<p{p_class}><img loading="lazy"{alt_attr} src="{url_part}"{width_attr}></p>'

    # Регулярное выражение перехватывает все стандартные Markdown-картинки ![alt](url)
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
