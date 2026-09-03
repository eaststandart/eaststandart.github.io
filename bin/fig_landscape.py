#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script fig_landscape.py
@about Полный независимый модуль для обработки одиночных журнальных блоков (Landscape / Portrait / Custom).
@purpose Находит новые ссылки вида ![{fig...}], за один шаг определяет ориентацию 
         и кастомные размеры кадра, дублирует подпись в пустой alt и собирает HTML.
         Ювелирно защищен от обработки примеров в бэктиках.
@author TechLab
@version 1.2-stable
"""

import re

def process_single_figure_landscape(markdown_content):
    """
    Ищет маркдаун-ссылки журнального типа со скобками {fig} 
    и преобразует их в независимые HTML-блоки figure.
    """
    # Возвращаем твой родной, жадный и полностью рабочий паттерн
    pattern = r'!\[(.*?)\]\((.*?)\)'
    
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

    def replacer(match):
        alt_content = match.group(1).strip()
        img_url = match.group(2).strip()

        # 🛡️ ЖЕЛЕЗНАЯ КУРСОРНАЯ ЗАЩИТА: 
        # Если перед ссылкой или в ней есть бэктики — это текстовый пример для людей!
        # Проверяем границы захвата и внутренности контента
        if '`' in match.group(0) or '`' in alt_content or '`' in img_url:
            return match.group(0) # Возвращаем строку как есть, полностью игнорируя её

        # Если это не наша новая целевая ссылка со скобками {fig}, возвращаем её без изменений
        if '{fig' not in alt_content:
            return match.group(0)

        # --- ШАГ 1: ГЛОБАЛЬНЫЙ ЗАКОН ОЧИСТКИ ХВОСТОВ ОБСИДИАНА (|400) ---
        alt_content = re.sub(r'\|\s*\d+\s*$', '', alt_content).strip()

        # --- ШАГ 2: ИЗОЛЯЦИЯ СОДЕРЖИМОГО ФИГУРНЫХ СКОБОК ---
        inner_match = re.search(r'\{(fig.*?)\}', alt_content)
        inner_bracket = inner_match.group(1).strip() if inner_match else ""
        
        # Контент снаружи — это всё, что осталось после удаления фигурных скобок
        outside_content = alt_content.replace(f"{{{inner_bracket}}}", "").strip("| ")

        # --- ШАГ 3: ОПРЕДЕЛЕНИЕ КЛАССА И ГЕОМЕТРИИ ЗА 1 ШАГ ---
        target_class = "img-single-figure-landscape"
        custom_attrs_str = ""

        bracket_clean = inner_bracket.lower().replace(' ', '')

        # Проверяем кастомный размер (например, 320x405) по аналогии с images.py
        size_match = re.search(r'(\d+)[xх](\d+)', bracket_clean, re.IGNORECASE)

        if size_match:
            width, height = int(size_match.group(1)), int(size_match.group(2))
            if width > height:
                target_class = "img-single-figure-custom-landscape"
            else:
                target_class = "img-single-figure-custom-portrait"
            custom_attrs_str = f' width="{width}" height="{height}" style="aspect-ratio: {width} / {height} !important;"'

        # Если размеров нет, проверяем стандартный флаг вертикали 'v'
        elif '|v' in bracket_clean or 'v|' in bracket_clean or bracket_clean == 'fig|v':
            target_class = "img-single-figure-portrait"

        # Начисто вырезаем служебные маркеры fig, v и размеры из скрытой части для получения clean_alt
        clean_alt = re.sub(r'\b(fig|v)\b|\d+[xх]\d+', '', inner_bracket, flags=re.IGNORECASE)
        clean_alt = re.sub(r'[\s|]+', ' ', clean_alt).strip()

        # --- ШАГ 4: РАЗБОР ЖИВОГО ТЕКСТА ДЛЯ ПОДПИСИ И ЗАЩИТА ALT ---
        outside_text = outside_content if outside_content else ""

        # Если скрытый SEO alt пуст, но есть живая подпись — дублируем её в alt для поисковиков
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

        # --- ШAG 6: СБОРКА СЕМАНТИЧЕСКОГО HTML ---
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

    return re.sub(pattern, replacer, markdown_content)
