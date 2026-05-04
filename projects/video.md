---
layout: default
title: Пример
tags: [видео, электроника]
sources: "[Публичная библиотека]"
parent_name: "Проекты"
parent_url: "/projects/"
---

---
layout: default
title: Тест видео в ряд
---

<style>
    /* 1. КОНТЕЙНЕР (имитируем поведение параграфа с медиа) */
    .video-test-row {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin: 20px 0;
        align-items: flex-start;
    }

    /* 2. ВИДЕО НА ПК (как фото 250px) */
    .video-test-row video {
        height: 250px !important; /* Фиксируем высоту */
        width: auto !important;   /* Ширина подстроится сама */
        max-width: 100%;
        border-radius: 8px;
        background: #000;
        object-fit: contain;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* 3. МОБИЛЬНАЯ АДАПТАЦИЯ */

    /* Вертикальный режим: видео в столбик на всю ширину */
    @media (max-width: 600px) and (orientation: portrait) {
        .video-test-row {
            flex-direction: column !important;
        }
        .video-test-row video {
            width: 100% !important;
            height: auto !important; /* В столбике высота свободная */
        }
    }

    /* Горизонтальный режим: видео в ряд, но низкие (180px) */
    @media (max-height: 500px) and (orientation: landscape) {
        .video-test-row {
            flex-direction: row !important;
            gap: 10px;
        }
        .video-test-row video {
            height: 180px !important;
            width: auto !important;
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


![](1.webm)

---


<video src="/projects/1.webm" controls></video><video src="1.webm" controls></video><video controls><source src="1.webm" type="video/webm"></video><video controls><source src="/projects/1.webm" type="video/webm"></video>

