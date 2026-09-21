---
layout: feed
title: Медиа-материалы
description: Лента постов с медиа материалами по выполненным проектам.
permalink: /media/
per_page: 10
emoji: "👀"
---

{% comment %} 
emoji: "👀📷🎬"
СТРАНИЦА: ГЛАВНЫЙ МЕДИА-АРХИВ САЙТА (\_pages/media.md)
Назначение: Выводит хронологическую ленту всех записей папки media в формате Журнала.
{% endcomment %}

{% assign limit = page.per_page | default: 10 %}
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit basket="media" %}