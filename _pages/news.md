---
layout: default
description: Новости сайта
title: Лента новостей
git-title: "Поделки"
permalink: /news/
---

<div class="news-feed">
  {% for post in site.posts %}
    <article style="margin-bottom: 20px; border-bottom: 1px solid #f0f0f0; padding-bottom: 15px;">
      
      {% comment %} Вывод даты {% endcomment %}
      <span style="color: #888; font-size: 0.85rem;">
        {{ post.date | date: "%d.%m.%Y" }}
      </span>

      {% comment %} Вывод категорий {% endcomment %}
      {% if post.categories.size > 0 %}
        <span style="margin-left: 10px; font-size: 0.8rem; color: #3498db; text-transform: uppercase;">
          {% for category in post.categories %}
            #{{ category }}
          {% endfor %}
        </span>
      {% endif %}

      {% comment %} Заголовок со ссылкой {% endcomment %}
      <h2 style="margin-top: 5px; margin-bottom: 5px; font-size: 1.4rem;">
        <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: var(--text-color);">
          {{ post.title }}
        </a>
      </h2>

      {% comment %} Краткое описание, если оно есть {% endcomment %}
      {% if post.description %}
        <p style="margin-top: 0; color: #555;">{{ post.description }}</p>
      {% endif %}

    </article>
  {% endfor %}
</div>

