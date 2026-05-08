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
        {% assign folder = project.path | split: "/" | last | replace: ".md", "" %}
        {% comment %} Добавили класс fair-img-round {% endcomment %}
        <img src="{{ project.url | append: folder | append: '.webp' | relative_url }}" class="fair-img-round">
        <h3>{{ project.title }}</h3>
      </a>
    {% endunless %}
  {% endfor %}
</div>

<div class="fair-list">
    <a href="/fair/simple-cardboard-walking-robot/" class="fair-card">
        <img src="simple-cardboard-walking-robot/simple-cardboard-walking-robot.webp" class="fair-img-round">
        <h3>Робот двуногий шагающий из картона</h3>
    </a>
    
    <a href="/simple-cardboard-walking-robot/" class="fair-card">
        <img src="/assets/icons/through-hole-red-led-2.web" class="fair-img-round">
        <h3>Название поделки</h3>
    </a>
  </div>
