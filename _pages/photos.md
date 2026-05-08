---
layout: default
title: Фотографии работ участников
permalink: /photos/
---

{% comment %} Сюда скрипт вставит кнопку Назад, если нужно {% endcomment %}
<div id="dynamic-nav" style="margin-bottom: 15px; display: none;">
    <span style="color: #ccc; margin: 0 5px;">|</span>
    <a href="javascript:history.back()" class="back-link" style="color: #3498db; font-size: 0.9rem;">Назад</a>
</div>

<div id="photos-container">
  {% for post in site.posts %}
    {% if post.categories contains "photo" %}
      <div class="photo-entry" data-project="{{ post.categories | first }}" style="display: none; margin-bottom: 50px;">
        <h2>{{ post.title }}</h2>
        <div class="photo-content">{{ post.content }}</div>
        <hr>
      </div>
    {% endif %}
  {% endfor %}
</div>

<script>
  const urlParams = new URLSearchParams(window.location.search);
  const selectedProject = urlParams.get('project');

  if (selectedProject) {
    // 1. Показываем кнопку Назад, только если есть параметр project
    document.getElementById('dynamic-nav').style.display = 'inline';

    // 2. Фильтруем фото
    document.querySelectorAll('.photo-entry').forEach(item => {
      if (item.getAttribute('data-project') === selectedProject) {
        item.style.display = 'block';
      }
    });
  } else {
    // 3. Если параметра нет — показываем ВООБЩЕ ВСЕ фото (для общей галереи)
    document.querySelectorAll('.photo-entry').forEach(item => {
        item.style.display = 'block';
    });
  }
</script>
