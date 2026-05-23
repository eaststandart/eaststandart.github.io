---
layout: default
title: Тест пульта управления и кнопок навигации (Вариант 3)
---

<!-- 
=============================================================================
ТЕСТОВЫЙ МАКЕТ ВАРИАНТ 3: ГОРИЗОНТАЛЬНЫЕ КНОПКИ СВЕРХУ + СТРОКА ВВОДА СНИЗУ
============================================================================= 
-->

<style>
    /* 1. ГЕОМЕТРИЯ И ВЫРАВНИВАНИЕ ШАПКИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: flex-start !important; /* Выравниваем левый и правый блоки по верхней линии */
        justify-content: space-between !important;
        width: 100% !important;
        padding: 15px 0 !important;
        margin-bottom: 25px !important;
        border-bottom: 1px solid #eee !important;
        gap: 30px !important;
    }

    /* Левый блок: Оригинальный логотип + Выравнивание текста по левому краю */
    .test-header-left {
        display: flex !important;
        align-items: center !important; /* Внутри левого блока текст центрирован по высоте значка */
        gap: 20px !important;
    }

    .test-header-left .main-avatar {
        flex-shrink: 0 !important;
        margin: 0 !important;
    }

    .test-brand-text-block {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: flex-start !important;
    }

    .brand-line-1 {
        font-size: 1.1rem !important; 
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;

    }

    .brand-line-2 {
        font-size: 0.95rem !important; 
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin: 4px 0 0 0 !important;
        padding: 0 !important;

    }

    .brand-description {
        font-size: 0.8rem !important;
        font-weight: normal !important;
        color: #24292e !important;
        margin: 12px 0 0 0 !important;
        line-height: 1.4 !important;
        max-width: 500px !important;
    }

    /* Правый блок: Двухуровневая горизонтальная панель инструментов */
    .test-header-right-panel {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important; /* Плотный зазор между верхним рядом кнопок и строкой ввода */
        width: 100% !important;
        max-width: 340px !important; /* Немного расширили блок, чтобы две кнопки комфортно встали в ряд */
        flex-shrink: 0 !important;
        margin-top: 5px !important; /* Микро-сдвиг для идеального выравнивания по верху логотипа */
    }

    /* Уровень 1: Горизонтальный ряд для двух кнопок */
    .panel-buttons-row {
        display: flex !important;
        flex-direction: row !important;
        gap: 8px !important; /* Расстояние между кнопками */
        width: 100% !important;
    }

    /* Общие стили для компактных кнопок навигации */
    .panel-action-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        flex: 1 !important; /* Кнопки делят ширину строки строго поровну */
        box-sizing: border-box !important;
        padding: 6px 10px !important; /* Более компактные отступы */
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        font-family: monospace !important;
        font-size: 0.8rem !important;
        font-weight: bold !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        white-space: nowrap !important;
    }

    .btn-search {
        background-color: #f6f8fa !important;
        color: #555 !important;
    }
    .btn-search:hover {
        background-color: #fff !important;
        color: #2188ff !important;
        border-color: #2188ff !important;
    }

    .btn-tg {
        background-color: #eef7fd !important;
        color: #0088cc !important;
        border-color: #b3e0f2 !important;
    }
    .btn-tg:hover {
        background-color: #0088cc !important;
        color: #fff !important;
        border-color: #0088cc !important;
    }

    /* Уровень 2: Консоль ввода терминала */
    .console-input-wrapper {
        position: relative !important;
        width: 100% !important;
    }

    .console-input-field {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 6px 10px 6px 24px !important; /* Сжатые по высоте инпуты */
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

    /* 2. МОБИЛЬНАЯ АДАПТАЦИЯ ШАПКИ */
    @media (max-width: 900px) {
        .test-header {
            flex-direction: column !important; /* На телефонах выстраиваемся вертикально */
            align-items: flex-start !important;
            gap: 20px !important;
            padding: 10px 0 !important;
        }

        .test-header-left {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 15px !important;
        }

        .brand-line-1, .brand-line-2 {
            font-size: 0.7rem !important;
        }

        .test-header-right-panel {
            max-width: 100% !important;
            width: 100% !important;
        }
    }
</style>

<!-- СБОРКА ОБНОВЛЕННОЙ ШАПКИ (ВАРИАНТ 3) -->
<header class="test-header">
    
    <!-- Левая сторона: Твой оригинальный логотип + Выравнивание текста по левому краю -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
        <div class="test-brand-text-block">
            <h1 class="brand-line-1">ТВОРЧЕСКАЯ ЛАБОРАТОРИЯ</h1>
            <h1 class="brand-line-2">ПОЗНАВАТЕЛЬНОГО РАЗВИТИЯ</h1>
            <p class="brand-description">Для тех, кто хочет знать как все устроено<br> и создавать технологии своими руками</p>
        </div>
    </div>

    <!-- Правая сторона: Двухуровневая компактная панель управления -->
    <div class="test-header-right-panel">
        
        <!-- Уровень 1: Поиск и Telegram в один горизонтальный ряд -->
        <div class="panel-buttons-row">
            <a href="/tags.html" class="panel-action-btn btn-search">
                <span>#️⃣</span> Поиск по тегам
            </a>
            <a href="https://t.me" target="_blank" class="panel-action-btn btn-tg">
                <span>✈️</span> Написать в телег
            </a>
        </div>

        <!-- Уровень 2: Строка ввода консоли управления -->
        <div class="console-input-wrapper">
            <span class="console-prompt-symbol">&gt;</span>
            <input type="text" class="console-input-field" placeholder="введите команду..." autocomplete="off" spellcheck="false">
        </div>

    </div>

</header>

<div class="test-page-content" style="padding: 10px 0; color: #555; font-size: 0.95rem;">
    <p>📐 <strong>Панель перестроена точно по вашему описанию:</strong></p>
    <ul>
        <li>Блок управления выровнен по верхней кромке логотипа [0.1].</li>
        <li>Кнопка поиска и кнопка Telegram стоят в одну горизонтальную линию [0.1].</li>
        <li>Нижним этажом под ними аккуратно расположилась строка терминала [0.1].</li>
    </ul>
</div>
