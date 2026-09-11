---
layout: page
title: Все записи журнала проекта
permalink: /journal-posts-page/
mathjax: true
---

{% comment %} 
ПОДКЛЮЧАЕМ ГОТОВЫЙ МОНОЛИТНЫЙ МОДУЛЬ ARCHIVE С ФИЛЬТРАЦИЕЙ
Параметр category указывает скрипту собирать записи строго из папки journal.
{% endcomment %}
{% include media-archive.liquid category="journal" %}
