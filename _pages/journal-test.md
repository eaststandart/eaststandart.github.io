---
layout: default
title: Тест бортового журнала проекта
permalink: /journal-test/
---

{% comment %} 

ТЕСТОВАЯ ИЗОЛИРОВАННАЯ СТРАНИЦА: ЖУРНАЛ С ИСПРАВЛЕННЫМ ФИЛЬТРОМ
Назначение: Фильтрация запускается ДО пагинации, гарантируя вывод нужных постов.
Зависимости: Использует твой project-loop.liquid для вывода строк.

{% endcomment %}

<!-- Пульт ручного переключения режимов -->
<div style="margin-bottom: 20px; padding: 10px; background: #e8f4fd; border: 1px solid #bee5eb; border-radius: 6px;">
  <strong>🕹️ ПУЛЬТ ТЕСТИРОВАНИЯ ФИЛЬТРА:</strong><br>
  1. <a href="{{ '/journal-test/' | relative_url }}" style="color: #0366d6; font-weight: bold;">Показать СОВСЕМ ВСЕ посты сайта</a><br>
  2. <a href="{{ '/journal-test/' | relative_url }}?project=simple-cardboard-walking-robot" style="color: #0366d6; font-weight: bold;">Отфильтровать: Только Картонный робот →</a>
</div>

<div class="updates-feed">
  <ul id="test-updates-list" style="list-style: none; padding: 0;">
    <!-- Твой тестовый модуль сбора постов -->
    {% include project-loop.liquid folder="" %}
  </ul>
</div>

<!-- Контейнер для кнопок страниц -->
<div id="test-news-pagination"></div>

<!-- 
  1. СКРИПТ ФИЛЬТРАЦИИ: Срабатывает ПЕРВЫМ, очищает HTML-список от чужого контента
-->
<script>
  (function() {
    var urlParams = new URLSearchParams(window.location.search);
    var projectFilter = urlParams.get('project');
    
    if (projectFilter) {
      var list = document.getElementById('test-updates-list');
      if (list) {
        var items = Array.from(list.children);
        items.forEach(function(el) {
          var aTag = el.querySelector('.item-link');
          if (aTag) {
            var href = aTag.getAttribute('href');
            // Если в ссылке нет имени робота — физически удаляем строку из дерева HTML
            if (href && !href.includes(projectFilter)) {
              el.remove();
            }
          }
        });
      }
    }
  })();
</script>

<!-- 
  2. ПАГИНАЦИЯ: Запускается СЛЕДОМ. 
  Она увидит уже идеально чистый список и построит кнопки ровно под количество постов робота.
-->
{% include pagination.liquid list_id="test-updates-list" controls_id="test-news-pagination" per_page=10 pinned_url="" %}
