---
layout: default
title: Исправление Концепта v1.0
---
<!-- [КЛ] 1: Отступы 25px. 2: Текст во всю ширину. 3: 3 серые кнопки + консоль. 4: Плотный верх по логотипу. 5: Плотный низ по логотипу. 6: Компенсация заводского зазора шрифта -6px. -->
<style>
    .test-header { display: flex !important; flex-direction: row !important; align-items: stretch !important; width: 100% !important; box-sizing: border-box !important; padding: 0 !important; margin-top: 0 !important; margin-bottom: 0 !important; gap: 25px !important; min-width: 0 !important; outline: 2px dashed #999 !important; background: rgba(0,0,0,0.02) !important; }
    .test-header-left { flex-shrink: 0 !important; display: flex !important; align-items: flex-start !important; outline: 2px solid #00f !important; }
    .test-header-left .main-avatar { display: block !important; margin: 0 !important; box-shadow: 0 0 0 2px #00f !important; background: rgba(0,0,255,0.05) !important; }
    .test-header-content-zone { position: relative !important; display: flex !important; flex-direction: column !important; justify-content: space-between !important; flex-grow: 1 !important; min-width: 0 !important; outline: 2px solid #0b0 !important; background: rgba(0,255,0,0.02) !important; }
    .header-center-red-axis { position: absolute !important; left: 0 !important; right: 0 !important; top: 50% !important; transform: translateY(-50%) !important; height: 1px !important; background-color: #e1e4e8 !important; border: none !important; margin: 0 !important; padding: 0 !important; z-index: 10 !important; pointer-events: none !important; }
    .header-text-tier { display: flex !important; flex-direction: column !important; width: 100% !important; align-items: flex-start !important; padding: 0 !important; margin: 0 !important; outline: 1px dotted #f0f !important; }
    /* ИСПРАВЛЕНО: margin-top: -6px нативно компенсирует пустой внутренний зазор букв и поднимает их ровно на верхнюю грань */
    .brand-line-1 { font-size: 1.28rem !important; font-weight: bold !important; line-height: 1.0 !important; color: var(--text-color, #24292e) !important; margin: -6px 0 0 0 !important; padding: 0 !important; white-space: nowrap !important; text-align: justify !important; text-align-last: justify !important; width: 100% !important; letter-spacing: -0.2px !important; }
    .brand-description { font-size: 0.98rem !important; font-weight: normal !important; line-height: 1.1 !important; color: #666 !important; margin: 6px 0 0 0 !important; padding: 0 !important; text-align: justify !important; text-align-last: justify !important; width: 100% !important; }
    .header-tools-tier { display: flex !important; flex-direction: row !important; align-items: center !important; gap: 15px !important; width: 100% !important; height: 34px !important; margin: 0 !important; padding: 0 !important; outline: 1px dotted #0af !important; }
    .tools-buttons-group { display: flex !important; flex-direction: row !important; gap: 10px !important; width: 50% !important; flex-shrink: 0 !important; }
    .panel-action-btn { display: flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; height: 34px !important; box-sizing: border-box !important; padding: 0 !important; border: 1px solid #e1e4e8 !important; border-radius: 6px !important; font-family: monospace !important; font-size: 0.8rem !important; font-weight: bold !important; text-decoration: none !important; transition: all 0.2s ease !important; cursor: pointer !important; white-space: nowrap !important; flex: 1 !important; background-color: #f6f8fa !important; color: #555 !important; }
    .panel-action-btn:hover { background-color: #fff !important; color: #2188ff !important; border-color: #2188ff !important; }
    .console-input-wrapper { position: relative !important; width: 50% !important; flex-grow: 1 !important; }
    .console-input-field { width: 100% !important; height: 34px !important; box-sizing: border-box !important; padding: 0 10px 0 24px !important; background-color: #f6f8fa !important; border: 1px solid #e1e4e8 !important; border-radius: 6px !important; font-family: "SFMono-Regular", Consolas, monospace !important; font-size: 0.85rem !important; color: #24292e !important; outline: none !important; transition: all 0.2s ease !important; }
    .console-input-field:focus { background-color: #fff !important; border-color: #2188ff !important; box-shadow: 0 0 0 3px rgba(3,102,214,0.3) !important; }
    .console-prompt-symbol { position: absolute !important; left: 10px !important; top: 50% !important; transform: translateY(-50%) !important; font-family: monospace !important; font-size: 0.85rem !important; font-weight: bold !important; color: #2188ff !important; user-select: none !important; }
    .test-header-hr { border: 0 !important; border-top: 1px solid #eee !important; margin-top: 25px !important; margin-bottom: 30px !important; width: 100% !important; }
    .visual-control-panel { padding: 20px !important; background-color: #f9f9f9 !important; border: 1px dashed #ccc !important; border-radius: 8px !important; font-family: monospace !important; font-size: 0.9rem !important; color: #333 !important; }
    .control-title { font-weight: bold !important; color: #d9534f !important; margin-bottom: 12px !important; text-transform: uppercase !important; }
    .control-item { margin-bottom: 6px !important; line-height: 1.4 !important; }
    @media (max-width: 900px) {
        .test-header { flex-direction: column !important; align-items: flex-start !important; gap: 15px !important; padding: 15px !important; }
        .brand-line-1 { white-space: normal !important; font-size: 1.2rem !important; text-align: left !important; text-align-last: left !important; margin: 0 !important; }
        .brand-description { text-align: left !important; text-align-last: left !important; }
        .header-tools-tier { flex-direction: column !important; align-items: stretch !important; height: auto !important; gap: 8px !important; }
        .tools-buttons-group { width: 100% !important; }
        .panel-action-btn, .console-input-wrapper { width: 100% !important; }
    }
</style>
<header class="test-header">
    <div class="test-header-left"><img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar"></div>
    <div class="test-header-content-zone">
        <hr class="header-center-red-axis">
        <div class="header-text-tier">
            <h1 class="brand-line-1">ТВОРЧЕСКАЯ ЛАБОРАТОРИЯ ПОЗНАВАТЕЛЬНОГО РАЗВИТИЯ</h1>
            <p class="brand-description">для тех, кто хочет знать как все устроено и создавать технологии своими руками</p>
        </div>
        <div class="header-tools-tier">
            <div class="tools-buttons-group">
                <a href="/tags.html" class="panel-action-btn btn-search"><span>#️⃣</span> Поиск</a>
                <a href="https://t.me" target="_blank" class="panel-action-btn btn-tg"><span>✈️</span> Телеграм</a>
                <a href="mailto:info@example.com" class="panel-action-btn btn-email"><span>✉️</span> Почта</a>
            </div>
            <div class="console-input-wrapper">
                <span class="console-prompt-symbol">&gt;</span>
                <input type="text" class="console-input-field" placeholder="введите команду..." autocomplete="off" spellcheck="false">
            </div>
        </div>
    </div>
</header>
<hr class="test-header-hr">
<div class="visual-control-panel">
    <div class="control-title">📋 КОНТРОЛЬНЫЙ ЛИСТ ВЫПОЛНЕНИЯ ИНЖЕНЕРНЫХ ПРАВИЛ (Концепт Шапки v1.0 • Компенсация зазора):</div>
    <div class="control-item"><strong>[Пункт 1]</strong> Отступ логотипа от левого края возвращён к стандарту оригинальной темы. Зазор до текста равен точно 25px.</div>
    <div class="control-item"><strong>[Пункт 2]</strong> Текст 1 и 2 строк через свойства justify принудительно натянут на всю доступную ширину до правого края контента "флаг к флагу".</div>
    <div class="control-item"><strong>[Пункт 3]</strong> В ряд инструментов встали 3 серые кнопки одинаковой ширины (50% яруса) + строка ввода консоли до правого края страницы (вторые 50%).</div>
    <div class="control-item"><strong>[Пункт 4]</strong> Первая строка заголовка за счет margin-top: -6px компенсировала зазор глифов и встала ровно по верхней синей кромке.</div>
    <div class="control-item"><strong>[Пункт 5]</strong> Линейка кнопок и инпут консоли прижаты строго к нижней грани оригинального логотипа темы.</div>
    <div class="control-item"><strong>[Пункт 6]</strong> Масштаб логотипа не затрагивается. Тонкая серая ось делит контент ровно посередине аватара.</div>
</div>
