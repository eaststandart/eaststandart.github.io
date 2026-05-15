---
layout: default
title: Что нового?
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    {% assign all_content = site.posts | concat: site.pages | concat: site.people %}
    
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}

        {% comment %} ОПРЕДЕЛЯЕМ ЦВЕТ ПРЯМО ТУТ, КАК В ТВОЕМ ОРИГИНАЛЕ {% endcomment %}
        {% assign text_color = "#3498db" %}
        {% if is_post %}{% assign text_color = "#bbb" %}{% endif %}

        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}"
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
{% include pagination.liquid list_id="live-updates-list" controls_id="pagination-controls" per_page=10 %}
