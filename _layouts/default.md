---
about: Глобальный шаблон оформления страниц сайта.
purpose: Базовый скелет для всего сайта (шапка, меню, подвал). Является родительским для шаблонов page, faire, news и т.д.
---
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
     
    <!-- Подключение MathJax  -->
    {% if page.mathjax == true %}
        {%- include mathjax.html -%}
     {% endif %}
</head>

<body>

<div class="content-wrapper">
    <!-- Блок навигации -->
    {% include navigation.liquid %}

    <h1 style="margin-top: 0;">{{ page.title }}</h1>

    <div class="main-content">
        <p class="page-description">{{ page.description }}</p>
        {% comment %} Вывод основного содержимого страницы или дочернего шаблона {% endcomment %}

{%- assign blocks = content | split: '[[' -%}
{%- for block in blocks -%}
  {%- if forloop.first -%}
    {{ block }}
  {%- else -%}
    {%- assign link_and_text = block | split: ']]' -%}
    {%- assign inside_brackets = link_and_text | first -%}
    {%- assign after_brackets = link_and_text | last -%}
    
    {%- if inside_brackets contains '|' -%}
      {{ inside_brackets | split: '|' | last }}{{ after_brackets }}
    {%- else -%}
      {{ inside_brackets }}{{ after_brackets }}
    {%- endif -%}
  {%- endif -%}{%- endfor -%}




    </div>
</div>

<!-- БЛОК ЛИЦЕНЗИИ -->
{% include footer.liquid %}

</body>
</html>
