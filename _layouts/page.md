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
ТОТАЛЬНАЯ СЕРВЕРНАЯ МАСКИРОВКА МЕДИА СТРОГО ДЛЯ ТЕКСТА СТАТЕЙ (ЧЕРЕЗ SPLIT)
Пагинация, авторы и источники выводятся отдельно и физически не могут сломаться!
============================================================================= 
{% endcomment %}

{% comment %} 1. Берем чистый текст статьи из Markdown и разрезаем его по ссылке гитхаба {% endcomment %}
{% assign content_chunks = page.content | split: 'src="github/eaststandart.github.io/' %}
{% assign final_html = "" %}

{% for chunk in content_chunks %}
  {% if forloop.first %}
    {% assign final_html = chunk %}
  {% else %}
    {% if chunk contains '.webm' or chunk contains '.mp4' %}
      {% comment %} Это ВИДЕО: на сервере превращаем в data-src {% endcomment %}
      {% assign final_html = final_html | append: 'data-src="/' | append: chunk %}
    {% else %}
      {% comment %} Это КАРТИНКА: на сервере превращаем в data-src и добавляем loading="lazy" {% endcomment %}
      {% assign final_html = final_html | append: 'loading="lazy" data-src="/' | append: chunk %}
    {% endif %}
  {% endif %}
{% endfor %}

{% comment %} Выводим обработанный текст статьи, превратив Markdown в HTML {% endcomment %}
{{ final_html | markdownify }}


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
