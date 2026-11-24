#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_discussion_83.py
@about   Форматтер комментариев для GitHub Discussion #83.
@purpose Формирует заголовок, основной текст, отдельные фото- и видеоблоки и подвал комментария на основе Markdown и метаданных Front Matter.
@author  TechLab
@version 1.0.0
"""

import logging
import re
from datetime import datetime


logger = logging.getLogger(__name__)

MEDIA_HEADINGS = {
    "## 📸 Фотоматериалы": "photo",
    "## 🎥 Видеоматериалы": "video",
}
PHOTO_DEFAULT_TITLE = "📸 Фото-моменты"
VIDEO_DEFAULT_TITLE = "🎥 Видео-моменты"


class Discussion83FormatError(Exception):
    """Ошибка подготовки Markdown для Discussion #83."""


def _heading_level(line):
    match = re.match(r"^(#{1,6})\s+", line.strip())
    return len(match.group(1)) if match else None


def _extract_section(lines, heading, start=0, end=None):
    """Возвращает содержимое H3-раздела до следующего заголовка того же или более высокого уровня."""
    if end is None:
        end = len(lines)

    for index in range(start, end):
        if lines[index].strip() == heading:
            section_end = end
            for next_index in range(index + 1, end):
                level = _heading_level(lines[next_index])
                if level is not None and level <= 3:
                    section_end = next_index
                    break
            return "\n".join(lines[index + 1:section_end]).strip(), index, section_end

    return "", -1, -1


def _extract_media_blocks(lines):
    """Извлекает медиаблоки в исходном порядке манифеста."""
    blocks = []
    index = 0

    while index < len(lines):
        heading = lines[index].strip()
        if heading not in MEDIA_HEADINGS:
            index += 1
            continue

        end = index + 1
        while end < len(lines):
            if _heading_level(lines[end]) == 2:
                break
            end += 1

        blocks.append({
            "type": MEDIA_HEADINGS[heading],
            "lines": lines[index + 1:end],
        })
        index = end

    return blocks


def _extract_block_field(lines, heading):
    """Извлекает одно поле медиаблока между соседними H3-заголовками."""
    return _extract_section(lines, heading)[0]


def _extract_media_links(content, media_type):
    """Извлекает уже загруженные GitHub URL из Markdown-ссылок."""
    if media_type == "photo":
        pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    else:
        pattern = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")

    return [
        {"alt": match.group(1), "url": match.group(2).strip()}
        for match in pattern.finditer(content)
    ]


def _format_date(value):
    """Преобразует дату Front Matter в ДД.ММ.ГГГГ."""
    if value is None or not str(value).strip():
        raise Discussion83FormatError("В Front Matter отсутствует дата публикации.")

    raw_date = str(value).strip()
    try:
        parsed = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = datetime.strptime(raw_date[:10], "%Y-%m-%d")
        except ValueError as error:
            raise Discussion83FormatError(
                f"Некорректная дата публикации в Front Matter: {raw_date}"
            ) from error

    return parsed.strftime("%d.%m.%Y")


def _format_teacher(teacher):
    """Формирует подпись преподавателя из единственного поля teacher."""
    value = str(teacher or "eaststandart").strip().lstrip("@")
    if not value:
        value = "eaststandart"

    # Для аккаунта клуба показываем имя и логин обычным текстом.
    if value.casefold() in {"techlab", "eaststandart"}:
        return "TechLab @eaststandart"

    return f"@{value}"


def _format_photo_block(title, description, media_content):
    photos = _extract_media_links(media_content, "photo")
    parts = [f"### {title}"]

    if description:
        parts.extend(["", description])

    if photos:
        gallery = ["<div>"]
        for photo in photos:
            url = photo["url"]
            gallery.extend([
                f'<a href="{url}">',
                f'  <img width="371" height="209" alt="" src="{url}" />',
                "</a>",
            ])
        gallery.append("</div>")
        parts.extend(["", "\n".join(gallery)])

    return "\n".join(parts)


def _format_video_block(title, description, media_content):
    videos = _extract_media_links(media_content, "video")
    parts = [f"### {title}"]

    if description:
        parts.extend(["", description])

    if videos:
        video_lines = [
            f'[{video["alt"]}]({video["url"]})'
            for video in videos
        ]
        details = [
            "<details>",
            " <summary>Смотреть видео-материалы 👀</summary>",
            "&thinsp;",
            "",
            '<div>',
            "",
            "\n\n".join(video_lines),
            "",
            "</div>",
            "</details>",
        ]
        parts.extend(["", "\n".join(details)])

    return "\n".join(parts)


def format_comment(markdown: str, metadata=None) -> str:
    """Формирует готовый комментарий для GitHub Discussion #83."""
    if not isinstance(markdown, str):
        raise Discussion83FormatError("В форматтер передано некорректное Markdown-тело.")
    if not isinstance(metadata, dict):
        raise Discussion83FormatError("Форматтеру не переданы метаданные Front Matter.")

    lines = markdown.splitlines()
    date_text = _format_date(metadata.get("date"))

    title, _, _ = _extract_section(lines, "### Заголовок комментария")
    if not title:
        title = str(metadata.get("title") or "").strip()
    if not title:
        title = "В объективе клуба"

    main_text, _, _ = _extract_section(lines, "### Основной текст")
    footer, _, _ = _extract_section(lines, "### Подвал комментария")

    result = [f"## {date_text} · {title}"]
    if main_text:
        result.extend(["", main_text])

    for block in _extract_media_blocks(lines):
        block_lines = block["lines"]
        block_title = _extract_block_field(block_lines, "### Заголовок блока")
        description = _extract_block_field(block_lines, "### Описание блока")
        media_content = _extract_block_field(block_lines, "### Медиафайлы")

        if block["type"] == "photo":
            heading = block_title or PHOTO_DEFAULT_TITLE
            if not heading.lstrip().startswith("📸"):
                heading = f"📸 {heading}"
            result.extend(["", _format_photo_block(heading, description, media_content)])
        else:
            heading = block_title or VIDEO_DEFAULT_TITLE
            if not heading.lstrip().startswith("🎥"):
                heading = f"🎥 {heading}"
            result.extend(["", _format_video_block(heading, description, media_content)])

    if footer:
        result.extend(["", footer])
    else:
        teacher = _format_teacher(metadata.get("teacher"))
        result.extend([
            "",
            "🎬 **В кадре:** Юные инженеры",
            f"👨‍🏫 **Преподаватель:** {teacher}",
            "🏢 **Место:** Детско-юношеский инженерный клуб, г. Владивосток",
            "🌐 **Источник:** [Творческая лаборатория познавательного развития](https://eaststandart.github.io/)",
        ])

    formatted = "\n".join(result).strip()
    logger.info(
        "Discussion #83: сформировано медиаблоков=%d; символов=%d.",
        len(_extract_media_blocks(lines)),
        len(formatted),
    )
    return formatted
