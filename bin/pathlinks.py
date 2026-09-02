#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script pathlinks.py
@about Модуль глобальной очистки путей, конвертации Wiki-ссылок и текстовых связей Obsidian.
@purpose v3.1 🚀 ИСПРАВЛЕНО: Усилена защита одиночных бэктиков от ложного срабатывания чистильщика.
@author TechLab
@version 3.1 (Часть 1)
"""

import re

def process_markdown_paths(markdown_content):
    """
    Конвертирует Wiki-медиа, вырезает текстовые Wiki-связи Obsidian и чистит пути,
    полностью защищая блоки кода от изменений.
    """
    # А. МАССИВ ИСКЛЮЧЕНИЙ
    ignored_patterns = [
        r'https?://',            
        r'mailto:',              
        r'telegram\.org',        
    ]
    
    for pattern in ignored_patterns:
        if re.search(pattern, markdown_content, re.IGNORECASE) and not re.search(r'github/eaststandart', markdown_content):
            pass

    # Б. ЗАМОРОЗКА БЛОКОВ КОДА (Сейф)
    code_vault = []
    
    def code_freezer(match):
        code_vault.append(match.group(0))
        return f'==CODE_BLOCK_{len(code_vault)-1}=='

    # 1. Замораживаем многострочный код (``` ... ```)
    temporary_content = re.sub(r'```[\s\S]*?```', code_freezer, markdown_content)
    
    # 🔥 ИСПРАВЛЕНО: Бронебойная регулярка для строчного кода (` ... `). 
    # Она гарантированно поглощает любые спецсимволы и ссылки внутри кавычек, не пропуская их наружу!
    temporary_content = re.sub(r'`[\s\S]*?`', code_freezer, temporary_content)

    # В. ЧИСТКА ДОМЕНОВ И ПУТЕЙ
    domain_pattern = r'(https?://)?github/eaststandart\.github\.io/'
    temporary_content = re.sub(domain_pattern, '/', temporary_content)
    temporary_content = re.sub(re.escape('../faire/'), '/faire/', temporary_content)

    wiki_media_pattern = r'!\[\[(.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))(?:\|(.*?))?\]\]'

    # 3. Функция-заменитель для пересборки медиа-ссылок Wiki в классический вид
    def wiki_media_replacer(match):
        img_url = match.group(1).strip()
        alt_content = match.group(2).strip() if match.group(2) else ""
        
        if not img_url.startswith('/'):
            img_url = '/' + img_url
            
        return f'![{alt_content}]({img_url})'

    # Запускаем конвертацию всех МЕДИА Wiki-ссылок в тексте
    temporary_content = re.sub(wiki_media_pattern, wiki_media_replacer, temporary_content, flags=re.IGNORECASE)
    
    # Г. КОНВЕРТАЦИЯ ТЕКСТОВЫХ ССЫЛОК OBSIDIAN [[План|Текст]] -> Текст
    wiki_text_pattern = r'\[\[([^\]\n|]+)(?:\|([^\]\n]+))?\]\]'
    
    def wiki_text_replacer(match):
        link_target = match.group(1).strip()
        visible_text = match.group(2).strip() if match.group(2) else link_target
        return visible_text

    # Превращаем обсидиановые текстовые связи в чистые слова контента
    temporary_content = re.sub(wiki_text_pattern, wiki_text_replacer, temporary_content)

    # Ваша родная страховка от случайных двойных слэшей
    temporary_content = temporary_content.replace('//', '/')
    
    # 🌟 Д. РАЗМОРОЗКА БЛОКОВ КОДА: Возвращаем примеры из сейфа в полной целости
    for idx, original_code in enumerate(code_vault):
        temporary_content = temporary_content.replace(f'==CODE_BLOCK_{idx}==', original_code)
        
    return temporary_content
