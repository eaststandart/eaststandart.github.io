---
layout: page
description: Работы юных инженеров и мастеров.
title: Ярмарка поделок
custom_css: ["/css/fair.css"]
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
    <a href="simple-cardboard-walking-robot.html" class="fair-card">
        <img src="/assets/icons/simple-cardboard-walking-robot.webp" class="fair-img-round">
        <h3>Робот двуногий шагающий из картона</h3>
    </a>
    
    <a href="/simple-cardboard-walking-robot/" class="fair-card">
        <img src="/assets/icons/through-hole-red-led-2.web" class="fair-img-round">
        <h3>Название поделки</h3>
    </a>

    <a href="project-1.html" class="fair-card">
        <img src="/assets/icons/through-hole-red-led-2.web" class="fair-img-round">
        <h3>Название поделки</h3>
    </a>
    
    <a href="project-2.html" class="fair-card">
        <img src="/assets/icons/through-hole-red-led-2.web" class="fair-img-round">
        <h3>Название поделки</h3>
    </a>

    <a href="project-1.html" class="fair-card">
        <img src="/assets/icons/through-hole-red-led-2.web" class="fair-img-round">
        <h3>Название поделки</h3>
    </a>
    
    <a href="project-2.html" class="fair-card">
        <img src="/assets/icons/through-hole-red-led-2.web" class="fair-img-round">
        <h3>Название поделки</h3>
    </a>
    
</div>
