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
        if (cats.includes(project)) { 
          item.style.setProperty('display', 'block', 'important'); // Наш проект — открываем
          
          // МГНОВЕННАЯ АКТИВАЦИЯ КАРТИНОК: Возвращаем src картинкам ТОЛЬКО нашего проекта
          item.querySelectorAll('img[data-src]').forEach(function(img) {
              var srcVal = img.getAttribute('data-src') || "";
              // Если файл НЕ является видеороликом — включаем картинку в штатный режим!
              if (!srcVal.endsWith('.mp4') && !srcVal.endsWith('.webm')) {
                  img.setAttribute('src', srcVal);
                  img.removeAttribute('data-src');
                  img.setAttribute('loading', 'lazy'); // Нативный ленивый атрибут для картинок
              }
          });

        } else {
          item.remove(); // Чужой проект — полностью стираем из кода страницы
        }
      } else {
        // Режим общей страницы (без 0): показываем все посты и активируем только картинки
        item.style.setProperty('display', 'block', 'important');
        item.querySelectorAll('img[data-src]').forEach(function(img) {
            var srcVal = img.getAttribute('data-src') || "";
            if (!srcVal.endsWith('.mp4') && !srcVal.endsWith('.webm')) {
                img.setAttribute('src', srcVal);
                img.removeAttribute('data-src');
                img.setAttribute('loading', 'lazy');
            }
        });
      }
    });

    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ ДЛЯ ЛЮБОЙ СТРАНИЦЫ САЙТА
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry, .posts-page-list .posts-page-item, .project-list li'));

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      
      // Намертво обнуляем нижний маргин и падинг у финишного поста страницы
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      lastItem.style.setProperty('padding-bottom', '0px', 'important');
      
      // Находим и полностью скрываем разделительную линию под ним (если она есть)
      var hr = lastItem.querySelector('.media-entry-hr, hr');
      if (hr) {
        hr.style.setProperty('display', 'none', 'important');
      }
      
      if (lastItem.nextElementSibling && lastItem.nextElementSibling.tagName === 'HR') {
        lastItem.nextElementSibling.style.setProperty('display', 'none', 'important');
      }
    }

    // ШАГ 3: Принудительно запускаем оригинальный видео-скрипт для оставшегося на экране поста
    if (typeof runVideoLazyLoad === 'function') {
        runVideoLazyLoad();
    }
}
