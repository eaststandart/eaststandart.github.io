---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

 <div class="updates-feed">
  <ul style="list-style: none; padding: 0;">
    {% comment %} 1. Собираем список только из тех элементов, где есть дата {% endcomment %}
    {% assign valid_items = "" | split: "," %}
    {% assign all_content = site.posts | concat: site.pages %}

    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" %}
        {% assign valid_items = valid_items | push: item %}
      {% endif %}
    {% endfor %}

    {% comment %} 2. Теперь сортируем уже чистый список {% endcomment %}
    {% assign sorted_updates = valid_items | sort: "date" | reverse %}

    {% for item in sorted_updates limit: 10 %}
      <li style="margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
        <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
        <span style="margin: 0 8px; font-weight: bold; color: #444;">
          {% if item.path contains '_posts' %} Добавлена запись: {% else %} Новый проект: {% endif %}
        </span>
        <a href="{{ item.url | relative_url }}" style="color: #3498db; text-decoration: none;">
          {{ item.title }}
        </a>
      </li>
    {% endfor %}
  </ul>
</div>
