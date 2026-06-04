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
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      
      // ИСПРАВЛЕНО: ищем линию ТОЛЬКО как прямой дочерний элемент карточки, не трогая Giscus
      var hr = lastItem.querySelector(':scope > .media-entry-hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
    }
}
