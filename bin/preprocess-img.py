import os
import re

def process_file(file_path):
    print(f"[НАЙДЕН ФАЙЛ]: Обрабатываю {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_links(match):
        alt_part = match.group(1)
        url_part = match.group(2)
        alt_escaped = alt_part.replace('|', '\\|')
        return f'![{alt_escaped}]({url_part})'

    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_links, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Получаем абсолютный путь к корню репозитория (на уровень выше папки bin)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"[СТАРТ]: Корень репозитория определен как: {root_dir}")
print(f"[СПИСОК ПАПОК В КОРНЕ]: {os.listdir(root_dir)}")

md_counter = 0
for root, dirs, files in os.walk(root_dir):
    # Пропускаем только служебные папки сборщика
    if any(p in root for p in ['.git', '.github', '_site', '.jekyll-cache', 'bin']):
        continue
    for file in files:
        if file.endswith('.md'):
            md_counter += 1
            process_file(os.path.join(root, file))

print(f"[ИТОГ]: Скрипт успешно завершил обход. Всего изменено файлов: {md_counter}")
