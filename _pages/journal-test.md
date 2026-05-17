---
layout: default
title: Тест бортового журнала проекта
permalink: /journal-test/
---

{% comment %} 
ТЕСТОВАЯ ИЗОЛИРОВАННАЯ СТРАНИЦА: ЖУРНАЛ С ФИЛЬТРОМ (?project=...)
Назначение: Безопасная проверка автоматического отсечения чужих постов.
Зависимости: Использует готовый project-loop.liquid и pagination.liquid.
{% endcomment %}

<!-- Ссылки для ручного тестирования фильтра прямо на экране -->
<div style="margin-bottom: 20px; padding: 10px; background: #e8f4fd; border: 1px solid #bee5eb; border-radius: 6px;">
  <strong>🕹️ ПУЛЬТ ТЕСТИРОВАНИЯ ФИЛЬТРА:</strong><br>
  1. <a href="{{ '/journal-test/' | relative_url }}" style="color: #0366d6; font-weight: bold;">Показать СОВСЕМ ВСЕ посты сайта</a> (как сейчас в оригинале)<br>
  2. <a href="{{ '/journal-test/' | relative_url }}?project=simple-cardboard-walking-robot" style="color: #0366d6; font-weight: bold;">Отфильтровать: Только Картонный робот →</a>
</div>

<div class="updates-feed">
  <ul id="test-updates-list" style="list-style: none; padding: 0;">
    <!-- Вызываем наш универсальный цикл. Выведет пока всё подряд -->
    {% include project-loop.liquid type="news" folder="" %}
  </ul>
</div>

<!-- Подключаем универсальное ядро пагинации, задаем уникальные ID для теста -->
<div id="test-news-pagination"></div>
{% include pagination.liquid list_id="test-updates-list" controls_id="test-news-pagination" per_page=10 pinned_url="" %}

<!-- УМНЫЙ СКРИПТ ФИЛЬТРАЦИИ ПЕРЕД ЗАПУСКОМ ПАГИНАЦИИ -->
<script>
  (function() {
    // 1. Читаем параметр из адресной строки (например, ?project=simple-cardboard-walking-robot)
    var urlParams = new URLSearchParams(window.location.search);
    var projectFilter = urlParams.get('project');
    
    if (projectFilter) {
      var list = document.getElementById('test-updates-list');
      if (!list) return;

      var items = Array.from(list.children);
      var removedCount = 0;
      
      // 2. Безжалостно стираем из HTML все строки, которые не принадлежат этому роботу
      items.forEach(function(el) {
        var aTag = el.querySelector('.item-link');
        if (aTag) {
          var href = aTag.getAttribute('href');
          if (href && !href.includes(projectFilter)) {
            el.remove();
            removedCount++;
          }
        }
      });
      
      console.log("ТЕСТ ФИЛЬТРА: Удалено чужих постов с экрана: " + removedCount);
    }
  })();
</script>
