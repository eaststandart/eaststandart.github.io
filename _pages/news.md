---
layout: default
layout_css: "/assets/css/news.css"
title: Что нового?
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0; margin: 0;">
    {% assign all_content = site.posts | concat: site.pages %}
    
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}

        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}" 
            data-is-post="{{ is_post }}"
            style="display: none; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          
          <small>{{ item.date | date: "%d.%m.%Y" }}&nbsp;»&nbsp;</small>
          
          <a href="{{ item.url | relative_url }}" class="item-link" style="text-decoration: none; margin-left: 8px;">
            {{ item.title }}
          </a>
        </li>
      {% endif %}
    {% endfor %}
  </ul>
  
  <!-- Блок кнопок пагинации -->
  <div id="pagination-controls" style="margin-top: 25px; display: flex; gap: 8px; justify-content: center;"></div>
</div>

<script>
  (function() {
    var list = document.getElementById('live-updates-list');
    var controls = document.getElementById('pagination-controls');
    var items = Array.from(list.getElementsByClassName('update-item'));
    
    var itemsPerPage = 10; 
    var currentPage = 1;

    // Сортировка по датам в браузере (не роняет сборку)
    items.sort(function(a, b) {
      return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
    });

    var totalPages = Math.ceil(items.length / itemsPerPage);

    function renderPage(page) {
      list.innerHTML = '';
      var start = (page - 1) * itemsPerPage;
      var end = start + itemsPerPage;
      
      items.slice(start, end).forEach(function(el) {
        el.style.display = 'flex'; 
        el.style.alignItems = 'flex-start'; 
        list.appendChild(el);
      });

      renderControls();
    }

    function renderControls() {
      controls.innerHTML = '';
      if (totalPages <= 1) return;

      for (var i = 1; i <= totalPages; i++) {
        var btn = document.createElement('button');
        btn.innerText = i;
        btn.className = 'page-btn';
        if (i === currentPage) btn.classList.add('active');

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
