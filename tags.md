---
layout: page
title: Поиск по тегам
---

<div class="tags-page">

<div style="margin-bottom: 15px;">
    <input type="text" id="tag-search" onkeyup="searchTags()" placeholder="🔍 Поиск тега по названию..." 
    style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 0.9rem;">
</div>
    
    <!-- Кнопка управления облаком -->
    <div style="margin-bottom: 20px;">
        <button id="toggle-cloud-btn" onclick="toggleCloud()" style="padding: 8px 15px; background: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; cursor: pointer; font-size: 0.9rem;">
            #️⃣ Показать облако тегов
        </button>
    </div>

    <!-- ПОДКЛЮЧАЕМ НАШ МОНОЛИТНЫЙ LIQUID-МОДУЛЬ ЯДРА ДАННЫХ -->
    {% include tags-logic.liquid %}

</div>

<!-- ПОДКЛЮЧАЕМ ВНЕШНИЙ ИЗОЛИРОВАННЫЙ ФАЙЛ СКРИПТА С КЭШИРОВАНИЕМ -->
<script src="{{ '/assets/js/tags-search.js' | relative_url }}"></script>
