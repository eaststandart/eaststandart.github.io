---
layout: news
title: Журнал проекта
description: Журнал, дневник, блог и прочие записи
permalink: /journal/
folder: journal
emoji: "🔥"
---

<div class="updates-feed">
  <ul id="posts-list" style="list-style: none; padding: 0;">
    <!-- ВРЕМЕННО: Переключили на изолированный дебаг-цикл -->
    {% include journal-debug-loop.liquid type="news" folder=page.folder %}
  </ul>
</div>
