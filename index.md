---
layout: home
title: Творческая лаборатория познавательного развития
---

<div class="main-updates-informer" style="box-sizing: border-box; width: 100%; max-width: 100%; margin: 20px auto 30px auto; padding: 15px 20px; border: 1px solid #e1e4e8; border-radius: 6px; background-color: #fafbfc;">
  
  <!-- Шапка информера -->
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #f1f1f1; padding-bottom: 8px;">
    <h3 style="margin: 0; font-size: 1.1rem; font-weight: 600; color: #24292e;">Что нового?</h3>
    <a href="{{ '/news/' | relative_url }}" style="text-decoration: none; font-size: 0.85rem; font-weight: normal;">Смотреть все →</a>
  </div>

  <!-- Список новостей -->
  <ul id="live-updates-list" style="list-style: none; padding: 0; margin: 0;">
    {% assign all_content = site.posts | concat: site.pages %}
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}
        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}" 
            data-is-post="{{ is_post }}"
            style="display: none; margin-bottom: 8px; font-size: 0.9rem; line-height: 1.4;">      
          <small style="font-family: monospace; color: #6a737d;">{{ item.date | date: "%d.%m.%Y" }}</small>
          <a href="{{ item.url | relative_url }}" class="item-link" style="text-decoration: none; margin-left: 10px;">
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
    items.slice(0, 3).forEach(function(el) {
      var isPost = el.getAttribute('data-is-post') === 'true';
      var link = el.querySelector('.item-link');
      
      if (isPost) {
        link.style.color = '#586069'; // Спокойный темно-серый для постов (читается лучше, чем совсем светлый)
      } else {
        link.style.color = '#0366d6'; // Стандартный синий GitHub-стиль для страниц
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
