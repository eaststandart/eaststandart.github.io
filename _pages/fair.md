---
layout: fair
description: Работы юных инженеров и мастеров.
title: Ярмарка поделок
permalink: /fair/
---

<div class="fair-list">
  {% for item in site.pages %}
    {% if item.permalink contains '/fair/' and item.permalink != '/fair/' %}
      
      {% comment %} Определяем путь к папке и имя картинки {% endcomment %}
      {% assign path_parts = item.path | split: "/" %}
      {% assign file_name = path_parts | last | split: "." | first %}
      
      {% assign folder_path = "" %}
      {% for part in path_parts %}
        {% unless forloop.last %}
          {% assign folder_path = folder_path | append: "/" | append: part %}
        {% endunless %}
      {% endfor %}

      {% assign image_url = folder_path | append: "/" | append: file_name | append: ".webp" %}

      <a href="{{ item.url | relative_url }}" class="fair-card">
          <img src="{{ image_url | relative_url }}" class="fair-img-round">
          <h3>{{ item.title }}</h3>
      </a>

    {% endif %}
  {% endfor %}
</div>
