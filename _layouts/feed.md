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

{%- comment -%}
{% assign limit = page.per_page | default: 10 %}
{% assign emoji_flag = page.emoji_display | default: "Y" %}
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit pinned_url=page.pinned_url emoji=emoji_flag %}
{%- endcomment -%}

{% assign limit = page.per_page | default: 10 %} 
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit %}