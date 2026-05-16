---
layout: default
title: Что нового?
permalink: /news/
---

<div class="updates-feed">
  <ul id="live-updates-list" style="list-style: none; padding: 0;">
    
    {% comment %} 1. Цикл для постов и страниц разделов {% endcomment %}
    {% assign all_content = site.posts | concat: site.pages %}
    {% for item in all_content %}
      {% if item.date and item.url != "/" and item.url != "/tags.html" and item.url != "/news/" %}
        {% assign is_post = false %}
        {% if item.path contains '_posts' %}{% assign is_post = true %}{% endif %}

        {% assign url_parts = item.url | split: "/" %}
        {% assign first_folder = url_parts[1] %}
        {% assign item_section = "/" | append: first_folder | append: "/" %}
        
        {% if item.path contains '_posts' %}
          {% assign first_cat = item.categories | first %}
          {% assign item_section = "/" | append: first_cat | append: "/" %}
        {% endif %}
        
        {% assign parent_page = site.pages | where: "permalink", item_section | first %}
        {% assign section_emoji = parent_page.emoji | default: "" %}

        <li class="update-item" data-date="{{ item.date | date: '%Y-%m-%d' }}" data-is-post="{{ is_post }}" data-emoji="{{ section_emoji }}" style="display: none; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          <small style="color: #888;">{{ item.date | date: "%d.%m.%Y" }}</small>
          <a href="{{ item.url | relative_url }}" class="item-link" style="text-decoration: none; margin-left: 8px;">
            {{ item.title }}
          </a>
        </li>
      {% endif %}
    {% endfor %}
    {% comment %} 2. Цикл для коллекции Людей — очищен от ручных эмодзи {% endcomment %}
    {% for person in site.people %}
      {% if person.date %}
        <li class="update-item" data-date="{{ person.date | date: '%Y-%m-%d' }}" data-is-post="false" data-emoji="" style="display: none; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;">
          <small style="color: #888;">{{ person.date | date: "%d.%m.%Y" }}</small>
          <a href="{{ person.url | relative_url }}" class="item-link" style="text-decoration: none; margin-left: 8px;">
            {{ person.title }}
          </a>
        </li>
      {% endif %}
    {% endfor %}
  </ul>
</div>

<!-- ВЫЗОВ УНИВЕРСАЛЬНОЙ ПАГИНАЦИИ -->
{% include pagination.liquid list_id="live-updates-list" controls_id="news-pagination" per_page=10 pinned_url="" %}
