---
layout: default
title: Тест мобильной шапки v1.3
---
<!-- [КЛ] 1: Отступы 0. 2: Логотип и Название вверху. 3: Слоган бренда опущен вниз, но ВСЁ находится СТРОГО ВНУТРИ единого серого прямоугольника шапки. -->
<style>
    /* ИСПРАВЛЕНО: Возвращаем единый, общий серый прямоугольник для всей мобильной шапки целиком */
    .mob-main-gray-box { display: flex !important; flex-direction: column !important; width: 100% !important; box-sizing: border-box !important; background-color: #f6f8fa !important; border: 1px solid #e1e4e8 !important; border-radius: 6px !important; padding: 12px !important; gap: 12px !important; outline: 2px dashed #999 !important; /* ДЕБАГ-СЕТКА ВСЕЙ СЕРОЙ КОРОБКИ */ }
    /* Верхний ярус внутри серого прямоугольника: Логотип и Линия 1 */
    .mob-header-top-row { display: flex !important; flex-direction: row !important; align-items: flex-start !important; width: 100% !important; gap: 12px !important; }
    .mob-header-left { flex-shrink: 0 !important; outline: 2px solid #00f !important; }
    .mob-header-left .main-avatar { display: block !important; margin: 0 !important; width: 90px !important; height: 90px !important; box-shadow: 0 0 0 2px #00f !important; }
    .mob-header-content-top { display: flex !important; flex-direction: column !important; flex-grow: 1 !important; min-width: 0 !important; outline: 2px solid #0b0 !important; }
    .mob-line-1 { font-size: 1.05rem !important; font-weight: bold !important; line-height: 1.1 !important; color: var(--text-color, #24292e) !important; margin: 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #f0f !important; }
    /* ИСПРАВЛЕНО: Текст второй линии опущен в самый низ, но жестко заперт внутри общего серого прямоугольника */
    .mob-description-bottom { display: block !important; width: 100% !important; font-size: 0.82rem !important; font-weight: normal !important; line-height: 1.3 !important; color: #555 !important; margin: 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #0af !important; box-sizing: border-box !important; }
    .mob-header-hr { border: 0 !important; border-top: 1px solid #eee !important; margin-top: 15px !important; margin-bottom: 20px !important; width: 100% !important; }
</style>
<!-- ИСПРАВЛЕНО: Логотип, Линия 1 и Линия 2 собраны ВНУТРИ одного серого блока-контейнера -->
<div class="mob-main-gray-box">
    <!-- Ярус 1: Логотип (синий) и Линия 1 названия (зеленый) плечом к плечу -->
    <div class="mob-header-top-row">
        <div class="mob-header-left"><img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar"></div>
        <div class="mob-header-content-top">
            <h1 class="mob-line-1">Творческая лаборатория познавательного развития</h1>
        </div>
    </div>
    <!-- Ярус 2: Текст слогана опущен вниз под них на всю ширину, но не выходит за рамки серой коробки -->
    <p class="mob-description-bottom">[ для тех, кто хочет знать как всё устроено и создавать технологии своими руками ]</p>
</div>
<hr class="mob-header-hr">
<div style="font-family: monospace; font-size: 0.9rem; padding: 15px; background: #f9f9f9; border-radius: 6px;">
    <strong>📱 МОБИЛЬНЫЙ ПОЛИГОН v1.3 ОБНОВЛЕН:</strong><br>
    - Структура возвращена обратно на 100% [0.1].<br>
    - Логотип, Линия 1 и Линия 2 теперь лежат <u>СТРОГО ВНУТРИ одной серой коробки</u> сайта [0.1].<br>
    - Слоган бренда перенесён в самый низ этой общей коробки на полную ширину экрана [0.1].
</div>
