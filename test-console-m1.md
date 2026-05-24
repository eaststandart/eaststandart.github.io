---
layout: default
title: Тест мобильной шапки v1.4
---
<!-- [КЛ] 1: Квадратные углы серой коробки. 2: Логотип и Название прижаты к самому верху. 3: Слоган прижат к самому низу внутри серого прямоугольника. -->
<style>
    /* ИСПРАВЛЕНО: Квадратные углы (border-radius: 0) и жесткое распределение элементов к верху и низу */
    .mob-main-gray-box { display: flex !important; flex-direction: column !important; justify-content: space-between !important; width: 100% !important; box-sizing: border-box !important; background-color: #f6f8fa !important; border: 1px solid #e1e4e8 !important; border-radius: 0px !important; padding: 0 !important; height: 90px !important; min-height: 90px !important; outline: 2px dashed #999 !important; }
    /* Верхний ярус внутри серого прямоугольника: жестко прижат к верху */
    .mob-header-top-row { display: flex !important; flex-direction: row !important; align-items: flex-start !important; width: 100% !important; gap: 10px !important; margin-top: 0 !important; padding: 0 !important; }
    .mob-header-left { flex-shrink: 0 !important; outline: 2px solid #00f !important; }
    .mob-header-left .main-avatar { display: block !important; margin: 0 !important; width: 90px !important; height: 90px !important; box-shadow: 0 0 0 2px #00f !important; }
    .mob-header-content-top { display: flex !important; flex-direction: column !important; flex-grow: 1 !important; min-width: 0 !important; padding-top: 2px !important; outline: 2px solid #0b0 !important; }
    .mob-line-1 { font-size: 1.05rem !important; font-weight: bold !important; line-height: 1.1 !important; color: var(--text-color, #24292e) !important; margin: 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #f0f !important; }
    /* ИСПРАВЛЕНО: Текст второй линии намертво прижат к нижнему краю серого прямоугольника шапки */
    .mob-description-bottom { display: block !important; width: 100% !important; font-size: 0.8rem !important; font-weight: normal !important; line-height: 1.0 !important; color: #666 !important; margin: 0 !important; padding: 0 !important; margin-bottom: 2px !important; text-align: left !important; outline: 1px dotted #0af !important; box-sizing: border-box !important; }
    .mob-header-hr { border: 0 !important; border-top: 1px solid #eee !important; margin-top: 15px !important; margin-bottom: 20px !important; width: 100% !important; }
</style>
<div class="mob-main-gray-box">
    <!-- Ярус 1: Намертво прижат к верху (Логотип и Название) -->
    <div class="mob-header-top-row">
        <div class="mob-header-left"><img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar"></div>
        <div class="mob-header-content-top">
            <h1 class="mob-line-1">Творческая лаборатория познавательного развития</h1>
        </div>
    </div>
    <!-- Ярус 2: Намертво прижат к нижнему срезу серой коробки шапки -->
    <p class="mob-description-bottom">[ для тех, кто хочет знать как всё устроено и создавать технологии своими руками ]</p>
</div>
<hr class="mob-header-hr">
<div style="font-family: monospace; font-size: 0.9rem; padding: 15px; background: #f9f9f9; border-radius: 6px;">
    <strong>📱 МОБИЛЬНЫЙ ПОЛИГОН v1.4 ОБНОВЛЕН:</strong><br>
    - Углы серого прямоугольника сделаны <u>строго квадратными</u> [0.1].<br>
    - Включен прижим: Логотип и Линия 1 коснулись самого верха коробки [0.1].<br>
    - Линия 2 слогана легла ровно на нижний обрез серого прямоугольника контента [0.1].
</div>
