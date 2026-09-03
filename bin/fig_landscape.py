#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script fig_landscape.py
@about Полный независимый модуль для обработки одиночных журнальных блоков (Landscape / Portrait / Custom).
@purpose Находит новые ссылки вида ![{fig...}], за один шаг определяет ориентацию 
         и кастомные размеры кадра, дублирует подпись в пустой alt и собирает HTML.
         Железно защищен от обработки внутри кода (```), HTML и Liquid комментариев.
@author TechLab
@version 1.4
"""

import re

def process_single_figure_landscape(markdown_content):
    """
    Ищет маркдаун-ссылки журнального типа со скобками {fig} 
    и преобразует их в независимые HTML-блоки figure.
    Полностью игнорирует закомментированные и кодовые блоки.
    """
    # 🔒 ЭТАП А: ЖЕЛЕЗНЫЙ СЕЙФ (Замораживаем всё, что нельзя трогать)
    vault = []
    
    def freezer(match):
        vault.append(match.group(0))
        return f'==FIG_VAULT_BLOCK_{len(vault)-1}=='

    # 1. Прячем многострочные блоки кода ``` ... ```
    temporary_content = re.sub(r'```[\s\S]*?```', freezer, markdown_content)
    
    # 2. Прячем Liquid-комментарии {% comment %} ... {% endcomment %}
    temporary_content = re.sub(r'{%\s*comment\s*%}[\s\S]*?{%\s*endcomment\s*%}', freezer, temporary_content)
    
    # 3. Прячем HTML-комментарии <!-- ... -->
    temporary_content = re.sub(r'<!--[\s\S]*?-->', freezer, temporary_content)
    
    # 4. Прячем строчный код ` ... `
    temporary_content = re.sub(r'`{1,3}[^`\n]+?`{1,3}', freezer, temporary_content)

    # 🎯 ЭТАП Б: ОБРАБОТКА ЦЕЛЕВЫХ ССЫЛОК
    pattern = r'!\[([^\]]*\{fig[^\]]*)\].*?\]\(([^)]*)\)'
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

    def replacer(match):
        alt_content = match.group(1).strip()
        img_url = match.group(2).strip()

        # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА (|400) ---
        alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()

        # --- ШАГ 2: ИЗОЛЯЦИЯ СОДЕРЖИМОГО ФИГУРНЫХ СКОБОК ---
        inner_match = re.search(r'\{(fig.*?)\}', alt_content)
        inner_bracket = inner_match.group(1).strip() if inner_match else ""
        
        outside_content = alt_content.replace(f"{{{inner_bracket}}}", "").strip("| ")

        # --- ШАГ 3: ОПРЕДЕЛЕНИЕ КЛАССА И ГЕОМЕТРИИ ЗА 1 ШАГ ---
        target_class = "img-single-figure-landscape"
        custom_attrs_str = ""

        bracket_clean = inner_bracket.lower().replace(' ', '')

        size_match = re.search(r'(\d+)[xх](\d+)', bracket_clean, re.IGNORECASE)

        if size_match:
            width, height = int(size_match.group(1)), int(size_match.group(2))
            if width > height:
                target_class = "img-single-figure-custom-landscape"
            else:
                target_class = "img-single-figure-custom-portrait"
            custom_attrs_str = f' width="{width}" height="{height}" style="aspect-ratio: {width} / {height} !important;"'

        elif '|v' in bracket_clean or 'v|' in bracket_clean or bracket_clean == 'fig|v':
            target_class = "img-single-figure-portrait"

        clean_alt = re.sub(r'\b(fig|v)\b|\d+[xх]\d+', '', inner_bracket, flags=re.IGNORECASE)
        clean_alt = re.sub(r'[\s|]+', ' ', clean_alt).strip()

        # --- ШАГ 4: РАЗБОР ЖИВОГО ТЕКСТА ДЛЯ ПОДПИСИ И ЗАЩИТА ALT ---
        outside_text = outside_content if outside_content else ""

        if not clean_alt and outside_text:
            clean_alt = outside_text

        # --- ШАГ 5: ВЫВОД ОЧИЩЕННЫХ ДАННЫХ В ЛОГ-СИСТЕМУ ---
        print("\n" + "="*70)
        print("[FIG-LANDSCAPE-LOG] Найдена целевая ссылка на обработку:")
        print(f"  • Исходная строка: {match.group(0)}")
        print(f"  • Выбранный класс:       '{target_class}'")
        print(f"  • Скрытый alt (из {{}}):  '{clean_alt}'")
        print(f"  • Текст для подписи:      '{outside_text}'")
        print(f"  • Кастомные атрибуты:     '{custom_attrs_str.strip()}'")
        print(f"  • Путь к медиафайлу:      '{img_url}'")
        print("-"*70)

        figcaption_html = ""
        if outside_text:
            figcaption_html = f'\n        <figcaption class="img-figcaption">{outside_text}</figcaption>'

        html_output = (
            f'<div class="img-single-figure">\n'
            f'    <figure class="img-figure">\n'
            f'        <img class="{target_class}"{custom_attrs_str} alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
            f'{figcaption_html}\n'
            f'    </figure>\n'
            f'</div>'
        )

        print("[FIG-LANDSCAPE-LOG] Успешная трансформация в HTML:")
        print(html_output)
        print("="*70)

        return html_output

    # Запускаем трансформацию на защищенном контенте
    temporary_content = re.sub(pattern, replacer, temporary_content)

    # 🔓 ЭТАП В: РАЗМОРОЗКА (Возвращаем всё из сейфа на свои места)
    for idx, original_block in enumerate(vault):
        temporary_content = temporary_content.replace(f'==FIG_VAULT_BLOCK_{idx}==', original_block)
        
    return temporary_content
