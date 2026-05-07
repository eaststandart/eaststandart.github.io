---
layout: fair
description: Работы юных инженеров и мастеров.
title: Ярмарка поделок
permalink: /fair/
---

{% for item in site.pages %}
  {% if item.permalink contains '/fair/' and item.permalink != '/fair/' %}
    <a href="{{ item.url | relative_url }}">
      {{ item.title }}
    </a>
  {% endif %}
{% endfor %}

{% for item in site.pages %}
  {% if item.permalink contains '/fair/' and item.permalink != '/fair/' %}
    
    {% comment %} 1. Получаем путь к папке и имя файла без расширения {% endcomment %}
    {% assign path_parts = item.path | split: "/" %}
    {% assign file_full_name = path_parts | last %} {% comment %} Например: robot.md {% endcomment %}
    {% assign file_name = file_full_name | split: "." | first %} {% comment %} Получаем: robot {% endcomment %}
    
    {% comment %} 2. Собираем путь к папке (все части, кроме последней) {% endcomment %}
    {% assign folder_path = "" %}
    {% for part in path_parts %}
      {% unless forloop.last %}
        {% assign folder_path = folder_path | append: "/" | append: part %}
      {% endunless %}
    {% endfor %}

    {% comment %} 3. Собираем путь к картинке: папка + имя файла + .webp {% endcomment %}
    {% assign image_url = folder_path | append: "/" | append: file_name | append: ".webp" %}

    <a href="{{ item.url | relative_url }}" class="fair-card">
        <img src="{{ image_url | relative_url }}" class="fair-img-round">
        <h3>{{ item.title }}</h3>
    </a>

  {% endif %}
{% endfor %}

