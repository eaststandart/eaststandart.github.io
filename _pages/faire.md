---
workflow: " в секциях sitemap.yml у файлов не полный путь!!! faire, а должно быть _pages/faire.md"
layout: faire
description: Проекты дополнительные к учебным программам для юных инженеров и мастеров по техническим направлениям.
title: Ярмарка поделок
crumbtitle: "Поделки"
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