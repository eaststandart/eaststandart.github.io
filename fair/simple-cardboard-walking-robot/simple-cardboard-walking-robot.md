---
layout: default
description: Развитие навыков конструирования.
title: Робот двуногий шагающий из картона
tags: [конструированиеимоделирование, проектучебный, 5класс, проект, роботдвуногийшагающийизкартона]
sources: "[Walking Robot – Templates pdf – Blackfish](https://blackfishspace.com/product/walking-robot-templates-pdf/)"
published: 2026-05-07
permalink: /fair/simple-cardboard-walking-robot/
---

### Описание проекта
Создание конструкции шагающего робота из картона, приводимого в движение электромотором и оснащённого самодельным редуктором с ремённой передачей.

![](simple-cardboard-walking-robot-1.webp)
![](simple-cardboard-walking-robot-2.webp)
![](simple-cardboard-walking-robot-3.webp)
![](simple-cardboard-walking-robot-4.webp)

> **Смотри также:** [Принцип работы гофрированного картона](https://www.antech.ru/wiki/stati/gofrokarton/).

### Область применения
Принцип движения этого робота можно применить в настоящих космических роботах-помощниках, которые будут переносить инструменты и запчасти между базами на других планетах. Такие машины смогут автоматически доставлять грузы, переступая через небольшие препятствия на своем пути.

![video](simple-cardboard-walking-robot-1.webm)
![video](simple-cardboard-walking-robot-2.webm)

> **Смотри также:** [Шагающие машины ВНИИ Трансмаш, 1980 год](https://youtu.be/hQSO-6LvINQ).

### Развитие проекта
Возможны варианты модификации робота путем добавления в его конструкцию светодиодов для зажигания глаз, функции дистанционного управления и разворота при встрече с препятствием.

### Файлы проекта
1. 📄[Сборочный чертеж, PDF](simple-cardboard-walking-robot.pdf)
2. 📐[Сборочный чертеж, LibreCAD](simple-cardboard-walking-robot.dxf)

### Журнал проекта
**Назначение:** этапы создания, отладка и усовершенствование.
<ul>
  {% assign project_slug = page.url | split: "/" | last %}
  {% for post in site.categories[project_slug] %}
    {% if post.categories contains "feed" and post.categories contains "journal" %}
      <li>
        {{ post.date | date: "%d.%m.%Y" }} — 
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>

### Галерея работ
**Назначение:** демонстрация (фото, видео) выполненного проекта от участников.
{% include link-to-media.liquid %}

---

<div style="background: #fdf6e3; padding: 15px; border: 1px dashed #b58900; font-family: monospace; font-size: 0.85rem; line-height: 1.5;">
  <strong>ТЕСТ ЛОГИКИ ПУТЕЙ:</strong><br>
  URL страницы: {{ page.url }}<br>
  <hr>
  
  {% comment %} ТВОЯ ЛОГИКА (ПО ИНДЕКСАМ) {% endcomment %}
  {% assign parts_yours = page.url | split: "/" %}
  <strong>Твоя логика (Index 1 и 2):</strong><br>
  Section [1]: "{{ parts_yours[1] }}"<br>
  Project [2]: "{{ parts_yours[2] }}"<br>
  <br>

  {% comment %} МОЯ ЛОГИКА (FIRST/LAST + COMPACT) {% endcomment %}
  {% assign parts_mine = page.url | split: "/" | compact %}
  <strong>Моя логика (First и Last + Compact):</strong><br>
  Section (first): "{{ parts_mine | first }}"<br>
  Project (last): "{{ parts_mine | last }}"<br>
  <hr>
  
  <strong>КАК ЭТО ПОВЛИЯЕТ НА ССЫЛКУ:</strong><br>
  Твоя: ?project={{ parts_yours[2] }}&nav={{ parts_yours[1] }}<br>
  Моя: ?project={{ parts_mine | last }}&nav={{ parts_mine | first }}
</div>

---

<ul>
  {% assign project_slug = page.url | split: "/" | last %}
  {% for post in site.categories[project_slug] %}
    {% if post.categories contains "media" %}
      <li>
        {{ post.date | date: "%d.%m.%Y" }} — 
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
