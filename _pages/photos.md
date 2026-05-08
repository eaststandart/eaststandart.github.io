---
layout: default
title: Фотографии работ участников
permalink: /photos/
---

<h1 id="page-title">Фотографии работ</h1>

<div id="photos-container">
  {% for post in site.posts %}
    {% if post.categories contains "photo" %}
      <div class="photo-entry" data-project="{{ post.categories | first }}" style="display: none; margin-bottom: 50px;">
        <h2>{{ post.title }}</h2>
        <small>{{ post.date | date: "%d.%m.%Y" }}</small>
        <div class="photo-content">
          {{ post.content }}
        </div>
        <hr>
      </div>
    {% endif %}
  {% endfor %}
</div>

<script>
  const urlParams = new URLSearchParams(window.location.search);
  const selectedProject = urlParams.get('project');

  if (selectedProject) {
    let projectFound = false;
    document.querySelectorAll('.photo-entry').forEach(item => {
      if (item.getAttribute('data-project') === selectedProject) {
        item.style.display = 'block';
        projectFound = true;
      }
    });

    // Если нашли посты, можно даже оставить заголовок как есть 
    // или программно его чуть подправить, если нужно.
  }
</script>
