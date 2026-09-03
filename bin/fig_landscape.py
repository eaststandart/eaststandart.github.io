#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script fig_landscape.py
@about Изолированный модуль для обработки одиночных журнальных блоков (Landscape / Portrait).
@purpose Находит новые ссылки вида ![{fig...}] с поддержкой обсидиановых хвостов,
         за один шаг определяет ориентацию кадра и собирает семантическую HTML-структуру.
@author TechLab
@version 1.1
"""

import re

def process_single_figure_landscape(markdown_content):
    """
    Ищет маркдаун-ссылки журнального типа со скобками {fig} 
    и преобразует их в независимые HTML-блоки figure.
    """
    # Универсальный паттерн: находит квадратные скобки, внутри которых есть {fig...}
    pattern = r'!\[(.*?)\]\((.*?)\)'
    
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

    def replacer(match):
        alt_content = match.group(1).strip()
        img_url = match.group(2).strip()

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

        # --- ШАГ 3: ОПРЕДЕЛЕНИЕ КЛАССА И ОЧИСТКА ALT ЗА 1 ШАГ ---
        # Проверяем наличие ключа 'v' внутри скобок как отдельного элемента
        bracket_clean = inner_bracket.lower().replace(' ', '')
        if '|v' in bracket_clean or 'v|' in bracket_clean or bracket_clean == 'fig|v':
            target_class = "img-single-figure-portrait"
        else:
            target_class = "img-single-figure-landscape"

        # Начисто вырезаем служебные маркеры fig и v из внутренней части, чтобы получить скрытый alt
        clean_alt = re.sub(r'\b(fig|v)\b', '', inner_bracket)
        clean_alt = re.sub(r'[\s|]+', ' ', clean_alt).strip()

        # --- ШАГ 4: РАЗБОР ЖИВОГО ТЕКСТА ДЛЯ ПОДПИСИ ---
        outside_text = outside_content if outside_content else ""

        # --- ШАГ 5: ВЫВОД ИСПРАВЛЕННЫХ ДАННЫХ В ЛОГ-СИСТЕМУ ---
        print("\n" + "="*70)
        print("[FIG-LANDSCAPE-LOG] Найдена целевая ссылка на обработку:")
        print(f"  • Исходная строка: {match.group(0)}")
        print(f"  • Выбранный класс:       '{target_class}'")
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
            f'        <img class="{target_class}" alt="{clean_alt}" src="{transparent_pixel}" data-src="{img_url}">'
            f'{figcaption_html}\n'
            f'    </figure>\n'
            f'</div>'
        )

        print("[FIG-LANDSCAPE-LOG] Успешная трансформация в HTML:")
        print(html_output)
        print("="*70)

        return html_output

    return re.sub(pattern, replacer, markdown_content)
