---
layout: default
title: Ярмарка поделок
custom_css: ["/css/fair.css"]
---

Проекты для юных инженеров.

<div class="fair-list">
  {% for item in site.test %}
    <a href="{{ item.url }}" class="fair-card">
        <img src="{{ item.icon }}" class="fair-img-round">
        <h3>{{ item.title }}</h3>
    </a>
  {% endfor %}
</div>
