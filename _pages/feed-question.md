---
layout: feed
title: Вопросы проектов
description: Лента постов вопросов по выполненным проектам.
permalink: /question/
per_page: 10
emoji: "❓"
---

{% comment %} 
СТРАНИЦА: ГЛАВНЫЙ ЖУРНАЛ САЙТА (\_pages/question.md)
Назначение: Выводит хронологическую ленту всех записей категории question.
{% endcomment %}

{% assign limit = page.per_page | default: 10 %}
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit basket="question" %}
