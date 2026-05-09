---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

 <div class="updates-feed">
  <ul style="list-style: none; padding: 0;">
    {% assign all_content = site.posts | concat: site.pages %}
    
    {% comment %} 
      Фильтруем: берем только посты И страницы, где ДАТА прописана явно,
      и исключаем главную страницу и поиск.
    {% endcomment %}
    {% assign updates = all_content | where_exp: "item", "item.date" | where_exp: "item", "item.url != '/'" | where_exp: "item", "item.url != '/tags.html'" | sort: "date" | reverse %}

    {% for item in updates limit: 10 %}
      <li style="margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
        <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
        <span style="margin: 0 8px; font-weight: bold;">
          {% if item.path contains '_posts' %} Добавлена запись: {% else %} Новый проект: {% endif %}
        </span>
        <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
      </li>
    {% endfor %}
  </ul>
</div>

