---
layout: default
title: Фотографии работ участников
permalink: /photos/
---

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
    // 1. Вставляем кнопку "Назад" прямо в строку навигации
    const navContainer = document.getElementById('dynamic-back');
    if (navContainer) {
      navContainer.innerHTML = '<span style="color: #ccc; margin: 0 15px;">|</span><a href="javascript:history.back()" class="back-link" style="margin-bottom: 0;">Назад</a>';
    }

    // 2. Фильтруем фото (как и раньше)
    document.querySelectorAll('.photo-entry').forEach(item => {
      if (item.getAttribute('data-project') === selectedProject) {
        item.style.display = 'block';
      }
    });
  } else {
    // Если параметра нет — показываем всё
    document.querySelectorAll('.photo-entry').forEach(item => {
        item.style.display = 'block';
    });
  }
</script>

