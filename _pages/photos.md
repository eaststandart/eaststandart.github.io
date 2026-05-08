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
    // 1. Находим заголовок h1 и вставляем ссылку ПОСЛЕ него
    const title = document.querySelector('h1');
    if (title) {
      title.insertAdjacentHTML('afterend', '<p><a href="javascript:history.back()" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">← Назад к проекту</a></p>');
    }

    // 2. Фильтруем фото
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

