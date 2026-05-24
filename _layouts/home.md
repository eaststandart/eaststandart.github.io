{% comment %} 
\==========================================================================
СПЕЦИАЛЬНЫЙ АВТОНОМНЫЙ ШАБЛОН: ГЛАВНАЯ СТРАНИЦА (\_layouts/home.html)
Назначение: Отображение уникального интерфейса главной страницы с широкой сеткой карточек.
Изоляция: Работает полностью независимо от default.html, сохраняя собственную геометрию в 1000px.
Стили: Внутренний тег <\style> содержит правила, которые нужны ТОЛЬКО для главной страницы.
\========================================================================== 
{% endcomment %}

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page.title }}</title>
    <!-- Подключение центральных модулей стилей сайта -->
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/header-desktop.css">
    <link rel="stylesheet" href="/assets/css/pagination.css">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">

    
</head>
<body>

 <!-- Главная верхняя шапка с круглым логотипом -->
<div class="header-desktop-only" style="max-width: 1000px !important; margin: 0 !important;">
    {% include header-desktop.liquid %}
</div>

    <!-- Основной внедряемый Jekyll-контент Главной страницы (из index.md) -->
    {{ content }}

    <!-- Нижняя контентная кнопка перехода в Telegram -->
    <footer class="main-footer">
        <a href="https://t.me" target="_blank" class="tg-button">
            <span>✈️</span> Написать в Telegram
        </a>        
    </footer>

    {% include footer.liquid %}

</body>
</html>
