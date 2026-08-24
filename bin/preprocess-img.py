import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Заменяем палочки | на \| строго внутри альтернативного текста картинок
    def replace_links(match):
        alt_part = match.group(1)
        url_part = match.group(2)
        alt_escaped = alt_part.replace('|', '\\|')
        return f'![{alt_escaped}]({url_part})'

    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_links, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Поднимаемся на уровень выше папки bin и сканируем весь репозиторий
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

for root, dirs, files in os.walk(root_dir):
    if any(p in root for p in ['.git', '.github', '_site', '.jekyll-cache', 'bin']):
        continue
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(root, file))
