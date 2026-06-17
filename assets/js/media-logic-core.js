/* ==========================================================================
   ЕДИНОЕ ЯДРО ПАРСИНГА МЕДИАФАЙЛОВ ОБСИДИАНА (media-logic-core.js)
   ========================================================================== */

function parseObsidianMedia() {
    // Находим все текстовые абзацы, в которых есть метки Obsidian
    const paragraphs = document.querySelectorAll('.main-content p');

    paragraphs.forEach(p => {
        const text = p.textContent.trim();

        // Если внутри абзаца есть хотя бы одна скобка Obsidian
        if (text.includes('![[')) {
            
            // Регулярное выражение находит все вхождения ![[...]] внутри абзаца
            const regex = /!\[\[([^\]]+)\]\]/g;
            let match;
            
            // Контейнеры для красивого вывода сеток в строку
            let imgContainer = null;
            let videoContainer = null;
            let hasMedia = false;

            // Ищем все ссылки в текущем абзаце по очереди
            while ((match = regex.exec(text)) !== null) {
                let rawPath = match[1].trim();
                
                // ВЫРЕЗАЕМ ТЕХНИЧЕСКИЙ КОРЕНЬ GITHUB
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
                    video.preload = "none"; // Жесткий запрет трафика видео на старте
                    
                    videoContainer.appendChild(video);
                    hasMedia = true;
                } 
                // Б. ЕСЛИ ЭТО КАРТИНКА (.webp, .jpg, .png, .svg)
                else if (lowerPath.endsWith('.webp') || lowerPath.endsWith('.jpg') || lowerPath.endsWith('.png') || lowerPath.endsWith('.svg')) {
                    if (!imgContainer) {
                        imgContainer = document.createElement('div');
                        imgContainer.className = 'image-test-row-obsidian';
                        imgContainer.style.display = 'flex';
                        imgContainer.style.flexWrap = 'wrap';
                        imgContainer.style.gap = '15px';
                        imgContainer.style.marginBottom = '20px'; // Чтобы абзацы не липли друг к другу
                    }
                    const img = document.createElement('img');
                    // Даем прямой src — твой image-lazy-load.js сам добавит loading="lazy"!
                    img.setAttribute('src', cleanPath); 
                    img.style.height = "250px";
                    img.style.width = "auto";
                    img.style.objectFit = "cover";
                    img.alt = "Obsidian Image";
                    
                    imgContainer.appendChild(img);
                    hasMedia = true;
                }
            }

            // Если медиафайлы были найдены — заменяем старый текстовый абзац p на наши новые сетки
            if (hasMedia) {
                if (imgContainer) p.parentNode.insertBefore(imgContainer, p);
                if (videoContainer) p.parentNode.insertBefore(videoContainer, p);
                p.remove(); // Стираем сырые скобки Obsidian с экрана
            }
        }
    });
}
