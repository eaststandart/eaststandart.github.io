/* ==========================================================================
   ОРИГИНАЛЬНЫЙ МОДУЛЬ ОПТИМИЗАЦИИ И ИСТИННОГО ЛЕЗИ-ЛОАДА ВИДЕО (video-lazy-load.js)
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
        rootMargin: "200px" // Триггер сработает за 200px до появления видео в поле зрения
    });

    // ==========================================================================
    // 2. АНАЛИЗ АБЗАЦЕВ И КОНВЕРТАЦИЯ ФЕЙКОВЫХ ИЗОБРАЖЕНИЙ В ТЕГИ VIDEO
    // ==========================================================================
    paragraphs.forEach(p => {
        // ИСПРАВЛЕНО: Теперь ищем картинки-заглушки как с src, так и с безопасным data-src
        const fakeVideos = p.querySelectorAll('img[src$=".mp4"], img[src$=".webm"], img[data-src$=".mp4"], img[data-src$=".webm"]');
        
        if (fakeVideos.length > 0) {
            const container = document.createElement('div');
            container.className = 'video-test-row';

            fakeVideos.forEach(img => {
                // Забираем ссылку из любого доступного атрибута (data-src или src)
                const realSrc = img.getAttribute('data-src') || img.getAttribute('src');

                // Собираем настоящий нативный тег плеера <video>
                const video = document.createElement('video');
                video.src = realSrc;
                video.controls = true;
                video.muted = true;
                video.setAttribute('playsinline', ''); 
                
                // КРИТИЧЕСКИ ВАЖНО: Полностью блокируем загрузку данных для экономии трафика
                video.preload = "none"; 

                // Передаем созданный плеер под контроль нашему ленивому наблюдателю
                videoObserver.observe(video);

                // Добавляем плеер в строку-контейнер, а старую картинку-заглушку удаляем
                container.appendChild(video);
                img.remove();
            });

            p.insertAdjacentElement('beforebegin', container);

            if (p.textContent.trim() === "" && p.querySelectorAll('*').length === 0) {
                p.remove();
            }
        }
    });
}
