---
layout: default
title: Тест мобильной шапки v1.0
---

<style>
    /* Базовый контейнер мобильной шапки */
    .mob-header {
        display: flex !important;
        flex-direction: row !important; /* Логотип и текстовая зона идут в одну линию */
        align-items: flex-start !important;
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 0px 0px !important; /* Уплотненные мобильные отступы от краев экрана */
        gap: 15px !important; /* Зазор между иконкой и текстом */
        background: rgba(0,0,0,0.02) !important;
        outline: 2px dashed #999 !important; /* ДЕБАГ-СЕТКА ДЛЯ КОНТРОЛЯ ГЕОМЕТРИИ */
    }

    /* Левый блок: Мобильный уменьшенный аватар */
    .mob-header-left {
        flex-shrink: 0 !important;
        outline: 2px solid #00f !important;
    }
    .mob-header-left .main-avatar {
        display: block !important;
        margin: 0 !important;
        width: 80px !important; /* Компактный мобильный размер значка */
        height: 80px !important;
        box-shadow: 0 0 0 2px #00f !important;
    }

    /* Правый блок: Вся текстовая зона */
    .mob-header-content {
        display: flex !important;
        flex-direction: column !important; /* Строки текста строятся друг под другом */
        flex-grow: 1 !important;
        min-width: 0 !important;
        outline: 2px solid #0b0 !important;
    }

    /* Строка 1: Главное название (идет справа от логотипа вровень с его верхом) */
    .mob-line-1 {
        font-size: 1rem !important; /* Аккуратный мобильный кегль */
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: left !important;
        outline: 1px dotted #f0f !important;
    }

    /* Строка 2: Описание (начинается под первой строкой) */
    .mob-description {
        font-size: 0.8rem !important; /* Уменьшенный шрифт для смартфонов */
        font-weight: normal !important;
        line-height: 1.2 !important;
        color: #666 !important;
        margin: 6px 0 0 0 !important; /* Небольшой вертикальный зазор от первой строки */
        padding: 0 !important;
        text-align: left !important;
        outline: 1px dotted #0af !important;
    }

    /* Тонкая разделительная серая линия под мобильной шапкой */
    .mob-header-hr {
        border: 0 !important;
        border-top: 1px solid #eee !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
        width: 100% !important;
    }
</style>

<!-- СБОРКА СТАРТОВОГО МОБИЛЬНОГО МАКЕТА -->
<header class="mob-header">
    
    <!-- Левая сторона: Компактный логотип 60px -->
    <div class="mob-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
    </div>

    <!-- Правая сторона: Двухуровневый текст -->
    <div class="mob-header-content">
        <h1 class="mob-line-1">Творческая лаборатория познавательного развития</h1>
        <p class="mob-description">[ для тех, кто хочет знать как все устроено и создавать технологии своими руками ]</p>
    </div>

</header>

<hr class="mob-header-hr">

<div style="font-family: monospace; font-size: 0.9rem; padding: 15px; background: #f9f9f9; border-radius: 6px;">
    <strong>📱 МОБИЛЬНЫЙ ПОЛИГОН v1.0 ОТКРЫТ:</strong><br>
    - Конструкция зафиксирована: логотип слева (синий контур) [0.1].<br>
    - Справа идет Линия 1 (пурпурный пунктир) [0.1].<br>
    - Ниже нее встал текст Линии 2 (голубой пунктир) [0.1].<br>
    - Включена рентген-сетка дебага для точного контроля смещений [0.1].
</div>
