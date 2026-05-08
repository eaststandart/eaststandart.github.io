---
layout: default
description: Фото, видео выполненного пректа от участноков
title: Медиа-материалы проекта
permalink: /media/
---

<div id="media-container">
  {% for post in site.posts %}
    {% comment %} Проверяем, что пост относится к медиа {% endcomment %}
    {% if post.categories contains "media" %}
      {% comment %} Передаем ВСЕ категории через пробел в атрибут data-project {% endcomment %}
      <div class="media-entry" data-project="{{ post.categories | join: ' ' }}" style="display: none; margin-bottom: 50px;">
        <h3>{{ post.title }}</h3>
        <small style="color: #888;">{{ post.date | date: "%d.%m.%Y" }}</small>
        <div class="media-content" style="margin-top: 15px;">
          {{ post.content }}
        </div>
        <hr style="border: 0; border-top: 1px solid #eee; margin-top: 30px;">
      </div>
    {% endif %}
  {% endfor %}
</div>

<script>
  var urlParams = new URLSearchParams(window.location.search);
  var project = urlParams.get('project');
  var nav = urlParams.get('nav');
  var navTitle = urlParams.get('title');

  // Теперь проверяем только наличие проекта
  if (project) {
    var title = document.querySelector('h1');
    if (title) {
      // Ссылка на проект (если nav пустой, попробуем вернуться через историю)
      var projectUrl = (nav) ? '/' + nav + '/' + project + '/' : 'javascript:history.back()';
      
      var navHtml = '<p style="margin-bottom: 12px;">' +
                    '<a href="' + projectUrl + '" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">← Назад к проекту</a>';

      // Добавляем раздел, только если nav не пустой
      if (nav) {
        var sectionUrl = '/' + nav + '/';
        var sectionName = (navTitle && navTitle !== "") ? navTitle : nav;
        navHtml += '<span style="color: #ccc; margin: 0 5px;">|</span>' +
                   '<a href="' + sectionUrl + '" style="color: #3498db; text-decoration: none; font-size: 0.9rem;">Раздел: ' + sectionName + '</a>';
      }

      navHtml += '</p><hr>';
      title.insertAdjacentHTML('afterend', navHtml);
    }

    // Фильтрация постов
    document.querySelectorAll('.media-entry').forEach(function(item) {
      var cats = item.getAttribute('data-project') || "";
      if (cats.split(' ').indexOf(project) !== -1) {
        item.style.display = 'block';
      }
    });
  } else {
    // Если параметров нет вообще — показываем всё
    document.querySelectorAll('.media-entry').forEach(function(item) {
        item.style.display = 'block';
    });
  }
</script>

