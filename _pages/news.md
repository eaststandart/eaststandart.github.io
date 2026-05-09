---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

<div class="updates-feed">
  <ul style="list-style: none; padding: 0;">
    {% comment %} Собираем всё и ищем страницы/посты с полем update {% endcomment %}
    {% assign all_content = site.posts | concat: site.pages %}
    {% assign updates = all_content | where_exp: "item", "item.update" | sort: "update" | reverse %}

    {% for item in updates limit: 10 %}
      <li style="margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
        <small style="color: #888;">{{ item.update | date: "%d.%m.%Y" }}</small>
        <span style="margin: 0 8px; font-weight: bold;">
          {% if item.path contains '_posts' %} Запись: {% else %} Проект: {% endif %}
        </span>
        <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
      </li>
    {% else %}
      <li>Пока новостей нет. Добавьте 'update: ГГГГ-ММ-ДД' в параметры страницы.</li>
    {% endfor %}
  </ul>
</div>



