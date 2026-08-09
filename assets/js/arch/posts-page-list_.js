/* ==========================================================================
   УНИВЕРСАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ТОТАЛЬНОЙ ЗАЧИСТКИ ХВОСТОВ (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Получаем, например, "robot-korova-iz-kartona"

    // 1. Делаем изолированный снимок всех блоков, чтобы изменения DOM не ломали индексы
    var allEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));

    allEntries.forEach(function(item) {
      var cats = item.getAttribute('data-project') || "";
      
      if (project) {
        // РЕЖИМ КНОПКИ 0: Активируем только наш проект, чужие — полностью стираем
        if (cats.includes(project)) { 
          item.style.setProperty('display', 'block', 'important'); 
          
          // Активируем медиафайлы текущего проекта (data-src -> src)
          item.querySelectorAll('[data-src]').forEach(function(mediaElement) {
              mediaElement.setAttribute('src', mediaElement.getAttribute('data-src'));
              mediaElement.removeAttribute('data-src');
          });
        } else {
          item.remove(); // Намертво вырезаем чужие проекты из кода страницы
        }
      } else {
        // РЕЖИМ ГЛАВНОЙ СТРАНИЦЫ (БЕЗ ПАРАМЕТРОВ): Показываем всё и активируем медиа
        item.style.setProperty('display', 'block', 'important');
        item.querySelectorAll('[data-src]').forEach(function(mediaElement) {
            mediaElement.setAttribute('src', mediaElement.getAttribute('data-src'));
            mediaElement.removeAttribute('data-src');
        });
      }
    });

    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ ДЛЯ ЛЮБОЙ СТРАНИЦЫ САЙТА
    // Находим финишный видимый элемент списка (на любой странице это самый нижний пост)
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry, .posts-page-list .posts-page-item, .project-list li'));

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      
      // Намертво обнуляем нижний маргин и падинг (пустые отступы) у финишного поста страницы
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      lastItem.style.setProperty('padding-bottom', '0px', 'important');
      
      // Находим и полностью скрываем разделительную линию под ним (если она есть)
      var hr = lastItem.querySelector('.media-entry-hr, hr');
      if (hr) {
        hr.style.setProperty('display', 'none', 'important');
      }
      
      // Если линия hr идет как соседний элемент сразу ПОСЛЕ последнего поста, убираем и её
      if (lastItem.nextElementSibling && lastItem.nextElementSibling.tagName === 'HR') {
        lastItem.nextElementSibling.style.setProperty('display', 'none', 'important');
      }
    }
}
