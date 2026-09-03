#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script fig_landscape.py
@about Изолированный тестовый модуль для обработки одиночных горизонтальных журнальных блоков.
@purpose Находит новые ссылки вида ![{fig|alt}|text] с поддержкой обсидиановых хвостов,
         выводит подробные логи трансформации и собирает утвержденную HTML-структуру.
@author TechLab
@version 1.0
"""

import re

def process_single_figure_landscape(markdown_content):
    """
    Ищет маркдаун-ссылки журнального типа и преобразует их в HTML-блоки.
    Полностью изолирован от старого кода.
    """
    # 🎯 УЛЬТИМАТИВНЫЙ ПАТТЕРН:
    # 1. !\[\{fig — Ищет жесткое начало ![{fig
    # 2. ([^}]*) — Группа 1: Всё, что внутри скобок после fig (например, '|скрытый alt')
    # 3. \}(?:\|([^\]]*))? — Находит } и опционально захватывает Группу 2: Всё, что после скобки до конца знака ]
    # 4. \(([^)]*)\) — Группа 3: Вытаскивает чистый URL из круглых скобок
    pattern = r'!\[\{fig([^}]*)\}(?:\|([^\]]*))?\]\(([^)]*)\)'
    
    transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

    def replacer(match):
        inner_content = match.group(1).strip()  # Служебная часть внутри {}
        outside_text = match.group(2).strip() if match.group(2) else ""   # Пользовательский текст
        img_url = match.group(3).strip()

        # --- ШАГ 1: БЕЗОПАСНАЯ ОЧИСТКА ОБСИДИАНОВЫХ ХВОСТОВ ШИРИНЫ (|400) ---
        # Если в самом конце внешнего текста затесался хвост ширины, намертво стираем его
        outside_text = re.sub(r'\|\s*\d+\s*$', '', outside_text).strip()

        # --- ШАГ 2: РАЗБОР СКРЫТОГО SEO ALT-ТЕКСТА ---
        # Вытаскиваем alt text, если он передан внутри фигурных скобок через пайп
        clean_alt = ""
        if inner_content.startswith('|'):
            clean_alt = inner_content[1:].strip()

        # --- ШАГ 3: ФИКСАЦИЯ ДАННЫХ В ЛОГ-СИСТЕМУ ---
        print("\n" + "="*70)
        print("[FIG-LANDSCAPE-LOG] Найдена целевая ссылка на обработку:")
        print(f"  • Исходная строка: {match.group(0)}")
        print(f"  • Служебный раздел {{fig}}: '{inner_content}' ➡️ Скрытый alt: '{clean_alt}'")
        print(f"  • Текст для подписи:      '{outside_text}'")
        print(f"  • Путь к медиафайлу:      '{img_url}'")
        print("-"*70)

        # --- ШАГ 4: СБОРКА СЕМАНТИЧЕСКОГО HTML ---
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


# ==========================================================================
# БЛОК ЛОКАЛЬНОГО ТЕСТИРОВАНИЯ (ЭМУЛЯЦИЯ СТАТЬИ ИЗ OBSIDIAN)
# ==========================================================================
if __name__ == '__main__':
    # Входной тестовый текст с тремя разными вариантами написания и хвостами ширины
    test_markdown = """
# Тестовая статья Obsidian

Привет! Вот пример чистой журнальной горизонтальной картинки без текстов:
![{fig}](/assets/photo1.webp)

А вот вариант со скрытым SEO-текстом и текстом для людей, плюс хвост ширины Обсидиана 400:
![{fig|Скрытый SEO-текст}|Живая подпись для людей|400](/assets/photo2.jpg)

И еще один вариант без SEO, но с подписью читателям и хвостом 300:
![{fig}|Просто красивая подпись кадра|300](/assets/photo3.png)

Конец теста.
    """

    print("--- ЗАПУСК ИЗОЛИРОВАННОГО ТЕСТА МОДУЛЯ ---")
    final_html = process_single_figure_landscape(test_markdown)
