---
workflow: " в секциях sitemap.yml у файлов не полный путь!!! faire, а должно быть _pages/faire.md"
layout: faire
title: Ярмарка поделок
crumbtitle: "Поделки"
description: Проекты дополнительные к учебным программам для юных инженеров и мастеров по техническим направлениям.
date: 2025-08-01
permalink: /faire/
emoji: "🔥"
---

{% comment %} 
РАЗДЕЛ: ЯРМАРКА ПОДЕЛОК
Назначение: Страница-витрина для вывода списка всех дополнительных поделок.
Зависимости: Использован шаблон layouts/faire.md и изолированная сетка faire-grid.liquid.
{% endcomment %}

{% include faire-grid.liquid %}

{% comment %}  Ссылки на статьи в /\_posts по этому проекту
![[../../../templates/bases/страницы раздела – github.base]]
{% endcomment %}