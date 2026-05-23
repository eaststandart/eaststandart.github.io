---
layout: default
title: Тест консоли управления (Вариант 2)
---

<!-- 
=============================================================================
ТЕСТОВЫЙ МАКЕТ ВАРИАНТ 2: ОРИГИНАЛЬНЫЙ ЛОГОТИП И ДВУХСТРОЧНЫЙ ЗАГЛОВОК
============================================================================= 
-->

<style>
    /* 1. ГЕОМЕТРИЯ И ВЫРАВНИВАНИЕ ШАПКИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important; /* Намертво центрирует текст и консоль по горизонтальной оси значка */
        justify-content: space-between !important;
        width: 100% !important;
        padding: 15px 0 !important;
        margin-bottom: 25px !important;
        border-bottom: 1px solid #eee !important;
        gap: 20px !important;
    }

    /* Левый блок: Сохраняем логотип и прижимаем к нему двухстрочный текст */
    .test-header-left {
        display: flex !important;
        align-items: center !important; /* Центрирует двухстрочный блок по высоте логотипа */
        gap: 15px !important;
    }

    /* Размер логотипа остается оригинальным, как на вашей Главной */
    .test-header-left .main-avatar {
        width: 80px !important; /* Твой оригинальный брендовый размер */
        height: 80px !important;
        margin: 0 !important;
        flex-shrink: 0 !important;
    }

    /* Контейнер для двух строк текста */
    .test-brand-text-block {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        line-height: 1.2 !important;
    }

    /* Строка 1 */
    .brand-line-1 {
        font-family: monospace !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        color: #222 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    /* Строка 2 */
    .brand-line-2 {
        font-family: monospace !important;
        font-size: 0.85rem !important;
        font-weight: normal !important;
        color: #666 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-top: 2px !important;
    }

    /* Правый блок: Минималистичная консоль терминала */
    .test-header-right {
        display: flex !important;
        align-items: center !important;
        flex-grow: 1 !important;
        max-width: 250px !important; /* Компактный размер для правого угла */
    }

    .console-input-wrapper {
        position: relative !important;
        width: 100% !important;
    }

    .console-input-field {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 8px 10px 8px 24px !important;
        background-color: #f6f8fa !important;
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        font-family: "SFMono-Regular", Consolas, monospace !important;
        font-size: 0.85rem !important;
        color: #24292e !important;
        outline: none !important;
        transition: all 0.2s ease !important;
    }

    .console-input-field:focus {
        background-color: #fff !important;
        border-color: #2188ff !important;
        box-shadow: 0 0 0 3px rgba(3,102,214,0.3) !important;
    }

    .console-prompt-symbol {
        position: absolute !important;
        left: 10px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        font-family: monospace !important;
        font-size: 0.85rem !important;
        font-weight: bold !important;
        color: #2188ff !important;
        user-select: none !important;
    }

    /* 2. МОБИЛЬНАЯ АДАПТАЦИЯ (УМНОЕ СЖАТИЕ) */
    @media (max-width: 768px) {
        .test-header {
            flex-direction: column !important; /* На смартфонах выстраиваем элементы друг под другом */
            align-items: flex-start !important;
            gap: 15px !important;
            padding: 10px 0 !important;
        }

        /* Логотип на мобильных чуть-чуть уменьшаем, чтобы он не съедал пол-экрана */
        .test-header-left .main-avatar {
            width: 55px !important;
            height: 55px !important;
        }

        .brand-line-1 { font-size: 0.85rem !important; }
        .brand-line-2 { font-size: 0.75rem !important; }

        .test-header-right {
            max-width: 100% !important; /* Строка ввода растягивается во всю ширину экрана телефона */
            width: 100% !important;
        }
    }
</style>

<!-- СБОРКА ОБНОВЛЕННОЙ ШАПКИ (ВАРИАНТ 2) -->
<header class="test-header">
    
    <!-- Левая сторона: Оригинальный логотип + Двухстрочный текст с центрированием -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
        <div class="test-brand-text-block">
            <span class="brand-line-1">Творческая лаборатория</span>
            <span class="brand-line-2">познавательного развития</span>
        </div>
    </div>

    <!-- Правая сторона: Минималистичный пульт консоли -->
    <div class="test-header-right">
        <div class="console-input-wrapper">
            <span class="console-prompt-symbol">&gt;</span>
            <input type="text" class="console-input-field" placeholder="введите команду..." autocomplete="off" spellcheck="false">
        </div>
    </div>

</header>

<!-- СЕТКА ДЛЯ ПРОВЕРКИ ВИЗУАЛЬНОГО БАЛАНСА -->
<div class="test-page-content" style="padding: 10px 0; color: #444; font-size: 0.95rem; line-height: 1.5;">
    <p>📐 <strong>Оцените геометрию Варианта №2:</strong></p>
    <ul>
        <li>Значок остался крупным, как вы и просили [0.1].</li>
        <li>Текст разбился на две строчки («Творческая лаборатория» и «познавательного развития») [0.1].</li>
        <li>Обе строки идеально сцентрированы по горизонтальной оси (посередине) круглого логотипа [0.1].</li>
        <li>Справа аккуратно встала строка пульта управления, завершая баланс [0.1].</li>
    </ul>
    <p>На смартфонах элементы перестраиваются вертикально, но за счёт компактных шрифтов и плотных падингов вся шапка занимает в два раза меньше места, освобождая первый экран под рабочие разделы [0.1].</p>
</div>
