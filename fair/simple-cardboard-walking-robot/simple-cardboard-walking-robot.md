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

### Дневник проекта
<ul>
  {% assign project_slug = page.url | split: "/" | last %}
  {% for post in site.categories[project_slug] %}
    {% if post.categories contains "diary" %}
      <li>
        {{ post.date | date: "%d.%m.%Y" }} — 
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>

### Фотографии работ

{% assign project_slug = page.url | split: "/" | last %}
[Все фотографии работ →](/photos/?project={{ project_slug }})

{%- assign project_slug = page.url | split: "/" | last -%}
[Смотреть все фотографии работ →](/photos/?project={{ project_slug }}&nav={{ page.url | split: '/' | [1] }})

<ul>
  {% assign project_slug = page.url | split: "/" | last %}
  {% for post in site.categories[project_slug] %}
    {% if post.categories contains "photo" %}
      <li>
        {{ post.date | date: "%d.%m.%Y" }} — 
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>

