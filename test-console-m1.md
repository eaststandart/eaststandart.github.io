---
layout: default
title: Тест мобильной шапки v1.2
---
<!-- [КЛ] 1: Отступы 0. 2: Логотип и Линия 1 сверху. 3: Текст слогана из синей рамки перенесен в монолитный серый блок в самом низу во всю ширину экрана. -->
<style>
    .mob-header-top-row { display: flex !important; flex-direction: row !important; align-items: flex-start !important; width: 100% !important; box-sizing: border-box !important; padding: 0 !important; gap: 10px !important; background: rgba(0,0,0,0.02) !important; outline: 2px dashed #999 !important; }
    .mob-header-left { flex-shrink: 0 !important; outline: 2px solid #00f !important; }
    .mob-header-left .main-avatar { display: block !important; margin: 0 !important; width: 90px !important; height: 90px !important; box-shadow: 0 0 0 2px #00f !important; }
    .mob-header-content-top { display: flex !important; flex-direction: column !important; flex-grow: 1 !important; min-width: 0 !important; outline: 2px solid #0b0 !important; }
    .mob-line-1 { font-size: 1.05rem !important; font-weight: bold !important; line-height: 1.1 !important; color: var(--text-color, #24292e) !important; margin: 0 !important; padding: 0 !important; text-align: left !important; outline: 1px dotted #f0f !important; }
    /* ИСПРАВЛЕНО: Превращаем нижнюю строку в плотную, красивую серую брендовую плашку во всю ширину */
    .mob-description-gray-block { display: block !important; width: 100% !important; box-sizing: border-box !important; background-color: #f6f8fa !important; border: 1px solid #e1e4e8 !important; border-radius: 6px !important; padding: 8px 12px !important; margin: 12px 0 0 0 !important; font-size: 0.82rem !important; font-weight: normal !important; line-height: 1.3 !important; color: #555 !important; text-align: left !important; outline: 1px dotted #0af !important; }
    .mob-header-hr { border: 0 !important; border-top: 1px solid #eee !important; margin-top: 15px !important; margin-bottom: 20px !important; width: 100% !important; }
</style>
<div style="display: flex !important; flex-direction: column !important; width: 100% !important;">
    <!-- Ряд 1: Логотип и Название -->
    <header class="mob-header-top-row">
        <div class="mob-header-left"><img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar"></div>
        <div class="mob-header-content-top">
            <h1 class="mob-line-1">Творческая лаборатория познавательного развития</h1>
        </div>
    </header>
    <!-- ИСПРАВЛЕНО: Текст из синей рамки упакован в монолитный серый блок-подвал бренда -->
    <div class="mob-description-gray-block">
        [ для тех, кто хочет знать как всё устроено и создавать технологии своими руками ]
    </div>
</div>
<hr class="mob-header-hr">
<div style="font-family: monospace; font-size: 0.9rem; padding: 15px; background: #f9f9f9; border-radius: 6px;">
    <strong>📱 МОБИЛЬНЫЙ ПОЛИГОН v1.2 ОБНОВЛЕН:</strong><br>
    - Текст описания из синей рамки извлечен [0.1].<br>
    - Сформирован монолитный серый блок-плашка в самом низу (`#f6f8fa`) [0.1].<br>
    - Слоган бренда растянут на всю ширину страницы смартфона строго под логотипом [0.1].
</div>
