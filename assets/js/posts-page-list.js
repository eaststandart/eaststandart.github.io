/* ==========================================================================
   УНИВЕРСАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Получаем, например, "robot-korova-iz-kartona"

    // 1. Делаем изолированный снимок всех блоков и вырезаем чужие проекты из памяти устройства
    var allEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));

    allEntries.forEach(function(item) {
      var cats = item.getAttribute('data-project') || "";
      
      if (project) {
        // Режим кнопки 0: Оставляем только текущий проект, чужие — полностью стираем
        if (cats.includes(project)) { 
          item.style.setProperty('display', 'block', 'important'); // Наш проект — открываем
        } else {
          item.remove(); // Чужой проект — полностью вырезаем из кода страницы
        }
      } else {
        // Режим общей страницы: показываем все посты сайта
        item.style.setProperty('display', 'block', 'important');
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
