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
       
    <!-- Глобальные базовые стили сайта (остаются всегда) -->
    <link rel="stylesheet" href="/assets/css/style.css">
    <!-- Подключение центральных модулей стилей сайта -->
    <link rel="stylesheet" href="/assets/css/pagination.css">

	<!-- Автоматическое подключение стилей шапки в зависимости от выбранной темы -->
	{% if page.header_theme == "panel" %}
	    <link rel="stylesheet" href="{{ '/assets/css/header-panel.css' | relative_url }}">
	{% else %}
	    <link rel="stylesheet" href="{{ '/assets/css/header-classic.css' | relative_url }}">
	{% endif %}

    <style>
    
        /* ==========================================================================
           1. СЕТКА ГЛАВНОГО КОНТЕЙНЕРА КАРТОЧЕК
           ========================================================================== */
        .grid-container {
            display: grid;
            /* Автоматическое перестроение колонок при минимальной ширине карточки 320px */
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            width: 100%;
            max-width: 1000px;
            margin-top: 0;
        }

        /* Базовая стилизация отдельной карточки-раздела */
        .category-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-top: 8px solid; /* Цвет верхней рамки задаётся ниже через переменные */
            transition: transform 0.2s;
        }
        
        /* Визуальный интерактивный подъём карточки при наведении */
        .category-card:hover { 
            transform: translateY(-5px); 
        }

        /* Привязка цветов верхних рамок карточек к переменным :root */
        .tech-creative { border-top-color: var(--card-tech); }
        .my-projects { border-top-color: var(--card-my); }
        
        /* ИСПРАВЛЕНО: Красная рамка карточки новостей теперь берётся из центральной переменной */
        .site-news { border-top-color: var(--card-news); }

        /* Шапка внутри карточки (Иконка + Заголовок H2) */
        .card-header { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
            margin-bottom: 20px; 
        }
        
        /* Круглые брендовые мини-иконки разделов */
        .section-icon { 
            width: 60px; 
            height: 60px; 
            border-radius: 50%; 
            object-fit: cover; 
            border: 2px solid #eee; 
            background: #fff; 
        }


        /* ==========================================================================
           2. СТИЛИЗАЦИЯ СТРОК ОБНОВЛЕНИЙ И КНОПОК СПИСКА
           ========================================================================== */

        /* Плашка компактной строки новости в карточке "Что нового?" */
        .news-item-compact { 
            display: flex; 
            align-items: flex-start; 
            margin-bottom: 4px !important; 
            font-size: 0.9rem; 
            line-height: 1.2; 
            padding: 3px 8px; 
            border-radius: 6px; 
            background: #f9f9f9;
            transition: 0.2s;
            border: 1px solid transparent;
        }

        /* Эффект расширения и подсветки плашки новости при наведении */
        .news-item-compact:hover { 
            background: #fff; 
            border-color: #ddd; 
            padding-left: 18px; 
        }

        /* Текстовый контейнер даты внутри плашки */
        .news-item-compact small { 
            flex-shrink: 0; 
            font-family: monospace; 
            color: #6a737d;
            padding-top: 1px; 
            line-height: 1.2;
        }

        /* Внутренняя ссылка на публикацию */
        .news-item-compact .item-link { 
            text-decoration: none;
            font-weight: normal;
            transition: 0.2s;
        }

        /* Затемнение текста ссылки при наведении на всю площадь плашки */
        .news-item-compact:hover .item-link {
            color: #000 !important;
        }
        
        /* Параметры шрифтов и заголовков */
        h2 { margin: 0; font-size: 1.3rem; color: #333; }
        
        /* Стилизация списков внутренних ссылок в карточках */
        .project-list { list-style: none; padding: 0; margin: 0; }
        .project-list li { margin-bottom: 12px; }
        
        /* Кнопка-ссылка на внутренний раздел */
        .project-list a {
            text-decoration: none;
            color: #555;
            display: flex;
            align-items: center;
            padding: 10px;
            border-radius: 8px;
            background: #f9f9f9;
            transition: 0.2s;
            border: 1px solid transparent;
        }
        
        /* Анимация смещения ссылки списка вбок при наведении */
        .project-list a:hover { 
            background: #fff; 
            color: #000; 
            border-color: #ddd; 
            padding-left: 18px; 
        }


        /* ==========================================================================
           3. МОБИЛЬНАЯ АДАПТАЦИЯ ШАБЛОНА ГЛАВНОЙ СТРАНИЦЫ
           ========================================================================== */
        @media (max-width: 900px) {
            /* Перевод контейнера в резиновый мобильный full-width режим */
            .grid-container {
                max-width: 100% !important;
                gap: 15px; 
            }
            
            /* Уплотнение внутренних воздушных полей карточек на смартфонах */
            .category-card {
                padding: 15px !important; 
            }

            /* Уменьшение отступа шапки карточки */
            .card-header {
                margin-bottom: 10px !important;
            }
        }

/* ========================================== 4. ЗНАЧКИ СВЯЗИ В НОВОСТЯХ ========================================== */
.social-badge-wrapper{margin-left:auto;display:flex;gap:10px;align-items:center;}
.social-badge-click{display:block;width:32px;height:32px;border-radius:50%;background-size:55% !important;background-position:center !important;background-repeat:no-repeat !important;box-shadow:0 2px 6px rgba(0,0,0,0.1);transition:transform 0.2s,box-shadow 0.2s;}
.social-badge-click.github-brand{background-color:#24292e;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://w3.org' viewBox='0 0 24 24' fill='%23fff'%3E%3Cpath d='M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12'%3E%3C/path%3E%3C/svg%3E");}
.social-badge-click.telegram-brand{background-color:#24A1DE;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://w3.org' viewBox='0 0 24 24' fill='%23fff'%3E%3Cpath d='M23.912 2.41a.5.5 0 0 0-.5-.154L.435 10.158a.5.5 0 0 0-.083.924l5.526 2.1 2.8 8.6a.5.5 0 0 0 .823.18l3.66-3.66 4.7 3.52a.5.5 0 0 0 .8-.3l4.25-18.5a.5.5 0 0 0-.1-.432zm-5.26 4.67l-10.4 6.64-1.33-4.13 11.73-2.51zm-10.4 7.64l1.64 5.08-.43-5.08 1.4-1.4z'/%3E%3C/svg%3E");}
.social-badge-click:hover{transform:translateY(-2px) scale(1.05);box-shadow:0 4px 10px rgba(0,0,0,0.18);}
.social-badge-click:active{transform:scale(0.95);}
@media (max-width:900px){.social-badge-click{width:28px;height:28px;}.social-badge-wrapper{gap:8px;}}



    </style>
</head>
<body>

	{% include header-theme.liquid %}
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
