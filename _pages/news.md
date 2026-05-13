---
layout: default
title: Тест ленты обновлений
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    {% assign all_content = site.posts | concat: site.pages %}
    
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" %}
        {% comment %} Запоминаем, пост это или нет, для скрипта {% endcomment %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}

        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}" 
            data-is-post="{{ is_post }}"
            style="display: none; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          
          <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
          
          {% comment %} Убрали слова "Запись" и "Страница", оставили только ссылку {% endcomment %}
          <a href="{{ item.url | relative_url }}" class="item-link" style="text-decoration: none; margin-left: 8px;">
            {{ item.title }}
          </a>
        </li>
      {% endif %}
    {% endfor %}
  </ul>
</div>

<script>
  (function() {
    var list = document.getElementById('live-updates-list');
    var items = Array.from(list.getElementsByClassName('update-item'));

    items.sort(function(a, b) {
      return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
    });

    list.innerHTML = '';
    items.slice(0, 10).forEach(function(el) {
      // КРАСИМ: если пост - серый, если страница - синий
      var isPost = el.getAttribute('data-is-post') === 'true';
      var link = el.querySelector('.item-link');
      
      if (isPost) {
        link.style.color = '#bbb'; // Светло-серый
      } else {
        link.style.color = '#3498db'; // Синий
      }

      el.style.display = 'block'; 
      list.appendChild(el);
    });
  })();
</script>

