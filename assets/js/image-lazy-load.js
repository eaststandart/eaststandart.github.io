/**
 * @file Модуль лези-лоада картинок для сайта Лаборатории.
 * @description Откладывает загрузку изображений поделок до момента их появления на экране.
 * @author TechLab
 * @version 1.0.0
 */

function runImageLazyLoad() {
    // 1. СОЗДАНИЕ НАБЛЮДАТЕЛЯ СТРОГО ДЛЯ КАРТИНОК
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            // Когда картинка приближается к экрану на 200 пикселей
            if (entry.isIntersecting) {
                const img = entry.target;
                const srcVal = img.getAttribute('data-src') || "";
                
                // Защита: если картинка находится внутри скрытого поста архива, игнорируем ее
                if (img.closest('.media-entry') && img.closest('.media-entry').style.display === 'none') {
                    return; 
                }

                // Переносим data-src в src, активируя нативную загрузку браузера
                if (srcVal) {
                    img.setAttribute('src', srcVal);
                    img.removeAttribute('data-src');
                }
                
                // Снимаем слежку с этой картинки
                observer.unobserve(img);
            }
        });
    }, { 
        rootMargin: "200px", // Зазор из статьи на Хабре: включаем за 200px до появления
        threshold: 0.01
    });

    // 2. НАХОДИМ ТОЛЬКО КАРТИНКИ И СТАВИМ ИХ НА УЧЕТ
    // Ищем все img, у которых есть data-src, но ИСКЛЮЧАЕМ видеофайлы
    document.querySelectorAll('.main-content img[data-src]').forEach(img => {
        const srcVal = img.getAttribute('data-src') || "";
        if (!srcVal.endsWith('.mp4') && !srcVal.endsWith('.webm')) {
            imageObserver.observe(img);
        }
    });
}
