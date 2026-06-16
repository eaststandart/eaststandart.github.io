---
layout: page
title: Медиа-материалы проекта
permalink: /media-posts-page/
---

{% comment %} 
Вычисляем, какой проект запрошен, проверяя URL-параметры сборщика
{% endcomment %}
{% assign current_project = page.url | split: "project=" | last | split: "&" | first %}

{% comment %} 
Вызываем твой медиа-лист и жестко передаем ему имя требуемого проекта
{% endcomment %}
{% include media-archive.liquid category="media" project_slug=current_project %}
