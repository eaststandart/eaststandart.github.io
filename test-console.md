---
layout: default
title: Тест двухъярусного пульта управления
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
        align-items: stretch !important; /* [Пункт 6] Натягивает контент на высоту оригинального логотипа */
        width: 100% !important;
        box-sizing: border-box !important;
        
        /* [Пункт 1] Полный возврат к оригинальным отступам темы, убираем огромные дыры */
        padding: 0 !important; 
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        
        /* [Пункт 1] Зазор от правой стороны логотипа до начала текста равен точно 25px */
        gap: 25px !important; 
        min-width: 0 !important;
    }

    /* Левый блок: Наш главный оригинальный логотип */
    .test-header-left {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: flex-start !important; /* [Пункт 4] Привязка верха логотипа строго к базовой линии текста */
    }
    
    /* [Пункт 6] МАСШТАБ ЛОГОТИПА: Полностью оригинальный из темы, размеры картинки не затрагиваются */
    .test-header-left .main-avatar {
        display: block !important;
        margin: 0 !important;
    }

    /* Правый блок: Вся контентная зона до правого края страницы */
    .test-header-content-zone {
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important; /* [Пункт 6] Распределяет текст по верху, а кнопки по низу */
        flex-grow: 1 !important;
        min-width: 0 !important;
    }

    /* ==========================================================================
       [Пункт 4] ЯРУС 1 (ВЕРХНИЙ): ТЕКСТОВЫЙ БЛОК (ПРИВЯЗКА К ВЕРХУ ЛОГОТИПА)
       ========================================================================== */
    .header-text-tier {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        align-items: flex-start !important;
    }

    /* Название: Заглавные буквы, строго в одну строку без переносов */
    .brand-line-1 {
        font-size: 1.28rem !important; /* Ювелирный размер для идеального укладывания строки в один ряд */
        font-weight: bold !important;
        line-height: 1.0 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: nowrap !important;
        
        /* [Пункт 2] Вытягиваем заглавные буквы первой строки ровно до правого края страницы */
        text-align: justify !important;
        text-align-last: justify !important;
        width: 100% !important;
        letter-spacing: -0.2px !important;
    }

    /* Описание под заголовком */
    .brand-description {
        font-size: 0.98rem !important; 
        font-weight: normal !important;
        line-height: 1.1 !important;
        color: #666 !important;
        margin: 6px 0 0 0 !important;
        padding: 0 !important;
        
        /* [Пункт 2] Текст второй строки вытянут по ширине до конца страницы вровень с первой */
        text-align: justify !important;
        text-align-last: justify !important;
        width: 100% !important;
    }

    /* ==========================================================================
       [Пункт 5] ЯРУС 2 (НИЖНИЙ): СТРОКА ИНСТРУМЕНТОВ (ПРИВЯЗКА К НИЗУ ЛОГОТИПА)
       ========================================================================== */
    .header-tools-tier {
        display: flex !important;
        flex-direction: row !important; 
        align-items: center !important;
        gap: 15px !important; 
        width: 100% !important;
        height: 34px !important; /* Компактная фиксированная высота элементов */
        margin-bottom: 2px !important; /* [Пункт 5] Выравнивание кнопок точно по нижнему краю аватара темы */
    }

    /* Контейнер для трех кнопок одинаковой ширины (Занимает ровно 50% строки) */
    .tools-buttons-group {
        display: flex !important;
        flex-direction: row !important;
        gap: 10px !important;
        width: 50% !important; 
        flex-shrink: 0 !important;
    }

    /* [Пункт 3] Общие стили для трех кнопок одинаковой ширины */
    .panel-action-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        height: 34px !important; 
        box-sizing: border-box !important;
        padding: 0 !important; 
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        font-family: monospace !important;
        font-size: 0.8rem !important;
        font-weight: bold !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        flex: 1 !important; /* Все 3 кнопки делят свои 50% пространства математически поровну */
    }

    .btn-search { background-color: #f6f8fa !important; color: #555 !important; }
    .btn-search:hover { background-color: #fff !important; color: #2188ff !important; border-color: #2188ff !important; }

    .btn-tg { background-color: #eef7fd !important; color: #0088cc !important; border-color: #b3e0f2 !important; }
    .btn-tg:hover { background-color: #0088cc !important; color: #fff !important; border-color: #0088cc !important; }

    /* Третья кнопка Почты [Пункт 3] */
    .btn-email { background-color: #fcf8e3 !important; color: #a67507 !important; border-color: #fbeed5 !important; }
    .btn-email:hover { background-color: #a67507 !important; color: #fff !important; border-color: #a67507 !important; }

    /* [Пункт 3] Строка ввода команд занимает всю оставшуюся вторую половину (50%) строки контента */
    .console-input-wrapper {
        position: relative !important;
        width: 50% !important; 
        flex-grow: 1 !important;
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

    /* ЛИНИЯ ОТЧЕРКИВАНИЯ ШАПКИ: Настройка зазора, чтобы не прижималась к логотипу */
    .test-header-hr {
        border: 0 !important;
        border-top: 1px solid #eee !important;
        margin-top: 25px !important; /* Создает необходимый чистый воздух под аватаром */
        margin-bottom: 30px !important;
        width: 100% !important;
    }

    /* СТИЛИ ОТОБРАЖЕНИЯ КОНТРОЛЬНОГО ЛИСТА В САМОМ НИЗУ СТРАНИЦЫ */
    .visual-control-panel {
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
        margin-bottom: 12px !important;
        text-transform: uppercase !important;
    }
    .control-item {
        margin-bottom: 6px !important;
        line-height: 1.4 !important;
    }

    /* МОБИЛЬНАЯ АДАПТАЦИЯ */
    @media (max-width: 900px) {
        .test-header {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 15px !important;
            padding: 15px !important;
        }
        .brand-line-1 {
            white-space: normal !important;
            font-size: 1.2rem !important;
            text-align: left !important;
            text-align-last: left !important;
        }
        .brand-description {
            text-align: left !important;
            text-align-last: left !important;
        }
        .header-tools-tier {
            flex-direction: column !important;
            align-items: stretch !important;
            height: auto !important;
            gap: 8px !important;
        }
        .tools-buttons-group {
            width: 100% !important;
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
            <!-- Три фиксированные компактные кнопки одинаковой ширины (Занимают первые 50% строки) -->
            <div class="tools-buttons-group">
                <a href="/tags.html" class="panel-action-btn btn-search">
                    <span>#️⃣</span> Поиск
                </a>
                <a href="https://t.me" target="_blank" class="panel-action-btn btn-tg">
                    <span>✈️</span> Телеграм
                </a>
                <a href="mailto:info@example.com" class="panel-action-btn btn-email">
                    <span>✉️</span> Почта
                </a>
            </div>

            <!-- Широкая строка ввода консоли до самого правого края страницы (Занимает вторые 50% строки) -->
            <div class="console-input-wrapper">
                <span class="console-prompt-symbol">&gt;</span>
                <input type="text" class="console-input-field" placeholder="введите команду..." autocomplete="off" spellcheck="false">
            </div>

        </div>

    </div>

</header>

<!-- ЛИНИЯ ОТЧЕРКИВАНИЯ ШАПКИ (Вынесена наружу, имеет фиксированный зазор от логотипа) -->
<hr class="test-header-hr">

<!-- ВЫВОД КОНТРОЛЬНОГО ЛИСТА В САМОМ КОНЦЕ СТРАНИЦЫ (СТРОГО НИЖЕ ЛИНИИ ОТЧЕРКИВАНИЯ) -->
<div class="visual-control-panel">
    <div class="control-title">📋 КОНТРОЛЬНЫЙ ЛИСТ ВЫПОЛНЕНИЯ ИНЖЕНЕРНЫХ ПРАВИЛ:</div>
    <div class="control-item"><strong>[Пункт 1]</strong> Отступ логотипа от левого края страницы полностью возвращён к оригинальному стандарту вашей главной темы. Лишние огромные дыры удалены. Расстояние от правой стороны логотипа до начала текста равно точно 25px.</div>
    <div class="control-item"><strong>[Пункт 2]</strong> Текст 1 строки («ТВОРЧЕСКАЯ...») и 2 строки («для тех...») через свойства `justify` принудительно натянут на всю доступную ширину до правого края страницы контента, делая строки визуально равными флаг к флагу.</div>
    <div class="control-item"><strong>[Пункт 3]</strong> В ряд инструментов добавлена третья кнопка «Почта». Все 3 кнопки имеют математически равную ширину и занимают ровно 50% яруса, а строка ввода консоли восстановлена и занимает вторые 50% пространства до правого края страницы.</div>
    <div class="control-item"><strong>[Пункт 4]</strong> Первая строка заголовка выровнена пиксель-в-пиксель по верхней грани оригинального логотипа за счет прижатия `align-items: flex-start`.</div>
    <div class="control-item"><strong>[Пункт 5]</strong> Линейка кнопок и инпут консоли идут строго в один уровень по нижней грани оригинального логотипа.</div>
    <div class="control-item"><strong>[Пункт 6]</strong> Масштаб логотипа не затрагивается, элементы распределены по его краям на равном удалении от горизонтальной оси центра. Линия отчеркивания шапки вынесена ниже и получила правильный отступ контента.</div>
</div>
