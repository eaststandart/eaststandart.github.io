/* ==========================================================================
   УНИВЕРСАЛЬНЫЙ МОДУЛЬ КОНВЕРТАЦИИ ОБСИДИАН-ВИДЕО (video-lazy-load.js)
   ========================================================================== */

function runVideoLazyLoad() {
    // 1. Создаем стандартного наблюдателя для ленивой подгрузки метаданных на экране
    const videoObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target;
                
                if (video.closest('.media-entry') && video.closest('.media-entry').style.display === 'none') {
                    return; 
                }

                // Видео подошло к экрану — разрешаем скачать первый кадр и длину роликов
                video.preload = "metadata"; 
                observer.unobserve(video);
            }
        });
    }, { 
        rootMargin: "200px" // Включаем плеер за 200px до появления
    });

    // 2. Находим ВСЕ абзацы на странице. Если Kramdown встретил ![[...]], он выведет это как текст внутри <p>
    const paragraphs = document.querySelectorAll('.main-content p');

    paragraphs.forEach(p => {
        const text = p.textContent.trim();

        // Регулярное выражение ищет формат Obsidian: ![[ любой_путь.webm ]] или .mp4
        if (text.startsWith('![[') && (text.endsWith('.webm]]') || text.endsWith('.mp4]]'))) {
            
            // Вытаскиваем чистый путь к файлу из скобок (убираем ![[ , ]], а также точки слэши ../)
            let cleanPath = text.replace('![[', '').replace(']]', '').trim();
            cleanPath = cleanPath.replace('../', '').replace('../', ''); // Чистим относительные пути Obsidian
            
            // Если путь начинается не со слэша, добавляем его для корня сайта
            if (!cleanPath.startsWith('/')) {
                cleanPath = '/' + cleanPath;
            }

            // Создаем красивую строку-контейнер плеера, как в твоем оригинале
            const container = document.createElement('div');
            container.className = 'video-test-row';

            const video = document.createElement('video');
            video.src = cleanPath; // Получаем идеальный адрес: /faire/robot-korova-iz-kartona/...
            video.controls = true;
            video.muted = true;
            video.setAttribute('playsinline', '');
            
            // ЖЕСТКИЙ ЗАПРЕТ ТРАФИКА: изначально видео весит 0 байт и ничего не качает
            video.preload = "none"; 

            // Отдаем плеер под контроль ленивому наблюдателю прокрутки
            videoObserver.observe(video);

            container.appendChild(video);
            
            // Вставляем готовый плеер вместо текстовой строки Obsidian
            p.parentNode.insertBefore(container, p);
            p.remove(); // Удаляем старый текстовый абзац
        }
    });
}
