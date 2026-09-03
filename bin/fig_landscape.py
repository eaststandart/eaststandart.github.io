import re

def process_single_figure_landscape(markdown_content):
    """
    Изолированная обработка одиночных горизонтальных журнальных блоков 
    с поддержкой фигурных скобок по аналогии с простыми картинками.
    """
    # Паттерн ищет открытые квадратные скобки, внутри которых обязательно есть {fig...}
    pattern = r'!\[([^\]]*\{fig[^\]]*)\].*?\]\(([^)]*)\)'
    
    # Но мы применим более точный и чистый вариант, который сразу делит на контент и URL:
    pattern = r'!\[(.*?)\]\((.*?)\)'
    
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

    def replacer(match):
        alt_content = match.group(1).strip()
        img_url = match.group(2).strip()

        # Проверяем, является ли эта картинка нашей целевой одиночной {fig}
        if '{fig' not in alt_content:
            return match.group(0) # Если это не {fig}, возвращаем как было без изменений

        # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА (|400) ---
        alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()

        # --- ШАГ 2: ИЗОЛЯЦИЯ СОДЕРЖИМОГО ФИГУРНЫХ СКОБОК ---
        # Вытаскиваем то, что внутри скобок {}, и то, что осталось снаружи
        inner_match = re.search(r'\{(fig.*?)\}', alt_content)
        
        inner_bracket = inner_match.group(1).strip() if inner_match else ""
        # К контенту снаружи относится всё, что осталось после удаления фигурных скобок и лишних пайпов
        outside_content = alt_content.replace(f"{{{inner_bracket}}}", "").strip("| ")

        # --- ШАГ 3: РАЗБОР СКРЫТОГО SEO ALT-ТЕКСТА ---
        # Убираем само слово fig из внутренней части
        inner_parts = [p.strip() for p in inner_bracket.split('|') if p.strip()]
        if inner_parts and inner_parts[0] == 'fig':
            inner_parts.pop(0) # Удаляем служебное слово 'fig'
        
        clean_alt = " | ".join(inner_parts) if inner_parts else ""

        # --- ШАГ 4: РАЗБОР ТЕКСТА ДЛЯ ПОДПИСИ ---
        outside_text = outside_content if outside_content else ""

        # --- ШАГ 5: ВЫВОД ИСПРАВЛЕННЫХ ДАННЫХ В ЛОГ-СИСТЕМУ ---
        print("\n" + "="*70)
        print("[FIG-LANDSCAPE-LOG] Найдена целевая ссылка на обработку:")
        print(f"  • Исходная строка: {match.group(0)}")
        print(f"  • Скрытый alt (из {{}}):  '{clean_alt}'")
        print(f"  • Текст для подписи:      '{outside_text}'")
        print(f"  • Путь к медиафайлу:      '{img_url}'")
        print("-"*70)

        # --- ШАГ 6: СБОРКА СЕМАНТИЧЕСКОГО HTML ---
        figcaption_html = ""
        if outside_text:
            figcaption_html = f'\n        <figcaption class="img-figcaption">{outside_text}</figcaption>'

        html_output = (
            f'<div class="img-single-figure">\n'
            f'    <figure class="img-figure">\n'
            f'        <img class="img-single-figure-landscape" alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
            f'{figcaption_html}\n'
            f'    </figure>\n'
            f'</div>'
        )

        print("[FIG-LANDSCAPE-LOG] Успешная трансформация в HTML:")
        print(html_output)
        print("="*70)

        return html_output

    return re.sub(pattern, replacer, markdown_content)
