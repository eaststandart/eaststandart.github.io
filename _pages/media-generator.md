---
layout: media-archive-page
render_with_liquid: true
---
{% for project in site.faire %}
  {% comment %} 
  Используем твою логику: вычисляем чистый слаг проекта из его пути 
  {% endcomment %}
  {% assign url_parts = project.url | split: "/" %}
  {% assign slug = url_parts[2] | default: project.slug %}

  {% if slug and slug != "" %}
    {% comment %} 
    Системная команда Jekyll: создает на диске изолированные легкие HTML-файлы!
    Чужой код из других проектов сюда физически не попадет.
    {% endcomment %}
    <!-- permalink: /media-posts-page/{{ slug }}/ -->
    <!-- project_slug: {{ slug }} -->
    <!-- title: {{ project.title }} -->
  {% endif %}
{% endfor %}
