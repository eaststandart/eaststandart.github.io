#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@module  cb_discussion_44.py
@about   Форматтер комментариев для GitHub Discussion #44.
@purpose Формирует заголовок, основной текст, медиаблоки и универсальный подвал комментария.
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
DEFAULT_PLACE = "Детско-юношеский инженерный клуб, г. Владивосток"
DEFAULT_SOURCE = "[Творческая лаборатория познавательного развития](https://eaststandart.github.io/)"


class Discussion44FormatError(Exception):
    """Ошибка подготовки Markdown для Discussion #44."""


def _heading_level(line):
    match = re.match(r"^(#{1,6})\s+", line.strip())
    return len(match.group(1)) if match else None


def _extract_section(lines, heading, start=0, end=None):
    """Извлекает раздел до следующего заголовка того же или более высокого уровня."""
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
    """Извлекает фото- и видеоблоки в порядке манифеста."""
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

        blocks.append({"type": MEDIA_HEADINGS[heading], "lines": lines[index + 1:end]})
        index = end

    return blocks


def _extract_block_field(lines, heading):
    return _extract_section(lines, heading)[0]


def _extract_media_links(content, media_type):
    """Извлекает URL фото или видео после загрузки вложений."""
    if media_type == "photo":
        pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    else:
        pattern = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")

    return [
        {"alt": match.group(1), "url": match.group(2).strip()}
        for match in pattern.finditer(content)
    ]


def _format_date(value):
    if value is None or not str(value).strip():
        raise Discussion44FormatError("В Front Matter отсутствует дата публикации.")

    raw_date = str(value).strip()
    try:
        parsed = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = datetime.strptime(raw_date[:10], "%Y-%m-%d")
        except ValueError as error:
            raise Discussion44FormatError(
                f"Некорректная дата публикации в Front Matter: {raw_date}"
            ) from error

    return parsed.strftime("%d.%m.%Y")


def _format_teacher(teacher):
    """Формирует подпись преподавателя по правилам Discussion #83."""
    value = str(teacher or "eaststandart").strip().lstrip("@")
    if not value:
        value = "eaststandart"
    if value.casefold() in {"techlab", "eaststandart"}:
        return "TechLab @eaststandart"
    return f"@{value}"


def _format_media_title(value, media_type):
    """Пустой заголовок пропускает; специальное значение none включает заголовок по умолчанию."""
    value = str(value or "").strip()
    if not value:
        return ""

    if value.casefold() == "none":
        return PHOTO_DEFAULT_TITLE if media_type == "photo" else VIDEO_DEFAULT_TITLE

    prefix = "📸" if media_type == "photo" else "🎥"
    return value if value.startswith(prefix) else f"{prefix} {value}"


def _format_photo_block(title, description, media_content):
    photos = _extract_media_links(media_content, "photo")
    parts = []
    if title:
        parts.append(f"### {title}")
    if description:
        if parts:
            parts.append("")
        parts.append(description)

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
        if parts:
            parts.append("")
        parts.append("\n".join(gallery))

    return "\n".join(parts)


def _format_video_block(title, description, media_content):
    videos = _extract_media_links(media_content, "video")
    parts = []
    if title:
        parts.append(f"### {title}")
    if description:
        if parts:
            parts.append("")
        parts.append(description)

    if videos:
        video_lines = [f'[{video["alt"]}]({video["url"]})' for video in videos]
        details = [
            "<details>",
            " <summary>Смотреть видео-материалы 👀</summary>",
            "&thinsp;",
            "",
            "<div>",
            "",
            "\n\n".join(video_lines),
            "",
            "</div>",
            "</details>",
        ]
        if parts:
            parts.append("")
        parts.append("\n".join(details))

    return "\n".join(parts)


def _parse_footer(footer):
    """Извлекает переопределения автора, места и источника; остальные строки сохраняет."""
    values = {"author": None, "place": None, "source": None}
    labels = {
        "автор": "author",
        "место": "place",
        "источник": "source",
    }
    remaining = []

    for line in footer.splitlines():
        match = re.match(r"^\s*([^:]+)\s*:\s*(.*?)\s*$", line)
        key = match.group(1).strip().casefold() if match else ""
        if key in labels:
            values[labels[key]] = match.group(2).strip()
        else:
            remaining.append(line)

    return "\n".join(remaining).strip(), values


def format_comment(markdown: str, metadata=None) -> str:
    """Формирует готовый комментарий для GitHub Discussion #44."""
    if not isinstance(markdown, str):
        raise Discussion44FormatError("В форматтер передано некорректное Markdown-тело.")
    if not isinstance(metadata, dict):
        raise Discussion44FormatError("Форматтеру не переданы метаданные Front Matter.")

    lines = markdown.splitlines()
    date_text = _format_date(metadata.get("date"))

    title, _, _ = _extract_section(lines, "### Заголовок комментария")
    if not title:
        title = str(metadata.get("title") or "").strip()
    if not title:
        title = "[укажите наименование работы]"

    main_text, _, _ = _extract_section(lines, "### Основной текст")
    footer, _, _ = _extract_section(lines, "### Подвал комментария")
    extra_footer, footer_values = _parse_footer(footer)

    result = [f"## {date_text} · {title}"]
    if main_text:
        result.extend(["", main_text])

    media_blocks = _extract_media_blocks(lines)
    for block in media_blocks:
        block_lines = block["lines"]
        block_title = _extract_block_field(block_lines, "### Заголовок блока")
        description = _extract_block_field(block_lines, "### Описание блока")
        media_content = _extract_block_field(block_lines, "### Медиафайлы")
        heading = _format_media_title(block_title, block["type"])

        if block["type"] == "photo":
            formatted_block = _format_photo_block(heading, description, media_content)
        else:
            formatted_block = _format_video_block(heading, description, media_content)

        if formatted_block:
            result.extend(["", formatted_block])

    if extra_footer:
        result.extend(["", extra_footer])

    author = footer_values["author"] or ""
    place = footer_values["place"] or DEFAULT_PLACE
    source = footer_values["source"] or DEFAULT_SOURCE
    teacher = _format_teacher(metadata.get("teacher"))

    result.extend([
        "",
        f"👨🏻‍🎓 **Автор:**{(' ' + author) if author else ''}",
        f"👨‍🏫 **Преподаватель:** {teacher}",
        f"🏢 **Место:** {place}",
        f"🌐 **Источник:** {source}",
    ])

    formatted = "\n".join(result).strip()
    logger.info(
        "Discussion #44: сформировано медиаблоков=%d; символов=%d.",
        len(media_blocks),
        len(formatted),
    )
    return formatted
