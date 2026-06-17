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
БЛОК БЕЗОПАСНОЙ СЕРВЕРНОЙ ОПТИМИЗАЦИИ: РАЗДЕЛЬНАЯ ОБРАБОТКА ПО РАСШИРЕНИЯМ
============================================================================= {% endcomment %}

{% comment %} Шаг 1. Сначала изолируем ВИДЕОФАЙЛЫ, переименовав их src в data-src, чтобы они не качались на старте {% endcomment %}
{% assign safe_page_content = content | replace: '.webm"', '.webm" data-video-file="Y"' | replace: '.mp4"', '.mp4" data-video-file="Y"' %}
{% assign safe_page_content = safe_page_content | replace: 'src="github/eaststandart.github.io/faire/', 'data-src="/faire/' | replace: 'src="http://github/eaststandart.github.io/faire/', 'data-src="/faire/' %}

{% comment %} Шаг 2. Теперь обрабатываем только КАРТИНКИ: даем им чистый src и нативный ленивый атрибут {% endcomment %}
{% assign safe_page_content = safe_page_content | replace: 'src="github/eaststandart.github.io/', 'loading="lazy" src="/' | replace: 'src="http://github/eaststandart.github.io/', 'loading="lazy" src="/' %}

{% comment %} Выводим безупречно очищенный HTML контента {% endcomment %}
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
