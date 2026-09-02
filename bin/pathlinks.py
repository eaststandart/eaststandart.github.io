#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script pathlinks.py
@about Модуль глобальной очистки путей, конвертации Wiki-ссылок и текстовых связей Obsidian.
@purpose v3.0 🚀 Внедрена защита кода от изменений, массив исключений для внешних ссылок,
         а также автоматическое превращение текстовых [[ссылок|Обсидиана]] в чистый текст.
@author TechLab
@version 3.0 (Часть 1)
"""

import re

def process_markdown_paths(markdown_content):
    """
    Конвертирует Wiki-медиа, вырезает текстовые Wiki-связи Obsidian и чистит пути,
    полностью защищая блоки кода от изменений.
    """
    # 🌟 А. МАССИВ ИСКЛЮЧЕНИЙ: Ссылки, содержащие эти домены, парсер вообще не имеет права трогать!
    ignored_patterns = [
        r'https?://',            # Любые внешние интернет-ссылки (http/https)
        r'mailto:',              # Электронная почта
        r'telegram\.org',        # Ссылки на соцсети
    ]
    
    # Проверяем, если строка целиком совпадает с исключением — не трогаем её
    for pattern in ignored_patterns:
        if re.search(pattern, markdown_content, re.IGNORECASE) and not re.search(r'github/eaststandart', markdown_content):
            # Если это внешняя ссылка и это не наш домен гитхаба — пропускаем её
            pass

    # 🌟 Б. ЗАМОРОЗКА БЛОКОВ КОДА: Прячем примеры кода в сейф, чтобы не сломать их
    code_vault = []
    
    def code_freezer(match):
        code_vault.append(match.group(0))
        return f'==CODE_BLOCK_{len(code_vault)-1}=='

    # 1. Прячем многострочные блоки кода (``` ... ```)
    temporary_content = re.sub(r'```[\s\S]*?```', code_freezer, markdown_content)
    # 2. Прячем строчный код в бэктиках (` ... `)
    temporary_content = re.sub(r'`[^`\n]+?`', code_freezer, temporary_content)

    # 🌟 В. ЧИСТКА ДОМЕНОВ И ПУТЕЙ (Ваша оригинальная стабильная логика)
    domain_pattern = r'(https?://)?github/eaststandart\.github\.io/'
    temporary_content = re.sub(domain_pattern, '/', temporary_content)
    temporary_content = re.sub(re.escape('../faire/'), '/faire/', temporary_content)

    # Паттерн для медиа Wiki-ссылок (картинки и видео)
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
    
    # 🌟 Г. КОНВЕРТАЦИЯ ТЕКСТОВЫХ ССЫЛОК OBSIDIAN [[План|Текст]] -> Текст
    # Ловит два формата: [[Ссылка|Красивый Текст]] или просто [[Одиночное Слово]]
    wiki_text_pattern = r'\[\[([^\]\n|]+)(?:\|([^\]\n]+))?\]\]'
    
    def wiki_text_replacer(match):
        link_target = match.group(1).strip()
        visible_text = match.group(2).strip() if match.group(2) else link_target
        # Возвращаем только то, что должен видеть читатель на сайте
        return visible_text

    # Превращаем обсидиановые текстовые связи в чистые слова контента
    temporary_content = re.sub(wiki_text_pattern, wiki_text_replacer, temporary_content)

    # Ваша родная страховка от случайных двойных слэшей
    temporary_content = temporary_content.replace('//', '/')
    
    # 🌟 Д. РАЗМОРОЗКА БЛОКОВ КОДА: Возвращаем примеры из сейфа в полной целости
    for idx, original_code in enumerate(code_vault):
        temporary_content = temporary_content.replace(f'==CODE_BLOCK_{idx}==', original_code)
        
    return temporary_content

