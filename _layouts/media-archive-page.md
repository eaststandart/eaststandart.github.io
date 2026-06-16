---
layout: page
---
{% comment %} 
Серверный цикл Jekyll: ищет посты строго текущего проекта (page.project_slug)
{% endcomment %}
<div id="media-container" class="media-archive-list-wrapper">
  {% for post in site.posts %}
    {% if post.categories contains "media" and post.categories contains page.project_slug %}
      {% if post.media-post-page == "N" or post["media-post-page"] == "N" %}{% continue %}{% endif %}
      
      <div class="media-entry" style="display: block; margin-bottom: 30px;">
        
        <!-- Контейнер строки даты и заголовка -->
        <div class="media-entry-title-row">
          <span class="media-entry-date">{{ post.date | date: "%d.%m.%Y" }}</span>
          <h3 class="media-entry-title">{{ post.title }}</h3>
        </div>
        
        <!-- Оболочка основного контента статьи -->
        <div class="media-content main-content">
          {% if post.description and post.description != "" %}
            <p class="page-description">{{ post.description }}</p>
          {% endif %}

          {{ post.content }}
        </div>
        
        <hr class="media-entry-hr" style="border: 0; border-top: 1px solid #eee; margin-top: 25px;">
      </div>

    {% endif %}
  {% endfor %}
</div>
