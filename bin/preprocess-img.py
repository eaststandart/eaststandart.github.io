import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements_count = 0

    def replace_md_links(match):
        nonlocal replacements_count
        alt_part = match.group(1)
        url_part = match.group(2)
        
        # Если внутри alt-текста обычной картинки есть палочка, экранируем её
        if '|' in alt_part and '\\|' not in alt_part:
            alt_escaped = alt_part.replace('|', '\\|')
            replacements_count += 1
            return f'![{alt_escaped}]({url_part})'
        return match.group(0)

    # ТОЧНЫЙ ФИКС: Экранировали скобку (\]), чтобы регулярка железно находила стык скобок ](
    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_md_links, content)

    if replacements_count > 0:
        print(f"[ИЗМЕНЕН]: {file_path} — сделано замен: {replacements_count}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Сканируем строго текущую рабочую папку репозитория
md_files_found = 0
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', '.github', '_site', '.jekyll-cache', 'bin']):
        continue
    for file in files:
        if file.endswith('.md'):
            md_files_found += 1
            process_file(os.path.join(root, file))

print(f"[УСПЕХ]: Проверено заметок: {md_files_found}")
