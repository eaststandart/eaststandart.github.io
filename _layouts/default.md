{%- comment -%} 
ГЛОБАЛЬНЫЙ ШАБЛОН САЙТА: КАРКАС (\_layouts/default.html)
Назначение: Базовый скелет для всего сайта (шапка, меню, подвал).
ВНИМАНИЕ: Очищен от специфики статей (тегов, библиографии, видео-логики).
Наследование: Является родительским для шаблонов page, faire, news и т.д.
{%- endcomment -%}
<!DOCTYPE html> 
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page.title }}</title>
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">

    <!-- Базовые стили для всего сайта -->
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/pagination.css">
    <link rel="stylesheet" href="/assets/css/footnotes.css">
    <link rel="stylesheet" href="/assets/css/giscus.css">

    <!-- Стили страницы или ее родительских шаблонов -->
    {% if page.custom_css %}
      {%- for style in page.custom_css -%}
        <link rel="stylesheet" href="{{ style | relative_url }}">
      {%- endfor -%}
    {%- endif -%}
    {%- if layout.custom_css -%}
      {%- for style in layout.custom_css -%}
        <link rel="stylesheet" href="{{ style | relative_url }}">
      {%- endfor -%}
    {% endif %}

<!-- Mathjax Support --> 
<script type="text/javascript" id="MathJax-script" async src="https://jsdelivr.net"> </script>

</head>

<body>

<div class="content-wrapper">
    <!-- Блок навигации -->
    {% include navigation.liquid %}

    <h1 style="margin-top: 0;">{{ page.title }}</h1>

    <div class="main-content">
        <p class="page-description">{{ page.description }}</p>
        {% comment %} Вывод основного содержимого страницы или дочернего шаблона {% endcomment %}
        {{ content }}
    </div>
</div>

<!-- БЛОК ЛИЦЕНЗИИ -->
{% include footer.liquid %}

</body>
</html>
