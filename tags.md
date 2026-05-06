---
layout: page
title: Поиск по тегам
---

{%- assign all_pages = site.pages | concat: site.documents -%}
{%- assign raw_tags = "" -%}{%- for p in all_pages -%}{%- if p.tags -%}{%- for t in p.tags -%}{%- assign raw_tags = raw_tags | append: t | append: "|" -%}{%- endfor -%}{%- endif -%}{%- endfor -%}
{%- assign unique_tags = raw_tags | split: "|" | uniq | sort -%}

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

    <!-- 1. Облако тегов -->
    <div id="tags-cloud" style="display: none; flex-wrap: wrap; gap: 10px; margin-bottom: 30px; padding: 20px; background: #f9f9f9; border-radius: 8px; border: 1px solid #eee;">
        {% for tag in unique_tags %}
            {% assign tag_clean = tag | replace: '#', '' | strip %}
            <!-- Убрали style, добавили класс tag-item и выводим без решетки внутри, так как она добавится через CSS или останется только текстом -->
            <a href="#{{ tag_clean | slugify }}" class="tag-item" onclick="filterTag('{{ tag_clean | slugify }}')">{{ tag_clean }}</a>
        {% endfor %}
    </div>

    <!-- Заголовок выбранного тега -->
    <div id="active-tag-info" style="margin: 20px 0; padding: 15px; border-left: 5px solid #3498db; background: #eef7fd; display: none;">
        <span style="font-size: 1.2rem; color: #2c3e50;">Статьи по тегу: <strong id="tag-label"></strong></span>
        <a href="{{ '/tags.html' | relative_url }}" onclick="resetFilter();" style="margin-left: 20px; font-size: 0.9rem; color: #3498db; text-decoration: underline;">Сбросить</a>
    </div>

    <!-- 2. Списки страниц -->
    <div class="tags-lists">
        {% for tag in unique_tags %}
            {% assign tag_clean = tag | replace: '#', '' | strip %}
            <div class="tag-group" id="{{ tag_clean | slugify }}" style="display: none; margin-bottom: 40px;">
                <ul style="list-style: none; padding: 0;">
                    {% for p in all_pages %}
                        {% if p.tags contains tag %}
                            <li style="margin-bottom: 12px; padding: 10px; border-bottom: 1px solid #f0f0f0;">
                                <a href="{{ p.url | relative_url }}" style="text-decoration: none; color: #3498db; font-weight: 500; font-size: 1.1rem; display: block;">{{ p.title | default: p.url }}</a>
                                <span style="color: #999; font-size: 0.85rem;">Раздел: {{ p.parent_name | default: 'Прочее' }}</span>
                            </li>
                        {% endif %}
                    {% endfor %}
                </ul>
            </div>
        {% endfor %}
    </div>
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
    }
}

function resetFilter() {
    const groups = document.querySelectorAll('.tag-group');
    groups.forEach(g => g.style.display = 'none');
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
