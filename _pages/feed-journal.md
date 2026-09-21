---
workflow: "Нужно ленты переименовать в feed-journal, но при этом чтобы эмодзи не пропали в ленте новостей на главной. И решить со свойством emoji_display N (скрывает эмодзи в самой ленте) - как его убрать, чтобы не прописывать руками (но возможность дописывать отдельному посту эмодзи - нужно оставить или добавить)."
layout: feed
title: Журнал
description: Лента постов журнальных записей по проектам.
permalink: /journal/
per_page: 10
emoji: "✍🏻"
---

{% comment %} 
СТРАНИЦА: ГЛАВНЫЙ ЖУРНАЛ САЙТА (\_pages/journal.md)
Назначение: Выводит хронологическую ленту всех записей категории journal.
{% endcomment %}

{% assign limit = page.per_page | default: 10 %}
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit basket="journal" %}
