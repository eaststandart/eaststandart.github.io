/* ==========================================================================
   УНИВЕРСАЛЬНЫЙ МОДУЛЬ КОНВЕРТАЦИИ ОБСИДИАН-ВИДЕО И СЕТОК (video-lazy-load.js)
   ========================================================================== */

function runVideoLazyLoad() {
    // 1. СОЗДАНИЕ НАБЛЮДАТЕЛЯ (INTERSECTION OBSERVER) ДЛЯ ЛЕНИВОЙ ЗАГРУЗКИ ВИДЕО
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
        // Настройка зазора: триггер загрузки сработает за 200px до появления видео в поле зрения
        rootMargin: "200px" 
    });

    // ==========================================================================
    // 2. АНАЛИЗ АБЗАЦЕВ И КОНВЕРТАЦИЯ ССЫЛОК ОБСИДИАНА В ТЕГИ VIDEO С СЕТКАМИ
    // ==========================================================================
    const paragraphs = document.querySelectorAll('.main-content p');

    paragraphs.forEach(p => {
        const htmlContent = p.innerHTML.trim();

        // Проверяем, есть ли вообще внутри этого абзаца хотя бы одна метка Obsidian видео
        if (htmlContent.includes('![[') && (htmlContent.includes('.webm') || htmlContent.includes('.mp4'))) {
            
            // Разделяем содержимое абзаца по переносам строк или тегам <br>, чтобы обработать каждое видео отдельно
            const lines = htmlContent.split(/<br>\n|<br>|\n/);
            
            // Создаем новый блочный контейнер-строку для видеоряда (твоя оригинальная сетка)
            const container = document.createElement('div');
            container.className = 'video-test-row';
            
            let videosFound = false;

            lines.forEach(line => {
                let cleanLine = line.trim();
                
                // Проверяем, является ли эта конкретная строка ссылкой Obsidian на видео
                if (cleanLine.startsWith('![[') && (cleanLine.endsWith('.webm]]') || cleanLine.endsWith('.mp4]]'))) {
                    
                    // Вытаскиваем чистый путь к файлу из скобок
                    let rawPath = cleanLine.replace('![[', '').replace(']]', '').trim();
                    
                    // ВЫРЕЗАЕМ ТЕХНИЧЕСКИЙ КОРЕНЬ ОБСИДИАНА ПО ТВОЕМУ ТРЕБОВАНИЮ
                    let cleanPath = rawPath.replace('github/eaststandart.github.io', '').trim();
                    
                    // Если после вырезания путь начинается не со слэша, добавляем его для корня сайта
                    if (!cleanPath.startsWith('/')) {
                        cleanPath = '/' + cleanPath;
                    }

                    // Собираем настоящий нативный тег плеера <video>
                    const video = document.createElement('video');
                    video.src = cleanPath; // Сюда прилетает идеальный веб-путь: /faire/проект/файл.webm
                    video.controls = true;
                    video.muted = true;
                    video.setAttribute('playsinline', ''); // Фикс для Safari на iOS
                    
                    // КРИТИЧЕСКИ ВАЖНО: Полностью блокируем загрузку данных для экономии трафика
                    video.preload = "none"; 

                    // Передаем созданный плеер под контроль нашему ленивому наблюдателю
                    videoObserver.observe(video);

                    // Добавляем плеер в строку-контейнер
                    container.appendChild(video);
                    videosFound = true;
                }
            });

            // Если видеоролики были успешно найдены и собраны в сетку
            if (videosFound) {
                // Выносим готовый контейнер с видео из абзаца наружу, вставив его ПЕРЕД текущим абзацем
                p.parentNode.insertBefore(container, p);
                p.remove(); // Полностью удаляем старый текстовый абзац с сырыми скобками Obsidian
            }
        }
    });
}
