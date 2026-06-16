/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Например, "robot-korova-iz-kartona"

    // Превращаем коллекцию в статичный массив, чтобы удаление элементов не ломало цикл
    var allEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));

    // 1. Цикл фильтрации и жесткого удаления постов по data-project
    allEntries.forEach(function(item) {
      if (project) {
        var cats = item.getAttribute('data-project') || "";
        
        // Прямая и точная проверка: ищем слаг нашего проекта в атрибуте
        if (cats.split(' ').indexOf(project) !== -1) { 
          item.style.display = 'block'; // Наш проект — открываем
        } else {
          item.remove(); // Чужой проект — полностью стираем из HTML-кода страницы!
        }
      } else {
        item.style.display = 'block';
      }
    });

    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ: Работаем с уже полностью очищенным DOM
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      // Полностью обнуляем маргин и прячем разделительную линию у финишного поста
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      var hr = lastItem.querySelector('.media-entry-hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
    }
}
