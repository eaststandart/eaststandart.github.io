---
layout: fair
description: Работы юных инженеров и мастеров.
title: Ярмарка поделок
navtitle: "Поделки"
permalink: /fair/
---

<div class="fair-list">
  {% assign current_section = page.url %}
  {% assign projects = site.pages | where_exp: "item", "item.url contains current_section" | sort: "date" | reverse %}
  
  {% for project in projects %}
    {% unless project.url == current_section %}
      <a href="{{ project.url | relative_url }}" class="fair-card">
        {% assign folder = project.url | split: "/" | last %}
        <img src="{{ project.url | append: folder | append: '.webp' | relative_url }}" class="fair-img-round">
        <h3>{{ project.title }}</h3>
      </a>
    {% endunless %}
  {% endfor %}
</div>

