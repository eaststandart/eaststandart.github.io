---
layout: default
description: Журнал, дневник, блог и прочие записи
title: Лента новостей
permalink: /feed/
---

<ul>
  {% for post in site.posts %}
    <li>
      {{ post.date | date: "%d.%m.%Y" }} –
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a> 
      {% if post.categories.size > 0 %}
        #{{ post.categories | join: " #" }}
      {% endif %}
    </li>
  {% endfor %}
</ul>

