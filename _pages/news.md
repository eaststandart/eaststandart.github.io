---
layout: default
title: Что нового?
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    {% assign all_content = site.posts | concat: site.pages | concat: site.people %}
    
    {% for item in all_content %}
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

<!-- Контейнер для кнопок страниц -->
<div id="pagination-controls" style="margin-top: 25px; display: flex; gap: 8px; justify-content: center;"></div>

<script>
  (function() {
    var list = document.getElementById('live-updates-list');
    var controls = document.getElementById('pagination-controls');
    var items = Array.from(list.getElementsByClassName('update-item'));

    var itemsPerPage = 10; // Твоя норма в 30 пунктов
    var currentPage = 1;

    // Сортировка элементов по дате
    items.sort(function(a, b) {
      return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
    });

    var totalPages = Math.ceil(items.length / itemsPerPage);

    // Функция отрисовки конкретной страницы
    function renderPage(page) {
      list.innerHTML = '';
      var start = (page - 1) * itemsPerPage;
      var end = start + itemsPerPage;
      
      items.slice(start, end).forEach(function(el) {
        var isPost = el.getAttribute('data-is-post') === 'true';
        var link = el.querySelector('.item-link');
        
        // ТВОЯ ОРИГИНАЛЬНАЯ КРАСКА ИЗ КОДА
        if (isPost) {
          link.style.color = '#bbb'; 
        } else {
          link.style.color = '#3498db'; 
        }

        el.style.display = 'block'; // Твой оригинальный вывод block
        list.appendChild(el);
      });

      renderControls();
    }

    // Функция создания кнопок
    function renderControls() {
      controls.innerHTML = '';
      if (totalPages <= 1) return;

      for (var i = 1; i <= totalPages; i++) {
        var btn = document.createElement('button');
        btn.innerText = i;
        
        // Стили кнопок прямо в JS, чтобы не ломать каскад CSS
        btn.style.padding = '6px 12px';
        btn.style.border = '1px solid #e1e4e8';
        btn.style.borderRadius = '6px';
        btn.style.cursor = 'pointer';
        btn.style.fontSize = '0.9rem';
        btn.style.fontWeight = '600';
        
        if (i === currentPage) {
          btn.style.backgroundColor = '#3498db'; // Твой синий для активной
          btn.style.color = '#fff';
          btn.style.borderColor = '#3498db';
        } else {
          btn.style.backgroundColor = '#fff';
          btn.style.color = '#24292e';
        }

        (function(pageIndex) {
          btn.addEventListener('click', function() {
            currentPage = pageIndex;
            renderPage(currentPage);
            window.scrollTo(0, 0); 
          });
        })(i);

        controls.appendChild(btn);
      }
    }

    renderPage(currentPage);
  })();
</script>
