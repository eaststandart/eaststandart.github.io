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

    <!-- ПОДКЛЮЧАЕМ НАШ НОВЫЙ МОНОЛИТНЫЙ LIQUID-МОДУЛЬ ЯДРА ДАННЫХ -->
    {% include tags-logic.liquid %}

</div>

<script>

function searchTags() {
    let input = document.getElementById('tag-search').value.toLowerCase();
    let tags = document.querySelectorAll('#tags-cloud .tag-item');
    
    // Если начали писать, разворачиваем облако, если оно было скрыто
    const cloud = document.getElementById('tags-cloud');
    if (input.length > 0) {
        cloud.style.display = 'flex';
        document.getElementById('toggle-cloud-btn').innerText = '🔼 Скрыть облако тегов';
    }

    tags.forEach(tag => {
        let text = tag.innerText.toLowerCase();
        // Если слово совпадает, показываем тег, если нет — скрываем
        tag.style.display = text.includes(input) ? 'inline-flex' : 'none';
    });
}

function toggleCloud() {
    const cloud = document.getElementById('tags-cloud');
    const btn = document.getElementById('toggle-cloud-btn');
    if (cloud.style.display === 'none') {
        cloud.style.display = 'flex';
        btn.innerText = '🔼 Скрыть облако тегов';
    } else {
        cloud.style.display = 'none';
        btn.innerText = '#️⃣ Показать облако тегов';
    }
}

function filterTag(tagSlug) {
    // Скрываем всё
    const groups = document.querySelectorAll('.tag-group');
    groups.forEach(g => g.style.display = 'none');

    // Показываем только выбранный тег
    const target = document.getElementById(tagSlug);
    if (target) {
        target.style.display = 'block';
        document.getElementById('active-tag-info').style.display = 'block';
        document.getElementById('tag-label').innerText = '#' + tagSlug;
        // Скрываем облако после выбора, чтобы не мешало
        document.getElementById('tags-cloud').style.display = 'none';
        document.getElementById('toggle-cloud-btn').innerText = '#️⃣ Показать облако тегов';
        
        // Полноценное обнуление инлайнового маргина у единственной видимой группы
        target.style.setProperty('margin-bottom', '0px', 'important');
    }
}

function resetFilter() {
    const groups = document.querySelectorAll('.tag-group');
    groups.forEach(g => {
        g.style.display = 'none';
        g.style.setProperty('margin-bottom', '40px', 'important');
    });
    document.getElementById('active-tag-info').style.display = 'none';
    document.getElementById('tags-cloud').style.display = 'flex';
}

// Слушаем изменение хэша (когда кликаем по тегу из другой статьи)
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.substring(1);
    if (hash) filterTag(decodeURIComponent(hash));
});

// При первой загрузке
window.addEventListener('load', () => {
    const hash = window.location.hash.substring(1);
    if (hash) {
        filterTag(decodeURIComponent(hash));
    }
});
</script>
