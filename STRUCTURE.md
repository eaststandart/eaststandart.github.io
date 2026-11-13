# Структура репозитория eaststandart.github.io

```text
eaststandart.github.io/
├── .github/
│   └── workflows/
│       ├── deploy.yml — about отсутствует
│       ├── journal-attendance.yml   # Модуль формирования Журнала посещений.
│       └── media-receiver-test.yml   # Временный тестовый робот приема сигналов медиа-шлюза.
├── _actions/
│   └── journal_attendance/
│       ├── __init__.py — about отсутствует
│       ├── ja_data_parser.py   # Модуль сетевого парсинга и сборщика отчетов.
│       ├── ja_gate_closer.py   # Модуль шлюзового обновления данных и очистки.
│       ├── ja_report_builder.py   # Модуль маркдаун-дизайна и GraphQL-публикации отчётов.
│       ├── ja_tgbot_notify.py   # Модуль отправки отчетов в каналы и группы Телеграм.
│       ├── ja_tgbot_personal.py   # Модуль отправки персональных отчетов в Телеграм.
│       ├── ja_wabot_personal.py   # Модуль отправки персональных отчетов в WhatsApp.
│       ├── journal_attendance.py   # Модуль управления сборкой отчета посещений.
│       └── README.md
├── _engineers/
│   └── liza-b.md   # title: Дневник инженера: Лиза Б.
├── _includes/
│   ├── comment-builder.liquid   # Модуль шаблона интерфейса Конструктора комментариев.
│   ├── discus.liquid   # Интеграция и вывод блока дискуссий giscus.
│   ├── faire-grid.liquid   # Универсальный модуль автоматической генерации сеток разделов сайта.
│   ├── feed.liquid   # Сборка и рендер первой страницы обновлений на основе квантованных корзин feed.yml.
│   ├── footer.liquid   # Подвал сайта.
│   ├── header-theme.liquid   # Смена логотипа главной страницы сайта.
│   ├── journal-attendance.liquid   # Модуль шаблона интерфейса Журнала посещений.
│   ├── mathjax.html   # Подключение математического движка MathJax v3.
│   ├── media-logic.liquid   # Глобальный модуль оптимизации медиаконтента.
│   ├── navigation.liquid   # Модуль навигации сайта.
│   ├── pagination.liquid   # Модуль пагинации страниц.
│   ├── posts-page.liquid   # Модуль автоматического вывода локальных лент постов на страницах проектов.
│   ├── posts-page-open.liquid   # Изолированный модуль развернутого вывода постов проекта.
│   ├── README.md
│   ├── seo-meta.liquid   # Модуль сборки SEO и Open Graph мета-тегов.
│   ├── tags-logic.liquid   # Сбор и генерация структуры тегов.
│   └── zoom.liquid   # Модульный HTML-контейнер и подключение скрипта зума картинок.
├── _layouts/
│   ├── default.md   # Глобальный шаблон оформления страниц сайта.
│   ├── faire.md   # Шаблон структуры страниц в разделе faire.
│   ├── feed.md   # Шаблон ленты новостей.
│   ├── home.md   # Шаблон главной страницы сайта.
│   ├── page.md   # Шаблон для базовых страниц сайт.
│   └── README.md
├── _pages/
│   ├── comment-builder.md   # title: Конструктор дискуссий
│   ├── engineers.md   # title: Работы юных инженеров
│   ├── faire.md   # title: Ярмарка поделок
│   ├── feed-journal.md   # title: Журнал проектов
│   ├── feed-media.md   # title: Медиа материалы
│   ├── feed-news.md   # title: Новости уголка конструктора
│   ├── feed-post.md   # title: Посты
│   ├── feed-question.md   # title: Вопросы проектов
│   ├── feed-reference.md   # title: Справочные материалы
│   ├── journal-attendance.md   # Веб-страница Журнала посещений
│   ├── people.md   # title: Люди
│   ├── process.md   # title: Творческий процесс
│   └── README.md
├── _people/
│   └── fran-blanche.md   # title: Фрэн Бланш (Fran Blanche)
├── _posts/
│   ├── 2025-10-26-simple-cardboard-walking-robot.md   # title: Робот двуногий шагающий из картона: галерея
│   ├── 2025-10-27-simple-cardboard-walking-robot.md   # title: Робот двуногий шагающий из картона: вопросы по проекту
│   ├── 2025-10-28-simple-cardboard-walking-robot.md   # title: Робот двуногий шагающий из картона: раскачивание корпуса
│   ├── 2025-10-30-nastolnaya-svetodiodnaya-lampa-s-rasteniem.md   # title: Настольная светодиодная лампа с растением: галерея
│   ├── 2025-10-31-nastolnaya-svetodiodnaya-lampa-s-rasteniem.md   # title: Настольная светодиодная лампа с растением: вопросы по проекту
│   ├── 2025-11-02-besprovodnoj-telegraf.md   # title: Беспроводной телеграф: галерея
│   ├── 2025-11-03-besprovodnoj-telegraf.md   # title: Беспроводной телеграф: вопросы по проекту
│   ├── 2025-11-06-sputnik-1.md   # title: Спутник-1: галерея
│   ├── 2025-11-07-sputnik-1.md   # title: Спутник-1: вопросы по проекту
│   ├── 2025-11-08-sputnik-1.md   # title: Спутник-1: общий вид
│   ├── 2025-11-12-fonarik-svetodiodnyj-bumazhnyj.md   # title: Фонарик светодиодный бумажный: галерея
│   ├── 2025-11-13-fonarik-svetodiodnyj-bumazhnyj.md   # title: Фонарик светодиодный бумажный: вопросы по проекту
│   ├── 2025-11-14-fonarik-svetodiodnyj-bumazhnyj.md   # title: Фонарик светодиодный бумажный: описание работы
│   ├── 2025-11-21-vibrohod-iz-zubnoj-shchetki.md   # title: Виброход из зубной щетки: галерея
│   ├── 2025-11-22-vibrohod-iz-zubnoj-shchetki.md   # title: Виброход из зубной щетки: вопросы по проекту
│   ├── 2025-11-23-vibrohod-iz-zubnoj-shchetki.md   # title: Робот зубочист: вариант конструкции
│   ├── 2025-11-24-vibrohod-iz-zubnoj-shchetki.md   # title: Робот зубочист: скорость движения
│   ├── 2025-11-26-robot-strannik.md   # title: Робот странник: галерея
│   ├── 2025-11-27-robot-strannik.md   # title: Робот странник: вопросы по проекту
│   ├── 2025-11-28-robot-strannik.md   # title: Робот странник: модель №1
│   ├── 2025-11-29-robot-strannik.md   # title: Робот странник: тип движения
│   ├── 2025-12-22-yablonevoe-derevo.md   # title: Яблоневое дерево: галерея
│   ├── 2025-12-23-yablonevoe-derevo.md   # title: Яблоневое дерево: вопросы по проекту
│   ├── 2026-01-25-blaster-elektroakusticheskij.md   # title: Бластер электроакустический: галерея
│   ├── 2026-01-26-blaster-elektroakusticheskij.md   # title: Бластер электроакустический: вопросы по проекту
│   ├── 2026-01-27-blaster-elektroakusticheskij.md   # title: Бластер электроакустический: подключение индикатора
│   ├── 2026-01-29-detektor-pereliva.md   # title: Детектор перелива: галерея
│   ├── 2026-01-30-detektor-pereliva.md   # title: Детектор перелива: вопросы по проекту
│   ├── 2026-01-31-detektor-pereliva.md   # title: Детектор перелива: общий вид
│   ├── 2026-02-01-detektor-pereliva.md   # title: Детектор перелива: описание работы
│   ├── 2026-02-02-prazdnichnyj-domik.md   # title: Праздничный домик: галерея
│   ├── 2026-02-03-prazdnichnyj-domik.md   # title: Праздничный домик: вопросы по проекту
│   ├── 2026-02-04-prazdnichnyj-domik.md   # title: Праздничный домик: создала Лиза Б.
│   ├── 2026-02-05-prazdnichnyj-domik.md   # title: Праздничный домик: создал Кирилл К.
│   ├── 2026-02-10-elektronnyj-organ.md   # title: Электронный орган: галерея
│   ├── 2026-02-11-elektronnyj-organ.md   # title: Электронный орган: вопросы по проекту
│   ├── 2026-02-12-elektronnyj-organ.md   # title: Электронный орган: создала Лиза Б.
│   ├── 2026-02-13-elektronnyj-organ.md   # title: Электронный орган: этапы создания
│   ├── 2026-02-14-elektronnyj-organ.md   # title: Электронный орган: паразитная генерация
│   ├── 2026-02-22-robot-korova-iz-kartona.md   # title: Робот корова из картона: галерея
│   ├── 2026-02-23-robot-korova-iz-kartona.md   # title: Робот корова из картона: вопросы по проекту
│   ├── 2026-02-24-robot-korova-iz-kartona.md   # title: Робот корова из картона: вид и движение
│   ├── 2026-03-08-robot-krolik-iz-kartona.md   # title: Робот кролик из картона: галерея
│   ├── 2026-03-09-robot-krolik-iz-kartona.md   # title: Робот кролик из картона: вопросы по проекту
│   ├── 2026-03-10-robot-krolik-iz-kartona.md   # title: Робот кролик из картона: вид и движение
│   ├── 2026-03-11-robot-krolik-iz-kartona.md   # title: Робот кролик из картона: самодельный редуктор
│   ├── 2026-03-13-plavnoe-zazhiganie-svetodioda.md   # title: Эффект плавного зажигания светодиода: галерея
│   ├── 2026-03-14-plavnoe-zazhiganie-svetodioda.md   # title: Эффект плавного зажигания светодиода: вопросы по проекту
│   ├── 2026-03-15-plavnoe-zazhiganie-svetodioda.md   # title: Эффект плавного зажигания светодиода: макет эксперимента
│   ├── 2026-03-16-plavnoe-zazhiganie-svetodioda.md   # title: Эффект плавного зажигания светодиода: время зажигания и гашения
│   ├── 2026-04-03-pano-uslovnye-oboznacheniya.md   # title: Условные обозначения: галерея
│   ├── 2026-04-04-pano-uslovnye-oboznacheniya.md   # title: Условные обозначения: вопросы по проекту
│   ├── 2026-04-06-avtomobil-s-polnym-privodom-iz-kartona.md   # title: Автомобиль 4wd из картона: галерея
│   ├── 2026-04-07-avtomobil-s-polnym-privodom-iz-kartona.md   # title: Автомобиль 4wd из картона: вопросы по проекту
│   ├── 2026-04-08-avtomobil-s-polnym-privodom-iz-kartona.md   # title: Автомобиль 4wd из картона: вид и движение
│   ├── 2026-04-10-podstavka-dlya-oscillografa.md   # title: Подставка для осциллографа: галерея
│   ├── 2026-04-11-podstavka-dlya-oscillografa.md   # title: Подставка для осциллографа: вопросы по проекту
│   ├── 2026-04-12-podstavka-dlya-oscillografa.md   # title: Подставка для осциллографа: общий вид
│   ├── 2026-04-14-muzykalnyj-karandash.md   # title: Музыкальный карандаш: галерея
│   ├── 2026-04-15-muzykalnyj-karandash.md   # title: Музыкальный карандаш: вопросы по проекту
│   ├── 2026-04-16-muzykalnyj-karandash.md   # title: Музыкальный карандаш: общий вид
│   ├── 2026-04-17-muzykalnyj-karandash.md   # title: Музыкальный карандаш: сборка
│   ├── 2026-04-18-muzykalnyj-karandash.md   # title: Музыкальный карандаш: описание работы
│   ├── 2026-04-19-muzykalnyj-karandash.md   # title: Музыкальный карандаш: тестирование
│   ├── 2026-04-20-muzykalnyj-karandash.md   # title: Музыкальный карандаш: применение
│   ├── 2026-05-11-metronom-signalnyj.md   # title: Метроном сигнальный: галерея
│   ├── 2026-05-12-metronom-signalnyj.md   # title: Метроном сигнальный: вопросы по проекту
│   ├── 2026-05-13-metronom-signalnyj.md   # title: Метроном сигнальный: изделие №1
│   ├── 2026-05-14-metronom-signalnyj.md   # title: Метроном сигнальный: этапы создания
│   ├── 2026-05-15-metronom-signalnyj.md   # title: Метроном сигнальный: общий вид
│   ├── 2026-06-05-robot-krolik-iz-kartona.md   # title: Робот кролик из картона: модель с разворотом
│   └── 2026-06-10-multivibrator-nesimmetrichnyj.md   # title: Мультивибратор несимметричный
├── _process/
│   ├── 2026-creative-proces-regular.md — about отсутствует
│   ├── 2026-creative-process-regular-techlab.md   # title: Инженерные занятия: 2026 [TechLab]
│   └── 2026-creative-process-regular-valery.md   # title: Инженерные занятия: 2026 – Валерий Р.
├── _reference/
├── assets/
│   ├── batchfiles/
│   │   ├── generate_readme.bat   # Скрипт автоматического сбора описаний и документирования файлов папки.
│   │   ├── README.md
│   │   ├── structure_tree.bat   # Скрипт автоматической генерации интерактивной структуры дерева репозитория.
│   │   └── webm_optimization.bat   # Скрипт для оптимизации видео в формате webm сайта Лаборатории.
│   ├── css/
│   │   ├── biblio.css   # Модуль стилей для отображения карточек книг электронной библиотеки сайта.
│   │   ├── comment-builder.css   # Модуль стилей веб-страницы формы комментариев.
│   │   ├── diary.css   # Модуль стилей для отображения карточек Дневника инженера.
│   │   ├── faire.css   # Модуль изолированных стилей раздела Ярмарки поделок
│   │   ├── footnotes.css   # Модуль стилей для оформления блока примечаний и академических сносок.
│   │   ├── giscus.css   # Модуль адаптивной верстки интерактивного виджета комментариев Giscus.
│   │   ├── giscus-gallery.css   # Модуль изолированных стилей страницы дискусий Галерея раздела Ярмарка поделок
│   │   ├── giscus-process.css   # Модуль изолированных стилей страницы дискусий раздела Творческий процесс
│   │   ├── giscus-v1.0.css — about отсутствует
│   │   ├── giscus-v1.1-0.css — about отсутствует
│   │   ├── header-classic.css   # Модуль стилей глобальной шапки и элементов брендинга главной страницы.
│   │   ├── header-desktop.css   # Модуль тестовой интерактивной шапки сайта с имитацией псевдоконсоли
│   │   ├── header-panel.css   # Модуль стилей интерактивной панели управления и консольной шапки сайта.
│   │   ├── images.css   # Модуль изображений.
│   │   ├── journal-attendance.css   # Модуль стилей веб-страницы журнала посещений.
│   │   ├── pagination.css   # Модуль универсальной пагинации, крошек навигации и лент обновлений
│   │   ├── projects.css   # Модуль стилей двухмерной сетки для раздела Учебные проекты.
│   │   ├── README.md
│   │   ├── style.css   # Ядро главных стилей сайта Лаборатории.
│   │   ├── tools.css   # Модуль стилей для отображения карточек используемого инструментария и инженерного ПО.
│   │   ├── video.css   # Модуль стилей для отображения видеоплееров, оптимизации загрузки и антипрыжка контента.
│   │   ├── video-figure.css — about отсутствует
│   │   ├── video-figure-v.css — about отсутствует
│   │   ├── video-gallery.css — about отсутствует
│   │   └── zoom.css   # Модуль центрированного модального зума (Лайтбокса) для картинок.
│   ├── icons/
│   │   ├── aluminum-electrolytic-capacitor.webp
│   │   ├── analog-panel-meter.webp
│   │   ├── carbon-film-resistor.webp
│   │   ├── ceramic-disc-capacitor.webp
│   │   ├── chto-novogo.svg
│   │   ├── detskij-inzhenernyj-klub.svg
│   │   ├── favicon.svg
│   │   ├── fritzing.webp
│   │   ├── getting-started-in-electronics.webp
│   │   ├── logo.svg
│   │   ├── logo-github.svg
│   │   ├── logo-readme.svg
│   │   ├── logo-telegram.svg
│   │   ├── magnetic-buzzer.webp
│   │   ├── our-dream.webp
│   │   ├── sprintlayout.webp
│   │   ├── strontium-atom.webp
│   │   ├── through-hole-red-led.webp
│   │   └── ugolok-mladshego-konstruktora.svg
│   ├── img/
│   ├── js/
│   │   ├── comment-builder/
│   │   │   ├── 01-comment-notify.js   # Модуль уведомлений и статусов конструктора.
│   │   │   ├── 02-comment-auth.js   # Модуль авторизации и проверки доступа к Конструктору.
│   │   │   ├── 03-comment-form.js   # Модуль инициализации и сброса формы конструктора.
│   │   │   ├── 04-drafts-parser.js   # Модуль разбора структуры черновиков Markdown.
│   │   │   ├── 05-drafts-loader.js   # Модуль загрузки списка черновиков из GitHub.
│   │   │   ├── 06-drafts-injector.js   # Модуль восстановления выбранного черновика в конструкторе.
│   │   │   ├── 07-drafts-delete.js   # Модуль управления удалением черновиков.
│   │   │   ├── 08-comment-validation.js   # Модуль проверки данных комментария.
│   │   │   ├── 09-comment-lock.js   # Модуль блокировки формы конструктора.
│   │   │   ├── 10-media-blocks.js   # Модуль создания и удаления медиаблоков.
│   │   │   ├── 11-media-files.js   # Модуль управления данными медиафайлов.
│   │   │   ├── 12-media-files-ui.js   # Модуль интерфейса списка медиафайлов.
│   │   │   ├── 13-media-upload.js   # Модуль загрузки медиафайлов в буферный репозиторий.
│   │   │   ├── 14-comment-markdown.js   # Модуль формирования и кодирования Markdown комментария.
│   │   │   ├── 15-comment-github-save.js   # Модуль сохранения Markdown-файлов через GitHub API.
│   │   │   ├── 16-comment-submit.js   # Модуль обработки отправки комментария и сохранения черновика.
│   │   │   └── README.md
│   │   ├── journal-attendance/
│   │   │   ├── 01-core-auth.js   # Модуль авторизации и контроля доступа.
│   │   │   ├── 02-students-loader.js   # Модуль сетевой загрузки базы расписания.
│   │   │   ├── 03-yaml-parser.js   # Модуль объектного парсинга и валидации синтаксиса.
│   │   │   ├── 04-journal-ui.js   # Модуль динамической отрисовки интерфейса.
│   │   │   ├── 05-attendance-commands.js   # Модуль сбора посещаемости и обработки системных команд.
│   │   │   ├── 06-status-and-repair.js   # Модуль управления состояниями и опроса сервера.
│   │   │   ├── 07-validation.js   # Модуль контроля безопасности строк.
│   │   │   └── README.md
│   │   ├── image-lazy-load.js   # Модуль лези-лоада картинок.
│   │   ├── pagination-logic.js   # Модуль пагинации.
│   │   ├── posts-page-list.js   # Модуль фильтрации и зачистки ленты медиа.
│   │   ├── posts-page-nav.js   # Модуль локальной пагинации проектов.
│   │   ├── README.md
│   │   ├── tags-search.js   # Модуль js-фильтрации страницы поиска по тегам.
│   │   ├── video-lazy-load.js   # Профессиональный модуль ленивой предзагрузки нативных видеоплееров.
│   │   └── zoom.js   # Модуль идеального центрированного модального зума (Лайтбокса) для картинок.
│   └── README.md
├── biblio/
│   ├── files/
│   │   └── materialy-dlya-samostoyatelnogo-izucheniya-osnov-elektroniki.pdf
│   ├── img/
│   │   ├── berezanskaya-e-c-sbornik-zadach-i-uprazhnenij-po-arifmetike-2021.webp
│   │   ├── borisov-v-g-enciklopediya-yunogo-radiolyubitelya-konstruktora-2001.webp
│   │   ├── borisov-v-g-yunyj-radiolyubitel-1992.webp
│   │   ├── chernenko-g-t-a-vse-taki-poletim-1984.webp
│   │   ├── chernenko-g-t-chto-umeyut-mashiny-rasskazy-ob-avtomatike-1986.webp
│   │   ├── chernenko-g-t-kak-chelovek-poletel-v-kosmos-1987.webp
│   │   ├── chernenko-g-t-kak-roboty-rabotat-nauchilis-1989.webp
│   │   ├── chernenko-g-t-na-polzu-i-slavu-otechestva-1988.webp
│   │   ├── chernenko-g-t-nashi-krylya-1979.webp
│   │   ├── chernenko-g-t-prostaya-avtomatika-1989.webp
│   │   ├── chernenko-g-t-puteshestvie-v-stranu-robotov-1977.webp
│   │   ├── chernenko-g-t-tvorcy-nauk-rossijskih-1989.webp
│   │   ├── chernenko-g-t-zvezdy-planety-teleskopy-1991.webp
│   │   ├── kiselev-a-p-arifmetika-dlya-pyatogo-klassa-srednej-shkoly-2021.webp
│   │   ├── kiselyov-l-kniga-yunogo-tekhnika-1948.webp
│   │   ├── kiselyov-l-kniga-yunogo-tekhnika-2025.webp
│   │   ├── materialy-dlya-samostoyatelnogo-izucheniya-osnov-elektroniki.webp
│   │   ├── pchyolko-a-s-arifmetika-dlya-chetvertogo-klassa-nachalnoj-shkoly-2021.webp
│   │   ├── pchyolko-a-s-arifmetika-dlya-pervogo-klassa-nachalnoj-shkoly-2022.webp
│   │   ├── pchyolko-a-s-arifmetika-dlya-tretego-klassa-nachalnoj-shkoly-2021.webp
│   │   ├── pchyolko-a-s-arifmetika-dlya-vtorogo-klassa-nachalnoj-shkoly-2022.webp
│   │   ├── popova-n-s-pchyolko-a-s-sbornik-arifmeticheskih-zadach-chast-1-2022.webp
│   │   ├── popova-n-s-pchyolko-a-s-sbornik-arifmeticheskih-zadach-chast-2-2022.webp
│   │   ├── popova-n-s-pchyolko-a-s-sbornik-arifmeticheskih-zadach-chast-3-2022.webp
│   │   ├── popova-n-s-pchyolko-a-s-sbornik-arifmeticheskih-zadach-chast-4-2022.webp
│   │   ├── rostovcev-n-n-metodika-prepodavaniya-risovaniya-v-1-i-2-klassah-1958.webp
│   │   ├── rostovcev-n-n-risovanie-1-4-klass-1957.webp
│   │   ├── rostovcev-n-n-risovanie-1-klass-1957.webp
│   │   ├── svoren-r-a-elektronika-shag-za-shagom-1991.webp
│   │   ├── svoren-r-a-elektronika-shag-za-shagom-2001.webp
│   │   ├── svoren-r-a-elektronika-shag-za-shagom-2020.webp
│   │   ├── zak-a-z-intellektika-1-klass-2024.webp
│   │   ├── zak-a-z-intellektika-2-klass-2024.webp
│   │   ├── zak-a-z-intellektika-3-klass-2024.webp
│   │   └── zak-a-z-intellektika-4-klass-2024.webp
│   ├── borisov-v-g-enciklopediya-yunogo-radiolyubitelya-konstruktora-2001.md   # title: Энциклопедия юного радиолюбителя-конструктора
│   ├── chernenko-g-t-puteshestvie-v-stranu-robotov-1977.md   # title: Путешествие в страну роботов
│   ├── index.md   # title: Список литературы
│   ├── kiselyov-l-kniga-yunogo-tekhnika-1948.md   # title: Книга юного техника
│   ├── materialy-dlya-samostoyatelnogo-izucheniya-osnov-elektroniki.md   # title: Материалы для самостоятельного изучения основ электроники
│   ├── pchyolko-a-s-arifmetika-dlya-nachalnoj-shkoly-1955.md   # title: Книги по арифметике, сборники задач и упражнений к ним
│   ├── rostovcev-n-n-risovanie-1957.md   # title: Рисование, 1-4 класс
│   ├── svoren-r-a-elektronika-shag-za-shagom-1991.md   # title: Электроника шаг за шагом
│   └── zak-a-z-intellektika-2024.md   # title: Интеллектика. Тетрадь для развития мыслительных способностей
├── bin/
│   ├── feed.py   # Изолированный монолитный сборщик единой ленты обновлений из Источника Правды.
│   ├── images.py   # Монолитный объединенный модуль предобработки изображений для Obsidian -> Jekyll.
│   ├── pathlinks.py   # Модуль глобальной очистки путей, конвертации Wiki-ссылок и текстовых связей Obsidian.
│   ├── postpage.py   # Изолированный автономный генератор физических md-страниц архивов проектов.
│   ├── preprocess.py   # Главный менеджер автоматической предобработки контента Obsidian перед сборкой Jekyll.
│   ├── sitemap.py   # Главный диспетчер и общий купол конвейера
│   ├── smLinks.py   # Геометрия каркаса и связей сайта.
│   ├── smPropsIn.py   # Обогащение карты и расчет инвариантных дат
│   ├── smPropsOut.py   # Расчет тегов, категорий контура и сохранение файлов
│   ├── vault.py   # Автономный сквозной точечный сейф исключений для защиты примеров кода.
│   └── videos.py   # Модуль предобработки видео-ссылок для Obsidian -> Jekyll с поддержкой ленивой загрузки.
├── diary/
│   ├── index.md   # title: Дневник инженера
│   └── note-schematics.md   # title: Заметки по схемотехнике
├── faire/
│   ├── avtomobil-s-polnym-privodom-iz-kartona/
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona.md   # title: Автомобиль с полным приводом из картона
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-01.webm
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-01.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-02.webm
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-02.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-03.webm
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-03.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-04.webm
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-04.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-05.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-06.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-07.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-08.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-09.webp
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-10.webp
│   │   └── avtomobil-s-polnym-privodom-iz-kartona-11.webp
│   ├── besprovodnoj-telegraf/
│   │   ├── besprovodnoj-telegraf.md   # title: Беспроводной телеграф
│   │   ├── besprovodnoj-telegraf.webp
│   │   ├── besprovodnoj-telegraf-01.webm
│   │   ├── besprovodnoj-telegraf-01.webp
│   │   └── besprovodnoj-telegraf-02.webp
│   ├── blaster-elektroakusticheskij/
│   │   ├── blaster-elektroakusticheskij.md   # title: Бластер электроакустический
│   │   ├── blaster-elektroakusticheskij.webp
│   │   ├── blaster-elektroakusticheskij-01.webm
│   │   ├── blaster-elektroakusticheskij-01.webp
│   │   ├── blaster-elektroakusticheskij-02.webp
│   │   ├── blaster-elektroakusticheskij-03.webp
│   │   ├── blaster-elektroakusticheskij-ad.dxf
│   │   ├── blaster-elektroakusticheskij-ad.pdf
│   │   ├── blaster-elektroakusticheskij-esd.pdf
│   │   └── blaster-elektroakusticheskij-esd.spl8
│   ├── detektor-pereliva/
│   │   ├── detektor-pereliva.md   # title: Детектор перелива
│   │   ├── detektor-pereliva.webp
│   │   ├── detektor-pereliva-01.webm
│   │   ├── detektor-pereliva-01.webp
│   │   ├── detektor-pereliva-02.webm
│   │   ├── detektor-pereliva-02.webp
│   │   ├── detektor-pereliva-03.webp
│   │   ├── detektor-pereliva-04.webp
│   │   ├── detektor-pereliva-05.webp
│   │   ├── detektor-pereliva-06.webp
│   │   ├── detektor-pereliva-07.webp
│   │   ├── detektor-pereliva-08.webp
│   │   ├── detektor-pereliva-09.webp
│   │   ├── detektor-pereliva-10.webp
│   │   ├── detektor-pereliva-11.webp
│   │   ├── detektor-pereliva-12.webp
│   │   ├── detektor-pereliva-13.webp
│   │   ├── detektor-pereliva-14.webp
│   │   ├── detektor-pereliva-15.webp
│   │   ├── detektor-pereliva-16.webp
│   │   ├── detektor-pereliva-17.webp
│   │   ├── detektor-pereliva-18.webp
│   │   ├── detektor-pereliva-19.webp
│   │   ├── detektor-pereliva-20.webp
│   │   ├── detektor-pereliva-21.webp
│   │   ├── detektor-pereliva-22.webp
│   │   ├── detektor-pereliva-23.webp
│   │   ├── detektor-pereliva-esd.pdf
│   │   ├── detektor-pereliva-esd.spl8
│   │   ├── detektor-perelivaj-ad.dxf
│   │   └── detektor-perelivaj-ad.pdf
│   ├── elektronnyj-organ/
│   │   ├── elektronnyj-organ.md   # title: Электронный орган
│   │   ├── elektronnyj-organ.webp
│   │   ├── elektronnyj-organ-01.webm
│   │   ├── elektronnyj-organ-01.webp
│   │   ├── elektronnyj-organ-02.webm
│   │   ├── elektronnyj-organ-02.webp
│   │   ├── elektronnyj-organ-03.webm
│   │   ├── elektronnyj-organ-03.webp
│   │   ├── elektronnyj-organ-04.webm
│   │   ├── elektronnyj-organ-04.webp
│   │   ├── elektronnyj-organ-05.webm
│   │   ├── elektronnyj-organ-05.webp
│   │   ├── elektronnyj-organ-06.webp
│   │   ├── elektronnyj-organ-07.webp
│   │   ├── elektronnyj-organ-08.webp
│   │   ├── elektronnyj-organ-09.webp
│   │   ├── elektronnyj-organ-10.webp
│   │   ├── elektronnyj-organ-11.webp
│   │   ├── elektronnyj-organ-12.webp
│   │   ├── elektronnyj-organ-13.webp
│   │   ├── elektronnyj-organ-14.webp
│   │   ├── elektronnyj-organ-15.webp
│   │   ├── elektronnyj-organ-16.webp
│   │   ├── elektronnyj-organ-17.webp
│   │   ├── elektronnyj-organ-18.webp
│   │   ├── elektronnyj-organ-19.webp
│   │   ├── elektronnyj-organ-20.webp
│   │   ├── elektronnyj-organ-21.webp
│   │   ├── elektronnyj-organ-22.webp
│   │   ├── elektronnyj-organ-23.webp
│   │   ├── elektronnyj-organ-24.webp
│   │   ├── elektronnyj-organ-25.webp
│   │   ├── elektronnyj-organ-26.webp
│   │   ├── elektronnyj-organ-27.webp
│   │   ├── elektronnyj-organ-28.webp
│   │   ├── elektronnyj-organ-29.webp
│   │   ├── elektronnyj-organ-30.webp
│   │   ├── elektronnyj-organ-31.webp
│   │   ├── elektronnyj-organ-32.webp
│   │   ├── elektronnyj-organ-33.webp
│   │   ├── elektronnyj-organ-34.webp
│   │   ├── elektronnyj-organ-35.webp
│   │   ├── elektronnyj-organ-36.webp
│   │   ├── elektronnyj-organ-37.webp
│   │   ├── elektronnyj-organ-38.webp
│   │   ├── elektronnyj-organ-39.webp
│   │   ├── elektronnyj-organ-40.webp
│   │   ├── elektronnyj-organ-41.webp
│   │   ├── elektronnyj-organ-42.webp
│   │   └── elektronnyj-organ-pcb.lay6
│   ├── fonarik-svetodiodnyj-bumazhnyj/
│   │   ├── fonarik-svetodiodnyj-bumazhnyj.md   # title: Фонарик светодиодный бумажный
│   │   ├── fonarik-svetodiodnyj-bumazhnyj.pdf
│   │   ├── fonarik-svetodiodnyj-bumazhnyj.spl8
│   │   ├── fonarik-svetodiodnyj-bumazhnyj.webp
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-01.webm
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-01.webp
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-02.webp
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-03.webp
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-04.webp
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-05.webp
│   │   └── fonarik-svetodiodnyj-bumazhnyj-trafaret.pdf
│   ├── metronom-signalnyj/
│   │   ├── metronom-signalnyj.md   # title: Метроном сигнальный
│   │   ├── metronom-signalnyj.webp
│   │   ├── metronom-signalnyj-01.webm
│   │   ├── metronom-signalnyj-01.webp
│   │   ├── metronom-signalnyj-02.webm
│   │   ├── metronom-signalnyj-02.webp
│   │   ├── metronom-signalnyj-03.webm
│   │   ├── metronom-signalnyj-03.webp
│   │   ├── metronom-signalnyj-04.webm
│   │   ├── metronom-signalnyj-04.webp
│   │   ├── metronom-signalnyj-05.webm
│   │   ├── metronom-signalnyj-05.webp
│   │   ├── metronom-signalnyj-06.webm
│   │   ├── metronom-signalnyj-06.webp
│   │   ├── metronom-signalnyj-07.webm
│   │   ├── metronom-signalnyj-07.webp
│   │   ├── metronom-signalnyj-08.webp
│   │   ├── metronom-signalnyj-09.webp
│   │   ├── metronom-signalnyj-10.webp
│   │   ├── metronom-signalnyj-11.webp
│   │   ├── metronom-signalnyj-12.webp
│   │   ├── metronom-signalnyj-13.webp
│   │   ├── metronom-signalnyj-14.webp
│   │   ├── metronom-signalnyj-15.webp
│   │   ├── metronom-signalnyj-16.webp
│   │   ├── metronom-signalnyj-17.webp
│   │   ├── metronom-signalnyj-18.webp
│   │   ├── metronom-signalnyj-19.webp
│   │   ├── metronom-signalnyj-20.webp
│   │   ├── metronom-signalnyj-21.webp
│   │   ├── metronom-signalnyj-22.webp
│   │   ├── metronom-signalnyj-23.webp
│   │   ├── metronom-signalnyj-24.webp
│   │   ├── metronom-signalnyj-25.webp
│   │   ├── metronom-signalnyj-26.webp
│   │   ├── metronom-signalnyj-27.webp
│   │   ├── metronom-signalnyj-28.webp
│   │   ├── metronom-signalnyj-29.webp
│   │   ├── metronom-signalnyj-30.webp
│   │   ├── metronom-signalnyj-31.webp
│   │   ├── metronom-signalnyj-esd.pdf
│   │   └── metronom-signalnyj-esd.spl8
│   ├── muzykalnyj-karandash/
│   │   ├── muzykalnyj-karandash.md   # title: Музыкальный карандаш
│   │   ├── muzykalnyj-karandash.webp
│   │   ├── muzykalnyj-karandash-01.webm
│   │   ├── muzykalnyj-karandash-01.webp
│   │   ├── muzykalnyj-karandash-02.webm
│   │   ├── muzykalnyj-karandash-02.webp
│   │   ├── muzykalnyj-karandash-03.webm
│   │   ├── muzykalnyj-karandash-03.webp
│   │   ├── muzykalnyj-karandash-04.webm
│   │   ├── muzykalnyj-karandash-04.webp
│   │   ├── muzykalnyj-karandash-05.webm
│   │   ├── muzykalnyj-karandash-05.webp
│   │   ├── muzykalnyj-karandash-06.webm
│   │   ├── muzykalnyj-karandash-06.webp
│   │   ├── muzykalnyj-karandash-07.webm
│   │   ├── muzykalnyj-karandash-07.webp
│   │   ├── muzykalnyj-karandash-08.webm
│   │   ├── muzykalnyj-karandash-08.webp
│   │   ├── muzykalnyj-karandash-09.webm
│   │   ├── muzykalnyj-karandash-09.webp
│   │   ├── muzykalnyj-karandash-10.webm
│   │   ├── muzykalnyj-karandash-10.webp
│   │   ├── muzykalnyj-karandash-11.webm
│   │   ├── muzykalnyj-karandash-11.webp
│   │   ├── muzykalnyj-karandash-12.webm
│   │   ├── muzykalnyj-karandash-12.webp
│   │   ├── muzykalnyj-karandash-13.webm
│   │   ├── muzykalnyj-karandash-13.webp
│   │   ├── muzykalnyj-karandash-14.webm
│   │   ├── muzykalnyj-karandash-14.webp
│   │   ├── muzykalnyj-karandash-15.webm
│   │   ├── muzykalnyj-karandash-15.webp
│   │   ├── muzykalnyj-karandash-16.webm
│   │   ├── muzykalnyj-karandash-16.webp
│   │   ├── muzykalnyj-karandash-17.webm
│   │   ├── muzykalnyj-karandash-17.webp
│   │   ├── muzykalnyj-karandash-18.webm
│   │   ├── muzykalnyj-karandash-18.webp
│   │   ├── muzykalnyj-karandash-19.webm
│   │   ├── muzykalnyj-karandash-19.webp
│   │   ├── muzykalnyj-karandash-20.webm
│   │   ├── muzykalnyj-karandash-20.webp
│   │   ├── muzykalnyj-karandash-21.webp
│   │   ├── muzykalnyj-karandash-22.webp
│   │   ├── muzykalnyj-karandash-23.webp
│   │   ├── muzykalnyj-karandash-24.webp
│   │   ├── muzykalnyj-karandash-esd.jpg
│   │   ├── muzykalnyj-karandash-esd.pdf
│   │   ├── muzykalnyj-karandash-trafaret.pdf
│   │   └── muzykalnyj-karandash-trafaret.spl8
│   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem/
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem 1.webp
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem.md   # title: Настольная светодиодная лампа с растением
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem.webp
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-01.webm
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-01.webp
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-02.webp
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-03.webp
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-04.webp
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniemj-ad.dxf
│   │   └── nastolnaya-svetodiodnaya-lampa-s-rasteniemj-ad.pdf
│   ├── pano-uslovnye-oboznacheniya/
│   │   ├── pano-uslovnye-oboznacheniya.md   # title: Условные обозначения
│   │   ├── pano-uslovnye-oboznacheniya.webp
│   │   ├── pano-uslovnye-oboznacheniya-01.webm
│   │   ├── pano-uslovnye-oboznacheniya-01.webp
│   │   └── pano-uslovnye-oboznacheniya-02.webp
│   ├── plavnoe-zazhiganie-svetodioda/
│   │   ├── plavnoe-zazhiganie-svetodioda.md   # title: Эффект плавного зажигания светодиода
│   │   ├── plavnoe-zazhiganie-svetodioda.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-01.webm
│   │   ├── plavnoe-zazhiganie-svetodioda-01.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-02.webm
│   │   ├── plavnoe-zazhiganie-svetodioda-02.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-03.webm
│   │   ├── plavnoe-zazhiganie-svetodioda-03.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-04.webm
│   │   ├── plavnoe-zazhiganie-svetodioda-04.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-05.webm
│   │   ├── plavnoe-zazhiganie-svetodioda-05.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-06.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-07.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-08.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-09.webp
│   │   ├── plavnoe-zazhiganie-svetodioda-esd.jpg
│   │   └── plavnoe-zazhiganie-svetodioda-esd.pdf
│   ├── podstavka-dlya-oscillografa/
│   │   ├── podstavka-dlya-oscillografa.md   # title: Подставка для осциллографа
│   │   ├── podstavka-dlya-oscillografa.webp
│   │   ├── podstavka-dlya-oscillografa-01.webp
│   │   ├── podstavka-dlya-oscillografa-02.webp
│   │   ├── podstavka-dlya-oscillografa-03.webp
│   │   ├── podstavka-dlya-oscillografa-04.webp
│   │   ├── podstavka-dlya-oscillografa-05.webp
│   │   ├── podstavka-dlya-oscillografa-06.webp
│   │   ├── podstavka-dlya-oscillografa-07.webp
│   │   ├── podstavka-dlya-oscillografa-08.webp
│   │   ├── podstavka-dlya-oscillografa-09.webp
│   │   └── podstavka-dlya-oscillografa-10.webp
│   ├── prazdnichnyj-domik/
│   │   ├── prazdnichnyj-domik.md   # title: Праздничный домик
│   │   ├── prazdnichnyj-domik.webp
│   │   ├── prazdnichnyj-domik-01.webm
│   │   ├── prazdnichnyj-domik-01.webp
│   │   ├── prazdnichnyj-domik-02.webm
│   │   ├── prazdnichnyj-domik-02.webp
│   │   ├── prazdnichnyj-domik-03.webm
│   │   ├── prazdnichnyj-domik-03.webp
│   │   ├── prazdnichnyj-domik-04.webm
│   │   ├── prazdnichnyj-domik-04.webp
│   │   ├── prazdnichnyj-domik-05.webm
│   │   ├── prazdnichnyj-domik-05.webp
│   │   ├── prazdnichnyj-domik-06.webm
│   │   ├── prazdnichnyj-domik-06.webp
│   │   ├── prazdnichnyj-domik-07.webm
│   │   ├── prazdnichnyj-domik-07.webp
│   │   ├── prazdnichnyj-domik-08.webp
│   │   └── prazdnichnyj-domik-09.webp
│   ├── robot-korova-iz-kartona/
│   │   ├── robot-korova-iz-kartona.md   # title: Робот корова из картона
│   │   ├── robot-korova-iz-kartona.webp
│   │   ├── robot-korova-iz-kartona-01.webm
│   │   ├── robot-korova-iz-kartona-01.webp
│   │   ├── robot-korova-iz-kartona-02.webm
│   │   ├── robot-korova-iz-kartona-02.webp
│   │   ├── robot-korova-iz-kartona-03.webm
│   │   ├── robot-korova-iz-kartona-03.webp
│   │   ├── robot-korova-iz-kartona-04.webm
│   │   ├── robot-korova-iz-kartona-04.webp
│   │   ├── robot-korova-iz-kartona-05.webp
│   │   ├── robot-korova-iz-kartona-06.webp
│   │   ├── robot-korova-iz-kartona-07.webp
│   │   ├── robot-korova-iz-kartona-08.webp
│   │   ├── robot-korova-iz-kartona-09.webp
│   │   └── robot-korova-iz-kartona-10.webp
│   ├── robot-krolik-iz-kartona/
│   │   ├── robot-krolik-iz-kartona.md   # title: Робот кролик из картона
│   │   ├── robot-krolik-iz-kartona.webp
│   │   ├── robot-krolik-iz-kartona-.webp
│   │   ├── robot-krolik-iz-kartona--.webp
│   │   ├── robot-krolik-iz-kartona-01.webm
│   │   ├── robot-krolik-iz-kartona-01.webp
│   │   ├── robot-krolik-iz-kartona-02.webm
│   │   ├── robot-krolik-iz-kartona-02.webp
│   │   ├── robot-krolik-iz-kartona-03.webm
│   │   ├── robot-krolik-iz-kartona-03.webp
│   │   ├── robot-krolik-iz-kartona-04.webm
│   │   ├── robot-krolik-iz-kartona-04.webp
│   │   ├── robot-krolik-iz-kartona-05.webm
│   │   ├── robot-krolik-iz-kartona-05.webp
│   │   ├── robot-krolik-iz-kartona-06.webp
│   │   ├── robot-krolik-iz-kartona-07.webp
│   │   ├── robot-krolik-iz-kartona-08.webp
│   │   ├── robot-krolik-iz-kartona-09.webp
│   │   ├── robot-krolik-iz-kartona-10.webp
│   │   ├── robot-krolik-iz-kartona-11.webp
│   │   ├── robot-krolik-iz-kartona-12.webp
│   │   ├── robot-krolik-iz-kartona-13.webp
│   │   ├── robot-krolik-iz-kartona-14.webp
│   │   ├── robot-krolik-iz-kartona-15.webp
│   │   ├── robot-krolik-iz-kartona-16.webp
│   │   ├── robot-krolik-iz-kartona-17.webp
│   │   ├── robot-krolik-iz-kartona-18.webp
│   │   ├── robot-krolik-iz-kartona-19.webp
│   │   ├── robot-krolik-iz-kartona-20.webp
│   │   ├── robot-krolik-iz-kartona-21.webp
│   │   ├── robot-krolik-iz-kartona-22.webp
│   │   ├── robot-krolik-iz-kartona-23.webp
│   │   ├── robot-krolik-iz-kartona-24.webp
│   │   └── robot-krolik-iz-kartona-25.webp
│   ├── robot-strannik/
│   │   ├── robot-strannik.md   # title: Робот странник
│   │   ├── robot-strannik.webp
│   │   ├── robot-strannik-01.webm
│   │   ├── robot-strannik-01.webp
│   │   ├── robot-strannik-02.webm
│   │   ├── robot-strannik-02.webp
│   │   ├── robot-strannik-03.webm
│   │   ├── robot-strannik-03.webp
│   │   ├── robot-strannik-04.webm
│   │   ├── robot-strannik-04.webp
│   │   ├── robot-strannik-05.webp
│   │   ├── robot-strannik-06.webp
│   │   ├── robot-strannik-07.webp
│   │   ├── robot-strannik-08.webp
│   │   ├── robot-strannik-09.webp
│   │   ├── robot-strannik-10.webp
│   │   ├── robot-strannik-11.webp
│   │   ├── robot-strannik-12.webp
│   │   └── robot-strannik-13.webp
│   ├── simple-cardboard-walking-robot/
│   │   ├── simple-cardboard-walking-robot.md   # title: Робот двуногий шагающий из картона
│   │   ├── simple-cardboard-walking-robot.webp
│   │   ├── simple-cardboard-walking-robot-01.webm
│   │   ├── simple-cardboard-walking-robot-01.webp
│   │   ├── simple-cardboard-walking-robot-02.webm
│   │   ├── simple-cardboard-walking-robot-02.webp
│   │   ├── simple-cardboard-walking-robot-03.webp
│   │   ├── simple-cardboard-walking-robot-04.webp
│   │   ├── simple-cardboard-walking-robotj-ad.dxf
│   │   └── simple-cardboard-walking-robotj-ad.pdf
│   ├── sputnik-1/
│   │   ├── sputnik-1.md   # title: Спутник-1
│   │   ├── sputnik-1.webp
│   │   ├── sputnik-1-01.webp
│   │   ├── sputnik-1-02.webp
│   │   ├── sputnik-1-03.webp
│   │   ├── sputnik-1-04.webp
│   │   ├── sputnik-1-05.webp
│   │   └── sputnik-1-06.webp
│   ├── vibrohod-iz-zubnoj-shchetki/
│   │   ├── vibrohod-iz-zubnoj-shchetki.md   # title: Виброход из зубной щетки
│   │   ├── vibrohod-iz-zubnoj-shchetki.webp
│   │   ├── vibrohod-iz-zubnoj-shchetki-01.webm
│   │   ├── vibrohod-iz-zubnoj-shchetki-01.webp
│   │   ├── vibrohod-iz-zubnoj-shchetki-02.webm
│   │   ├── vibrohod-iz-zubnoj-shchetki-02.webp
│   │   ├── vibrohod-iz-zubnoj-shchetki-03.webm
│   │   ├── vibrohod-iz-zubnoj-shchetki-03.webp
│   │   ├── vibrohod-iz-zubnoj-shchetki-04.webm
│   │   ├── vibrohod-iz-zubnoj-shchetki-04.webp
│   │   ├── vibrohod-iz-zubnoj-shchetki-05.webm
│   │   ├── vibrohod-iz-zubnoj-shchetki-05.webp
│   │   ├── vibrohod-iz-zubnoj-shchetki-06.webm
│   │   ├── vibrohod-iz-zubnoj-shchetki-06.webp
│   │   ├── vibrohod-iz-zubnoj-shchetki-07.webm
│   │   └── vibrohod-iz-zubnoj-shchetki-08.webm
│   └── yablonevoe-derevo/
│       ├── yablonevoe-derevo.md   # title: Яблоневое дерево
│       ├── yablonevoe-derevo.webp
│       ├── yablonevoe-derevo-01.webm
│       ├── yablonevoe-derevo-01.webp
│       ├── yablonevoe-derevo-02.webp
│       ├── yablonevoe-derevo-03.webp
│       ├── yablonevoe-derevo-04.webp
│       ├── yablonevoe-derevo-trafaret.pdf
│       └── yablonevoe-derevo-trafaret.spl8
├── inspiration/
│   ├── img/
│   │   ├── aluminum-electrolytic-capacitor-1.webp
│   │   ├── analog-panel-meter-1.webp
│   │   ├── analog-panel-meter-2.webp
│   │   ├── analog-panel-meter-3.webp
│   │   ├── carbon-film-resistor-1.webp
│   │   ├── carbon-film-resistor-2.webp
│   │   ├── carbon-film-resistor-3.webp
│   │   ├── ceramic-disc-capacitor-1.webp
│   │   ├── ceramic-disc-capacitor-2.webp
│   │   ├── ceramic-disc-capacitor-3.webp
│   │   ├── magnetic-buzzer-1.webp
│   │   ├── magnetic-buzzer-2.webp
│   │   ├── our-dream.webp
│   │   ├── strontium-atom-1.webp
│   │   ├── strontium-atom-2.webp
│   │   ├── through-hole-red-led-1.webp
│   │   └── through-hole-red-led-2.webp
│   ├── aluminum-electrolytic-capacitor.md   # title: Алюминиевый электролитический конденсатор
│   ├── analog-panel-meter.md   # title: Аналоговый стрелочный измерительный прибор
│   ├── carbon-film-resistor.md   # title: Углеродный пленочный резистор
│   ├── ceramic-disc-capacitor.md   # title: Керамический дисковый конденсатор
│   ├── index.md   # title: Техническое вдохновение
│   ├── magnetic-buzzer.md   # title: Магнитный зуммер
│   ├── our-dream.md   # title: Наша мечта ...
│   ├── strontium-atom.md   # title: Одиночный атом стронция в ионной ловушке
│   └── through-hole-red-led.md   # title: Красный светодиод с выводами для сквозного монтажа
├── projects/
│   ├── index.md   # title: Учебные проекты
│   └── novyj-robot-shagohod.md   # title: Робот новый
├── test/
│   ├── folder/
│   │   ├── test.webp
│   │   ├── test-v.webp
│   │   └── test-vertical.webm
│   ├── -figure-single.md   # title: Тестирование модуля одиночных журнальных блоков (fig)
│   ├── img-base.md   # title: Тестирование модуля базовых изображений (img_base.py)
│   ├── img-figure.md   # title: Тестирование модуля групповых журнальных блоков (img_figure.py)
│   ├── links.md   # title: Tест с преобразованием ссылок фото и видео
│   ├── -row-photo.md   # title: Tесты с групповыми фото
│   ├── -single-photo.md   # title: Tесты с одиночными фото
│   ├── vault.md   # title: Тестирование изолированных зон безопасности (vault.py)
│   ├── -video.md   # title: Tест с видео
│   └── Без названия 1.md — about отсутствует
├── tools/
│   ├── files/
│   │   ├── fritzing-led-sketch.fzz
│   │   ├── pianino-elektronnoe-proekt-uchebnyj.lay6
│   │   └── sprintlayout.zip
│   ├── img/
│   │   ├── fritzing-workflow-1-0-5.webp
│   │   └── sprintlayout-6-0-workflow.webp
│   ├── fritzing.md   # title: Fritzing
│   ├── index.md   # title: Полезные инструменты
│   └── sprintlayout.md   # title: Sprint Layout
├── .gitignore   # Файл исключений системы контроля версий Git
├── _config.yml — about отсутствует
├── 404.html — about отсутствует
├── CHANGELOG.md   # title: Журнал изменений проекта
├── CODE_OF_CONDUCT.md — about отсутствует
├── CONTRIBUTING.md   # title: Соавторство и вклад в развитие проекта.
├── giscus.json — about отсутствует
├── index.md   # title: Творческая лаборатория познавательного развития
├── LICENSE.txt — about отсутствует
├── README.md
├── ROADMAP.md   # title: Дорожная карта проекта
├── robots.txt — about отсутствует
├── STRUCTURE.md — about отсутствует
└── tags.md   # title: Поиск по тегам
```
