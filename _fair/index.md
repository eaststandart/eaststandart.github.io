---
layout: default
title: Ярмарка поделок
custom_css: ["/css/fair.css"]
---

Работы юных инженеров и мастеров.

<p>Количество проектов в коллекции: {{ site.fair | size }}</p>

<ul>
  {% for item in site.fair %}
    <li>Нашел файл: {{ item.path }} | Заголовок: {{ item.title }}</li>
  {% endfor %}
</ul>

