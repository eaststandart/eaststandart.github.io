---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

<div class="updates-feed">
  <ul style="list-style: none; padding: 0;">
    {% comment %} 
       Берем только самое свежее из постов (10 шт) и страниц (10 шт).
       Мы НЕ сортируем сайт целиком, чтобы не упасть.
    {% endcomment %}
    {% assign p_posts = site.posts | limit: 10 %}
    {% assign p_pages = site.pages | where_exp: "item", "item.date" | reverse | limit: 10 %}
    
    {% comment %} Сливаем их в один список {% endcomment %}
    {% assign all_content = p_posts | concat: p_pages %}

    {% comment %} 
       Сортируем только эти 20 элементов. 
       Сортировка маленького и чистого списка НЕ роняет сборку.
    {% endcomment %}
    {% assign sorted_updates = all_content | sort: "date" | reverse %}

    {% assign count = 0 %}
    {% for item in sorted_updates %}
      {% if count < 10 and item.url != "/" %}
        <li style="margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
          <span style="margin: 0 8px; font-weight: bold; color: #444;">
            {% if item.path contains '_posts' %} Добавлена запись: {% else %} Новый проект: {% endif %}
          </span>
          <a href="{{ item.url | relative_url }}" style="color: #3498db; text-decoration: none;">
            {{ item.title }}
          </a>
        </li>
        {% assign count = count | plus: 1 %}
      {% endif %}
    {% endfor %}
  </ul>
</div>

