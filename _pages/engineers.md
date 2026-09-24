---
layout: default
title: Работы юных инженеров
crumbtitle: Работы
description: Инженер начинается в школе... Представлены ссылки на дневники инженеров в которых можно посмотреть работы в дискусиях.
date: 2026-09-25
permalink: /engineers/
emoji: "💥"
keywords: {юный инженер, младший конструктор, инженерные работы}
---


---

{% for person in site.engineers %}
  <a href="{{ person.url | relative_url }}">{{ person.title }}</a>
{% endfor %}

{%- comment -%}

### 💥 Работы юных инженеров

<div class="students-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px;">
  {% for student in site.students %}
    <div class="student-card" style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: #fff;">
      <img src="{{ student.avatar }}" alt="{{ student.student_name }}" style="width: 100%; height: 180px; object-fit: cover; border-radius: 4px;">
      <h3>{{ student.student_name }}</h3>
      <p style="color: #666; font-size: 0.9rem;"><b>Возраст:</b> {{ student.age }}</p>
      <p>{{ student.bio }}</p>
      <a href="{{ student.url }}" class="btn" style="display: inline-block; background: #007bff; color: #fff; padding: 8px 12px; border-radius: 4px; text-decoration: none;">📖 Открыть дневник</a>
    </div>
  {% endfor %}
</div>

{%- endcomment -%}