#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@script pathlinks.py
@about Модуль глобальной очистки путей Obsidian для Jekyll.
@purpose Находит любые упоминания домена github/eaststandart.github.io/ 
         и превращает их в чистые относительные ссылки вида /faire/...
"""

import re

def process_markdown_paths(markdown_content):
    """
    Вырезает домен гитхаба из любых ссылок и путей в маркдауне.
    """
    # Регулярное выражение находит домен (с протоколом http/https или без него)
    domain_pattern = r'(https?://)?github/eaststandart\.github\.io/'
    
    # Заменяем домен на одиночный слэш, делая ссылку относительной от корня сайта
    cleaned_content = re.sub(domain_pattern, '/', markdown_content)
    
    # Страховка от двойных слэшей, если в Obsidian было написано /github/...
    cleaned_content = cleaned_content.replace('//', '/')
    
    return cleaned_content
