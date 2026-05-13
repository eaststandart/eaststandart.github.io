---
layout: home
title: Творческая лаборатория познавательного развития
---

<div class="main-updates-informer">
  <h3>Что нового?:</h4> <a href="{{ '/news/' | relative_url }}">Смотреть все →</a>
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    {% assign all_content = site.posts | concat: site.pages %}
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}
        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}" 
            data-is-post="{{ is_post }}"
            style="display: none; margin-bottom: 8px;">      
          <small>{{ item.date | date: "%d.%m.%Y" }}</small>
          <a href="{{ item.url | relative_url }}" class="item-link">
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
    // Берем строго первые 3 элемента для главной страницы
    items.slice(0, 3).forEach(function(el) {
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

    <!-- БЛОК 2: РЕЗЕРВ -->
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
