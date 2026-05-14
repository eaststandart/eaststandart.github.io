---
layout: default
title: Что нового?
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    <!-- Твой Liquid-цикл for item in all_content остается без изменений -->
    {% assign all_content = site.posts | concat: site.pages %}
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}
        <li class="update-item news-item-compact" data-date="{{ item.date | date: '%Y-%m-%d' }}" data-is-post="{{ is_post }}" style="display: none;">      
          <small>{{ item.date | date: "%d.%m.%Y" }}</small>
          <a href="{{ item.url | relative_url }}" class="item-link">{{ item.title }}</a>
        </li>
      {% endif %}
    {% endfor %}
  </ul>
  
  <!-- ДОБАВЛЕНО: Блок для кнопок страниц -->
  <div id="pagination-controls" style="margin-top: 20px; display: flex; gap: 8px; justify-content: center;"></div>
</div>

<script>
  (function() {
    var list = document.getElementById('live-updates-list');
    var controls = document.getElementById('pagination-controls');
    var items = Array.from(list.getElementsByClassName('update-item'));
    
    var itemsPerPage = 10; // Сколько выводить на одной странице
    var currentPage = 1;

    // 1. Твоя рабочая сортировка
    items.sort(function(a, b) {
      return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
    });

    var totalPages = Math.ceil(items.length / itemsPerPage);

    // 2. Функция рендеринга конкретной страницы
    function renderPage(page) {
      list.innerHTML = '';
      var start = (page - 1) * itemsPerPage;
      var end = start + itemsPerPage;
      
      var pageItems = items.slice(start, end);
      pageItems.forEach(function(el) {
        var isPost = el.getAttribute('data-is-post') === 'true';
        var link = el.querySelector('.item-link');
        
        if (isPost) { link.style.color = '#bbb'; } else { link.style.color = '#3498db'; }
        el.style.display = 'flex'; 
        list.appendChild(el);
      });

      renderControls();
    }

    // 3. Функция создания кнопок Назад/Вперед/Цифры
    function renderControls() {
      controls.innerHTML = '';
      if (totalPages <= 1) return; // Если страниц мало, кнопки не нужны

      for (var i = 1; i <= totalPages; i++) {
        var btn = document.createElement('button');
        btn.innerText = i;
        btn.style.padding = '5px 10px';
        btn.style.border = '1px solid #ddd';
        btn.style.borderRadius = '4px';
        btn.style.cursor = 'pointer';
        
        if (i === currentPage) {
          btn.style.background = '#3498db';
          btn.style.color = '#fff';
          btn.style.borderColor = '#3498db';
        } else {
          btn.style.background = '#fff';
          btn.style.color = '#333';
        }

        (function(pageIndex) {
          btn.addEventListener('click', function() {
            currentPage = pageIndex;
            renderPage(currentPage);
            window.scrollTo(0, 0); // Прокрутка вверх при смене страницы
          });
        })(i);

        controls.appendChild(btn);
      }
    }

    // Запуск первой страницы
    renderPage(currentPage);
  })();
</script>
