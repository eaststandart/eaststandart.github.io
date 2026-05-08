---
layout: fair
description: Работы юных инженеров и мастеров.
title: Ярмарка поделок
navtitle: "Поделки"
permalink: /fair/
---

<div class="fair-list">
  {% assign projects = site.pages | where_exp: "item", "item.path contains 'fair/'" | sort: "published" | reverse %}
  {% for project in projects %}
    {% unless project.url == "/fair/" %}
      <a href="{{ project.url | relative_url }}" class="fair-card">
        {% assign folder = project.path | split: "/" | last | replace: ".md", "" %}
        <img src="{{ project.url | append: folder | append: '.webp' | relative_url }}" class="fair-img-round">
        <h3>{{ project.title }}</h3>
      </a>
    {% endunless %}
  {% endfor %}
</div>
