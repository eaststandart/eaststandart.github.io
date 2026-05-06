---
layout: default
title: Ярмарка поделок
custom_css: ["/css/fair.css"]
---

Проекты для юных инженеров.

<div class="fair-list">
  {% for project in site.fair %}
    <a href="{{ project.url }}" class="fair-card">
        <img src="{{ project.icon }}" class="fair-img-round">
        <h3>{{ project.title }}</h3>
    </a>
  {% endfor %}
</div>
