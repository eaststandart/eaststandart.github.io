---
layout: page
title: "Медиа-материалы проекта"
autopages:
  permalink: /media-posts-page/:cat/
---

{% comment %} 
АВТОМАТИЧЕСКИЙ ВЫВОД: Джекилл сам найдет этот файл при сборке,
прочитает категории твоих постов из _posts и автоматически создаст 
изолированную страницу для каждого проекта!
{% endcomment %}
<div id="media-container" class="media-archive-list-wrapper">
  {% for post in site.posts %}
    {% comment %} 
    Проверяем, относится ли пост к текущей авто-генерируемой категории проекта
    {% endcomment %}
    {% if post.categories contains page.autopages.category %}
      {% if post.media-post-page == "N" or post["media-post-page"] == "N" or post.journal-post-page == "N" or post["journal-post-page"] == "N" %}{% continue %}{% endif %}
      
      <div class="media-entry" style="display: block; margin-bottom: 30px;">
        
        <div class="media-entry-title-row">
          <span class="media-entry-date">{{ post.date | date: "%d.%m.%Y" }}</span>
          <h3 class="media-entry-title">{{ post.title }}</h3>
        </div>
        
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
