---
layout: default
custom_css: ["/assets/css/video.css", "/assets/css/img.css"]
---
{%- comment -%} 
СПЕЦИАЛЬНЫЙ ШАБЛОН: СТАТЬИ И КНИГИ (\_layouts/page.html)
Назначение: Отображение конечных страниц контента (описания роботов, заметки, учебные статьи).
Наследование: Расширяет базовый каркас default.html (автоматически наследует навигацию и подвал).
Компоненты: Возвращает на место блоки тегов, библиографии, источников и логику видео-плееров.
{%- endcomment -%}

<!-- Замена по в медиафайлах src на data-src -->
{% include media-data-src.liquid %}

{%- if page.bibliography -%}
{% comment %} {% endcomment %}
<!-- Универсальный блок библиографии -->
<div class="bibliography-footer">
    <strong>Библиографическое описание:</strong>  
    {%- if page.bibliography.first -%}
        <ol style="margin: 0; padding-left: 25px;">
            {%- for item in page.bibliography -%}
            <li style="margin-bottom: 8px;">{{ item | markdownify | remove: '<p>' | remove: '</p>' }}</li>
            {%- endfor -%}
        </ol>
    {%- else -%}
        {{ page.bibliography | markdownify }}
    {%- endif -%}
</div>
{%- endif -%}

{%- if page.sources -%}
{% comment %} {% endcomment %}
<!-- Универсальный блок онлайн-источников -->
<div class="sources-inline">
    <strong>Источники:</strong> 
    <div class="sources-content">
        {{ page.sources  | markdownify }}
    </div>
</div>
{%- endif -%}

{%- if page.author and page.author != "" -%}
{% comment %} {% endcomment %}
<!-- Блок вывода автора публикации -->
<div class="author-inline">
    <strong>Автор:</strong> 
    <div class="sources-content">
	    {{ page.author}}
    </div>
</div>
{%- endif -%}

{%- if page.tags and page.tags.size > 0 -%}
{% comment %} {% endcomment %}
<!-- Блок кликабельных тегов -->
<div class="tag-container">
    {%- for tag in page.tags -%}
    {%- assign tag_clean = tag | replace: '#', '' | strip -%}
    <a href="{{ '/tags.html' | relative_url }}#{{ tag_clean | slugify }}" class="tag-item">{{ tag_clean }}</a>
    {%- endfor -%}
</div>
{%- endif -%}

{%- if page.discus and page.discus != "" and page.discus != nil and page.discus != false -%}
{% comment %} {% endcomment %}
<!-- Блок комментариев Giscus -->
<div class="discus-inline">
    {%- include discus.liquid -%}
</div>
{%- endif -%}
