---
layout: page
description: Проекты для юных инженеров.
title: Ярмарка поделок
custom_css: ["/assets/css/fair.css"]
---

{% for post in site.posts %}
  <div style="display: flex; margin-bottom: 40px; align-items: start;">
    
    <!-- Блок с картинкой -->
    <div style="flex-shrink: 0; margin-right: 20px;">
      {% if post.image %}
        <img src="{{ post.image }}" width="150" style="border-radius: 8px; object-fit: cover;">
      {% else %}
        <div style="width: 150px; height: 100px; background: #eee; border-radius: 8px; text-align: center; line-height: 100px; color: #999;">Нет фото</div>
      {% endif %}
    </div>

    <!-- Блок с текстом -->
    <div>
      <h3 style="margin-top: 0;">
        <a href="{{ post.url }}">{{ post.title }}</a>
      </h3>
      <p style="font-size: 0.9em; color: #666;">
        {{ post.excerpt | strip_html | truncatewords: 20 }}
      </p>
      <a href="{{ post.url }}">Посмотреть проект →</a>
    </div>

  </div>
{% endfor %}

<div class="fair-list">
  {% for item in site.test %}
    {% comment %} Вычисляем путь к папке проекта из его URL {% endcomment %}
    {% assign project_dir = item.url | replace: 'index.html', '' | replace: '/test/', '/_test/' %}
    
    <a href="{{ item.url }}" class="fair-card">
        <img src="{{ project_dir }}{{ item.icon_name }}" class="fair-img-round">
        <h3>{{ item.title }}</h3>
    </a>
  {% endfor %}
</div>

