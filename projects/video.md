---
layout: default
title: Тест видео в ряд
---

<style>
    /* Уходим от сложных структур, бьем прямо по тегу внутри контейнера */
    .video-test-row {
        display: block !important;
        width: 100% !important;
        margin: 20px 0 !important;
        /* Очищаем любые флоаты */
        clear: both;
    }

    .video-test-row video {
        display: inline-block !important; /* Ставит их в ряд как буквы */
        vertical-align: top !important;
        height: 200px !important; /* Уменьшим чуть-чуть для теста */
        width: auto !important;
        margin-right: 10px !important;
        margin-bottom: 10px !important;
        border-radius: 8px !important;
        background: #000 !important;
    }
</style>

Текст

<div class="video-test-row">
    <video src="/projects/1.webm" controls></video>
    <video src="/projects/1.webm" controls></video>
    <video src="/projects/1.webm" controls></video>
    <video src="/projects/1.webm" controls></video>
</div>

текст

<div class="video-test-row">
    <video src="/projects/1.webm" controls></video>
</div>

текст
