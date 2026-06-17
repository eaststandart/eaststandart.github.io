/* ==========================================================================
   ЕДИНОЕ ЯДРО ПАРСИНГА МЕДИАФАЙЛОВ ОБСИДИАНА (media-logic-core.js)
   ========================================================================== */

function parseObsidianMedia() {
    // Находим все текстовые абзацы внутри контента статьи
    const paragraphs = document.querySelectorAll('.main-content p');

    paragraphs.forEach(p => {
        const htmlContent = p.innerHTML.trim();

        // Если внутри абзаца есть хотя бы одна скобка Obsidian
        if (htmlContent.includes('![[')) {
            
            // Разделяем содержимое абзаца по переносам строк или тегам <br>, чтобы обработать каждый элемент отдельно
            const lines = htmlContent.split(/<br>\n|<br>|\n/);
            
            // Создаем новый блочный контейнер-строку для оригинальной видео-сетки (если будут видео подряд)
            let videoContainer = null;
            let videosFound = false;
            let hasOnlyImages = true;

            // Шаг 1: Проверяем, есть ли в этом абзаце видеоролики
            lines.forEach(line => {
                let cleanLine = line.trim();
                if (cleanLine.startsWith('![[') && (cleanLine.endsWith('.webm]]') || cleanLine.endsWith('.mp4]]'))) {
                    hasOnlyImages = false;
                }
            });

            // ШАГ 2: ОБРАБОТКА ПО ФОРМАТАМ (У каждого своя логика)
            if (hasOnlyImages) {
                // ЛОГИКА ДЛЯ КАРТИНОК (.webp): Просто превращаем текст в чистые оригинальные теги <img>
                const regex = /!\[\[([^\]\n\r<]+)\]\]/g;
                let cleanHtml = p.innerHTML.replace(regex, function(match, rawPath) {
                    let cleanPath = rawPath.replace('github/eaststandart.github.io', '').trim();
                    if (!cleanPath.startsWith('/')) cleanPath = '/' + cleanPath;
                    return '<img src="' + cleanPath + '" alt="" />';
                });
                p.innerHTML = cleanHtml;
            } else {
                // ЛОГИКА ДЛЯ ВИДЕО (.webm): Трансформируем текст СТРОГО в оригинальный видео-ряд твоей темы
                lines.forEach(line => {
                    let cleanLine = line.trim();
                    
                    if (cleanLine.startsWith('![[') && (cleanLine.endsWith('.webm]]') || cleanLine.endsWith('.mp4]]'))) {
                        let rawPath = cleanLine.replace('![[', '').replace(']]', '').trim();
                        let cleanPath = rawPath.replace('github/eaststandart.github.io', '').trim();
                        
                        if (!cleanPath.startsWith('/')) cleanPath = '/' + cleanPath;

                        if (!videoContainer) {
                            videoContainer = document.createElement('div');
                            videoContainer.className = 'video-test-row'; // Твой оригинальный класс сетки видео
                        }

                        // Собираем оригинальный нативный тег видео плеера
                        const video = document.createElement('video');
                        video.src = cleanPath;
                        video.controls = true;
                        video.muted = true;
                        video.setAttribute('playsinline', '');
                        video.preload = "none"; // Экономим 100% трафика на старте

                        // Если твой ленивый наблюдатель видео уже создан в системе, отдаем плеер под его контроль
                        if (typeof videoObserver !== 'undefined') {
                            videoObserver.observe(video);
                        }

                        videoContainer.appendChild(video);
                        videosFound = true;
                    }
                });

                // Если видео-сетка была успешно собрана, заменяем ей старый абзац скобок Obsidian
                if (videosFound) {
                    p.parentNode.insertBefore(videoContainer, p);
                    p.remove();
                }
            }
        }
    });
}
