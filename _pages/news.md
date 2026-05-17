---
layout: default
title: Что нового?
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    <!-- УНИФИЦИРОВАННЫЙ ВЫЗОВ ЦИКЛА ДЛЯ СТРАНИЦЫ АРХИВА -->
    {% include news-loop.liquid type="news" %}
  </ul>
</div>

<!-- ВЫЗОВ УНИВЕРСАЛЬНОЙ ПАГИНАЦИИ -->
{% include pagination.liquid list_id="live-updates-list" controls_id="news-pagination" per_page=10 pinned_url="" %}
