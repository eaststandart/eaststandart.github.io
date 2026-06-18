/* ==========================================================================
   ИЗОЛИРОВАННЫЙ МОДУЛЬ ЛЕЗИ-ЛОАДА ВИДЕОПЛЕЕРОВ (video-lazy-load.js)
   ========================================================================== */

function runVideoLazyLoad() {
    // 1. СОЗДАНИЕ НАБЛЮДАТЕЛЯ СТРОГО ДЛЯ ВИДЕОРОЛИКОВ
    const videoObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            // Когда видео-заглушка приближается к экрану на 200 пикселей
            if (entry.isIntersecting) {
                const img = entry.target;
                const srcVal = img.getAttribute('data-src') || "";
                
                // Защита: если элемент находится внутри скрытого поста архива, игнорируем его
                if (img.closest('.media-entry') && img.closest('.media-entry').style.display === 'none') {
                    return; 
                }

                if (srcVal && (srcVal.endsWith('.mp4') || srcVal.endsWith('.webm'))) {
                    // Создаем оригинальный контейнер-строку для твоей флекс-сетки
                    const container = document.createElement('div');
                    container.className = 'video-test-row';

                    // Собираем настоящий нативный тег плеера <video>
                    const video = document.createElement('video');
                    video.src = srcVal;
                    video.controls = true;
                    video.muted = true;
                    video.setAttribute('playsinline', ''); // Фикс для Safari на iOS
                    video.preload = "metadata"; // Загружаем превью и длину ролика строго на экране

                    container.appendChild(video);
                    
                    // Находим родительский абзац p и аккуратно выносим плеер наружу
                    const parentP = img.closest('p');
                    if (parentP) {
                        parentP.insertAdjacentElement('beforebegin', container);
                        img.remove(); // Стираем старую картинку-заглушку
                        if (parentP.textContent.trim() === "" && parentP.querySelectorAll('*').length === 0) {
                            parentP.remove(); // Зачищаем пустой абзац
                        }
                    }
                }
                
                // Снимаем слежку с этого элемента
                observer.unobserve(img);
            }
        });
    }, { 
        rootMargin: "200px", // Зазор из статьи на Хабре: включаем за 200px до появления
        threshold: 0.01
    });

    // 2. НАХОДИМ ТОЛЬКО ВИДЕО-ЗАГЛУШКИ И СТАВИМ ИХ НА УЧЕТ
    // Ищем все img с data-src, которые ведут на видеофайлы
    document.querySelectorAll('.main-content img[data-src]').forEach(img => {
        const srcVal = img.getAttribute('data-src') || "";
        if (srcVal.endsWith('.mp4') || srcVal.endsWith('.webm')) {
            videoObserver.observe(img);
        }
    });
}
