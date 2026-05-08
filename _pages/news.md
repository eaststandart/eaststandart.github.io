---
layout: default
description: Новости сайта
title: Лента новостей
git-title: "Поделки"
permalink: /news/
---

<div class="news-feed">
  {% for post in site.posts %}
    <article style="margin-bottom: 30px; border-bottom: 1px solid #f0f0f0; padding-bottom: 20px;">
      
      <h2 style="margin-bottom: 10px; font-size: 1.4rem;">
        <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: #2c3e50;">
          {{ post.title }}
        </a>
      </h2>

      {% comment %} Выводим description или кусочек текста, если описания нет {% endcomment %}
      <p style="margin-bottom: 10px; line-height: 1.5; color: #333;">
        {{ post.description | default: post.excerpt | strip_html | truncatewords: 20 }}
      </p>

      <div style="font-size: 0.85rem; color: #888;">
        <span>{{ post.date | date: "%d.%m.%Y" }}</span>

        {% comment %} Проверяем категории более надежно {% endcomment %}
        {% if post.categories %}
          <span style="margin-left: 15px; color: #3498db;">
            {% for category in post.categories %}
              #{{ category }}{% unless forloop.last %}, {% endunless %}
            {% endfor %}
          </span>
        {% endif %}
      </div>

    </article>
  {% endfor %}
</div>


