---
workflow: Разбить карточки на летнийлагерь и регулярныезанятия. разбивку сделать по цветам карточек - по цвету тегов еще которые буду назначать дискусиям
layout: default
title: Творческий процесс
crumbtitle: Творчество
description: "Здесь мы публикуем живые кадры из нашей мастерской. Вы можете посмотреть, как юные инженеры собирают свои первые проекты, а также поделиться своими фото и видео!"
year: "2026"
teacher: "Алексей Петров"
studytype: "regular"
date: 2026-09-25
permalink: /process/
emoji: "🎨"
keywords: {техничекское творчество, creative process}
---



---


{% for person in site.process %}
  <a href="{{ person.url | relative_url }}">{{ person.title }}</a>
{% endfor %}


