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
  var urlParams = new URLSearchParams(window.location.search);
  var selectedProject = urlParams.get('project');
  var navSlug = urlParams.get('nav'); // Здесь будет 'fair', 'lessons' и т.д.

  if (selectedProject) {
    var title = document.querySelector('h1');
    if (title) {
      // Собираем строку: Назад | Раздел
      var backLink = '<a href="javascript:history.back()" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">← Назад к проекту</a>';
      var sectionLink = '';

      if (navSlug) {
        sectionLink = '<span style="color: #ccc; margin: 0 5px;">|</span>' +
                      '<a href="/' + navSlug + '/" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">Перейти в раздел</a>';
      }

      title.insertAdjacentHTML('afterend', '<p style="margin-bottom: 20px;">' + backLink + sectionLink + '</p>');
    }

    // Фильтруем фото
    document.querySelectorAll('.photo-entry').forEach(function(item) {
      if (item.getAttribute('data-project') === selectedProject) {
        item.style.display = 'block';
      }
    });
  } else {
    // Если зашли просто так — показываем всё
    document.querySelectorAll('.photo-entry').forEach(function(item) {
        item.style.display = 'block';
    });
  }
</script>


