---
layout: default
title: Тест мобильной шапки v1.6
---
<!-- [КЛ] 1: Квадратные углы серой коробки. 2: Полное обнуление padding: 0. 3: Логотип и Линия 1 намертво прижаты к верхнему краю. 4: Линия 2 намертво прижата к нижнему краю. -->
<style>
    /* ИСПРАВЛЕНО: Полное обнуление полей по периметру. Высота коробки автоматически подстраивается под высоту логотипа и Линии 2 */
    .mob-main-gray-box { display: flex !important; flex-direction: column !important; justify-content: space-between !important; width: 100% !important; box-sizing: border-box !important; background-color: #f6f8fa !important; border: 1px solid #e1e4e8 !important; border-radius: 0px !important; padding: 0 !important; margin: 0 !important; gap: 0px !important; outline: 2px dashed #999 !important; }
    /* Верхний ряд: Логотип и Название прижаты строго к верхнему краю */
    .mob-header-top-row { display: flex !important; flex-direction: row !important; align-items: center !important; width: 100% !important; gap: 10px !important; margin: 0 !important; padding: 0 !important; }
    .mob-header-left { flex-shrink: 0 !important; outline: 2px solid #00f !important; }
    .mob-header-left .main-avatar { display: block !important; margin: 0 !important; width: 105px !important; height: 105px !important; box-shadow: 0 0 0 0 #00f !important; }
    .mob-header-content-top { display: flex !important; flex-direction: column !important; flex-grow: 1 !important; min-width: 0 !important; padding-top: 0px !important; outline: 2px solid #0b0 !important; }
    .mob-line-1 { font-size: 1.65rem !important; letter-spacing: -1px; font-weight: bold !important; line-height: 1 !important; color: var(--text-color, #24292e) !important; margin: -7px 0 0 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #f0f !important; }
    /* ИСПРАВЛЕНО: Линия 2 намертво прижата к самому нижнему обрезу серого прямоугольника шапки, margin-bottom: 0 */
    .mob-description-bottom { display: block !important; width: 100% !important; font-size: 0.9rem !important; font-weight: normal !important; line-height: 1.3 !important; color: #555 !important; margin: 0 !important; padding: 4px 0px !important; text-align: justify !important; text-align-last: justify !important; outline: 1px dotted #0af !important; box-sizing: border-box !important; }
    .mob-header-hr { border: 0 !important; border-top: 1px solid #eee !important; margin-top: 15px !important; margin-bottom: 20px !important; width: 100% !important; }
</style>
<div class="mob-main-gray-box">
    <!-- Ярус 1: Логотип (синий) и Линия 1 (зеленый) намертво прижаты к верху и левому краю коробки -->
    <div class="mob-header-top-row">
        <div class="mob-header-left"><img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar"></div>
        <div class="mob-header-content-top">
            <h1 class="mob-line-1">Творческая<br>лаборатория<br>познавательного<br>развития</h1>
        </div>
    </div>
</div>
<hr class="mob-header-hr">
