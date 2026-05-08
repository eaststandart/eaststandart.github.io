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
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a> 
      — {{ post.date | date: "%d.%m.%Y" }} 
      {% if post.categories.size > 0 %}
        #{{ post.categories | join: " #" }}
      {% endif %}
    </li>
  {% endfor %}
</ul>

