/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project');

    // 1. Цикл фильтрации постов по проекту
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

    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ: Находим последний ВИДИМЫЙ пост на экране
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry')).filter(function(el) {
      return el.style.display === 'block';
    });

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      
      // ПРОВЕРКА: Если внутри этой карточки есть блок Giscus, полностью ЗАПРЕЩАЕМ зачистку линий, чтобы не урезать его
      if (!lastItem.querySelector('.discus-inline') && !lastItem.querySelector('.giscus')) {
        lastItem.style.setProperty('margin-bottom', '0px', 'important');
        var hr = lastItem.querySelector('.media-entry-hr');
        if (hr) hr.style.setProperty('display', 'none', 'important');
      }
    }
}
