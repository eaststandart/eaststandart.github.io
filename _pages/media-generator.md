---
layout: media-archive-page
render_with_liquid: true
---
{% comment %} 
Безопасный цикл: бежим по обычным страницам сайта из папки /faire/
{% endcomment %}
{% for project_page in site.pages %}
  {% if project_page.url contains "/faire/" %}
    
    {% comment %} Извлекаем слаг проекта (например, robot-korova-iz-kartona) {% endcomment %}
    {% assign url_parts = project_page.url | split: "/" %}
    {% assign slug = url_parts[2] %}

    {% comment %} Исключаем дубли и пустые страницы главного индекса папки {% endcomment %}
    {% if slug and slug != "" and project_page.url != "/faire/" and project_page.url != "/faire/index.html" %}
      
      {% comment %} 
      Команда Jekyll: автоматически генерирует на диске изолированные 
      легкие HTML-файлы для медиа-листов под каждый найденный проект.
      {% endcomment %}
      <!-- permalink: /media-posts-page/{{ slug }}/ -->
      <!-- project_slug: {{ slug }} -->
      <!-- title: {{ project_page.title }} -->
      
    {% endif %}
  {% endif %}
{% endfor %}
