#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script pathlinks.py
@about Модуль глобальной очистки путей, конвертации Wiki-ссылок и текстовых связей Obsidian.
@purpose v3.2 🚀 ИСПРАВЛЕНО: Ультимативный чистильщик путей. Автоматически переводит любые относительные 
         адреса картинок (faire, folder и т.д.) в абсолютный стандарт /.../ с жесткой защитой кода в бэктиках.
@author TechLab
@version 3.2 (Часть 1)
"""

import re

def process_markdown_paths(markdown_content):
    """
    Конвертирует Wiki-медиа, вырезает текстовые Wiki-связи Obsidian и чистит любые пути,
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

    # 🌟 Б. ЗАМОРОЗКА БЛОКОВ КОДА (Железный сейф - Выполняется ПЕРВЫМ!)
    code_vault = []
    
    def code_freezer(match):
        code_vault.append(match.group(0))
        return f'==CODE_BLOCK_{len(code_vault)-1}=='

    # 1. Прячем многострочный код (``` ... ```)
    temporary_content = re.sub(r'```[\s\S]*?```', code_freezer, markdown_content)
    # 2. Прячем строчный код в бэктиках (` ... `)
    temporary_content = re.sub(r'`[\s\S]*?`', code_freezer, temporary_content)

    # 🌟 В. УЛЬТИМАТИВНАЯ ЧИСТКА ЛЮБЫХ МАРКДАУН-ПУТЕЙ КАРТИНОК И ВИДЕО
    # Ваша родная зачистка домена гитхаба
    domain_pattern = r'(https?://)?github/eaststandart\.github\.io/'
    temporary_content = re.sub(domain_pattern, '/', temporary_content)

    # Паттерн находит любые стандартные маркдаун-ссылки ![](путь) в тексте статьи
    classic_media_pattern = r'!\[(.*?)\]\((.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))\)'
    
    def classic_path_cleaner(match):
        alt_text = match.group(1).strip()
        img_url = match.group(2).strip()
        
        # Снимем любые относительные двоеточия и точки из начала пути (../ или ./)
        img_url = re.sub(r'^[\s./]+', '', img_url)
        
        # Гарантируем, что путь теперь железно начинается с абсолютного слэша /
        if not img_url.startswith('/'):
            img_url = '/' + img_url
            
        return f'![{alt_text}]({img_url})'

    # На лету выравниваем пути всех классических картинок до единого абсолютного стандарта
    temporary_content = re.sub(classic_media_pattern, classic_path_cleaner, temporary_content, flags=re.IGNORECASE)

    # Паттерн для Wiki-ссылок Obsidian
    wiki_media_pattern = r'!\[\[(.*?\.(?:webp|jpg|jpeg|png|gif|svg|webm|mp4))(?:\|(.*?))?\]\]'

    # 3. Функция-заменитель для пересборки медиа-ссылок Wiki в классический вид
    def wiki_media_replacer(match):
        img_url = match.group(1).strip()
        alt_content = match.group(2).strip() if match.group(2) else ""
        
        # Срезаем точки, двоеточия и слэши из начала пути Wiki-ссылки
        img_url = re.sub(r'^[\s./]+', '', img_url)
        
        # Гарантируем, что путь железно начинается с одиночного абсолютного слэша /
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
