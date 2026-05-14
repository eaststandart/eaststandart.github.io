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
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <img src="/assets/icons/logo.svg" alt="🔥" class="section-icon">
                <h2 style="margin: 0; font-size: 1.3rem; color: #333;">Что нового?</h2>
            </div>
            <a href="{{ '/news/' | relative_url }}" style="text-decoration: none; font-size: 0.85rem; color: #3498db;">Все →</a>
        </div>
        
        <ul id="live-updates-list" style="list-style: none; padding: 0; margin: 0;">
            {% comment %} Соединяем посты, страницы и новую коллекцию людей {% endcomment %}
            {% assign all_content = site.posts | concat: site.pages | concat: site.people %}
            
            {% for item in all_content %}
              {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
                
                {% assign is_post = false %}
                {% assign is_person = false %}
                
                {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}
                {% if item.path contains '_people' %}{% assign is_person = true %}{% endif %}

                <li class="update-item news-item-compact" 
                    data-date="{{ item.date | date: '%Y-%m-%d' }}" 
                    data-is-post="{{ is_post }}" 
                    data-is-person="{{ is_person }}"
                    style="display: none; margin-bottom: 6px; font-size: 0.9rem; line-height: 1.3;">      
                  <small style="font-family: monospace; color: #6a737d;">{{ item.date | date: "%d.%m.%Y" }}&nbsp;»&nbsp;</small>
                  <a href="{{ item.url | relative_url }}" class="item-link" style="text-decoration: none; font-weight: normal;">
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
      var isPerson = el.getAttribute('data-is-person') === 'true';
      var link = el.querySelector('.item-link');
      
      if (isPerson) {
        link.style.color = '#586069'; // Серый цвет, как у постов
        link.innerHTML += ' 🧍‍♂️';    // Добавляем эмодзи в конец ссылки
      } else if (isPost) {
        link.style.color = '#586069'; // Обычный серый для постов
      } else {
        link.style.color = '#0366d6'; // Синий для проектов и страниц
      }

      el.style.display = 'flex'; 
      el.style.alignItems = 'flex-start'; 
      list.appendChild(el);
    });
  })();
</script>
