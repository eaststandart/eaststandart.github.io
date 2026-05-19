---
layout: default
---
{% comment %} 
ТЕХНИЧЕСКИЙ ШАБЛОН: ЛЕНТЫ НОВОСТЕЙ (\_layouts/news.html)
Назначение: Автоматически строит каркас ленты и выводит кнопки пагинации.
{% endcomment %}

{{ content }}

<!-- ТЕХНИЧЕСКИЙ ШАБЛОН: ЛЕНТЫ НОВОСТЕЙ И ЖУРНАЛА -->
<div class="news-feed">
  <ul id="posts-list" style="list-style: none; padding: 0;">
    {% include news-loop.liquid type="news" folder=page.folder %}
  </ul>
</div>

{% assign limit = page.per_page | default: 10 %}
{% assign emoji_flag = page.emoji_display | default: "Y" %}
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit pinned_url=page.pinned_url emoji=emoji_flag %}
