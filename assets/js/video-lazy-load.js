/* ==========================================================================
   ОРИГИНАЛЬНЫЙ МОДУЛЬ ОПТИМИЗАЦИИ И ЛЕЗИ-ЛОАДА ВИДЕО (video-lazy-load.js)
   ========================================================================== */

function runVideoLazyLoad() {
    // Выбираем все текстовые абзацы внутри контента статьи
    const paragraphs = document.querySelectorAll('.main-content p');

    // ==========================================================================
    // 1. СОЗДАНИЕ НАБЛЮДАТЕЛЯ (INTERSECTION OBSERVER) ДЛЯ ЛЕНИВОЙ ЗАГРУЗКИ ВИДЕО
    // ==========================================================================
    const videoObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            // Когда видео-плеер пересекает невидимую границу и приближается к экрану
            if (entry.isIntersecting) {
                const video = entry.target;
                
                // Проверяем, не скрыт ли родительский пост через display: none
                if (video.closest('.media-entry') && video.closest('.media-entry').style.display === 'none') {
                    return; 
                }

                // Разрешаем видео-плееру подгрузить метаданные (размер, длительность, первый кадр)
                video.preload = "metadata"; 
                
                // Снимаем слежку с этого плеера, так как запуск загрузки уже выполнен
                observer.unobserve(video);
            }
        });
    }, { 
        // Настройка зазора: триггер загрузки сработает за 200px до появления video в поле зрения
        rootMargin: "200px" 
    });

    // ==========================================================================
    // 2. АНАЛИЗ АБЗАЦЕВ И КОНВЕРТАЦИЯ ФЕЙКОВЫХ ИЗОБРАЖЕНИЙ В ТЕГИ VIDEO
    // ==========================================================================
    paragraphs.forEach(p => {
        // ИСПРАВЛЕНО: Теперь ищем видео-заглушки по защищенному атрибуту [data-src]
        const fakeVideos = p.querySelectorAll('img[data-src$=".mp4"], img[data-src$=".webm"]');
        
        // Если фейковые видео-заглушки обнаружены, запускаем процесс трансформации
        if (fakeVideos.length > 0) {
            // Создаем новый блочный контейнер-строку для видеоряда
            const container = document.createElement('div');
            container.className = 'video-test-row';

            fakeVideos.forEach(img => {
                // Собираем настоящий нативный тег плеера <video>
                const video = document.createElement('video');
                // Забираем чистый путь из data-src
                video.src = img.getAttribute('data-src');
                video.controls = true;
                video.muted = true;
                video.setAttribute('playsinline', ''); // Фикс для Safari на iOS
                
                // КРИТИЧЕСКИ ВАЖНО: Изначально полностью блокируем загрузку данных для экономии трафика
                video.preload = "none"; 

                // Передаем созданный плеер под контроль нашему ленивому наблюдателю
                videoObserver.observe(video);

                // Добавляем плеер в строку-контейнер, а старую картинку-заглушку удаляем
                container.appendChild(video);
                img.remove();
            });

            // Выносим готовый контейнер с видео из абзаца наружу, вставив его ПЕРЕД текущим абзацем
            p.insertAdjacentElement('beforebegin', container);

            // Если после удаления картинок абзац остался пустым — полностью стираем его из HTML-дерева
            if (p.textContent.trim() === "" && p.querySelectorAll('*').length === 0) {
                p.remove();
            }
        }
    });
}
