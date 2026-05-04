---
layout: default
title: Тест видео в ряд
---

<style>
    /* 1. КОНТЕЙНЕР */
    .video-test-row {
        display: flex !important;
        flex-direction: row !important; /* Принудительно в ряд */
        flex-wrap: nowrap;             /* Запрещаем перенос на новую строку для теста */
        overflow-x: auto;              /* Если не влезут — появится боковой скролл, но они останутся в ряд */
        gap: 15px;
        margin: 20px 0;
        align-items: flex-start;
    }

    /* 2. ВИДЕО НА ПК */
    .video-test-row video {
        /* Устанавливаем высоту и ЗАПРЕЩАЕМ видео диктовать свою ширину */
        height: 250px !important; 
        width: auto !important;   
        flex: 0 0 auto !important; /* Важно: не дает видео растягиваться */
        max-width: 48%;            /* Чтобы два видео гарантированно влезли в ряд */
        border-radius: 8px;
        background: #000;
        object-fit: contain;
    }

    /* 3. МОБИЛЬНАЯ АДАПТАЦИЯ (Тут всё остается как было) */
    @media (max-width: 600px) and (orientation: portrait) {
        .video-test-row {
            flex-direction: column !important;
            overflow-x: visible;
        }
        .video-test-row video {
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
        }
    }
</style>


<p>Текст над видео для проверки отступов.</p>

<div class="video-test-row">
    <!-- Замени пути на реальные файлы для проверки -->
    <video src="1.webm" controls></video>
    <video src="1.webm" controls></video>
</div>

<p>Текст под видео.</p>

