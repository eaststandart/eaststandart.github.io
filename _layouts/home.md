{% comment %} 
СПЕЦИАЛЬНЫЙ АВТОНОМНЫЙ ШАБЛОН: ГЛАВНАЯ СТРАНИЦА (\_layouts/home.html)
Назначение: Отображение уникального интерфейса главной страницы с широкой сеткой карточек.
Изоляция: Работает полностью независимо от default.html, сохраняя собственную геометрию в 1000px.
Стили: Внутренний тег \<style> содержит правила, которые нужны ТОЛЬКО для главной страницы.
{% endcomment %}

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page.title }}</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <style>
        /* Стили только для главной страницы */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            width: 100%;
            max-width: 1000px;
            margin-top: 0;
        }

        .category-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-top: 8px solid;
            transition: transform 0.2s;
        }
        .category-card:hover { transform: translateY(-5px); }
        .tech-creative { border-top-color: var(--card-tech); }
        .my-projects { border-top-color: var(--card-my); }

        .card-header { display: flex; align-items: center; gap: 15px; margin-bottom: 20px; }
        .section-icon { 
            width: 60px; 
            height: 60px; 
            border-radius: 50%; 
            object-fit: cover; 
            border: 2px solid #eee; 
            background: #fff; 
        }

        /* Красная линия блока */
        .site-news { 
            border-top-color: #cb2431; 
        }

        /* Компактная строка новости */
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

        /* Эффект наведения на всю строку */
        .news-item-compact:hover { 
            background: #fff; 
            border-color: #ddd; 
            padding-left: 18px; 
        }

        /* Дата и стрелочка » */
        .news-item-compact small { 
            flex-shrink: 0; 
            font-family: monospace; 
            color: #6a737d;
            padding-top: 1px; 
            line-height: 1.2;
        }

        /* Ссылка на проект/новость */
        .news-item-compact .item-link { 
            text-decoration: none;
            font-weight: normal;
            transition: 0.2s;
        }

        /* Цвет текста при наведении */
        .news-item-compact:hover .item-link {
            color: #000 !important;
        }
        
        h1 { margin-bottom: 20px !important; }
        h2 { margin: 0; font-size: 1.3rem; color: #333; }
        header { margin-bottom: 10px !important; }
        
        .project-list { list-style: none; padding: 0; margin: 0; }
        .project-list li { margin-bottom: 12px; }
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
        
        .project-list a:hover { 
            background: #fff; 
            color: #000; 
            border-color: #ddd; 
            padding-left: 18px; 
        }

        @media (max-width: 900px) {
            .grid-container {
                max-width: 100% !important;
                gap: 15px; 
            }
            
            .category-card {
                padding: 15px !important; 
            }

            .card-header {
                margin-bottom: 10px !important;
            }
        }
    </style>
</head>
<body>
    <header>
        <img src="/assets/icons/logo.svg" alt="Логотип" class="main-avatar">
        <h1>{{ page.title }}</h1>
    </header>

    {{ content }}

    <footer class="main-footer">
        <a href="https://t.me" target="_blank" class="tg-button">
            <span>✈️</span> Написать в Telegram
        </a>        
    </footer>

    {% include footer.liquid %}

</body>
</html>
