---
about: Шаблон ленты новостей.
purpose: Автоматически строит каркас ленты и выводит кнопки пагинации.
layout: default
---
{{ content }}

<!-- ТЕХНИЧЕСКИЙ ШАБЛОН: ЛЕНТЫ НОВОСТЕЙ И ЖУРНАЛА -->
<div class="news-feed">
  <ul id="posts-list" style="list-style: none; padding: 0;">
    {% include feed.liquid type="feed" %}
  </ul>
</div>

{% comment %}
{% assign limit = page.per_page | default: 10 %} 
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit basket=current_section %}
{% endcomment %} 
