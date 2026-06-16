---
layout: page
title: Медиа-материалы проекта
render_with_liquid: true
---

{% comment %} 
БЕЗОПАСНЫЙ АВТОГЕНЕРАТОР ПО ТВОЕЙ ЛОГИКЕ РАЗБОРА ПУТИ:
Бежим по страницам сайта, находим проекты и создаем для каждого легкую страницу.
{% endcomment %}
{% for project_page in site.pages %}
  {% if project_page.url contains "/faire/" and project_page.url != "/faire/" and project_page.url != "/faire/index.html" %}
    
    {% comment %} Твой код разбора URL на части {% endcomment %}
    {% assign url_parts = project_page.url | split: "/" %}
    {% assign project_slug_last = url_parts[2] | default: url_parts.last %}

    {% if project_slug_last and project_slug_last != "" %}
      {% comment %} 
      Джекилл видит эти команды и физически создает на диске изолированные 
      легкие HTML-файлы! Чужой трафик сюда не попадет.
      {% endcomment %}
      <!-- permalink: /media-posts-page/{{ project_slug_last }}/ -->
      <!-- project_slug: {{ project_slug_last }} -->
      <!-- project_title: {{ project_page.title }} -->
    {% endif %}
  {% endif %}
{% endfor %}

{% comment %} 
Подключаем твой оригинальный модуль вывода публикаций
{% endcomment %}
{% include media-archive.liquid category="media" %}
