/* ==========================================================================
   ЕДИНОЕ ЯДРО ПАРСИНГА МЕДИАФАЙЛОВ ОБСИДИАНА (media-logic-core.js)
   ========================================================================== */

function parseObsidianMedia() {
    const paragraphs = document.querySelectorAll('.main-content p');

    paragraphs.forEach(p => {
        const htmlContent = p.innerHTML.trim();

        // Ищем, есть ли в абзаце ссылки Obsidian на картинки или видео
        if (htmlContent.includes('![[')) {
            const lines = htmlContent.split(/<br>\n|<br>|\n/);
            
            // Контейнеры для раздельного сбора сеток картинок и видео
            let imgContainer = null;
            let videoContainer = null;
            let hasMedia = false;

            lines.forEach(line => {
                let cleanLine = line.trim();
                
                if (cleanLine.startsWith('![[') && cleanLine.endsWith(']]')) {
                    // Вытаскиваем чистый путь и срезаем корень GitHub
                    let rawPath = cleanLine.replace('![[', '').replace(']]', '').trim();
                    let cleanPath = rawPath.replace('github/eaststandart.github.io', '').trim();
                    
                    if (!cleanPath.startsWith('/')) {
                        cleanPath = '/' + cleanPath;
                    }

                    const lowerPath = cleanPath.toLowerCase();

                    // А. ЕСЛИ ЭТО ВИДЕО (.mp4, .webm)
                    if (lowerPath.endsWith('.mp4') || lowerPath.endsWith('.webm')) {
                        if (!videoContainer) {
                            videoContainer = document.createElement('div');
                            videoContainer.className = 'video-test-row';
                        }
                        const video = document.createElement('video');
                        video.src = cleanPath;
                        video.controls = true;
                        video.muted = true;
                        video.setAttribute('playsinline', '');
                        video.preload = "none"; // Блокируем трафик видео на старте
                        
                        videoContainer.appendChild(video);
                        hasMedia = true;
                    } 
                    // Б. ЕСЛИ ЭТО КАРТИНКА (.webp, .jpg, .png, .svg)
                    else if (lowerPath.endsWith('.webp') || lowerPath.endsWith('.jpg') || lowerPath.endsWith('.png') || lowerPath.endsWith('.svg')) {
                        if (!imgContainer) {
                            imgContainer = document.createElement('div');
                            imgContainer.className = 'image-test-row-obsidian'; // Специальный класс-ряд для картинок в строку
                            imgContainer.style.display = 'flex';
                            imgContainer.style.flexWrap = 'wrap';
                            imgContainer.style.gap = '15px';
                        }
                        const img = document.createElement('img');
                        // Вшиваем безопасный data-src, чтобы картинки не качались до прокрутки экрана!
                        img.setAttribute('data-src', cleanPath); 
                        img.style.height = "250px";
                        img.style.width = "auto";
                        img.style.objectFit = "cover";
                        img.alt = "Obsidian Image";
                        
                        imgContainer.appendChild(img);
                        hasMedia = true;
                    }
                }
            });

            // Вставляем сгенерированные сетки в верстку перед текущим абзацем
            if (hasMedia) {
                if (imgContainer) p.parentNode.insertBefore(imgContainer, p);
                if (videoContainer) p.parentNode.insertBefore(videoContainer, p);
                p.remove(); // Стираем старый текстовый абзац скобок
            }
        }
    });
}
