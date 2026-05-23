---
layout: default
title: Тест консоли управления (Оригинальный масштаб)
---

<!-- 
=============================================================================
ТЕСТОВЫЙ МАКЕТ: ВОЗВРАТ К ОРИГИНАЛЬНЫМ МАСШТАБАМ КАРТИНКИ И ШРИФТА ТЕМЫ
============================================================================= 
-->

<style>
    /* 1. ГЕОМЕТРИЯ И ВЫРАВНИВАНИЕ ШАПКИ С ОРИГИНАЛЬНЫМИ МАСШТАБАМИ */
    .test-header {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important; /* Центрируем двухстрочный текст и пульт по горизонтальной оси значка */
        justify-content: flex-start !important;
        width: 100% !important;
        padding: 15px 0 !important;
        margin-bottom: 25px !important;
        border-bottom: 1px solid #eee !important;
        gap: 25px !important;
    }

    /* Левый блок: Прижимаем двухстрочный текст к оригинальному логотипу */
    .test-header-left {
        display: flex !important;
        align-items: center !important; /* Центрирует текст строго по высоте логотипа */
        gap: 20px !important;
    }

    /* ЖЕСТКИЙ ВОЗВРАТ: Логотип получает оригинальный CSS-класс main-avatar без урезания размеров */
    .test-header-left .main-avatar {
        /* Размеры и скругления полностью диктуются оригинальным файлом style.css твоей темы */
        flex-shrink: 0 !important;
        margin: 0 !important;
    }

    /* Контейнер для двух строк оригинального шрифта */
    .test-brand-text-block {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: flex-start !important;
    }

    /* ЖЕСТКИЙ ВОЗВРАТ: Строка 1 наследует оригинальный масштаб шрифта заголовка H1 твоей темы */
    .brand-line-1 {
        font-size: 1.5rem !important; /* Твой оригинальный размер H1 из style.css */
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin: 0 !important;
        padding: 0 !important;
        letter-spacing: normal !important;
        text-align: left !important;
    }

    /* Строка 2: Вторая половина оригинального шрифта */
    .brand-line-2 {
        font-size: 1.5rem !important; /* Масштаб сохраняется, чтобы строки были равноправны */
        font-weight: bold !important;
        line-height: 1.1 !important;
        color: var(--text-color, #24292e) !important;
        margin-top: 4px !important;
        padding: 0 !important;
        letter-spacing: normal !important;
        text-align: left !important;
    }

    /* Правый блок: Минималистичная консоль терминала */
    .test-header-right {
        display: flex !important;
        align-items: center !important;
        flex-grow: 1 !important;
        max-width: 250px !important; /* Компактный пульт в правом углу */
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

    /* 2. ЧИСТАЯ МОБИЛЬНАЯ АДАПТАЦИЯ (БЕЗ УРЕЗАНИЯ КАРТИНКИ) */
    @media (max-width: 900px) {
        .test-header {
            flex-direction: column !important; /* На смартфонах перестраиваемся вертикально */
            align-items: flex-start !important;
            gap: 15px !important;
            padding: 10px 0 !important;
        }

        /* На мобильных сохраняем оригинальный размер картинки темы */
        .test-header-left .main-avatar {
            margin: 0 auto 10px auto !important; /* Центрируем значок, если он не влезает */
        }

        /* Текст на мобильных просто аккуратно переносится по строкам, сохраняя масштаб */
        .brand-line-1, .brand-line-2 {
            font-size: 1.8rem !important; /* Легкое пропорциональное сжатие для мобильного экрана, чтобы текст не вылезал */
            text-align: left !important;
        }

        .test-header-right {
            max-width: 100% !important;
            width: 100% !important;
        }
    }
</style>

<!-- СБОРКА ШАПКИ НА ОСНОВЕ ТВОИХ ОРИГИНАЛЬНЫХ ПРОПОРЦИЙ -->
<header class="test-header">
    
    <!-- Левая сторона: Твой оригинальный логотип + Шрифт 2rem, разбитый на 2 строки -->
    <div class="test-header-left">
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
        <div class="test-brand-text-block">
            <h1 class="brand-line-1">ТВОРЧЕСКАЯ ЛАБОРАТОРИЯ</h1>
            <h1 class="brand-line-2">ПОЗНАВАТЕЛЬНОГО РАЗВИТИЯ</h1>
            Для тех кто хочет создавать<br> технологии своими руками
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

<!-- КОНТЕНТ ДЛЯ ОЦЕНКИ БАЛАНСА -->
<div class="test-page-content" style="padding: 10px 0; color: #444; font-size: 0.95rem; line-height: 1.5;">
    <p>📐 <strong>Текущий статус прототипа:</strong></p>
    <ul>
        <li>Размер картинки-логотипа полностью возвращён к оригинальному масштабу темы [0.1].</li>
        <li>Размер шрифта обеих строк жёстко зафиксирован на исходных <strong>`2rem`</strong> (оригинальный масштаб вашего H1) [0.1].</li>
        <li>Двухстрочный блок текста идеально выровнен по центру горизонтальной оси значка [0.1].</li>
        <li>Справа аккуратно выведена строка пульта управления [0.1].</li>
    </ul>
</div>
