---
layout: default
description: Новости сайта
title: Лента новостей
git-title: "Поделки"
permalink: /news/
---

<ul>
  {% for post in site.posts %}
    <li>
      {{ post.date | date: "%d.%m.%Y" }} — 
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a> 
      {% if post.categories.size > 0 %}
        #{{ post.categories | join: " #" }}
      {% endif %}
    </li>
  {% endfor %}
</ul>

