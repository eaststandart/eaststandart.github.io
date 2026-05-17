---
layout: default
custom_css: "/assets/css/pagination.css"
---

{% comment %} 
ТЕХНИЧЕСКИЙ ШАБЛОН: ЛЕНТЫ НОВОСТЕЙ (\_layouts/news.html)
Назначение: Автоматически строит каркас ленты и выводит кнопки пагинации.
Родитель: Наследует общую шапку/меню из default.html и подключает pagination.css.
{% endcomment %}
{% comment %} Сюда прилетит текст, если ты напишешь его на самой странице {% endcomment %}
{{ content }}

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    {% comment %} Вызываем наш универсальный цикл, имя папки берем из настроек страницы {% endcomment %}
    {% include news-loop.liquid type="news" folder=page.folder %}
  </ul>
</div>

{% comment %} Подключаем универсальное ядро пагинации, настройки берем из страницы {% endcomment %}
{% assign limit = page.per_page | default: 10 %}
{% include pagination.liquid list_id="live-updates-list" controls_id="news-pagination" per_page=limit pinned_url=page.pinned_url %}
