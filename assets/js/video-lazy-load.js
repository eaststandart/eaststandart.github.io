/**
 * @file video-lazy-load.js
 * @about Твой оригинальный рабочий модуль ленивой загрузки видеоплееров.
 * @purpose Отслеживает появление тегов <video> и за 200 пикселей до экрана активирует их src.
 */

function runVideoLazyLoad() {
    // Находим все видеоплееры контента, у которых подготовлен data-src
    const lazyVideos = document.querySelectorAll('video[data-src]');
    
    if ('IntersectionObserver' in window) {
        const videoObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(videoEntry) {
                // Твоя родная проверка на вхождение в зону 200px
                if (videoEntry.isIntersecting) {
                    const video = videoEntry.target;
                    
                    // СТРОГО ТВОЙ РАБОЧИЙ КОД ИЗ ФАЙЛА:
                    video.setAttribute('src', video.getAttribute('data-src'));
                    video.preload = "metadata"; // Запускаем предзагрузку метаданных
                    
                    video.onload = function() {
                        video.removeAttribute('data-src');
                    };
                    
                    // Перестаем следить за этим видео
                    videoObserver.unobserve(video);
                }
            });
        }, {
            // ТВОЯ НАСТРОЙКА: Ровно за 200 пикселей до появления на экране
            rootMargin: "0px 0px 200px 0px"
        });
        
        lazyVideos.forEach(function(video) {
            videoObserver.observe(video);
        });
    }
}

// Автоматический запуск движка при полной сборке страницы
document.addEventListener("DOMContentLoaded", runVideoLazyLoad);
