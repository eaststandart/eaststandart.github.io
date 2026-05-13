---
layout: home
title: Творческая лаборатория познавательного развития
---

<div class="grid-container">
    <!-- БЛОК 1 -->
    <section class="category-card my-projects">
        <div class="card-header">
            <img src="/assets/icons/ugolok-mladshego-konstruktora.svg" alt="✈️" class="section-icon">
            <h2>Уголок младшего конструктора</h2>
        </div>
        <ul class="project-list">
            <li><a href="/biblio/">📚 Список литературы</a></li>
            <li><a href="/diary/">📝 Дневник инженера</a></li>
            <li><a href="/projects/">🗂️ Учебные проекты</a></li>
            <li><a href="/fair/">🔥 Ярмарка поделок</a></li>
            <li><a href="/inspiration/">🚀 Техническое вдохновение</a></li>
            <li><a href="/tools/">🛠 Полезные инструменты</a></li>
        </ul>
    </section>

    <!-- БЛОК 2: ЧТО НОВОГО -->
    <section class="category-card site-news">
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <img src="/assets/icons/logo.svg" alt="🔥" class="section-icon">
                <h2>Что нового?</h2>
            </div>
            <a href="{{ '/news/' | relative_url }}" style="text-decoration: none; font-size: 0.85rem; color: #3498db;">Все →</a>
        </div>
        
        <ul id="live-updates-list" style="list-style: none; padding: 0; margin: 0;">
            {% assign all_content = site.posts | concat: site.pages %}
            {% for item in all_content %}
              {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
                {% assign is_post = false %}
                {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}
                <li class="update-item news-item-compact" data-date="{{ item.date | date: '%Y-%m-%d' }}" data-is-post="{{ is_post }}" style="display: none;">      
                  <small>{{ item.date | date: "%d.%m.%Y" }}</small> »
                  <a href="{{ item.url | relative_url }}" class="item-link">
                    {{ item.title }}
                  </a>
                </li>
              {% endif %}
            {% endfor %}
        </ul>
    </section>

    <!-- БЛОК 3: РЕЗЕРВ -->
    <section class="category-card tech-creative">
        <div class="card-header">
            <img src="/assets/icons/detskij-inzhenernyj-klub.svg" alt="✈️" class="section-icon">
            <h2>Информация юным техникам</h2>
        </div>
        <ul class="project-list">
            <li><a href="#">✨ Деятельность клуба</a></li>
            <li><a href="#">🎓 Регулярные занятия</a></li>
            <li><a href="#">🪁 Детско-юношеский лагерь</a></li>
            <li><a href="#">🎨 Творческий процесс</a></li>
            <li><a href="#">💥 Работы юных инженеров</a></li>
        </ul>
    </section>
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
      
      // Задаем только базовый цвет в зависимости от типа
      if (isPost) {
        link.style.color = '#586069'; 
      } else {
        link.style.color = '#0366d6'; 
      }

      el.style.display = 'flex'; // Меняем block на flex для выравнивания
      list.appendChild(el);
    });
  })();
</script>
