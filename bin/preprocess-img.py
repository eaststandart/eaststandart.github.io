import os

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements_count = 0
    new_content = ""
    cursor = 0
    length = len(content)

    # Ищем конструкции ![alt](url) посимвольно, чтобы исключить ошибки регулярных выражений
    while cursor < length:
        if content[cursor:cursor+2] == '![':
            # Нашли начало альтернативного текста картинки
            close_bracket = content.find('](', cursor)
            if close_bracket != -1:
                close_paren = content.find(')', close_bracket)
                if close_paren != -1:
                    # Вырезаем параметры картинки внутри квадратных скобок [ ]
                    alt_part = content[cursor+2:close_bracket]
                    url_part = content[close_bracket+2:close_paren]
                    
                    # Если внутри параметров есть палочки, экранируем их
                    if '|' in alt_part and '\\|' not in alt_part:
                        alt_escaped = alt_part.replace('|', '\\|')
                        new_content += f'![{alt_escaped}]({url_part})'
                        replacements_count += 1
                        cursor = close_paren + 1
                        continue
        
        new_content += content[cursor]
        cursor += 1

    if replacements_count > 0:
        print(f"[ИЗМЕНЕН]: {file_path} — экранировано палочек в картинках: {replacements_count}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Сканируем строго текущую рабочую папку репозитория на сервере GitHub
md_files_found = 0
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', '.github', '_site', '.jekyll-cache', 'bin']):
        continue
    for file in files:
        if file.endswith('.md'):
            md_files_found += 1
            process_file(os.path.join(root, file))

print(f"[УСПЕХ]: Проверено заметок: {md_files_found}")
