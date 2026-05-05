---
layout: default
title: Тест видео в ряд
---

<style>
    .video-test-row {
        display: block !important;
        width: 100% !important;
        /* Уменьшаем отступы самого контейнера, чтобы не было "дыр" */
        margin: 10px 0 0 0 !important; 
        clear: both;
        line-height: 0; /* Убирает "хвосты" под строчными элементами */
    }

    .video-test-row video {
        display: inline-block !important;
        vertical-align: top !important;
        height: 200px !important; 
        width: auto !important;
        margin-right: 12px !important;
        /* Этот отступ нужен только между рядами видео */
        margin-bottom: 12px !important; 
        border-radius: 8px !important;
        background: #000 !important;
    }

    /* Убираем отступ у текста, который идет сразу после блока видео */
    .video-test-row + p {
        margin-top: 0px !important;
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
