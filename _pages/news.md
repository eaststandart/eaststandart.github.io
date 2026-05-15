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

        {% comment %} 
          Вычисляем эмодзи точно так же, как на главной 
        {% endcomment %}
        {% assign url_parts = item.url | split: "/" %}
        {% assign first_folder = url_parts[1] %}
        {% assign item_section = "/" | append: first_folder | append: "/" %}
        
        {% if item.path contains '_posts' %}
          {% assign first_cat = item.categories | first %}
          {% assign item_section = "/" | append: first_cat | append: "/" %}
        {% endif %}
        
        {% assign parent_page = site.pages | where: "permalink", item_section | first %}
        {% assign section_emoji = parent_page.emoji | default: "" %}

        {% comment %} Для людей ставим фиксированный маркер {% endcomment %}
        {% if item.path contains '_people' %}
          {% assign section_emoji = "🧍‍♂️" %}
        {% endif %}

        <li class="update-item" 
            data-date="{{ item.date | date: '%Y-%m-%d' }}"
            data-is-post="{{ is_post }}"
            data-emoji="{{ section_emoji }}"
            style="display: none; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          
          <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
          
          <a href="{{ item.url | relative_url }}" class="item-link" style="text-decoration: none; margin-left: 8px;">
            {{ item.title }}
          </a>
        </li>
      {% endif %}
    {% endfor %}
  </ul>
</div>

<!-- 1. СНАЧАЛА КРАСИМ И СТАВИМ ЭМОДЗИ НА ВСЕ ЭЛЕМЕНТЫ -->
{% include news-emoji.liquid %}

<!-- 2. СЛЕДОМ ЧИСТЫЙ МОДУЛЬ БЬЕТ ИХ НА СТРАНИЦЫ ПО 10 ШТУК -->
{% include pagination-next.liquid list_id="live-updates-list" controls_id="news-pagination" per_page=1 %}
