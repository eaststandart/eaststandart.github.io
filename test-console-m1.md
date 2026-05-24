---
layout: default
title: Тест мобильной шапки v1.1
---
<!-- [КЛ] 1: Отступы 0. 2: Логотип 90px слева, Линия 1 названия справа от него. 3: Линия 2 описания перенесена вниз под весь блок во всю ширину экрана. -->
<style>
    .mob-header-top-row { display: flex !important; flex-direction: row !important; align-items: flex-start !important; width: 100% !important; box-sizing: border-box !important; padding: 0 !important; gap: 10px !important; background: rgba(0,0,0,0.02) !important; outline: 2px dashed #999 !important; }
    .mob-header-left { flex-shrink: 0 !important; outline: 2px solid #00f !important; }
    .mob-header-left .main-avatar { display: block !important; margin: 0 !important; width: 90px !important; height: 90px !important; box-shadow: 0 0 0 2px #00f !important; }
    .mob-header-content-top { display: flex !important; flex-direction: column !important; flex-grow: 1 !important; min-width: 0 !important; outline: 2px solid #0b0 !important; }
    .mob-line-1 { font-size: 1.05rem !important; font-weight: bold !important; line-height: 1.1 !important; color: var(--text-color, #24292e) !important; margin: 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #f0f !important; }
    /* ИСПРАВЛЕНО: Описание вынесено в отдельный блок под первый ряд контента и растянуто от края до края экрана смартфона */
    .mob-description-bottom { display: block !important; width: 100% !important; font-size: 0.8rem !important; font-weight: normal !important; line-height: 1.2 !important; color: #666 !important; margin: 10px 0 0 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #0af !important; box-sizing: border-box !important; }
    .mob-header-hr { border: 0 !important; border-top: 1px solid #eee !important; margin-top: 15px !important; margin-bottom: 20px !important; width: 100% !important; }
</style>
<!-- ИСПРАВЛЕНО: Двухуровневая мобильная архитектура вёрстки -->
<div style="display: flex !important; flex-direction: column !important; width: 100% !important;">
    <!-- Ряд 1: Логотип 90px слева, Название Линии 1 справа -->
    <header class="mob-header-top-row">
        <div class="mob-header-left"><img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar"></div>
        <div class="mob-header-content-top">
            <h1 class="mob-line-1">Творческая лаборатория познавательного развития</h1>
        </div>
    </header>
    <!-- Ряд 2: Линия описания перенесена строго вниз под логотип и название во всю ширину -->
    <p class="mob-description-bottom">[ для тех, кто хочет знать как всё устроено и создавать технологии своими руками ]</p>
</div>
<hr class="mob-header-hr">
<div style="font-family: monospace; font-size: 0.9rem; padding: 15px; background: #f9f9f9; border-radius: 6px;">
    <strong>📱 МОБИЛЬНЫЙ ПОЛИГОН v1.1 ОБНОВЛЕН:</strong><br>
    - Код уплотнен, пустые строки удалены [0.1].<br>
    - Логотип и Линия 1 названия идут в верхнем горизонтальном ряду [0.1].<br>
    - Линия 2 описания (голубой пунктир) перенесена в самый низ под весь блок на полную ширину страницы [0.1].
</div>
