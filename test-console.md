---
layout: default
title: Тест оригинального логотипа и выравнивания ярусов
---

<!-- 
=============================================================================
ЭТАЛОННЫЙ ТЕСТОВЫЙ МАКЕТ С ВЫВОДОМ КОНТРОЛЬНОГО ЛИСТА ВНИЗУ СТРАНИЦЫ
============================================================================= 
-->

<style>
    /* 1. ГЕНЕРАЛЬНАЯ ГЕОМЕТРИЯ КОНТЕЙНЕРА ШАПКИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important; /* Натягивает контент на физическую высоту оригинального логотипа */
        width: 100% !important;
        box-sizing: border-box !important;
        
        /* ПУНКТ 1: Полный возврат к оригинальным левым и правым отступам темы, убираем огромные дыры */
        padding: 0 !important; 
        margin-top: 0 !important;
        margin-bottom: 30px !important;
        border-bottom: 1px solid #eee !important;
        
        /* Расстояние от правой стороны логотипа до начала текста */
        gap: 15px !important; 
        min-width: 0 !important;
    }

    /* Левый блок: Твой оригинальный логотип */
    .test-header-left {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: flex-start !important; /* Прижимает верх логотипа строго к базовой линии вёрстки */
    }
    
    /* МАСШТАБ ЛОГОТИПА: Полностью оригинальный из темы, убраны любые пиксельные рамки */
    .test-header-left .main-avatar {
        display: block !important;
        margin: 0 !important;
    }

    /* Правый блок: Вся контентная зона до правого края страницы */
    .test-header-content-zone {
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important; /* Распределяет текст по верху, а кнопки по низу */
        flex-grow: 1 !important;
        min-width: 0 !important;
        padding-top: 2px !important; /* Тончайшее выравнивание букв точно по верхней грани логотипа */
    }

    /* ==========================================================================
       ЯРУС 1 (ВЕРХНИЙ): ТЕКСТОВЫЙ БЛОК (ПУНКТ 4)
       ========================================================================== */
    .header-text-tier {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        align-items: flex-start !important;
    }

    /* Название: Заглавные буквы, строго в одну строку, БЕЗ вылезаний за край страницы */
    .brand-line-1 {
        /* Умный адаптивный шрифт: плавно сжимается, если экран монитора становится уже */
        font-size: clamp(1.1rem, 2vw, 1.3rem) !important; 
        font-weight: bold !important;
        line-height: 1.0 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: left !important;
        white-space: nowrap !important; /* Запрещает перенос слов заголовка */
        letter-spacing: -0.4px !important; /* Уплотненный чертежный трекинг букв */
    }

    /* Описание под заголовком: Строго в одну строку, вровень с верхней */
    .brand-description {
        font-size: clamp(0.85rem, 1.5vw, 0.95rem) !important; 
        font-weight: normal !important;
        line-height: 1.0 !important;
        color: #666 !important;
        margin: 6px 0 0 0 !important;
        padding: 0 !important;
        text-align: left !important;
        white-space: nowrap !important; /* Запрещает перенос слов описания на вторую строчку */
        letter-spacing: -0.2px !important;
    }

    /* ==========================================================================
       ЯРУС 2 (НИЖНИЙ): СТРОКА ИНСТРУМЕНТОВ (ПУНКТ 5)
       ========================================================================== */
    .header-tools-tier {
        display: flex !important;
        flex-direction: row !important; 
        align-items: center !important;
        gap: 10px !important; 
        width: 100% !important;
        height: 34px !important; /* Компактная фиксированная высота */
        margin-bottom: 4px !important; /* Выравнивание строго по нижней кромке аватара темы */
    }

    /* Финксированные компактные кнопки */
    .panel-action-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        height: 34px !important; 
        box-sizing: border-box !important;
        padding: 0 12px !important; 
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        font-family: monospace !important;
        font-size: 0.8rem !important;
        font-weight: bold !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important;
    }

    .btn-search { background-color: #f6f8fa !important; color: #555 !important; }
    .btn-search:hover { background-color: #fff !important; color: #2188ff !important; border-color: #2188ff !important; }

    .btn-tg { background-color: #eef7fd !important; color: #0088cc !important; border-color: #b3e0f2 !important; }
    .btn-tg:hover { background-color: #0088cc !important; color: #fff !important; border-color: #0088cc !important; }

    /* Третья кнопка Почты одинаковой ширины с остальными */
    .btn-email { background-color: #fcf8e3 !important; color: #a67507 !important; border-color: #fbeed5 !important; }
    .btn-email:hover { background-color: #fcf8e3 !important; color: #2188ff !important; border-color: #2188ff !important; }

    /* Строка ввода команд терминала растягивается до правого края страницы */
    .console-input-wrapper {
        position: relative !important;
        flex-grow: 1 !important; 
        min-width: 150px !important;
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

    /* БЛОК ОТОБРАЖЕНИЯ КОНТРОЛЬНОГО ЛИСТА ВНИЗУ СТРАНИЦЫ */
    .visual-control-panel {
        margin-top: 50px !important;
        padding: 20px !important;
        background-color: #f9f9f9 !important;
        border: 1px dashed #ccc !important;
        border-radius: 8px !important;
        font-family: monospace !important;
        font-size: 0.9rem !important;
        color: #333 !important;
    }
    .control-title {
        font-weight: bold !important;
        color: #d9534f !important;
        margin-bottom: 10px !important;
        text-transform: uppercase !important;
    }
    .control-item {
        margin-bottom: 6px !important;
        line-height: 1.4 !important;
    }

    /* МОБИЛЬНАЯ АДАПТАЦИЯ (СПАСЕНИЕ ПЕРВОГО ЭКРАНА СМАРТФОНОВ) */
    @media (max-width: 900px) {
        .test-header {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 15px !important;
        }
        .brand-line-1, .brand-description {
            white-space: normal !important;
            text-align: left !important;
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

<!-- СБОРКА ОБНОВЛЕННОЙ ШАПКИ НА ОСНОВЕ ПРАВИЛ -->
<header class="test-header">
    
    <!-- Левая сторона: Оригинальный логотип темы (Отступы от края страницы возвращены к стандарту) -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
    </div>

    <!-- Правая сторона: Стабильная контентная зона до правого края -->
    <div class="test-header-content-zone">
        
        <!-- ЯРУС 1: ТЕКСТ (Выровнен точно по верхней грани оригинального логотипа) -->
        <div class="header-text-tier">
            <h1 class="brand-line-1">ТВОРЧЕСКАЯ ЛАБОРАТОРИЯ ПОЗНАВАТЕЛЬНОГО РАЗВИТИЯ</h1>
            <p class="brand-description">для тех, кто хочет знать как все устроено и создавать технологии своими руками</p>
        </div>

        <!-- ЯРУС 2: ИНСТРУМЕНТЫ (Выровнены точно по нижней грани оригинального логотипа) -->
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

            <!-- Широкая строка ввода консоли до самого правого края страницы -->
            <div class="console-input-wrapper">
                <span class="console-prompt-symbol">&gt;</span>
