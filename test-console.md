---
layout: home
title: Тест консоли управления
---

<!-- 
=============================================================================
ТЕСТОВЫЙ МАКЕТ: КОМПАКТНАЯ ШАПКА С ИНЖЕНЕРНЫМ ПУЛЬТОМ (test-console.html)
============================================================================= 
-->

<style>
    /* 1. СТИЛИЗАЦИЯ ОБНОВЛЕННОЙ КОМПАКТНОЙ ШАПКИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important; /* Разносим логотип влево, а пульт вправо */
        width: 100% !important;
        padding: 10px 0 !important;
        margin-bottom: 25px !important;
        border-bottom: 1px solid #eee !important; /* Легкая разделительная черта под шапкой */
    }

    /* Левая зона: Логотип и мини-маркер лаборатории */
    .test-header-left {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }

    .test-header-left .main-avatar {
        width: 60px !important;  /* Компактный размер для экономии высоты экрана */
        height: 60px !important;
        margin: 0 !important;
    }

    .test-brand-name {
        font-family: monospace !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        color: #555 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    /* Правая зона: Наша минималистичная инженерная консоль ввода */
    .test-header-right {
        display: flex !important;
        align-items: center !important;
        flex-grow: 1 !important;
        max-width: 280px !important; /* Ограничиваем длину строки на ПК, чтобы не растягивалась */
    }

    .console-input-wrapper {
        position: relative !important;
        width: 100% !important;
    }

    /* Оформление строки в стиле терминала Linux */
    .console-input-field {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 8px 10px 8px 24px !important; /* Отступ слева под символ приглашения > */
        background-color: #f6f8fa !important;  /* Бледный благородный серый бэкграунд */
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace !important; /* Чистый код-шрифт */
        font-size: 0.85rem !important;
        color: #24292e !important;
        outline: none !important;
        transition: all 0.2s ease !important;
    }

    /* Эффект фокуса: строка подсвечивается синим при клике, как в средах разработки */
    .console-input-field:focus {
        background-color: #fff !important;
        border-color: #2188ff !important;
        box-shadow: 0 0 0 3px rgba(3,102,214,0.3) !important;
    }

    /* Символ-приглашение командной строки > */
    .console-prompt-symbol {
        position: absolute !important;
        left: 10px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        font-family: monospace !important;
        font-size: 0.85rem !important;
        font-weight: bold !important;
        color: #2188ff !important; /* Яркий инженерный синий цвет */
        user-select: none !important;
    }

    /* 2. МОБИЛЬНАЯ АДАПТАЦИЯ ТЕСТОВОЙ ШАПКИ */
    @media (max-width: 600px) {
        .test-header {
            gap: 10px !important;
            padding: 5px 0 !important;
        }
        .test-brand-name {
            display: none !important; /* На смартфонах полностью прячем текст названия, оставляя только иконку */
        }
        .test-header-right {
            max-width: 100% !important; /* Консоль занимает всё оставшееся свободное пространство справа */
        }
    }
</style>

<!-- СБОРКА ОБНОВЛЕННОЙ ШАПКИ ДЛЯ ТЕСТИРОВАНИЯ ВНЕШНЕГО ВИДА -->
<header class="test-header">
    
    <!-- Левая сторона: Логотип сайта + Текст-маркер вместо H1 -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
        <span class="test-brand-name">Творческая лаборатория познавательного развития</span>
    </div>

    <!-- Правая сторона: Консоль ввода системных команд -->
    <div class="test-header-right">
        <div class="console-input-wrapper">
            <span class="console-prompt-symbol">&gt;</span>
            <input type="text" class="console-input-field" placeholder="введите команду..." autocomplete="off" spellcheck="false">
        </div>
    </div>

</header>

<!-- ДЕКОРАТИВНЫЙ ТЕКСТ ДЛЯ ПРОВЕРКИ ВИЗУАЛЬНОГО БАЛАНСА СЕТКИ СТАТЬИ -->
<div class="test-page-content" style="padding: 20px 0; color: #666; font-size: 0.95rem;">
    <p>💡 <strong>Это тестовый макет обновленного интерфейса.</strong></p>
    <p>Посмотрите, как изменились пропорции шапки: длинный заголовок полностью убран [0.1]. Логотип аккуратно сдвинут в левый угол [0.1], а правая пустующая часть на ПК теперь занята стильной строкой ввода команд в стиле терминала Linux [0.1].</p>
    <p>На смартфонах слово «Лаборатория» автоматически скрывается, а строка ввода растягивается рядом с мини-иконкой, благодаря чему весь этот блок занимает всего 50 пикселей высоты [0.1], и основные рабочие разделы сайта сразу поднимутся на первый экран устройства [0.1].</p>
</div>
