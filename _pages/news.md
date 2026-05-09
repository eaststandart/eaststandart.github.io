---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

<div class="updates-test-feed" style="margin-top: 20px;">
  <ul style="list-style: none; padding: 0;">
    {% comment %} 
      Собираем вместе посты и страницы, у которых есть дата в заголовке 
    {% endcomment %}
    {% assign all_content = site.posts | concat: site.pages %}
    {% assign sorted_content = all_content | where_exp: "item", "item.date" | sort: "date" | reverse %}

    {% for item in sorted_content limit: 10 %}
      <li style="margin-bottom: 12px; border-bottom: 1px solid #f9f9f9; padding-bottom: 8px;">
        <small style="color: #999; font-family: monospace;">
          {{ item.date | date: "%d.%m.%Y" }}
        </small>
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
