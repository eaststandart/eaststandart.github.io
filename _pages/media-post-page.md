---
layout: page
title: Медиа-материалы проекта
permalink: /media-post-page/
---

{% comment %} 
УМНЫЙ СКРИПТ: Вытаскиваем имя проекта из адреса ссылки (параметра ?project=)
прямо на этапе генерации страницы, чтобы Liquid знал, что фильтровать.
{% endcomment %}
{% assign current_project = page.url | split: "project=" | last | split: "&" | first %}

{% comment %} 
Передаем имя проекта внутрь нашего архивного модуля
{% endcomment %}
{% include media-archive.liquid category="media" project_slug=current_project %}
