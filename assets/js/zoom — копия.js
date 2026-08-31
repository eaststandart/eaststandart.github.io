/**
 * @about Модуль идеального центрированного модального зума (Лайтбокса) для картинок.
 * @purpose Защищает вёрстку от вылетов картинок за края экрана на ПК и смартфонах.
 * @author TechLab
 */

document.addEventListener("DOMContentLoaded", function() {
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    
    // Ищем все кликабельные картинки контента (базовые и журнальные figure)
    const articleImages = document.querySelectorAll(
        ".main-content p img:not(.content-img), .main-content .figure-img img.img-fig"
    );

    articleImages.forEach(img => {
        img.addEventListener("click", function() {
            lightboxImg.src = this.src;
            lightboxImg.alt = this.alt;
            lightbox.classList.add("is-active");
        });
    });

    // Мгновенное закрытие при клике в любую точку оверлея
    lightbox.addEventListener("click", function() {
        lightbox.classList.remove("is-active");
        setTimeout(() => { lightboxImg.src = ""; }, 300);
    });
});
