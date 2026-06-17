/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Получаем, например, "robot-korova-iz-kartona"

    // 1. Делаем изолированный снимок всех блоков и вырезаем чужие проекты
    var allEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));

    allEntries.forEach(function(item) {
      var cats = item.getAttribute('data-project') || "";
      
      if (project) {
        if (cats.includes(project)) { 
          item.style.setProperty('display', 'block', 'important'); // Наш проект — открываем
          
          // ЭТАП 1: Мгновенно возвращаем src СТРОГО КАРТИНКАМ текущего проекта
          item.querySelectorAll('[data-src]').forEach(function(media) {
              var srcVal = media.getAttribute('data-src') || "";
              if (!srcVal.endsWith('.mp4') && !srcVal.endsWith('.webm')) {
                  media.setAttribute('src', srcVal);
                  media.removeAttribute('data-src');
              }
          });

          // ЭТАП 2: С микро-задержкой включаем видео файлы, когда картинки уже заняли места
          setTimeout(function() {
              item.querySelectorAll('[data-src]').forEach(function(media) {
                  var srcVal = media.getAttribute('data-src') || "";
                  if (srcVal.endsWith('.mp4') || srcVal.endsWith('.webm')) {
                      media.setAttribute('src', srcVal);
                      media.removeAttribute('data-src');
                  }
              });
              
              // После того, как видео получили src, принудительно запускаем твой оригинальный плеер
              if (typeof runVideoLazyLoad === 'function') {
                  runVideoLazyLoad();
                }
          }, 100);

        } else {
          item.remove(); // Чужой проект — полностью стираем из кода страницы
        }
      } else {
        // Режим общей страницы: включаем всё сразу
        item.style.setProperty('display', 'block', 'important');
        item.querySelectorAll('[data-src]').forEach(function(media) {
            media.setAttribute('src', media.getAttribute('data-src'));
            media.removeAttribute('data-src');
        });
      }
    });

    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ ДЛЯ ЛЮБОЙ СТРАНИЦЫ САЙТА
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry, .posts-page-list .posts-page-item, .project-list li'));

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      lastItem.style.setProperty('padding-bottom', '0px', 'important');
      
      var hr = lastItem.querySelector('.media-entry-hr, hr');
      if (hr) {
        hr.style.setProperty('display', 'none', 'important');
      }
      
      if (lastItem.nextElementSibling && lastItem.nextElementSibling.tagName === 'HR') {
        lastItem.nextElementSibling.style.setProperty('display', 'none', 'important');
      }
    }
}
