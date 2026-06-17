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
    // ИСТИННЫЙ ЛЕЗИ-ЛОАД: Картинки и Видео трансформируются строго при прокрутке!
    // ==========================================================================
    var lazyMediaObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            // Когда элемент приближается к экрану на 200px
            if (entry.isIntersecting) {
                var img = entry.target;
                var srcVal = img.getAttribute('data-src') || "";
                
                if (srcVal) {
                    // ПРОВЕРКА: Если файл является ВИДЕОРОЛИКОМ (.mp4 или .webm)
                    if (srcVal.endsWith('.mp4') || srcVal.endsWith('.webm')) {
                        
                        // Создаем контейнер-строку для видео ряда, как в твоем оригинальном скрипте
                        var container = document.createElement('div');
                        container.className = 'video-test-row';

                        // Собираем настоящий нативный тег плеера <video>
                        var video = document.createElement('video');
                        video.src = srcVal;
                        video.controls = true;
                        video.muted = true;
                        video.setAttribute('playsinline', '');
                        video.preload = "metadata"; // Сразу подгружаем первый кадр и длину видео

                        container.appendChild(video);
                        
                        // Находим родительский абзац <p> и выносим видео-блок перед ним наружу
                        var parentP = img.closest('p');
                        if (parentP) {
                            parentP.insertAdjacentElement('beforebegin', container);
                            img.remove(); // Удаляем старый тег-заглушку картинки
                            
                            // Если абзац остался совсем пустым — стираем его из DOM
                            if (parentP.textContent.trim() === "" && parentP.querySelectorAll('*').length === 0) {
                                parentP.remove();
                            }
                        }
                    } else {
                        // Если это ОБЫЧНАЯ КАРТИНКА (.webp, .jpg, .png) — просто активируем её
                        img.setAttribute('src', srcVal);
                        img.removeAttribute('data-src');
                    }
                }
                // Снимаем слежку с этого элемента
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: "200px" // Включаем загрузку за 200px до появления элемента на экране
    });

    // Отдаем под контроль наблюдателю вообще все медиа-элементы с data-src на странице
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
