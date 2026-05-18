---
layout: default
title: Журнал проекта
description: Журнал, дневник, блог и прочие записи
permalink: /journal/
emoji: "✍🏻"
custom_css: "/assets/css/pagination.css"
---
{% comment %} 
СТРАНИЦА: ГЛАВНЫЙ БОРТОВОЙ ЖУРНАЛ САЙТА (\_pages/journal.md)
Назначение: Выводит хронологическую ленту всех записей категории journal.
ВНИМАНИЕ: Идентификаторы приведены к единому стандарту posts-list для активации стилей.
{% endcomment %}

<div class="updates-feed">
  <ul id="posts-list" style="list-style: none; padding: 0;">
    {% include news-loop.liquid type="news" folder="journal" %}
  </ul>
</div>

{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=10 pinned_url="" %}
