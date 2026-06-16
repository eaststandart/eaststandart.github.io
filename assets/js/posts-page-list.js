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
          // Это НАШ проект — делаем его видимым
          item.style.display = 'block'; 
        } else {
          // Это ЧУЖОЙ проект — полностью удаляем его до зачистки линий!
          item.remove();
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
      // Полностью обнуляем маргин и прячем разделительную линию у финишного поста
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      var hr = lastItem.querySelector('.media-entry-hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
    }
}
