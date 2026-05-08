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
  var project = urlParams.get('project');
  var nav = urlParams.get('nav');
  var navTitle = urlParams.get('title'); // Берем имя раздела из ссылки

  if (project && nav) {
    var title = document.querySelector('h1');
    if (title) {
      var projectUrl = '/' + nav + '/' + project + '/';
      var sectionUrl = '/' + nav + '/';
      var sectionName = navTitle ? navTitle : nav; // Если title нет, пишем латиницу

      var navHtml = '<p style="margin-bottom: 20px;">' +
                    '<a href="' + projectUrl + '" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">← Назад к проекту</a>' +
                    '<span style="color: #ccc; margin: 0 5px;">|</span>' +
                    '<a href="' + sectionUrl + '" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">Перейти в раздел: ' + sectionName + '</a>' +
                    '</p>';
      
      title.insertAdjacentHTML('afterend', navHtml);
    }

    document.querySelectorAll('.photo-entry').forEach(function(item) {
      if (item.getAttribute('data-project') === project) {
        item.style.display = 'block';
      }
    });
  } else {
    document.querySelectorAll('.photo-entry').forEach(function(item) {
        item.style.display = 'block';
    });
  }
</script>

