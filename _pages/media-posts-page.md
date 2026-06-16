---
layout: page
title: Медиа-материалы проекта
permalink: /media-posts-page/
---

{% comment %} 
ПОДКЛЮЧАЕМ ГОТОВЫЙ МОНОЛИТНЫЙ МОДУЛЬ ARCHIVE С ФИЛЬТРАЦИЕЙ
Параметр category указывает скрипту собирать записи строго из папки media.
{% endcomment %}
{% include media-archive.liquid category="media" %}
