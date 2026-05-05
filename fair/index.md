---
layout: default
title: Ярмарка поделок
custom_css: ["/css/fair.css"]
---

Работы юных инженеров и мастеров.

<div class="fair-list">
  {% for project in site.fair %}
    <a href="{{ project.url }}" class="fair-card">
        <img src="/img/icons/{{ project.icon }}" class="fair-img-round">
        <h3>{{ project.title }}</h3>
    </a>
  {% endfor %}
</div>
