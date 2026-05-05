---
layout: default
title: Тест видео в ряд
---

<style>
    .video-test-row {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 15px !important;
        margin: 20px 0 !important;
    }
    .video-test-row video {
        display: block !important;
        height: 250px !important; 
        width: auto !important;   
        flex: 0 0 auto !important; 
        max-width: 100% !important;
        border-radius: 8px !important;
    }
</style>

Текст над видео для проверки отступов.

<div class="video-test-row">
<video src="/projects/1.webm" controls></video>
</div>

Текст над видео для проверки отступов.

<div class="video-test-row">
<video src="/projects/1.webm" controls></video>
<video src="/projects/1.webm" controls></video>
<video src="/projects/1.webm" controls></video>
<video src="/projects/1.webm" controls></video>
</div>

<div class="video-test-row">
<video src="/projects/1.webm" controls></video>
<video src="/projects/1.webm" controls></video>
</div>
