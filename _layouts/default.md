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

{% if content contains '<table>' %}
  {%- assign tables = content | split: '<table>' -%}
  {{ tables[0] }}
  {%- for table_block in tables offset:1 -%}
    {%- assign table_end = table_block | split: '</table>' -%}
    {%- assign table_inside = table_end[0] -%}
    {%- assign table_after = table_end[1] -%}
    
    {%- if table_inside contains '<td>' -%}
      {%- assign cells = table_inside | split: '<td>' -%}
      
      {%- assign first_cell = cells[1] | split: '</td>' | first -%}
      {%- assign text_before_link = first_cell | split: '[[' | first -%}
      {{ text_before_link }}
      
      {%- assign second_cell = cells[2] | split: '</td>' | first -%}
      {%- assign text_after_link = second_cell | replace: ']]', '' -%}
      {{ text_after_link }}
    {%- else -%}
      <table>{{ table_inside }}</table>
    {%- endif -%}
    {{ table_after }}
  {%- endfor -%}
{%- else -%}
  {{ content }}
{% endif %}

    </div>
</div>

<!-- БЛОК ЛИЦЕНЗИИ -->
{% include footer.liquid %}

</body>
</html>
