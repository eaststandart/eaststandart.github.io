---
layout: default
title: Журнал проекта
description: Журнал, дневник, блог и прочие записи
permalink: /journal/
emoji: "✍🏻"
---

<div class="updates-feed">
  <ul id="journal-updates-list" style="list-style: none; padding: 0;">
    {% include news-loop.liquid type="news" folder="journal" %}
  </ul>
</div>

{% include pagination.liquid list_id="journal-updates-list" controls_id="journal-pagination" per_page=10 pinned_url="" %}
