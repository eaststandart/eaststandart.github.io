---
layout: feed
title: Новости уголка конструктора
permalink: /news/
per_page: 10
---

{% comment %} 
СТРАНИЦА: ОБЩИЙ АРХИВ НОВОСТЕЙ (\_pages/news.md)
Назначение: Указывает шаблону news.md выводить ВСЕ новости по 10 штук.
{% endcomment %}

{% assign limit = page.per_page | default: 10 %}
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit basket="news" %}