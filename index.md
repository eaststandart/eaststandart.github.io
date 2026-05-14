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
                <img src="/assets/icons/chto-novogo.svg" alt="🔥" class="section-icon">
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
                
                {% comment %} 
                  ИСПРАВЛЕННЫЙ БЛОК: Правильно вырезаем имя первого раздела из URL.
                  Для /fair/robot1/ он железно достанет слово "fair"
                {% endcomment %}
                {% assign url_parts = item.url | split: "/" %}
                {% assign first_folder = url_parts[1] %}
                {% assign item_section = "/" | append: first_folder | append: "/" %}
                
                {% if item.path contains '_posts' %}
                  {% assign first_cat = item.categories | first %}
                  {% assign item_section = "/" | append: first_cat | append: "/" %}
                {% endif %}
                
                {% assign parent_page = site.pages | where: "permalink", item_section | first %}
                {% assign section_emoji = parent_page.emoji | default: "" %}

                <li class="update-item news-item-compact" data-date="{{ item.date | date: '%Y-%m-%d' }}" data-is-post="{{ is_post }}" data-emoji="{{ section_emoji }}" style="display: none;">      
                  <small>{{ item.date | date: "%d.%m.%Y" }}&nbsp;»&nbsp;</small> 
                  <a href="{{ item.url | relative_url }}" class="item-link">
                    {{ item.title }}
                  </a>
                </li>
              {% endif %}
            {% endfor %}

            {% comment. ВТОРОЙ ЦИКЛ ДЛЯ ЛЮДЕЙ ОСТАЕТСЯ КАК ЕСТЬ %}
            {% assign people_parent = site.pages | where: "permalink", "/people/" | first %}
            {% assign people_emoji = people_parent.emoji | default: "🧍‍♂️" %}
            {% for person in site.people %}
              {% if person.date %}
                <li class="update-item news-item-compact" data-date="{{ person.date | date: '%Y-%m-%d' }}" data-is-post="false" data-emoji="{{ people_emoji }}" style="display: none;">      
                  <small>{{ person.date | date: "%d.%m.%Y" }}&nbsp;»&nbsp;</small> 
                  <a href="{{ person.url | relative_url }}" class="item-link">
                    {{ person.title }}
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
      var emoji = el.getAttribute('data-emoji'); // Читаем эмодзи из HTML-атрибута data-emoji
      var link = el.querySelector('.item-link');
      
      // Настройка цвета текста (посты остаются серыми, проекты/страницы - синими)
      if (isPost) {
        link.style.color = '#586069'; 
      } else {
        link.style.color = '#0366d6'; 
      }

      // Если для этой строки есть какой-либо эмодзи и он еще не добавлен - приклеиваем его
      if (emoji && !link.innerHTML.includes(emoji)) {
        link.innerHTML += ' ' + emoji;
      }

      el.style.display = 'flex'; 
      el.style.alignItems = 'flex-start'; 
      list.appendChild(el);
    });
  })();
</script>
