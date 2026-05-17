{% comment %} 
ГЛОБАЛЬНЫЙ ШАБЛОН САЙТА: КАРКАС (\_layouts/default.html)
Назначение: Базовый скелет для всего сайта (шапка, меню, подвал).
ВНИМАНИЕ: Очищен от специфики статей (тегов, библиографии, видео-логики).
Наследование: Является родительским для шаблонов page, faire, news и т.д.
{% endcomment %}

<!DOCTYPE html> 
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page.title }}</title>
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">

    <!-- ... БАЗОВЫЕ СТИЛИ ДЛЯ ВСЕГО САЙТА ... -->
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/footnotes.css">

    <!-- УНИВЕРСАЛЬНЫЙ БЛОК: СТИЛИ СТРАНИЦЫ ИЛИ ЕЁ РОДИТЕЛЬСКИХ ШАБЛОНОВ -->
    {% if page.custom_css %}
      {% for style in page.custom_css %}
        <link rel="stylesheet" href="{{ style | relative_url }}">
      {% endfor %}
    {% endif %}
    {% if layout.custom_css %}
      {% for style in layout.custom_css %}
        <link rel="stylesheet" href="{{ style | relative_url }}">
      {% endfor %}
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
        {{ content }}
    </div>

</div>

{% include footer.liquid %}

</body>
</html>
