---
layout: default
title: Люди
navtitle: "Люди"
permalink: /people/
emoji: "🧍‍♂️"
---

{% include media-archive.liquid category="people" %}

---

{% for person in site.people %}
  <a href="{{ person.url | relative_url }}">{{ person.title }}</a>
{% endfor %}
