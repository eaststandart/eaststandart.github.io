---
layout: default
title: Тест оригинального логотипа и выравнивания ярусов
---

<!-- 
=============================================================================
ЭТАЛОННЫЙ ТЕСТОВЫЙ МАКЕТ: ПОЛНЫЙ ВОЗВРАТ РАЗМЕРОВ ЛОГОТИПА И КРАЕВЫХ ОТСТУПОВ
============================================================================= 
-->

<style>
    /* 1. ГЕНЕРАЛЬНАЯ ГЕОМЕТРИЯ КОНТЕЙНЕРА ШАПКИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important; /* Натягивает контентную зону ровно на физическую высоту оригинального логотипа */
        width: 100% !important;
        max-width: 1000px !important;
        box-sizing: border-box !important;
        
        /* ПУНКТ 1: Равные внутренние отступы от краев страницы */
        padding: 20px 25px !important; 
        margin-bottom: 30px !important;
        border-bottom: 1px solid #eee !important;
        
        /* ПУНКТ 1: Расстояние от правой стороны логотипа до начала текста равно 25px */
        gap: 25px !important; 
        min-width: 0 !important;
    }

    /* Левый блок: Твой оригинальный логотип */
    .test-header-left {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* ЖЕСТКИЙ ВОЗВРАТ: Размеры логотипа полностью наследуются из оригинальной темы, трогать их нельзя */
    .test-header-left .main-avatar {
        display: block !important;
        margin: 0 !important;
        /* Убраны жесткие width и height в пикселях, масштаб полностью оригинальный */
    }

    /* Правый блок: Вся контентная зона до правого края страницы */
    .test-header-content-zone {
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important; /* ПУНКТ 6: Распределяет текст по верху, а кнопки по низу на равном удалении */
        flex-grow: 1 !important;
        min-width: 0 !important;
    }

    /* ==========================================================================
       ЯРУС 1 (ВЕРХНИЙ): ТЕКСТОВЫЙ БЛОК (ПУНКТ 2, 4)
       ========================================================================== */
    .header-text-tier {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        align-items: flex-start !important;
        /* ПУНКТ 4: Верхний край текста идет строго вровень с верхним краем логотипа */
        margin-top: 0 !important; 
    }

    /* Название: Заглавные буквы, строго в одну строку без переносов */
    .brand-line-1 {
        font-size: 1.3rem !important; /* Возвращен твой масштаб шрифта */
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: nowrap !important;
        
        /* ПУНКТ 2: Текст вытянут на всю ширину (буквы равномерно распределяются до правого края) */
        text-align: justify !important;
        text-align-last: justify !important;
        width: 100% !important;
    }

    /* Описание под заголовком */
    .brand-description {
        font-size: 1rem !important; /* Твой масштаб шрифта описания */
        font-weight: normal !important;
        line-height: 1.2 !important;
        color: #666 !important;
        margin: 4px 0 0 0 !important;
        padding: 0 !important;
        
        /* ПУНКТ 2: Текст вытянут на всю ширину (вровень с верхней строкой контента) */
        text-align: justify !important;
        text-align-last: justify !important;
        width: 100% !important;
    }

    /* ==========================================================================
       ЯРУС 2 (НИЖНИЙ): СТРОКА ИНСТРУМЕНТОВ И ШИРОКАЯ КОНСОЛЬ (ПУНКТ 3, 5)
       ========================================================================== */
    /* ПУНКТ 5: Кнопки идут строго по нижнему краю оригинального логотипа */
    .header-tools-tier {
        display: flex !important;
        flex-direction: row !important; 
        align-items: center !important;
        gap: 10px !important; 
        width: 100% !important;
        height: 34px !important; /* Фиксированная компактная высота элементов */
        margin-bottom: 0 !important;
    }

    /* Фиксированные компактные кнопки, не сжимаются */
    .panel-action-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        height: 34px !important; 
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
        flex-shrink: 0 !important;
    }

    .btn-search { background-color: #f6f8fa !important; color: #555 !important; }
    .btn-search:hover { background-color: #fff !important; color: #2188ff !important; border-color: #2188ff !important; }

    .btn-tg { background-color: #eef7fd !important; color: #0088cc !important; border-color: #b3e0f2 !important; }
    .btn-tg:hover { background-color: #0088cc !important; color: #fff !important; border-color: #0088cc !important; }

    /* ПУНКТ 3: Новая кнопка Почты (все 3 кнопки одинаковой ширины) */
    .btn-email { background-color: #fcf8e3 !important; color: #a67507 !important; border-color: #fbeed5 !important; }
    .btn-email:hover { background-color: #a67507 !important; color: #fff !important; border-color: #a67507 !important; }

    /* ПУНКТ 3: Строка ввода команд занимает всё оставшееся пространство до правого края страницы */
    .console-input-wrapper {
        position: relative !important;
        flex-grow: 1 !important; /* Растягивает инпут до упора вправо */
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

    /* 2. МОБИЛЬНАЯ АДАПТАЦИЯ */
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
        .panel-action-btn, .console-input-wrapper {
            width: 100% !important;
        }
    }
</style>

<!-- СБОРКА ОБНОВЛЕННОЙ ШАПКИ НА ОСНОВЕ ПРАВИЛ 1-6 -->
<header class="test-header">
    
    <!-- Левая сторона: Оригинальный логотип (Размеры полностью возвращены к исходным) -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
    </div>

    <!-- Правая сторона: Стабильная контентная зона до правого края -->
    <div class="test-header-content-zone">
        
        <!-- ЯРУС 1: ТЕКСТ (Выровнен по верхней грани оригинального логотипа) -->
        <div class="header-text-tier">
            <h1 class="brand-line-1">ТВОРЧЕСКАЯ ЛАБОРАТОРИЯ ПОЗНАВАТЕЛЬНОГО РАЗВИТИЯ</h1>
            <p class="brand-description">для тех, кто хочет знать как все устроено и создавать технологии своими руками</p>
        </div>

        <!-- ЯРУС 2: ИНСТРУМЕНТЫ (Выровнены по нижней грани оригинального логотипа) -->
        <div class="header-tools-tier">
            
            <!-- Три фиксированные компактные кнопки одинаковой ширины -->
            <a href="/tags.html" class="panel-action-btn btn-search">
                <span>#️⃣</span> Поиск
            </a>
            <a href="https://t.me" target="_blank" class="panel-action-btn btn-tg">
                <span>✈️</span> Телеграм
            </a>
            <a href="mailto:info@example.com" class="panel-action-btn btn-email">
                <span>✉️</span> Почта
            </a>

            <!-- Полноценная широкая строка ввода (занимает всё свободное место справа до края) -->
            <div class="console-input-wrapper">
                <span class="console-prompt-symbol">&gt;</span>
                <input type="text" class="console-input-field" placeholder="введите команду..." autocomplete="off" spellcheck="false">
            </div>

        </div>

    </div>

</header>
