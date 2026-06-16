---
layout: page
title: Медиа-материалы проекта
permalink: /media-posts-page/
---

{% comment %} 
ШАГ 1: Извлекаем имя проекта из параметров URL страницы (?project=robot-korova-iz-kartona)
{% endcomment %}
{% assign url_parts = page.url | split: "project=" %}
{% assign current_project = "" %}
{% if url_parts.size > 1 %}
  {% assign current_project = url_parts | last | split: "&" | first %}
{% endif %}

<div id="media-container" class="media-archive-list-wrapper">
  {% for post in site.posts %}
    {% if post.categories contains "media" %}
    
      {% comment %} 
      ОБЩЕЕ ПРАВИЛО: Если мы перешли с конкретного проекта, 
      Jekyll проверяет категории постов. Все чужие проекты (Бластер, Орган) 
      полностью отсекаются и НЕ генерируют HTML-код. Трафик свободен!
      {% endcomment %}
      {% if current_project != "" and current_project != page.url %}
        {% unless post.categories contains current_project %}
          {% continue %}
        {% endunless %}
      {% endif %}

      {% comment %} Пропускаем пост, если задан флаг N {% endcomment %}
      {% if post.media-post-page == "N" or post["media-post-page"] == "N" or post.journal-post-page == "N" or post["journal-post-page"] == "N" %}{% continue %}{% endif %}
    
      {% comment %} 
      Показываем блок сразу (block), так как чужого мусора в HTML больше нет!
      {% endcomment %}
      <div class="media-entry" data-project="{{ post.categories | join: ' ' }}" style="display: block; margin-bottom: 30px;">
        
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

<!-- ПОДКЛЮЧАЕМ ТВОИ ОРИГИНАЛЬНЫЕ СКРИПТЫ ЛИНИЙ И ВИДЕО -->
<script src="{{ '/assets/js/posts-page-list.js' | relative_url }}"></script>
<script>
  document.addEventListener("DOMContentLoaded", function() {
    runMediaArchiveFilter();
  });
</script>

<script src="{{ '/assets/js/video-lazy-load.js' | relative_url }}"></script>
<script>
  document.addEventListener("DOMContentLoaded", function() {
    runVideoLazyLoad();
  });
</script>
