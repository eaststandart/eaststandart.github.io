---
layout: media-archive-page
render_with_liquid: true
---
{% for project_page in site.pages %}
  {% if project_page.url contains "/faire/" and project_page.permalink %}
    {% assign slug = project_page.permalink | remove: "/faire/" | remove: "/" %}
    {% if slug != "" %}
      {% comment %} 
      Jekyll видит эту команду и физически нарезает на диске отдельные 
      легкие HTML-файлы под каждый проект!
      {% endcomment %}
      <!-- permalink: /media-posts-page/{{ slug }}/ -->
      <!-- project_slug: {{ slug }} -->
      <!-- title: {{ project_page.title }} -->
    {% endif %}
  {% endif %}
{% endfor %}
