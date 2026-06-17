/* ==========================================================================
   УНИВЕРСАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ИСТИННОГО ЛЕЗИ-ЛОАДА МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Получаем, например, "robot-korova-iz-kartona"

    // 1. Делаем изолированный снимок всех блоков, чтобы изменения DOM не ломали индексы
    var allEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));

    allEntries.forEach(function(item) {
      var cats = item.getAttribute('data-project') || "";
      
      if (project) {
        // РЕЖИМ КНОПКИ 0: Оставляем только наш проект, чужие — полностью стираем
        if (cats.includes(project)) { 
          item.style.setProperty('display', 'block', 'important'); 
        } else {
          item.remove(); // Намертво вырезаем чужие проекты из кода страницы
        }
      } else {
        // РЕЖИМ ГЛАВНОЙ СТРАНИЦЫ (БЕЗ ПАРАМЕТРОВ): Показываем всё
        item.style.setProperty('display', 'block', 'important');
      }
    });

    // ==========================================================================
    // НАСТОЯЩИЙ ЛЕЗИ-ЛОАД: Картинки и видео грузятся строго при прокрутке до них!
    // ==========================================================================
    var lazyMediaObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            // Когда элемент приближается к экрану
            if (entry.isIntersecting) {
                var media = entry.target;
                var srcVal = media.getAttribute('data-src');
                
                if (srcVal) {
                    media.setAttribute('src', srcVal);
                    media.removeAttribute('data-src'); // Зачищаем временный атрибут
                }
                // Снимаем слежку, так как файл уже начал скачиваться
                observer.unobserve(media);
            }
        });
    }, {
        rootMargin: "200px" // Включаем загрузку за 200px до появления элемента на экране
    });

    // Находим все заблокированные элементы data-src на странице и отдаем их под контроль наблюдателю
    document.querySelectorAll('.media-archive-list-wrapper [data-src]').forEach(function(media) {
        lazyMediaObserver.observe(media);
    });


    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ ДЛЯ ЛЮБОЙ СТРАНИЦЫ САЙТА
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry, .posts-page-list .posts-page-item, .project-list li'));

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      
      // Намертво обнуляем нижний маргин и падинг у финишного поста страницы
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      lastItem.style.setProperty('padding-bottom', '0px', 'important');
      
      // Находим и полностью скрываем разделительную линию под ним
      var hr = lastItem.querySelector('.media-entry-hr, hr');
      if (hr) {
        hr.style.setProperty('display', 'none', 'important');
      }
      
      if (lastItem.nextElementSibling && lastItem.nextElementSibling.tagName === 'HR') {
        lastItem.nextElementSibling.style.setProperty('display', 'none', 'important');
      }
    }
}
