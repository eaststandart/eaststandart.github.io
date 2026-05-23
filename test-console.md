---
layout: default
title: Тест выравнивания и вытягивания строк
---

<!-- 
=============================================================================
ЭТАЛОННЫЙ МАКЕТ ШАПКИ: МАТЕМАТИЧЕСКАЯ СЕТКА ПО ВЕРХНЕМУ И НИЖНЕМУ КРАЮ
============================================================================= 
-->

<style>
    /* 1. ГЕНЕРАЛЬНАЯ ГЕОМЕТРИЯ КОНТЕЙНЕРА ШАПКИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: flex-start !important; /* Строгая привязка к верхнему краю логотипа */
        width: 100% !important;
        max-width: 1000px !important;
        box-sizing: border-box !important;
        
        /* ПУНКТ 1: Равные падинги по краям страницы */
        padding: 20px 25px !important; 
        margin-bottom: 30px !important;
        border-bottom: 1px solid #eee !important;
        
        /* ПУНКТ 1: Расстояние между логотипом и началом текста равно 25px */
        gap: 25px !important; 
    }

    /* Левый блок: Наш оригинальный логотип */
    .test-header-left {
        flex-shrink: 0 !important;
    }
    
    .test-header-left .main-avatar {
        /* ЗАФИКСИРОВАНО ПО ВЕРТИКАЛЬНОЙ СЕТКЕ (42px текст + 14px воздух + 34px кнопки = 90px) */
        width: 90px !important; 
        height: 90px !important;
        margin: 0 !important;
        display: block !important;
    }

    /* Правый блок: Контентная зона до правого края страницы */
    .test-header-content-zone {
        display: flex !important;
        flex-direction: column !important;
        flex-grow: 1 !important;
        
        /* ЮВЕЛИРНЫЙ ВОЗДУХ: Расстояние между текстовым ярусом и кнопками */
        gap: 14px !important; 
    }

    /* ==========================================================================
       ЯРУС 1 (ВЕРХНИЙ): ВЫТЯГИВАНИЕ ТЕКСТА НА ВСЮ ШИРИНУ (ПУНКТ 2, 4)
       ========================================================================== */
    .header-text-tier {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        height: 42px !important; /* Фиксированная высота верхнего текстового этажа */
        justify-content: space-between !important;
    }

    /* ПУНКТ 4: Название идет строго по верхней грани логотипа */
    .brand-line-1 {
        font-size: 1.3rem !important; 
        font-weight: bold !important;
        line-height: 1.0 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;
        
        /* ПУНКТ 2: Растягиваем заглавные буквы первой строки от края до края */
        text-align: justify !important;
        text-align-last: justify !important;
        width: 100% !important;
    }

    /* Описание под заголовком */
    .brand-description {
        font-size: 1rem !important; 
        font-weight: normal !important;
        line-height: 1.0 !important;
        color: #666 !important;
        margin: 0 !important;
        padding: 0 !important;
        
        /* ПУНКТ 2: Растягиваем строчные буквы второй строки ровно на ту же ширину */
        text-align: justify !important;
        text-align-last: justify !important;
        width: 100% !important;
    }

    /* ==========================================================================
       ЯРУС 2 (НИЖНИЙ): ЕДИНАЯ СТРОКА ИНСТРУМЕНТОВ (ПУНКТ 3, 5)
       ========================================================================== */
    /* ПУНКТ 5: Кнопки привязаны к нижней грани логотипа */
    .header-tools-tier {
        display: flex !important;
        flex-direction: row !important; 
        align-items: center !important;
        gap: 10px !important; 
        width: 100% !important;
        height: 34px !important; /* Фиксированная высота нижнего этажа */
    }

    /* Контейнер для трех кнопок одинаковой ширины (ПУНКТ 3) */
    .tools-buttons-group {
        display: flex !important;
        flex-direction: row !important;
        gap: 10px !important;
        width: 50% !important; /* Занимает ровно половину от общей ширины строки */
        flex-shrink: 0 !important;
    }

    /* Общие стили для трех кнопок */
    .panel-action-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        height: 34px !important; 
        box-sizing: border-box !important;
        padding: 0 !important; /* Падинги убраны, кнопки делят пространство математически */
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        font-family: monospace !important;
        font-size: 0.8rem !important;
        font-weight: bold !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        flex: 1 !important; /* ПУНКТ 3: Все три кнопки имеют абсолютно одинаковую ширину */
    }

    .btn-search { background-color: #f6f8fa !important; color: #555 !important; }
    .btn-search:hover { background-color: #fff !important; color: #2188ff !important; border-color: #2188ff !important; }

    .btn-tg { background-color: #eef7fd !important; color: #0088cc !important; border-color: #b3e0f2 !important; }
    .btn-tg:hover { background-color: #0088cc !important; color: #fff !important; border-color: #0088cc !important; }

    /* Новая кнопка Почты (ПУНКТ 3) */
    .btn-email { background-color: #fcf8e3 !important; color: #a67507 !important; border-color: #fbeed5 !important; }
    .btn-email:hover { background-color: #a67507 !important; color: #fff !important; border-color: #a67507 !important; }

    /* ПУНКТ 3: Строка ввода команд занимает всю оставшуюся вторую половину строки */
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

    /* 2. МОБИЛЬНАЯ АДАПТАЦИЯ (СТРОГИЙ СБРОС ВЫТЯГИВАНИЯ СТРОК) */
    @media (max-width: 900px) {
        .test-header {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 15px !important;
            padding: 15px !important;
        }

        .header-text-tier {
            height: auto !important;
            gap: 6px !important;
        }

        /* На мобильных отключаем вытягивание строк, чтобы не разрывать короткие слова на весь экран телефона */
        .brand-line-1, .brand-description {
            text-align: left !important;
            text-align-last: left !important;
            font-size: 1.2rem !important;
        }
        .brand-description { font-size: 0.95rem !important; }

        .header-tools-tier {
            flex-direction: column !important;
            align-items: stretch !important;
            height: auto !important;
            gap: 8px !important;
        }

        .tools-buttons-group {
            width: 100% !important;
            gap: 8px !important;
        }

        .panel-action-btn, .console-input-wrapper {
            width: 100% !important;
        }
    }
</style>

<!-- СБОРКА ШАПКИ НА ОСНОВЕ МАТЕМАТИЧЕСКИХ ПУНКТОВ 1-6 -->
<header class="test-header">
    
    <!-- Левая сторона: Наш главный оригинальный логотип (Высота ровно 90px) -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
    </div>

    <!-- Правая сторона: Контентная зона до самого правого края страницы -->
    <div class="test-header-content-zone">
        
        <!-- ЯРУС 1 (ВЕРХНИЙ): ТЕКСТОВЫЙ БЛОК (Выровнен по верхней грани логотипа) -->
        <div class="header-text-tier">
            <h1 class="brand-line-1">ТВОРЧЕСКАЯ ЛАБОРАТОРИЯ ПОЗНАВАТЕЛЬНОГО РАЗВИТИЯ</h1>
            <p class="brand-description">для тех, кто хочет знать как все устроено и создавать технологии своими руками</p>
        </div>

        <!-- ЯРУС 2 (НИЖНИЙ): ЛИНЕЙКА ИНСТРУМЕНТОВ (Выровнена по нижней грани логотипа) -->
        <div class="header-tools-tier">
            
            <!-- Группа из трех кнопок одинаковой ширины (50% строки) -->
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

            <!-- Строка ввода команд терминала (Вторые 50% строки до правого края) -->
            <div class="console-input-wrapper">
                <span class="console-prompt-symbol">&gt;</span>
