---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

<div class="updates-test-feed">
  <ul style="list-style: none; padding: 0;">
    {% comment %} 
      1. Собираем все посты и страницы.
      2. Фильтруем только те, у которых дата — это строка или время (не массив и не пустота).
    {% endcomment %}
    {% assign all_content = site.posts | concat: site.pages %}
    
    {% comment %} 
      Создаем пустой массив через split, чтобы потом наполнить его через push 
    {% endcomment %}
    {% assign valid_items = "" | split: "," %}
    
    {% for item in all_content %}
      {% if item.date and item.title %}
        {% comment %} Проверка: дата не должна быть пустой и не должна быть главной страницей {% endcomment %}
        {% if item.url != "/" %}
          {% assign valid_items = valid_items | push: item %}
        {% endif %}
      {% endif %}
    {% endfor %}

    {% comment %} Сортируем по дате и переворачиваем (свежие сверху) {% endcomment %}
    {% assign sorted_content = valid_items | sort: "date" | reverse %}

    {% for item in sorted_content limit: 10 %}
      <li style="margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
        <small style="color: #888;">
          {{ item.date | date: "%d.%m.%Y" }}
        </small>
        <span style="margin: 0 8px; font-weight: bold; color: #444;">
          {% if item.path contains '_posts' %} 
            Добавлена запись: 
          {% else %} 
            Новый проект: 
          {% endif %}
        </span>
        <a href="{{ item.url | relative_url }}" style="color: #3498db; text-decoration: none;">
          {{ item.title }}
        </a>
      </li>
    {% endfor %}
  </ul>
</div>


