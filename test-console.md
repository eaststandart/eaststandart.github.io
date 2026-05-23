---
layout: default
title: Тест двухъярусного пульта управления
---

<!-- 
=============================================================================
ТЕСТОВЫЙ МАКЕТ: ДВУХЪЯРУСНАЯ СЕТКА ШАПКИ (ТЕКСТ СВЕРХУ, КНОПКИ СНИЗУ)
============================================================================= 
-->

<style>
    /* 1. ГЕОМЕТРИЯ И ВЫРАВНИВАНИЕ ВСЕЙ ШАПКИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: flex-start !important; /* Прижимаем блоки к верхнему краю для точного контроля высоты */
        width: 100% !important;
        padding: 15px 0 !important;
        margin-bottom: 25px !important;
        border-bottom: 1px solid #eee !important;
        gap: 25px !important; /* Фиксированный зазор между логотипом и контентной зоной */
    }

    /* Левый блок: Наш главный оригинальный логотип */
    .test-header-left {
        flex-shrink: 0 !important;
    }
    .test-header-left .main-avatar {
        margin: 0 !important;
        display: block !important;
    }

    /* Правый блок: Контентная зона, которая занимает всё оставшееся пространство до правого края */
    .test-header-content-zone {
        display: flex !important;
        flex-direction: column !important; /* Делим зону по высоте на два яруса */
        flex-grow: 1 !important;
        gap: 15px !important; /* Дистанция между верхним текстовым ярусом и нижним ярусом кнопок */
    }

    /* ==========================================
       ЯРУС 1 (ВЕРХНИЙ): ТЕКСТОВЫЙ БЛОК
       ========================================== */
    .header-text-tier {
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important; /* Строго выравниваем все буквы по левому краю */
    }

    /* Строка 1: Выровнена по верхней грани логотипа */
    .brand-line-1 {
        font-size: 1.5rem !important; /* Твой оригинальный масштаб H1 */
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: left !important;
    }

    /* Строка 2 */
    .brand-line-2 {
        font-size: 2rem !important; 
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin: 4px 0 0 0 !important;
        padding: 0 !important;
        text-align: left !important;
    }

    /* Серое описание мелким шрифтом под заголовком */
    .brand-description {
        font-size: 0.85rem !important; /* Уменьшенный аккуратный размер */
        font-weight: normal !important;
        color: #666 !important; /* Серый благородный цвет */
        margin: 8px 0 0 0 !important;
        line-height: 1.3 !important;
        text-align: left !important;
    }

    /* ==========================================
       ЯРУС 2 (НИЖНИЙ): ЕДИНАЯ СТРОКА ИНСТРУМЕНТОВ
       ========================================== */
    .header-tools-tier {
        display: flex !important;
        flex-direction: row !important; /* Все инструменты выстраиваются в одну линию под текстом */
        align-items: center !important;
        gap: 10px !important; /* Расстояние между элементами строки */
        width: 100% !important;
    }

    /* Общие стили для компактных кнопок */
    .panel-action-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        height: 34px !important; /* Единая фиксированная высота для всей строки инструментов */
        box-sizing: border-box !important;
        padding: 0 14px !important;
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

    /* Консоль ввода терминала встраивается прямо в общую линию инструментов */
    .console-input-wrapper {
        position: relative !important;
        flex-grow: 1 !important; /* Строка ввода занимает всё оставшееся свободное пространство до правого края страницы */
        max-width: 300px !important; /* Ограничиваем длину консоли, чтобы она не растягивалась избыточно */
    }

    .console-input-field {
        width: 100% !important;
        height: 34px !important; /* Высота идеально совпадает с кнопками */
        box-sizing: border-box !important;
        padding: 0 10px 0 24px !important;
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

    /* 2. МОБИЛЬНАЯ АДАПТАЦИЯ (СПАСЕНИЕ ПЕРВОГО ЭКРАНА) */
    @media (max-width: 900px) {
        .test-header {
            flex-direction: column !important; /* Складываемся вертикально на смартфонах */
            align-items: flex-start !important;
            gap: 15px !important;
            padding: 10px 0 !important;
        }

        .brand-line-1, .brand-line-2 {
            font-size: 1.5rem !important; /* Адаптивное уплотнение крупных букв */
        }

        .header-tools-tier {
            flex-direction: column !important; /* Инструменты на телефонах встают аккуратной стопкой во всю ширину */
            align-items: stretch !important;
            gap: 8px !important;
        }

        .panel-action-btn {
            height: 36px !important;
        }

        .console-input-wrapper {
            max-width: 100% !important;
            width: 100% !important;
        }
        .console-input-field {
            height: 36px !important;
        }
    }
</style>

<!-- СБОРКА ШАПКИ НА ОСНОВЕ ДВУХЪЯРУСНОЙ КОНЦЕПЦИИ -->
<header class="test-header">
    
    <!-- Левая сторона: Твой главный оригинальный логотип -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
    </div>

    <!-- Правая сторона: Контентная зона (Текст сверху, Пульт снизу) -->
    <div class="test-header-content-zone">
        
        <!-- ЯРУС 1: ТЕКСТОВЫЙ БЛОК (Выровнен по верхней грани логотипа) -->
        <div class="header-text-tier">
            <h1 class="brand-line-1">Творческая лаборатория познавательного развития</h1>
            <p class="brand-description">Для тех, кто хочет знать как все устроено и создавать технологии своими руками.</p>
        </div>

        <!-- ЯРУС 2: ЛИНЕЙКА ИНСТРУМЕНТОВ (Выровнена по нижней половине логотипа) -->
        <div class="header-tools-tier">
            
            <!-- Инструмент 1: Поиск -->
            <a href="/tags.html" class="panel-action-btn btn-search">
                <span>#️⃣</span> Поиск по тегам
            </a>
            
            <!-- Инструмент 2: Telegram -->
            <a href="https://t.me" target="_blank" class="panel-action-btn btn-tg">
                <span>✈️</span> Написать в телеграм
            </a>

            <!-- Инструмент 3: Консоль ввода команд (Растягивается до правого края) -->
            <div class="console-input-wrapper">
                <span class="console-prompt-symbol">&gt;</span>
                <input type="text" class="console-input-field" placeholder="введите команду..." autocomplete="off" spellcheck="false">
            </div>

        </div>

    </div>

</header>

<div class="test-page-content" style="padding: 10px 0; color: #555; font-size: 0.95rem;">
    <p>⚙️ <strong>Новая двухъярусная архитектура полностью собрана:</strong></p>
    <ul>
        <li>Текст начинается ровно по верхней грани логотипа, сохраняя оригинальный масштаб `2rem` [0.1].</li>
        <li>Нижняя строка описания сделана более мелкой и серой (`0.85rem`), уплотняя вёрстку [0.1].</li>
        <li>Под текстом сформирован единый горизонтальный ряд инструментов: кнопки и консоль идут плечом к плечу до самого правого края страницы [0.1].</li>
    </ul>
</div>
