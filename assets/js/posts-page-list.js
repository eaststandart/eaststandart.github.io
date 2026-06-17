function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project');

    console.log("[ДЕБАГ] Проект из URL:", project);

    // 1. Фильтрация блоков
    var allEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));
    allEntries.forEach(function(item) {
      var cats = item.getAttribute('data-project') || "";
      if (project) {
        if (cats.includes(project)) { 
          item.style.setProperty('display', 'block', 'important'); 
        } else {
          item.remove(); 
        }
      } else {
        item.style.setProperty('display', 'block', 'important');
      }
    });

    // ==========================================================================
    // ЛЕЗИ-ЛОАД С ДЕБАГОМ В КОНСОЛЬ
    // ==========================================================================
    var lazyMediaObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var img = entry.target;
                var srcVal = img.getAttribute('data-src') || "";
                
                console.log("[ДЕБАГ НАБЛЮДАТЕЛЯ] Элемент подошел к экрану! data-src =", srcVal);
                
                if (srcVal) {
                    if (srcVal.endsWith('.mp4') || srcVal.endsWith('.webm')) {
                        console.log("[ДЕБАГ] Трансформация в ТЕГ VIDEO:", srcVal);
                        var container = document.createElement('div');
                        container.className = 'video-test-row';

                        var video = document.createElement('video');
                        video.src = srcVal;
                        video.controls = true;
                        video.muted = true;
                        video.setAttribute('playsinline', '');
                        video.preload = "metadata";

                        container.appendChild(video);
                        
                        var parentP = img.closest('p');
                        if (parentP) {
                            parentP.insertAdjacentElement('beforebegin', container);
                            img.remove();
                            if (parentP.textContent.trim() === "" && parentP.querySelectorAll('*').length === 0) {
                                parentP.remove();
                            }
                        }
                    } else {
                        console.log("[ДЕБАГ] Активация КАРТИНКИ:", srcVal);
                        img.setAttribute('src', srcVal);
                        img.removeAttribute('data-src');
                    }
                }
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: "200px"
    });

    // Смотрим, сколько элементов с data-src скрипт вообще нашел в HTML
    var targets = document.querySelectorAll('.media-archive-list-wrapper [data-src]');
    console.log("[ДЕБАГ] Найдено элементов под контроль ленивой загрузки:", targets.length);

    targets.forEach(function(media) {
        lazyMediaObserver.observe(media);
    });

    // 2. ЗАЧИСТКА ХВОСТОВ
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry, .posts-page-list .posts-page-item, .project-list li'));
    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      lastItem.style.setProperty('padding-bottom', '0px', 'important');
      var hr = lastItem.querySelector('.media-entry-hr, hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
      if (lastItem.nextElementSibling && lastItem.nextElementSibling.tagName === 'HR') {
        lastItem.nextElementSibling.style.setProperty('display', 'none', 'important');
      }
    }
}
