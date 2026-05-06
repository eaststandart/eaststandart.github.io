---
layout: default
title: Робот двуногий шагающий из картона
icon: "{{ hpath }}simple-cardboard-walking-robot.webp"
tags: [конструированиеимоделирование, проектучебный, 5класс, проект, роботдвуногийшагающийизкартона]
sources: "[Walking Robot](https://blackfishspace.com/product/walking-robot-templates-pdf/)"
parent_name: "Поделки"
parent_url: "/fair/"
---

{% assign parts = page.path | split: "/" %}
{% assign last_index = parts.size | minus: 1 %}
{% assign ppath = "/" %}
{% for i in (0..last_index) %}
  {% if i < last_index %}
    {% capture ppath %}{{ ppath }}{{ parts[i] }}/{% endcapture %}
  {% endif %}
{% endfor %}

DEBUG: {{ ppath }}

{% assign dpath = page.path | replace: page.name, '' | prepend: '/' %} DEBUGd: {{ dpath }}

{% assign fpath = page.path | split: '/' | last | prepend: '/' | prepend: page.path | replace: page.path, '' | split: '/' | size | minus: 1 | assign: 'ignore' %}{% assign ppath = page.path | split: '/' | slice: 0, last_index | join: '/' | prepend: '/' | append: '/' %} DEBUGf: {{ fpath }}

{% capture gpath %}/{{ page.path | replace: page.name, '' }}{% endcapture %} DEBUGg: {{ gpath }}

{% assign hpath = page.path | split: "/" | compact | pop | join: "/" | prepend: "/" | append: "/" %} DEBUGh: {{ hpath }}

{% assign folder = page.path | split: '/' | last %}
{% assign kpath = page.path | replace: folder, '' | prepend: '/' %} DEBUGk: {{ kpath }}


### Описание проекта
Создание конструкции шагающего робота из картона, приводимого в движение электромотором и оснащённого самодельным редуктором с ремённой передачей.

![]({{ hpath }}simple-cardboard-walking-robot-1.webp)
![](/_fair/simple-cardboard-walking-robot/simple-cardboard-walking-robot-2.webp)
![](/_fair/simple-cardboard-walking-robot/simple-cardboard-walking-robot-3.webp)
![](/_fair/simple-cardboard-walking-robot/simple-cardboard-walking-robot-4.webp)

> **Смотри также:** [Принцип работы гофрированного картона](https://www.antech.ru/wiki/stati/gofrokarton/).

### Область применения
Принцип движения этого робота можно применить в настоящих космических роботах-помощниках, которые будут переносить инструменты и запчасти между базами на других планетах. Такие машины смогут автоматически доставлять грузы, переступая через небольшие препятствия на своем пути.

[video]({{ ppath }}simple-cardboard-walking-robot-1.webm)
[video]({{ppath}}simple-cardboard-walking-robot-2.webm)

> **Смотри также:** [Шагающие машины ВНИИ Трансмаш, 1980 год](https://youtu.be/hQSO-6LvINQ).

### Развитие проекта
Возможны варианты модификации робота путем добавления в его конструкцию светодиодов для зажигания глаз, функции дистанционного управления и разворота при встрече с препятствием.

### Файлы проекта
1. 📄[Сборочный чертеж, PDF](simple-cardboard-walking-robot/simple-cardboard-walking-robot.pdf)
2. 📐[Сборочный чертеж, LibreCAD](simple-cardboard-walking-robot/simple-cardboard-walking-robot.dxf)
