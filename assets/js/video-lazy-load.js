/**
 * @file video-lazy-load.js
 * @about Профессиональный модуль ленивой предзагрузки нативных видеоплееров.
 * @purpose Отслеживает появление тегов <video> и за 200 пикселей до экрана активирует их src.
 */

function runVideoLazyLoad() {
    // Находим все видеоплееры, у которых подготовлен data-src
    const lazyVideos = document.querySelectorAll('video[data-src]');
    
    if ('IntersectionObserver' in window) {
        const videoObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(videoEntry) {
                // Если видео оказалось в 200 пикселях от зоны видимости
                if (videoEntry.isIntersecting) {
                    const video = videoEntry.target;
                    
                    // Переносим ссылку в настоящий src и включаем предзагрузку метаданных
                    video.src = video.dataset.src;
                    video.preload = "metadata"; 
                    video.removeAttribute('data-src');
                    
                    // Перестаем следить за этим видео
                    videoObserver.unobserve(video);
                }
            });
        }, {
            // ТВОЯ НАСТРОЙКА: Начинать загрузку ровно за 200 пикселей до появления на экране!
            rootMargin: "0px 0px 200px 0px"
        });
        
        lazyVideos.forEach(function(video) {
            videoObserver.observe(video);
        });
    } else {
        // Резервный вариант для совсем старых браузеров: грузим всё сразу
        lazyVideos.forEach(function(video) {
            video.src = video.dataset.src;
            video.removeAttribute('data-src');
        });
    }
}

// Запускаем движок автоматически, если он подключен на странице
document.addEventListener("DOMContentLoaded", runVideoLazyLoad);
