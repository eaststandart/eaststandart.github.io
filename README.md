# Творческая лаборатория познавательного развития

Добро пожаловать в репозиторий проекта! Данный сайт разработан для поддержки технического творчества и обмена инженерным опытом. Он для тех, кто хочет знать как все устроено и создавать технологии своими руками.

A website for those who want to know how everything works and build technology with their own hands.

## О проекте и структуре Лаборатории

Для понимания структуры, целей и терминологии проекта ниже приведены ключевые определения:

1. **Творческая лаборатория познавательного развития** — глобальная философия, образовательная цель и общее название всей интернет-площадки.
2. **«Радиотехника»** — идейный, фундаментальный символ и движущая сила, стержень проектов Лаборатории (база, на которой строятся схемотехника, передача сигналов и управление роботами).
3. **Детско-юношеский инженерный клуб** — физическое место преподавательской деятельности, где данные проекты разрабатываются и тестируются с учащимися.
4. **TechLab** — личный авторский бренд Лаборатории, под которым создается код, контент и архитектура данного сайта.

### Структура репозитория сайта

```text
eaststandart.github.io/
├── _includes/                  # Повторяющиеся блоки страниц (Liquid-код)
│   ├── arch/
│   ├── discus.liquid
│   ├── faire-grid.liquid
│   ├── footer.liquid
│   ├── header-theme.liquid
│   ├── media-archive.liquid
│   ├── media-data-src.liquid
│   ├── media-logic.liquid
│   ├── navigation.liquid
│   ├── news-loop.liquid
│   ├── pagination.liquid
│   ├── posts-page.liquid
│   └── tags-logic.liquid
│
├── _layouts/                   # Шаблоны оформления страниц сайта
│   ├── arch/
│   ├── default.md
│   ├── faire.md
│   ├── home.md
│   ├── news.md
│   └── page.md
│
├── _pages/                     # Системные разделы и агрегаторы сайта
│   ├── faire.md
│   ├── journal-posts-page.md
│   ├── journal.md
│   ├── media-posts-page.md
│   ├── media.md
│   ├── news.md
│   └── people.md
│
├── _people/                    # Краткая библиография известных людей
│   └── fran-blanche.md
│
├── _posts/                     # Хронологические посты Лаборатории по дням
│   └── 2025-10-26-simple-cardboard-walking-robot.md
│   └── ... (хронология ежедневных отчётов о сборке поделок)
│
├── _reference/                 # Справочные материалы и исходники
│
├── assets/                     # Статические ресурсы сайта
│   ├── css/
│   ├── icons/
│   ├── img/
│   ├── js/
│   └── webm_optimization.bat
│
├── biblio/                     # Описание книг для изучения
│   ├── files/
│   ├── img/
│   ├── borisov-v-g-enciklopediya-yunogo-radiolyubitelya-konstruktora-2001.md
│   ├── chernenko-g-t-puteshestvie-v-stranu-robotov-1977.md
│   ├── index.md
│   ├── kiselyov-l-kniga-yunogo-tekhnika-1948.md
│   ├── materialy-dlya-samostoyatelnogo-izucheniya-osnov-elektroniki.md
│   ├── pchyolko-a-s-arifmetika-dlya-nachalnoj-shkoly-1955.md
│   ├── rostovcev-n-n-risovanie-1957.md
│   ├── svoren-r-a-elektronika-shag-za-shagom-1991.md
│   └── zak-a-z-intellektika-2024.md
│
├── diary/                      # Дневник инженера
│   ├── index.md
│   └── note-schematics.md
│
├── faire/                      # Инструкции и чертежи поделок (по алфавиту)
│   ├── avtomobil-s-polnym-privodom-iz-kartona
│   ├── besprovodnoj-telegraf
│   ├── blaster-elektroakusticheskij
│   ├── detektor-pereliva
│   ├── elektronnyj-organ
│   ├── fonarik-svetodiodnyj-bumazhnyj
│   ├── metronom-signalnyj
│   ├── muzykalnyj-karandash
│   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem
│   ├── pano-uslovnye-oboznacheniya
│   ├── plavnoe-zazhiganie-svetodioda
│   ├── podstavka-dlya-oscillografa
│   ├── prazdnichnyj-domik
│   ├── robot-korova-iz-kartona
│   ├── robot-krolik-iz-kartona
│   ├── robot-strannik
│   ├── simple-cardboard-walking-robot
│   ├── sputnik-1
│   ├── vibrohod-iz-zubnoj-shchetki
│   └── yablonevoe-derevo
│
├── inspiration/                # Посты на тему технического вдохновения
│   ├── img/
│   ├── aluminum-electrolytic-capacitor.md
│   ├── analog-panel-meter.md
│   ├── carbon-film-resistor.md
│   ├── ceramic-disc-capacitor.md
│   ├── index.md
│   ├── magnetic-buzzer.md
│   ├── our-dream.md
│   ├── strontium-atom.md
│   └── through-hole-red-led.md
│
├── projects/                   # Учебные проекты устройств 
│   ├── 1.webm
│   ├── index.md
│   ├── video.md
│   └── novyj-robot-shagohod.md
│
├── tools/                      # Описание используемого инструментария и ПО
│   ├── files/
│   ├── img/
│   ├── fritzing.md
│   ├── index.md
│   └── sprintlayout.md
│
├── _config.yml                 # Главный конфигурационный файл движка Jekyll
├── CODE_OF_CONDUCT.md          # Правила поведения в сообществе проекта
├── giscus.json                 # Настройки системы комментариев
├── index.md                    # Главная страница Творческой лаборатории
├── LICENSE.txt                 # Юридическая лицензия исходного кода
└── tags.md                     # Индекс тегов для быстрой навигации
```

