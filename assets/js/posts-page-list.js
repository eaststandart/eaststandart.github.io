/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Например, "robot-korova-iz-kartona"

    // 1. Сначала выполняем стандартную фильтрацию: открываем наш проект
    document.querySelectorAll('.media-archive-list-wrapper .media-entry').forEach(function(item) {
      if (project) {
        var cats = item.getAttribute('data-project') || "";
        if (cats.split(' ').indexOf(project) !== -1) { 
          item.style.display = 'block'; 
        }
      } else {
        item.style.display = 'block';
      }
    });

    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ: Скрываем разделительную линию у финишного поста
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry')).filter(function(el) {
      return el.style.display === 'block';
    });

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      var hr = lastItem.querySelector('.media-entry-hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
    }

    // 3. БЕЗОПАСНАЯ ТОТАЛЬНАЯ ОЧИСТКА DOM (ПО КАТЕГОРИИ)
    // Откладываем удаление на мгновение, чтобы дать видео-плеерному скрипту полностью отработать
    setTimeout(function() {
      if (project) {
        // Делаем статичный снимок элементов, чтобы удаление не ломало индексы цикла
        Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry')).forEach(function(item) {
          var cats = item.getAttribute('data-project') || "";
          
          // Если это чужой проект (его нет в категориях текущего проекта) — вырезаем его под корень
          if (cats.split(' ').indexOf(project) === -1) {
            item.remove();
          }
        });
      }
    }, 10); // Задержка 10 миллисекунд полностью решает конфликт скриптов
}
