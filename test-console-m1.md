---
layout: default
title: Тест мобильной шапки v1.5
---
<!-- [КЛ] 1: Квадратные углы серой коробки. 2: Логотип, Линия 1 и Линия 2 ЖЕСТКО ЗАПЕРТЫ ВНУТРИ одной серой плашки. 3: Высота коробки подстраивается автоматически, исключая вылеты текста наружу. -->
<style>
    /* ИСПРАВЛЕНО: Полный монолит. Убрана жесткая высота 90px. Включена авто-высота с внутренними полями padding: 12px */
    .mob-main-gray-box { display: flex !important; flex-direction: column !important; width: 100% !important; box-sizing: border-box !important; background-color: #f6f8fa !important; border: 1px solid #e1e4e8 !important; border-radius: 0px !important; padding: 12px !important; gap: 12px !important; outline: 2px dashed #999 !important; }
    /* Верхний ряд внутри серой коробки: Логотип и Название */
    .mob-header-top-row { display: flex !important; flex-direction: row !important; align-items: flex-start !important; width: 100% !important; gap: 12px !important; }
    .mob-header-left { flex-shrink: 0 !important; outline: 2px solid #00f !important; }
    .mob-header-left .main-avatar { display: block !important; margin: 0 !important; width: 90px !important; height: 90px !important; box-shadow: 0 0 0 2px #00f !important; }
    .mob-header-content-top { display: flex !important; flex-direction: column !important; flex-grow: 1 !important; min-width: 0 !important; padding-top: 2px !important; outline: 2px solid #0b0 !important; }
    .mob-line-1 { font-size: 1.05rem !important; font-weight: bold !important; line-height: 1.1 !important; color: var(--text-color, #24292e) !important; margin: 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #f0f !important; }
    /* ИСПРАВЛЕНО: Линия 2 лежит строго внутри серого контейнера, растягиваясь под логотипом и названием до границ плашки */
    .mob-description-bottom { display: block !important; width: 100% !important; font-size: 0.82rem !important; font-weight: normal !important; line-height: 1.3 !important; color: #555 !important; margin: 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #0af !important; box-sizing: border-box !important; }
    .mob-header-hr { border: 0 !important; border-top: 1px solid #eee !important; margin-top: 15px !important; margin-bottom: 20px !important; width: 100% !important; }
</style>
<!-- ВСЕ ЭЛЕМЕНТЫ БРЕНДА НАМЕРТВО ЗАПЕРТЫ ВНУТРИ ЕДИНОЙ СЕРОЙ ПЛАШКИ -->
<div class="mob-main-gray-box">
    <!-- Ярус 1: Логотип (синий контур) и Название (зеленый контур) -->
    <div class="mob-header-top-row">
        <div class="mob-header-left"><img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar"></div>
        <div class="mob-header-content-top">
            <h1 class="mob-line-1">Творческая лаборатория познавательного развития</h1>
        </div>
    </div>
    <!-- Ярус 2: Слоган (голубой контур) идет внизу, но железно ЗАШИТ ВНУТРИ серой коробки шапки -->
    <p class="mob-description-bottom">[ для тех, кто хочет знать как всё устроено и создавать технологии своими руками ]</p>
</div>
<hr class="mob-header-hr">
<div style="font-family: monospace; font-size: 0.9rem; padding: 15px; background: #f9f9f9; border-radius: 6px;">
    <strong>📱 МОБИЛЬНЫЙ ПОЛИГОН v1.5 ЗАФИКСИРОВАН:</strong><br>
    - Ошибка вылета текста устранена нативно за счет авто-высоты [0.1].<br>
    - Углы серого прямоугольника темы строго квадратные (`border-radius: 0`) [0.1].<br>
    - Логотип, Линия 1 и Линия 2 лежат <u>СТРОГО ВНУТРИ одной серой коробки</u> [0.1].
</div>
