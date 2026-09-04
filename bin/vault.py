#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module vault
@about Автономный сквозной точечный сейф исключений для защиты примеров кода.
@purpose Сканирует текст, изолирует опасные маркеры внутри кодовых блоков/комментариев
         и возвращает их обратно на выходе из конвейера.
@author TechLab
@version 1.0
"""

import re

def global_freeze_content(markdown_content, file_rel_path):
    """
    Сканирует кодовые блоки и комментарии, точечно замораживая только те элементы,
    внутри которых обнаружен маркер fig или медиа-расширения.
    """
    global_vault = []
    
    def freezer(match, block_type):
        raw_text = match.group(0)
        
        # Строгий точечный фильтр примеров кода и комментариев
        has_fig = 'fig' in raw_text.lower()
        has_media = re.search(r'\.(webp|jpg|jpeg|png|gif|svg|webm|mp4)\b', raw_text, re.IGNORECASE)
        
        if not (has_fig or has_media):
            return raw_text

        global_vault.append(raw_text)
        
        preview = raw_text.replace('\n', ' ')
        if len(preview) > 60:
            preview = preview[:57] + "..."
            
        print(f"📦 [VAULT-FREEZE] Изолирован {block_type}: `{preview}` | Файл: {file_rel_path}")
        return f'==GLOBAL_VAULT_BLOCK_{len(global_vault)-1}=='

    # Последовательная точечная заморозка зон безопасности
    temporary_content = re.sub(r'{%\s*comment\s*%}[\s\S]*?{%\s*endcomment\s*%}', lambda m: freezer(m, "Liquid-коммент  "), markdown_content)
    temporary_content = re.sub(r'<!--[\s\S]*?-->', lambda m: freezer(m, "HTML-коммент    "), temporary_content)
    temporary_content = re.sub(r'```[\s\S]*?```', lambda m: freezer(m, "блок кода (multi)"), temporary_content)
    temporary_content = re.sub(r'`{1,3}[^`\n]+?`{1,3}', lambda m: freezer(m, "строчный код    "), temporary_content)

    return temporary_content, global_vault

def global_unfreeze_content(markdown_content, global_vault, file_rel_path):
    """Возвращает все изолированные точечные блоки из глобального сейфа на свои места."""
    temporary_content = markdown_content
    for idx in reversed(range(len(global_vault))):
        marker = f'==GLOBAL_VAULT_BLOCK_{idx}=='
        
        if marker in temporary_content:
            print(f"🔓 [VAULT-UNFREEZE] Восстановлен маркер {marker} | Файл: {file_rel_path}")
            temporary_content = temporary_content.replace(marker, global_vault[idx])
            
    return temporary_content