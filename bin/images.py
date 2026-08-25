#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module images
@about Модуль предобработки изображений для Obsidian -> Jekyll.
@purpose Разбирает Obsidian-синтаксис строго по спецификации [Зона 1 | Зона 2].
         Выделяет свойства размеров, вычищает мусор Obsidian и формирует alt.
"""

import re

def process_markdown_images(markdown_content):
    """
    Ищет маркдаун-картинки и превращает их в HTML-блоки с классами и свойствами.
    """
    # Регулярное выражение ловит стандартный маркдаун: ![параметры](ссылка)
    pattern = r'!\[(.*?)\]\((.*?)\)'
    
    def replacer(match):
        alt_text = match.group(1).strip()
        img_url = match.group(2).strip()
        
        # Если внутри скобок совсем пусто (вариант `![](url)`) — отдаем чистый базовый тег
        if not alt_text:
            return f'<img alt="" src="{img_url}">'
            
        # Разбиваем параметры по палочке, убирая пустые пробелы
        parts = [p.strip() for p in alt_text.split('|')]
        
        # Фильтруем пустые строки, которые могли возникнуть из-за конструкций вида `![|400]`
        parts = [p for p in parts if p]
        
        # Если после фильтрации всё равно пусто — отдаем базовый тег
        if not parts:
            return f'<img alt="" src="{img_url}">'
            
        classes = []
        custom_attrs = []
        is_centered = False
        
        # --------------------------------------------------------
        # ШАГ 1: РАЗБОР ЗОНЫ 1 (На первом месте до палочки)
        # --------------------------------------------------------
        first_part = parts[0]
        
        if first_part.lower() == 'v':
            classes.append('img-v')
            parts.pop(0) # Удаляем маркер, чтобы не попал в alt
            
        elif first_part.lower() == 'center':
            classes.append('img-center')
            is_centered = True
            parts.pop(0) # Удаляем маркер, чтобы не попал в alt
            
        # Проверяем точечное совпадение с физическим разрешением (цифры + x + цифры)
        elif re.match(r'^\d+[xх]\d+$', first_part, re.IGNORECASE):
            # Разрезаем по букве X (учитываем латинскую x и русскую х)
            dimensions = re.split(r'[xх]', first_part, flags=re.IGNORECASE)
            width, height = dimensions[0], dimensions[1]
            
            # Добавляем родные HTML-свойства и класс индивидуального размера
            custom_attrs.append(f'width="{width}"')
            custom_attrs.append(f'height="{height}"')
            classes.append('img-custom')
            parts.pop(0) # Удаляем технический маркер, чтобы не попал в alt
            
        # --------------------------------------------------------
        # ШАГ 2: РАЗБОР ЗОНЫ 2 (Проверка хвоста на размер Obsidian)
        # --------------------------------------------------------
        if parts:
            last_part = parts[-1]
            # Если самый последний элемент — чистая одиночная цифра (размер вроде 400)
            if re.match(r'^\d+$', last_part):
                parts.pop() # Безвозвратно удаляем её из кода сайта
                
        # --------------------------------------------------------
        # ШАГ 3: СБОРКА СЕРЕДИНЫ (Чистый человеческий SEO-текст)
        # --------------------------------------------------------
        clean_alt = " | ".join(parts) if parts else ""
        
        # Формируем итоговые строки классов и кастомных атрибутов
        class_str = f' class="{" ".join(classes)}"' if classes else ''
        attr_str = f' {" ".join(custom_attrs)}' if custom_attrs else ''
        
        # Генерируем финальный HTML-тег картинки
        img_html = f'<img{class_str}{attr_str} alt="{clean_alt}" src="{img_url}">'
        
        # Если был маркер center — оборачиваем в готовый родительский класс абзаца
        if is_centered:
            return f'<p class="p-center">{img_html}</p>'
            
        return img_html

    return re.sub(pattern, replacer, markdown_content)
