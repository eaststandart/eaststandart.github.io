---
layout: page
title: Медиа-материалы проекта
render_with_liquid: true
---

{% comment %} 
ШАГ 1: Собираем список всех уникальных проектов из категорий постов
{% endcomment %}
{% assign raw_projects = "" %}
{% for post in site.posts %}
  {% if post.categories contains "media" %}
    {% for cat in post.categories %}
      {% if cat != "media" %}
        {% assign raw_projects = raw_projects | append: cat | append: "," %}
      {% endif %}
    {% endfor %}
  {% endif %}
{% endfor %}
{% assign unique_projects = raw_projects | split: "," | uniq %}

{% comment %} 
ШАГ 2: Перехватываем текущий проект из адреса URL (?project=) в браузере
{% endcomment %}
<script>
  var urlParams = new URLSearchParams(window.location.search);
  var currentProject = urlParams.get('project');
</script>

<div id="media-container" class="media-archive-list-wrapper">
  {% for project in unique_projects %}
    {% if project != "" %}
      
      {% comment %} 
      Для каждого проекта создаем свой собственный блок.
      По умолчанию он скрыт через data-attribute.
      {% endcomment %}
      <div class="project-media-block" data-project-id="{{ project }}" style="display: none;">
        
        {% for post in site.posts %}
          {% if post.categories contains "media" and post.categories contains project %}
            {% if post.media-post-page == "N" or post["media-post-page"] == "N" or post.journal-post-page == "N" or post["journal-post-page"] == "N" %}{% continue %}{% endif %}

            <div class="media-entry" style="display: block;">
              <div class="media-entry-title-row">
                <span class="media-entry-date">{{ post.date | date: "%d.%m.%Y" }}</span>
                <h3 class="media-entry-title">{{ post.title }}</h3>
              </div>
              
              <div class="media-content main-content">
                {% if post.description and post.description != "" %}
                  <p class="page-description">{{ post.description }}</p>
                {% endif %}

                {{ post.content }}
                
                <!-- А. БЛОК ВЫВОДА АВТОРА -->
                {% if post.author and post.author != "" %}
                <div class="author-inline">
                    <strong>Автор:</strong> 
                    <div class="sources-content">{{ post.author }}</div>
                </div>
                {% endif %}

                <!-- Б. БЛОК ВЫВОДА ИСТОЧНИКОВ -->
                {% if post.sources and post.sources != "" %}
                <div class="sources-inline">
                    <strong>Источники:</strong>
                    <div class="sources-content">{{ post.sources | markdownify }}</div>
                </div>
                {% endif %}

                <!-- В. БЛОК ВЫВОДА ТЕГОВ -->
                {% if post.tags.size > 0 %}
                <div class="tag-container">
                    {% for tag in post.tags %}
                        {% assign tag_clean = tag | replace: '#', '' | strip %}
                        <a href="{{ '/tags.html' | relative_url }}#{{ tag_clean | slugify }}" class="tag-item">{{ tag_clean }}</a>
                    {% endfor %}
                </div>
                {% endif %}
              </div>
              <hr class="media-entry-hr">
            </div>

          {% endif %}
        {% endfor %}

      </div>
    {% endif %}
  {% endfor %}
</div>

<!-- ==========================================================================
     ВЫЗОВ ОРИГИНАЛЬНЫХ СКРИПТОВ И ЖЕСТКАЯ ОЧИСТКА ТРАФИКА
     ========================================================================== -->
<script src="{{ '/assets/js/posts-page-list.js' | relative_url }}"></script>
<script src="{{ '/assets/js/video-lazy-load.js' | relative_url }}"></script>

<script>
  (function() {
    if (currentProject) {
      // 1. Находим блок, который относится к нашему проекту, и включаем его
      var activeBlock = document.querySelector('.project-media-block[data-project-id="' + currentProject + '"]');
      if (activeBlock) {
        activeBlock.style.display = 'block';
      }
      
      // 2. АВТОМАТИЧЕСКАЯ ЗАЧИСТКА: Находим ВСЕ чужие блоки проектов и стираем их из DOM до запуска видео!
      document.querySelectorAll('.project-media-block').forEach(function(block) {
        if (block.getAttribute('data-project-id') !== currentProject) {
          block.remove(); 
        }
      });
    }
    
    // Запускаем твои оригинальные скрипты линий и ленивых плееров видео на чистом HTML
    runMediaArchiveFilter();
    runVideoLazyLoad();
  })();
</script>
