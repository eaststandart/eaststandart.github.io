import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Печатаем для контроля все найденные картинки в лог
    all_links = re.findall(r'(!\[.*?\]\(.*?\))', content)
    for link in all_links:
        print(f"[ОТЛАДКА ИЗ ФАЙЛА {os.path.basename(file_path)}]: Найдена строка -> {link}")

    replacements_count = 0

    def replace_md_links(match):
        nonlocal replacements_count
        alt_part = match.group(1)
        url_part = match.group(2)
        
        # Если внутри квадратных скобок есть хоть одна палочка
        if '|' in alt_part:
            # Сначала полностью очищаем от старых обратных слэшей, чтобы не плодить мусор
            alt_clean = alt_part.replace('\\|', '|')
            # Заново и гарантированно экранируем КАЖДУЮ палочку
            alt_escaped = alt_clean.replace('|', '\\|')
            
            # Если строка изменилась, засчитываем замену
            if alt_escaped != alt_part:
                replacements_count += 1
                return f'![{alt_escaped}]({url_part})'
                
        return match.group(0)

    # Ищем конструкции ![alt](url) с любыми символами внутри
    new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_md_links, content)

    if replacements_count > 0:
        print(f"=== [ИЗМЕНЕН]: {file_path} — экранировано палочек: {replacements_count} ===")
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

print(f"[УСПЕХ]: Всего проверено заметок: {md_files_found}")
