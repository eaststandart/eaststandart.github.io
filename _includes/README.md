# Системные компоненты разметки

Каталог содержит переиспользуемые liquid-блоки кода, из которых движок Jekyll динамически собирает страницы сайта Лаборатории.

### Структура папки \_includes

```text
eaststandart.github.io/ 
└── _includes
    └── discus.liquid 
    └── faire-grid.liquid 
    └── footer.liquid 
    └── header-theme.liquid 
    └── media-archive.liquid 
    └── media-data-src.liquid 
    └── media-logic.liquid 
    └── navigation.liquid 
    └── news-loop.liquid 
    └── pagination.liquid 
    └── posts-page.liquid 
    └── tags-logic.liquid 
    └── README.md 
```

## Назначение модулей

*   **`discus.liquid`** — Интеграция и вывод блока дискуссий giscus. Для организации комментариев и Q&A под проектами.
*   **`faire-grid.liquid`** — Модуль автоматической сетки ярмарки поделок.
*   **`footer.liquid`** — Подвал сайта (копирайты, ссылки, контакты).
*   **`header-theme.liquid`** — Смена логотипа главной страницы сайта.
*   **`navigation.liquid`** — Модуль навигация сайта.
*   **`news-loop.liquid`** — Сборка и фильтрация ленты обновлений.
*   **`pagination.liquid`** — Модуль пагинации страниц.
*   **`posts-page.liquid`** — Локальные ленты постов на страницах проектов.
*   **`tags-logic.liquid`** — Сбор и генерация структуры тегов.
*   **`media-archive.liquid`** — Генерация и фильтрация общей ленты публикаций.
*   **`media-logic.liquid`** — Глобальный модуль оптимизации медиаконтента.
*   **`media-data-src.liquid`** — Замена по расширениям медиафайлов.
