#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Одноразовый тест короткого имени GitHub Discussion Attachment."""

import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

UPLOAD_URL = "https://uploads.github.com/user-attachments/assets"
REPOSITORY_ID = "1218168867"
SHORT_NAME = "test-video.webm"
TIMEOUT = 120


def main():
    folder = Path(__file__).resolve().parent
    candidates = [
        path for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() == ".webm"
        and path.name != SHORT_NAME
    ]

    if len(candidates) != 1:
        print("Положи в эту папку ровно один исходный файл .webm.")
        print(f"Найдено файлов: {len(candidates)}")
        for path in candidates:
            print(f"  {path.name}")
        raise SystemExit(1)

    source = candidates[0]
    token = os.environ.get("MY_ADMIN_TOKEN")
    if not token:
        print("Не задана переменная окружения MY_ADMIN_TOKEN.")
        raise SystemExit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "video/webm",
        "User-Agent": "TechLab-Attachment-Name-Test",
    }
    params = {
        "name": SHORT_NAME,
        "content_type": "video/webm",
        "repository_id": REPOSITORY_ID,
    }

    print(f"Исходный файл: {source.name}")
    print(f"Имя при загрузке: {SHORT_NAME}")
    print("Отправляю файл в GitHub Attachments...")

    with requests.Session() as session, source.open("rb") as stream:
        response = session.post(
            UPLOAD_URL,
            params=params,
            headers=headers,
            data=stream,
            timeout=TIMEOUT,
        )

    if not response.ok:
        print(f"Ошибка GitHub HTTP {response.status_code}:")
        print(response.text[:2000])
        raise SystemExit(1)

    try:
        payload = response.json()
    except ValueError:
        print("GitHub вернул ответ не в формате JSON:")
        print(response.text[:2000])
        raise SystemExit(1)

    url = payload.get("url") or payload.get("href")
    if not isinstance(url, str) or urlparse(url).scheme != "https":
        print("В ответе GitHub отсутствует корректный HTTPS URL:")
        print(payload)
        raise SystemExit(1)

    print("\nЗагрузка завершена.")
    print(f"URL: {url}")
    print(f"Markdown для Discussion: [{SHORT_NAME}]({url})")
    print("\nВставь Markdown в тестовую Discussion и проверь имя в шапке плеера.")


if __name__ == "__main__":
    main()
