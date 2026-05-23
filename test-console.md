---
layout: default
title: Исправление вёрстки шапки и консоли
---

<!-- 
=============================================================================
ЭТАЛОННЫЙ ТЕСТОВЫЙ МАКЕТ: ИСПРАВЛЕНИЕ ПЕРЕНOСОВ И СЖАТИЯ КОНСОЛИ
============================================================================= 
-->

<style>
    /* 1. ГЕНЕРАЛЬНАЯ ГЕОМЕТРИЯ КОНТЕЙНЕРА ШАПКИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: flex-start !important; /* Строгая привязка элементов к верхнему краю логотипа */
        width: 100% !important;
        max-width: 1000px !important;
        box-sizing: border-box !important;
        padding: 20px 25px !important; 
        margin-bottom: 30px !important;
        border-bottom: 1px solid #eee !important;
        gap: 25px !important; /* Расстояние от логотипа до контента */
    }

    /* Левый блок: Твой оригинальный логотип (Размеры строго зафиксированы) */
    .test-header-left {
        flex-shrink: 0 !important;
    }
    .test-header-left .main-avatar {
        width: 90px !important; /* Твой оригинальный размер, не трогаем */
        height: 90px !important;
        margin: 0 !important;
        display: block !important;
    }

    /* Правый блок: Вся контентная зона шапки */
    .test-header-content-zone {
        display: flex !important;
        flex-direction: column !important;
        flex-grow: 1 !important;
        gap: 16px !important; /* Фиксированный зазор между текстом и кнопками */
        min-width: 0 !important; /* Защита от распирания сетки */
    }

    /* ==========================================================================
       ЯРУС 1 (ВЕРХНИЙ): ТЕКСТОВЫЙ БЛОК (СТРОГО В ОДНУ СТРОКУ)
       ========================================================================== */
    .header-text-tier {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        align-items: flex-start !important;
    }

    /* Название: Железно в одну строку без переносов */
    .brand-line-1 {
        font-size: 1.15rem !important; /* Скорректированный размер для идеального вхождения */
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: left !important;
        white-space: nowrap !important; /* НАМЕРТВО ЗАПРЕЩАЕТ ПЕРЕНОС СЛОВ НА ВТОРУЮ СТРОКУ */
        letter-spacing: -0.3px !important; /* Плотное аккуратное сжатие букв */
    }

    /* Описание под заголовком */
    .brand-description {
        font-size: 0.95rem !important; 
        font-weight: normal !important;
        line-height: 1.2 !important;
        color: #666 !important;
        margin: 6px 0 0 0 !important;
        padding: 0 !important;
        text-align: left !important;
    }

    /* ==========================================================================
       ЯРУС 2 (НИЖНИЙ): СТРОКА ИНСТРУМЕНТОВ И ШИРОКАЯ КОНСОЛЬ
       ========================================================================== */
    .header-tools-tier {
        display: flex !important;
        flex-direction: row !important; 
        align-items: center !important;
        gap: 10px !important; /* Зазор между элементами в строке */
        width: 100% !important;
        height: 34px !important;
    }

    /* Компактные фиксированные кнопки (больше не сжимаются и не ломают вёрстку) */
    .panel-action-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        height: 34px !important; 
        box-sizing: border-box !important;
        padding: 0 12px !important; /* Аккуратные падинги */
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        font-family: monospace !important;
        font-size: 0.8rem !important;
        font-weight: bold !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important; /* Запрещает кнопкам сжиматься в микро-размеры */
    }

    .btn-search { background-color: #f6f8fa !important; color: #555 !important; }
    .btn-search:hover { background-color: #fff !important; color: #2188ff !important; border-color: #2188ff !important; }

    .btn-tg { background-color: #eef7fd !important; color: #0088cc !important; border-color: #b3e0f2 !important; }
    .btn-tg:hover { background-color: #0088cc !important; color: #fff !important; border-color: #0088cc !important; }

    .btn-email { background-color: #fcf8e3 !important; color: #a67507 !important; border-color: #fbeed5 !important; }
    .btn-email:hover { background-color: #a67507 !important; color: #fff !important; border-color: #a67507 !important; }

    /* Консоль ввода команд занимает ВСЁ свободное место до правого края страницы */
    .console-input-wrapper {
        position: relative !important;
        flex-grow: 1 !important; /* Растягивает консоль до упора вправо */
        min-width: 150px !important; /* Минимальный защитный размер строки */
    }

    .console-input-field {
        width: 100% !important;
        height: 34px !important; 
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

    /* 2. МОБИЛЬНАЯ АДАПТАЦИЯ */
    @media (max-width: 900px) {
        .test-header {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 15px !important;
            padding: 15px !important;
        }
        .brand-line-1 {
            white-space: normal !important; /* На смартфонах разрешаем перенос заголовка */
            font-size: 1.2rem !important;
        }
        .header-tools-tier {
            flex-direction: column !important;
            align-items: stretch !important;
            height: auto !important;
            gap: 8px !important;
        }
        .panel-action-btn, .console-input-wrapper {
            width: 100% !important;
        }
    }
</style>

<!-- СБОРКА ИСПРАВЛЕННОЙ ШАПКИ -->
<header class="test-header">
    
    <!-- Левая сторона: Оригинальный логотип -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
    </div>

    <!-- Правая сторона: Стабильная контентная зона -->
    <div class="test-header-content-zone">
        
        <!-- ЯРУС 1: ТЕКСТ (Выровнен по верхней грани логотипа) -->
        <div class="header-text-tier">
            <h1 class="brand-line-1">ТВОРЧЕСКАЯ ЛАБОРАТОРИЯ ПОЗНАВАТЕЛЬНОГО РАЗВИТИЯ</h1>
            <p class="brand-description">для тех, кто хочет знать как все устроено и создавать технологии своими руками</p>
        </div>

        <!-- ЯРУС 2: ИНСТРУМЕНТЫ (Выровнены по нижней грани логотипа) -->
        <div class="header-tools-tier">
            
            <!-- Три фиксированные компактные кнопки -->
            <a href="/tags.html" class="panel-action-btn btn-search">
                <span>#️⃣</span> Поиск
            </a>
            <a href="https://t.me" target="_blank" class="panel-action-btn btn-tg">
                <span>✈️</span> Телеграм
            </a>
            <a href="mailto:info@example.com" class="panel-action-btn btn-email">
                <span>✉️</span> Почта
            </a>

            <!-- Полноценная широкая строка ввода (занимает всё свободное место справа) -->
            <div class="console-input-wrapper">
                <span class="console-prompt-symbol">&gt;</span>
                <input type="text" class="console-input-field" placeholder="введите команду..." autocomplete="off" spellcheck="false">
            </div>

        </div>

    </div>

</header>
