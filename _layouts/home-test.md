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
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">

</head>
<body>

	<!-- Основной внедряемый Jekyll-контент Главной страницы (из index.md) -->
    {{ content }}

</body>
</html>
