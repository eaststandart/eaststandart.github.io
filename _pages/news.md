---
layout: default
title: Тест ленты обновлений
permalink: /news-test/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    {% comment %} 
      1. ТВОЙ РАБОЧИЙ КОД: просто собираем всё без сортировки, чтобы Jekyll не падал
    {% endcomment %}
    {% assign all_content = site.posts | concat: site.pages %}
    
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" %}
        {% comment %} 
          Добавляем data-date для JavaScript и скрываем элемент, 
          пока скрипт его не отсортирует
        {% endcomment %}
        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}" 
            style="display: none; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          
          <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
          <span style="margin: 0 8px; font-weight: bold; color: #444;">
            {% if item.path contains '_posts' %} Добавлена запись: {% else %} Новый проект: {% endif %}
          </span>
          <a href="{{ item.url | relative_url }}" style="color: #3498db; text-decoration: none;">
            {{ item.title }}
          </a>
        </li>
      {% endif %}
    {% endfor %}
  </ul>
</div>

<script>
  (function() {
    // 2. ОТДЕЛЬНЫЙ КОД ДЛЯ СОРТИРОВКИ (в браузере)
    var list = document.getElementById('live-updates-list');
    var items = Array.from(list.getElementsByClassName('update-item'));

    // Сортируем элементы по дате (от новых к старым)
    items.sort(function(a, b) {
      return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
    });

    // Очищаем список и вставляем отсортированные первые 10 элементов
    list.innerHTML = '';
    items.slice(0, 10).forEach(function(el) {
      el.style.display = 'block'; // Показываем отсортированный элемент
      list.appendChild(el);
    });
  })();
</script>


