---
layout: default
title: Журнал проекта
permalink: /journal/
emoji: "✍🏻"
---

Журнал, дневник, блог и прочие записи

<div class="updates-feed">
  <ul id="journal-updates-list" style="list-style: none; padding: 0;">
    {% comment %} 
      ВЫЗЫВАЕМ НАШ УНИВЕРСАЛЬНЫЙ ЦИКЛ:
      type="news" — даст красивый архивный стиль с линиями и блёклыми датами.
      folder="journal" — БЕЗОШИБОЧНО отсечет всё лишнее и выведет только посты из журнала.
    {% endcomment %}
    {% include news-loop.liquid type="news" folder="journal" %}
  </ul>
</div>

<!-- 
  ПОДКЛЮЧАЕМ НАШУ УНИВЕРСАЛЬНУЮ ПАГИНАЦИЮ:
  Задаем уникальные ID (journal-updates-list и journal-pagination), 
  чтобы кнопки на этой странице работали изолированно и не конфликтовали с другими разделами.
-->
{% include pagination.liquid list_id="journal-updates-list" controls_id="journal-pagination" per_page=10 pinned_url="" %}

<!--
---
layout: default
title: Журнал проекта
permalink: /journal/
emoji: "✍🏻"
---
Журнал, дневник, блог и прочие записи
{% include media-archive.liquid category="journal" %}
-->