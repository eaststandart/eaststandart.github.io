---
about: Шаблон главной страницы сайта.
purpose: Отображение интерфейса главной страницы с широкой сеткой карточек. Работает полностью независимо от default.md, сохраняя собственную геометрию в 1000px. Внутренний тег <\style> содержит правила, которые нужны ТОЛЬКО для главной страницы.
---
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
	{%- if page.header_theme == "panel" -%}
	    <link rel="stylesheet" href="{{ '/assets/css/header-panel.css' | relative_url }}">
	{%- else -%}
	    <link rel="stylesheet" href="{{ '/assets/css/header-classic.css' | relative_url }}">
	{%- endif -%}

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

		/* ==========================================
		   4. ЗНАЧКИ СВЯЗИ В НОВОСТЯХ
		   ========================================== */

		.social-badge-wrapper {
		    margin-left: auto !important;
		    display: flex !important;
		    align-items: center !important;
		    gap: 10px !important;
		}
		
		.social-badge-click {
		    display: inline-flex !important; 
		    align-items: center !important;
		    justify-content: center !important;
		    line-height: 0 !important;
		    cursor: pointer !important;
		    
		    /* Значок изначально на 100% яркий и статичный */
		    opacity: 1 !important; 
		    
		    /* Плавное изменение только для прозрачности */
		    transition: opacity 0.2s ease !important; 
		}
		
		/* Эффект при наведении курсора: значок просто плавно тускнеет */
		.social-badge-click:hover {
		    opacity: 0.6 !important; 
		}
		
		/* Эффект при клике (нажатии) */
		.social-badge-click:active {
		    opacity: 0.4 !important; 
		}
		
		/* GitHub */
		
		.social-github {
		    width: 30px !important;
		    height: 30px !important;
		    display: flex !important;
		    align-items: center !important;
		    justify-content: center !important;
		    border-radius: 50% !important;
		    box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
		    overflow: hidden !important;
		}
		
		.social-github .social-img-brand {
		    width: 100% !important;
		    height: 100% !important;
		    border-radius: 50% !important;
		    object-fit: contain !important;
			filter: invert(48%) sepia(34%) saturate(951%) hue-rotate(92deg) brightness(93%) contrast(82%) !important;
		}
		
		/* Telegram */
		.social-badge-click:not(.social-github) .social-img-brand {
		    width: 30px !important;
		    height: 30px !important;
		    border-radius: 50% !important;
		    box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
		    object-fit: сontain !important;
		}
		
		/* Мобильная адаптация под экраны до 900px */
		@media (max-width: 900px) {
		    .social-github {
		        width: 26px !important;
		        height: 26px !important;
		    }
		    .social-github .social-img-brand {
		        width: 100% !important;
		        height: 100% !important;
		    }
		    .social-badge-click:not(.social-github) .social-img-brand {
		        width: 26px !important;
		        height: 26px !important;
		    }
		    .social-badge-wrapper {
		        gap: 8px !important;
		    }
		}

    </style>
</head>
<body>

	{% include header-theme.liquid %}
	{{ content }}

    <!-- Нижняя контентная кнопка перехода в Telegram -->
    <footer class="main-footer">
        <a href="https://t.me/eaststandart" target="_blank" class="tg-button">
            <span>✈️</span> Написать в Telegram
        </a>        
    </footer>

    {% include footer.liquid %}

</body>
</html> 
