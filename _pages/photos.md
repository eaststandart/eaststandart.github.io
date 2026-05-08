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

