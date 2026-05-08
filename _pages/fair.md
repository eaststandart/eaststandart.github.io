---
layout: fair
description: Работы юных инженеров и мастеров.
title: Ярмарка поделок
git-title: "Поделки"
permalink: /fair/
---

<div class="fair-list">
  {% assign projects = site.pages | where_exp: "item", "item.path contains 'fair/'" %}
  
  {% for project in projects %}
    {% unless project.url == "/fair/" %}
      <a href="{{ project.url | relative_url }}" class="fair-card">
        {% comment %} Картинка: имя_папки.webp внутри папки проекта {% endcomment %}
        {% assign folder = project.path | split: "/" | last | replace: ".md", "" %}
        <img src="{{ project.url | append: folder | append: '.webp' | relative_url }}">
        <h3>{{ project.title }}</h3>
      </a>
    {% endunless %}
  {% endfor %}
</div>

