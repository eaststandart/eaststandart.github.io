/* ==========================================================================
   УНИВЕРСАЛЬНЫЙ МОДУЛЬ КОНВЕРТАЦИИ ОБСИДИАН-ВИДЕО И СЕТОК (video-lazy-load.js)
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

                // Видео подошло к экрану — разрешаем скачать превью и первый кадр
                video.preload = "metadata"; 
                observer.unobserve(video);
            }
        });
    }, { 
        rootMargin: "200px" // Включаем плеер за 200px до появления
    });

    // 2. Находим ВСЕ абзацы на странице
    const paragraphs = document.querySelectorAll('.main-content p');

    paragraphs.forEach(p => {
        const htmlContent = p.innerHTML.trim();

        // Проверяем, есть ли вообще внутри этого абзаца хотя бы одна метка Obsidian видео
        if (htmlContent.includes('![[') && (htmlContent.includes('.webm') || htmlContent.includes('.mp4'))) {
            
            // Разделяем содержимое абзаца по переносам строк или тегам <br>, чтобы обработать каждое видео отдельно
            const lines = htmlContent.split(/<br>\n|<br>|\n/);
            
            // Создаем новый блочный контейнер-строку для сетки видеоряда (как в твоем оригинале)
            const container = document.createElement('div');
            container.className = 'video-test-row';
            
            let videosFound = false;

            lines.forEach(line => {
                let cleanLine = line.trim();
                
                // Проверяем, является ли эта конкретная строка ссылкой Obsidian на видео
                if (cleanLine.startsWith('![[') && (cleanLine.endsWith('.webm]]') || cleanLine.endsWith('.mp4]]'))) {
                    
                    // Вытаскиваем чистый путь к файлу из скобок
                    let cleanPath = cleanLine.replace('![[', '').replace(']]', '').trim();
                    cleanPath = cleanPath.replace('../', '').replace('../', ''); // Чистим относительные пути Obsidian
                    
                    if (!cleanPath.startsWith('/')) {
                        cleanPath = '/' + cleanPath;
                    }

                    // Собираем настоящий нативный тег плеера <video>
                    const video = document.createElement('video');
                    video.src = cleanPath;
                    video.controls = true;
                    video.muted = true;
                    video.setAttribute('playsinline', '');
                    
                    // ЖЕСТКИЙ ЗАПРЕТ ТРАФИКА: видео ничего не качает на старте
                    video.preload = "none"; 

                    // Отдаем плеер под контроль ленивому наблюдателю прокрутки
                    videoObserver.observe(video);

                    // Складываем видео в наш контейнер-ряд
                    container.appendChild(video);
                    videosFound = true;
                }
            });

            // Если видеоролики были успешно найдены и собраны в сетку
            if (videosFound) {
                // Вставляем готовый контейнер со всей сеткой видео ПЕРЕД текущим абзацем
                p.parentNode.insertBefore(container, p);
                p.remove(); // Полностью удаляем старый текстовый абзац с сырыми скобками Obsidian
            }
        }
    });
}
