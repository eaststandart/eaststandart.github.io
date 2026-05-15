---
layout: default
title: What's New?
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    {% assign all_content = site.posts | concat: site.pages | concat: site.people %}
    
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}

        {% comment %} 
          1. ИСПРАВЛЕННЫЙ БЛОК: Вычисляем имя родительской папки раздела.
          Конструкция elsif теперь написана строго по правилам Jekyll.
        {% endcomment %}
        {% if item.path contains '_people' %}
          {% assign item_section = "/people/" %}
        {% else %}
          {% assign url_parts = item.url | split: "/" %}
          {% assign first_folder = url_parts[1] %}
          {% assign item_section = "/" | append: first_folder | append: "/" %}
          
          {% if item.path contains '_posts' %}
            {% assign first_cat = item.categories | first %}
            {% assign item_section = "/" | append: first_cat | append: "/" %}
          {% endif %}
        {% endif %}
        
        {% assign parent_page = site.pages | where: "permalink", item_section | first %}
        {% assign section_emoji = parent_page.emoji | default: "" %}

        {% comment %} ОПРЕДЕЛЯЕМ ЦВЕТ СТРОКИ ИЗ ТВОЕГО ОРИГИНАЛА {% endcomment %}
        {% assign text_color = "#3498db" %}
        {% if is_post %}{% assign text_color = "#bbb" %}{% endif %}

        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}"
            data-is-post="{{ is_post }}"
            data-emoji="{{ section_emoji }}"
            style="display: none; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          
          <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
          
          <a href="{{ item.url | relative_url }}" class="item-link" style="text-decoration: none; margin-left: 8px; color: {{ text_color }};">
            {{ item.title }}
          </a>
        </li>
      {% endif %}
    {% endfor %}
  </ul>
</div>

<!-- ВЫЗОВ УНИВЕРСАЛЬНОЙ ПАГИНАЦИИ -->
{% include pagination.liquid list_id="live-updates-list" controls_id="news-pagination" per_page=10 %}
