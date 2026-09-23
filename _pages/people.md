---
layout: default
title: Люди
description: Известные люди в инженерной и научно-технической области.
date: 2025-09-07
permalink: /people/
emoji: "🧍‍♂️"
---


---

{% for person in site.people %}
  <a href="{{ person.url | relative_url }}">{{ person.title }}</a>
{% endfor %}
