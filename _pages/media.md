---
layout: default
description: Фото, видео выполненного пректа от участноков
title: Медиа-материалы проекта
permalink: /media/
---

<div id="media-container">
  {% for post in site.posts %}
    {% comment %} Ищем категорию media {% endcomment %}
    {% if post.categories contains "media" %}
      <div class="media-entry" data-project="{{ post.categories | first }}" style="display: none; margin-bottom: 50px;">
        <h3>{{ post.title }}</h3>
        <small>{{ post.date | date: "%d.%m.%Y" }}</small>
        <div class="media-content">{{ post.content }}</div>
        <hr>
      </div>
    {% endif %}
  {% endfor %}
</div>

<script>
  var urlParams = new URLSearchParams(window.location.search);
  var project = urlParams.get('project');
  var nav = urlParams.get('nav');
  var navTitle = urlParams.get('title');

  if (project && nav) {
    var title = document.querySelector('h1');
    if (title) {
      var projectUrl = '/' + nav + '/' + project + '/';
      var sectionUrl = '/' + nav + '/';
      var sectionName = navTitle ? navTitle : nav;

      var navHtml = '<p style="margin-bottom: 12px;">' +
                    '<a href="' + projectUrl + '" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">→ Назад к проекту</a>' +
                    '<span style="color: #ccc; margin: 0 5px;">|</span>' +
                    '<a href="' + sectionUrl + '" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">Раздел: ' + sectionName + '</a>' + '<hr>' +
                    '</p>';
      
      title.insertAdjacentHTML('afterend', navHtml);
    }

    document.querySelectorAll('.media-entry').forEach(function(item) {
      if (item.getAttribute('data-project') === project) {
        item.style.display = 'block';
      }
    });
  } else {
    document.querySelectorAll('.media-entry').forEach(function(item) {
        item.style.display = 'block';
    });
  }
</script>

