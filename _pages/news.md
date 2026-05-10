---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---




<div class="updates-feed">
  <ul style="list-style: none; padding: 0;">
    {% comment %} 
      1. Сначала просто собираем все посты и страницы в одну кучу без сортировки 
    {% endcomment %}
    {% assign all_content = site.posts | concat: site.pages %}
    
    {% comment %} 
      2. Проходимся циклом и отбираем только те, у которых дата — это строка в формате YYYY-MM-DD.
      Мы не используем фильтр 'sort', чтобы сборка не упала.
    {% endcomment %}
    {% assign count = 0 %}
    
    {% comment %} 
      Поскольку мы не можем надежно отсортировать битый массив, 
      мы будем выводить последние записи по системному порядку Jekyll, 
      но только те, где дата реально прописана.
    {% endcomment %}
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and count < 10 %}
        <li style="margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          <small style="color: #888;">
            {{ item.date | date: "%d.%m.%Y" }}
          </small>
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

