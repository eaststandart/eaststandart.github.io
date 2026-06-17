---
layout: default
custom_css: "/assets/css/video.css"
---
{% comment %} 
СПЕЦИАЛЬНЫЙ ШАБЛОН: СТАТЬИ И КНИГИ (\_layouts/page.html)
Назначение: Отображение конечных страниц контента (описания роботов, заметки, учебные статьи).
Наследование: Расширяет базовый каркас default.html (автоматически наследует навигацию и подвал).
Компоненты: Возвращает на место блоки тегов, библиографии, источников и логику видео-плееров.
{% endcomment %}

{% comment %}

=============================================================================
БЛОК СЕРВЕРНОЙ ОПТИМИЗАЦИИ: ОЧИСТКА ПУТЕЙ И НАТИВНЫЙ LAZY-LOADING
============================================================================= {% endcomment %}

{% comment %} 1. Очищаем пути: намертво срезаем технический корень GitHub для всех медиафайлов {% endcomment %}
{% assign clean_content = content | replace: 'src="github/eaststandart.github.io/', 'src="/' | replace: 'src="http://github/eaststandart.github.io/', 'src="/' %}

{% comment %} 2. Нативная ленивая загрузка для КАРТИНОК: сервер сразу дописывает loading="lazy" {% endcomment %}
{% assign clean_content = clean_content | replace: '<img src="/', '<img loading="lazy" src="/' %}

{% comment %} 3. Защищаем трафик ВИДЕО: маскируем src под data-src и вешаем маркер видео {% endcomment %}
{% assign safe_page_content = clean_content | replace: '.webm"', '.webm" data-video-file="Y"' | replace: '.mp4"', '.mp4" data-video-file="Y"' %}
{% assign safe_page_content = safe_page_content | replace: 'loading="lazy" src="/faire/', 'data-src="/faire/' %}
{% assign safe_page_content = safe_page_content | replace: 'src="/faire/', 'data-src="/faire/' %}

{% comment %} Выводим очищенный и оптимизированный текст статьи {% endcomment %}
{{ safe_page_content }}


<!-- Универсальный блок библиографии -->
{% if page.bibliography %}
<div class="bibliography-footer">
    <strong>Библиографическое описание:</strong>
    
    {% if page.bibliography.first %}
        <ol style="margin: 0; padding-left: 25px;">
            {% for item in page.bibliography %}
            <li style="margin-bottom: 8px;">{{ item | markdownify | remove: '<p>' | remove: '</p>' }}</li>
            {% endfor %}
        </ol>
    {% else %}
        {{ page.bibliography | markdownify }}
    {% endif %}
</div>
{% endif %}

<!-- Универсальный блок онлайн-источников -->
{% if page.sources %}
<div class="sources-inline">
    <strong>Источники:</strong> 
    <div class="sources-content">
        {{ page.sources  | markdownify }}
    </div>
</div>
{% endif %}

<!-- БЛОК ВЫВОДА АВТОРА ПУБЛИКАЦИИ -->
{% if page.author and page.author != "" %}
<div class="author-inline">
    <strong>Автор:</strong> 
    <div class="sources-content">
	    {{ page.author}}
    </div>
</div>
{% endif %}

<!-- Блок кликабельных тегов -->
{% if page.tags and page.tags.size > 0 %}
<div class="tag-container">
    {% for tag in page.tags %}
    {% assign tag_clean = tag | replace: '#', '' | strip %}
    <a href="{{ '/tags.html' | relative_url }}#{{ tag_clean | slugify }}" class="tag-item">{{ tag_clean }}</a>
    {% endfor %}
</div>
{% endif %}

<!-- Блок комментариев Giscus -->
{% if page.discus and page.discus != "" and page.discus != nil and page.discus != false %}
<div class="discus-inline">
    {% include discus.liquid %}
</div>
{% endif %}
