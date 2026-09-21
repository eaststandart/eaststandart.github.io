---
about: Шаблон ленты новостей.
purpose: Автоматически строит каркас ленты и выводит кнопки пагинации.
layout: default
---

{% comment %} АВТОМАТ АДРЕСОВ: Нативно вырезаем имя текущей папки (journal/question) для пагинатора {% endcomment %} {%- assign current_path_clean = page.url | strip_search | strip_slash -%} {%- assign url_parts = current_path_clean | split: "/" -%} {%- assign current_section = url_parts | last | strip | downcase -%}

{{ content }}

<!-- ТЕХНИЧЕСКИЙ ШАБЛОН: ЛЕНТЫ НОВОСТЕЙ И ЖУРНАЛА -->
<div class="news-feed">
  <ul id="posts-list" style="list-style: none; padding: 0;">
    {% include feed.liquid type="feed" %}
  </ul>
</div>

{% assign limit = page.per_page | default: 10 %} 
{% include pagination.liquid list_id="posts-list" controls_id="news-pagination" per_page=limit basket=current_section %}