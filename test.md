---
layout: page
description: Проекты для юных инженеров.
title: Ярмарка поделок
custom_css: ["/css/fair.css"]
---

<div class="fair-list">
  {% for item in site.test %}
    {% comment %} Вычисляем путь к папке проекта из его URL {% endcomment %}
    {% assign project_dir = item.url | replace: 'index.html', '' | replace: '/test/', '/_test/' %}
    
    <a href="{{ item.url }}" class="fair-card">
        <img src="{{ project_dir }}{{ item.icon_name }}" class="fair-img-round">
        <h3>{{ item.title }}</h3>
    </a>
  {% endfor %}
</div>

