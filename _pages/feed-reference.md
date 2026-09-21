---
layout: feed
title: Справочник
description: Лента постов справочных материалов.
permalink: /reference/
per_page: 10
emoji: ""
---

{% comment %} 
СТРАНИЦА: ГЛАВНЫЙ ЖУРНАЛ САЙТА (\_pages/reference.md)
Назначение: Выводит хронологическую ленту всех записей категорииreference.
{% endcomment %}

{% assign limit = page.per_page | default: 10 %}
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit basket="reference" %}
