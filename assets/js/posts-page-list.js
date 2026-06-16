/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЛЕЗИ-ЛОАДА МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Например, "robot-korova-iz-kartona"

    // 1. Цикл фильтрации постов по проекту
    document.querySelectorAll('.media-archive-list-wrapper .media-entry').forEach(function(item) {
      if (project) {
        var cats = item.getAttribute('data-project') || "";
        
        // Твой оригинальный рабочий алгоритм поиска
        if (cats.split(' ').indexOf(project) !== -1) { 
          item.style.display = 'block'; // Наш проект — открываем на экране
          
          // АКТИВАЦИЯ МЕДИА: Возвращаем src только картинкам и видео НАШЕГО проекта!
          item.querySelectorAll('[data-src]').forEach(function(mediaElement) {
              mediaElement.setAttribute('src', mediaElement.getAttribute('data-src'));
              mediaElement.removeAttribute('data-src'); // Удаляем временный атрибут
          });

        } else {
          item.style.display = 'none'; // Чужие проекты просто скрываем визуально
        }
      } else {
        item.style.display = 'block';
      }
    });

    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ: Скрываем линию у финишного поста
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry')).filter(function(el) {
      return el.style.display === 'block';
    });

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      var hr = lastItem.querySelector('.media-entry-hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
    }
}
