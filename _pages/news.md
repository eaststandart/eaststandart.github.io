---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

<div class="updates-test-feed">
  <ul style="list-style: none; padding: 0;">
    {% comment %} Собираем контент и фильтруем только те объекты, где дата ВООБЩЕ есть {% endcomment %}
    {% assign all_content = site.posts | concat: site.pages %}
    {% assign filtered_content = "" | split: "," %}
    
    {% for item in all_content %}
      {% if item.date %}
        {% assign filtered_content = filtered_content | push: item %}
      {% endif %}
    {% endfor %}

    {% assign sorted_content = filtered_content | sort: "date" | reverse %}

    {% for item in sorted_content limit: 10 %}
      <li style="margin-bottom: 12px; border-bottom: 1px solid #f9f9f9; padding-bottom: 8px;">
        <small style="color: #999;">
          {{ item.date | date: "%d.%m.%Y" }}
        </small>
        <span style="margin: 0 8px; font-weight: bold;">
          {% if item.path contains '_posts' %} Запись: {% else %} Проект: {% endif %}
        </span>
        <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
      </li>
    {% endfor %}
  </ul>
</div>

