/**
 * @about Модуль идеального центрированного модального зума (Лайтбокса) для картинок.
 * @purpose Защищает вёрстку от вылетов картинок за края экрана на ПК и смартфонах.
 *          🔥 Исправлен баг срезания углов контента у вертикальных изображений.
 * @author TechLab
 */

document.addEventListener("DOMContentLoaded", function() {
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    
    // Намертво вырываем оверлей из контейнера статьи и переносим в корень body
    if (lightbox) {
        document.body.appendChild(lightbox);
    }
    
    // Ищем все кликабельные картинки контента (базовые и журнальные figure)
    const articleImages = document.querySelectorAll(
        ".main-content p img:not(.content-img), .main-content .figure-img img.img-fig"
    );

    articleImages.forEach(img => {
        img.addEventListener("click", function() {
            lightboxImg.src = this.src;
            lightboxImg.alt = this.alt;
            
            // 🔥 ТВОЯ ЛОГИКА: Проверяем, является ли картинка вертикальной
            if (this.classList.contains("img-v") || this.src.includes("-v") || this.naturalHeight > this.naturalWidth) {
                // Если картинка вертикальная — вешаем класс ужимания СТРОГО НА САМУ КАРТИНКУ
                lightboxImg.classList.add("img-v-zoom");
            } else {
                // Если горизонтальная — снимаем
                lightboxImg.classList.remove("img-v-zoom");
            }
            
            lightbox.classList.add("is-active");
        });
    });

    // Мгновенное закрытие при клике в любую точку оверлея
    if (lightbox) {
        lightbox.addEventListener("click", function() {
            lightbox.classList.remove("is-active");
            if (lightboxImg) {
                lightboxImg.classList.remove("img-v-zoom"); // Сбрасываем класс ужимания картинки
            }
            setTimeout(() => { lightboxImg.src = ""; }, 300);
        });
    }
});
