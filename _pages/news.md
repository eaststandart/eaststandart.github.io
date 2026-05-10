---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

<div class="updates-feed">
  <ul style="list-style: none; padding: 0;">
    {% comment %} 1. Берем только свежие посты {% endcomment %}
    {% assign recent_posts = site.posts | limit: 10 %}
    
    {% comment %} 2. Берем только те страницы, где ЕСТЬ дата {% endcomment %}
    {% assign recent_pages = "" | split: "," %}
    {% for p in site.pages %}
      {% if p.date and p.url != "/" %}{% assign recent_pages = recent_pages | push: p %}{% endif %}
    {% endfor %}
    {% assign recent_pages = recent_pages | sort: "date" | reverse | limit: 10 %}

    {% comment %} 3. Объединяем два маленьких чистых списка и сортируем их {% endcomment %}
    {% assign all_recent = recent_posts | concat: recent_pages | sort: "date" | reverse %}

    {% for item in all_recent limit: 10 %}
      <li style="margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
        <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
        <span style="margin: 0 8px; font-weight: bold; color: #444;">
          {% if item.path contains '_posts' %} Добавлена запись: {% else %} Новый проект: {% endif %}
        </span>
        <a href="{{ item.url | relative_url }}" style="color: #3498db; text-decoration: none;">{{ item.title }}</a>
      </li>
    {% endfor %}
  </ul>
</div>
