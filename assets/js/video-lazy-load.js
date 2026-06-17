/* ==========================================================================
   ОРИГИНАЛЬНЫЙ МОДУЛЬ ОПТИМИЗАЦИИ И ЛЕЗИ-ЛОАДА ВИДЕО (video-lazy-load.js)
   ========================================================================== */

function runVideoLazyLoad() {
    // Наблюдатель следит за созданными плеерами и подгружает метаданные у экрана
    const videoObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target;
                
                if (video.closest('.media-entry') && video.closest('.media-entry').style.display === 'none') {
                    return; 
                }

                video.preload = "metadata"; // Загружаем превью только на экране
                observer.unobserve(video);
            }
        });
    }, { 
        rootMargin: "200px" 
    });

    // Просто находим все теги video на странице (созданные ядром) и ставим на них слежку
    document.querySelectorAll('.main-content video').forEach(video => {
        videoObserver.observe(video);
    });
}
