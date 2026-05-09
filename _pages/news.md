---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

 <div class="updates-feed">
  <ul style="list-style: none; padding: 0;">
    {% comment %} 1. Просто объединяем всё в одну кучу {% endcomment %}
    {% assign all_content = site.posts | concat: site.pages %}
    
    {% comment %} 2. Сортируем (тут может быть риск, но мы попробуем самый простой метод) {% endcomment %}
    {% assign sorted_content = all_content | sort: "date" | reverse %}

    {% assign count = 0 %}
    {% for item in sorted_content %}
      {% comment %} 
         3. Проверяем: 
         - Дата должна быть (чтобы не было пустых строк)
         - Это не главная страница
         - Нам нужно только 10 последних (ограничиваем вручную)
      {% endcomment %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and count < 10 %}
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


