---
layout: default
title: Что нового?
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    {% assign all_content = site.posts | concat: site.pages %}
    
    {% for item in all_content %}
      {% comment %} Добавлено исключение самого себя: and item.url != "/news/" {% endcomment %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}

        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}" 
            data-is-post="{{ is_post }}"
            style="display: none; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          
          <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
          
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
      var isPost = el.getAttribute('data-is-post') === 'true';
      var link = el.querySelector('.item-link');
      
      if (isPost) {
        link.style.color = '#bbb'; 
      } else {
        link.style.color = '#3498db'; 
      }

      el.style.display = 'block'; 
      list.appendChild(el);
    });
  })();
</script>
