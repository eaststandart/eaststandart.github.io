---
layout: feed
title: Посты
description: Лента постов без типа (дополнительные и справочные посты).
permalink: /post/
per_page: 10
emoji: "📝"
---

{% comment %} 
СТРАНИЦА: ГЛАВНЫЙ ЖУРНАЛ САЙТА (\_pages/post.md)
Назначение: Выводит хронологическую ленту всех записей категории post.
{% endcomment %}

{% assign limit = page.per_page | default: 10 %}
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit basket="post" %}