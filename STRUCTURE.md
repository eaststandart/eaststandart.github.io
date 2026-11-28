# Структура репозитория eaststandart.github.io

```text
eaststandart.github.io/
├── .github/
│   └── workflows/
│       ├── deploy.yml              # Сценарий автоматической сборки и публикации сайта GitHub Pages.
│       ├── journal-attendance.yml  # Модуль формирования Журнала посещений.
│       └── media-receiver-test.yml # Временный тестовый робот приема сигналов медиа-шлюза.
├── _actions/
│   └── journal_attendance/
│       ├── __init__.py           # Пустой файл-маркер, обозначающий каталог journal_attendance как Python-пакет.
│       ├── ja_data_parser.py     # Модуль сетевого парсинга и сборщика отчетов.
│       ├── ja_gate_closer.py     # Модуль шлюзового обновления данных и очистки.
│       ├── ja_report_builder.py  # Модуль маркдаун-дизайна и GraphQL-публикации отчётов.
│       ├── ja_tgbot_notify.py    # Модуль отправки отчетов в каналы и группы Телеграм.
│       ├── ja_tgbot_personal.py  # Модуль отправки персональных отчетов в Телеграм.
│       ├── ja_wabot_personal.py  # Модуль отправки персональных отчетов в WhatsApp.
│       ├── journal_attendance.py # Модуль управления сборкой отчета посещений.
│       └── README.md
├── _engineers/
│   └── liza-b.md # Дневник инженера: Лиза Б.
├── _includes/
│   ├── comment-builder.liquid    # Модуль шаблона интерфейса Конструктора комментариев.
│   ├── discus.liquid             # Интеграция и вывод блока дискуссий giscus.
│   ├── faire-grid.liquid         # Универсальный модуль автоматической генерации сеток разделов сайта.
│   ├── feed.liquid               # Сборка и рендер первой страницы обновлений на основе квантованных корзин feed.yml.
│   ├── footer.liquid             # Подвал сайта.
│   ├── header-theme.liquid       # Смена логотипа главной страницы сайта.
│   ├── journal-attendance.liquid # Модуль шаблона интерфейса Журнала посещений.
│   ├── mathjax.html              # Подключение математического движка MathJax v3.
│   ├── media-logic.liquid        # Глобальный модуль оптимизации медиаконтента.
│   ├── navigation.liquid         # Модуль навигации сайта.
│   ├── pagination.liquid         # Модуль пагинации страниц.
│   ├── posts-page.liquid         # Модуль автоматического вывода локальных лент постов на страницах проектов.
│   ├── posts-page-open.liquid    # Изолированный модуль развернутого вывода постов проекта.
│   ├── README.md
│   ├── seo-meta.liquid           # Модуль сборки SEO и Open Graph мета-тегов.
│   ├── tags-logic.liquid         # Сбор и генерация структуры тегов.
│   └── zoom.liquid               # Модульный HTML-контейнер и подключение скрипта зума картинок.
├── _layouts/
│   ├── default.md # Глобальный шаблон оформления страниц сайта.
│   ├── faire.md   # Шаблон структуры страниц в разделе faire.
│   ├── feed.md    # Шаблон ленты новостей.
│   ├── home.md    # Шаблон главной страницы сайта.
│   ├── page.md    # Шаблон для базовых страниц сайт.
│   └── README.md
├── _pages/
│   ├── comment-builder.md    # Конструктор дискуссий
│   ├── engineers.md          # Работы юных инженеров
│   ├── faire.md              # Ярмарка поделок
│   ├── feed-journal.md       # Журнал проектов
│   ├── feed-media.md         # Медиа материалы
│   ├── feed-news.md          # Новости уголка конструктора
│   ├── feed-post.md          # Посты
│   ├── feed-question.md      # Вопросы проектов
│   ├── feed-reference.md     # Справочные материалы
│   ├── journal-attendance.md # Веб-страница Журнала посещений
│   ├── people.md             # Люди
│   ├── process.md            # Творческий процесс
│   └── README.md
├── _people/
│   └── fran-blanche.md # Фрэн Бланш (Fran Blanche)
├── _posts/
│   ├── 2025-10-26-simple-cardboard-walking-robot.md             # Робот двуногий шагающий из картона: галерея
│   ├── 2025-10-27-simple-cardboard-walking-robot.md             # Робот двуногий шагающий из картона: вопросы по проекту
│   ├── 2025-10-28-simple-cardboard-walking-robot.md             # Робот двуногий шагающий из картона: раскачивание корпуса
│   ├── 2025-10-30-nastolnaya-svetodiodnaya-lampa-s-rasteniem.md # Настольная светодиодная лампа с растением: галерея
│   ├── 2025-10-31-nastolnaya-svetodiodnaya-lampa-s-rasteniem.md # Настольная светодиодная лампа с растением: вопросы по проекту
│   ├── 2025-11-02-besprovodnoj-telegraf.md                      # Беспроводной телеграф: галерея
│   ├── 2025-11-03-besprovodnoj-telegraf.md                      # Беспроводной телеграф: вопросы по проекту
│   ├── 2025-11-06-sputnik-1.md                                  # Спутник-1: галерея
│   ├── 2025-11-07-sputnik-1.md                                  # Спутник-1: вопросы по проекту
│   ├── 2025-11-08-sputnik-1.md                                  # Спутник-1: общий вид
│   ├── 2025-11-12-fonarik-svetodiodnyj-bumazhnyj.md             # Фонарик светодиодный бумажный: галерея
│   ├── 2025-11-13-fonarik-svetodiodnyj-bumazhnyj.md             # Фонарик светодиодный бумажный: вопросы по проекту
│   ├── 2025-11-14-fonarik-svetodiodnyj-bumazhnyj.md             # Фонарик светодиодный бумажный: описание работы
│   ├── 2025-11-21-vibrohod-iz-zubnoj-shchetki.md                # Виброход из зубной щетки: галерея
│   ├── 2025-11-22-vibrohod-iz-zubnoj-shchetki.md                # Виброход из зубной щетки: вопросы по проекту
│   ├── 2025-11-23-vibrohod-iz-zubnoj-shchetki.md                # Робот зубочист: вариант конструкции
│   ├── 2025-11-24-vibrohod-iz-zubnoj-shchetki.md                # Робот зубочист: скорость движения
│   ├── 2025-11-26-robot-strannik.md                             # Робот странник: галерея
│   ├── 2025-11-27-robot-strannik.md                             # Робот странник: вопросы по проекту
│   ├── 2025-11-28-robot-strannik.md                             # Робот странник: модель №1
│   ├── 2025-11-29-robot-strannik.md                             # Робот странник: тип движения
│   ├── 2025-12-22-yablonevoe-derevo.md                          # Яблоневое дерево: галерея
│   ├── 2025-12-23-yablonevoe-derevo.md                          # Яблоневое дерево: вопросы по проекту
│   ├── 2026-01-25-blaster-elektroakusticheskij.md               # Бластер электроакустический: галерея
│   ├── 2026-01-26-blaster-elektroakusticheskij.md               # Бластер электроакустический: вопросы по проекту
│   ├── 2026-01-27-blaster-elektroakusticheskij.md               # Бластер электроакустический: подключение индикатора
│   ├── 2026-01-29-detektor-pereliva.md                          # Детектор перелива: галерея
│   ├── 2026-01-30-detektor-pereliva.md                          # Детектор перелива: вопросы по проекту
│   ├── 2026-01-31-detektor-pereliva.md                          # Детектор перелива: общий вид
│   ├── 2026-02-01-detektor-pereliva.md                          # Детектор перелива: описание работы
│   ├── 2026-02-02-prazdnichnyj-domik.md                         # Праздничный домик: галерея
│   ├── 2026-02-03-prazdnichnyj-domik.md                         # Праздничный домик: вопросы по проекту
│   ├── 2026-02-04-prazdnichnyj-domik.md                         # Праздничный домик: создала Лиза Б.
│   ├── 2026-02-05-prazdnichnyj-domik.md                         # Праздничный домик: создал Кирилл К.
│   ├── 2026-02-10-elektronnyj-organ.md                          # Электронный орган: галерея
│   ├── 2026-02-11-elektronnyj-organ.md                          # Электронный орган: вопросы по проекту
│   ├── 2026-02-12-elektronnyj-organ.md                          # Электронный орган: создала Лиза Б.
│   ├── 2026-02-13-elektronnyj-organ.md                          # Электронный орган: этапы создания
│   ├── 2026-02-14-elektronnyj-organ.md                          # Электронный орган: паразитная генерация
│   ├── 2026-02-22-robot-korova-iz-kartona.md                    # Робот корова из картона: галерея
│   ├── 2026-02-23-robot-korova-iz-kartona.md                    # Робот корова из картона: вопросы по проекту
│   ├── 2026-02-24-robot-korova-iz-kartona.md                    # Робот корова из картона: вид и движение
│   ├── 2026-03-08-robot-krolik-iz-kartona.md                    # Робот кролик из картона: галерея
│   ├── 2026-03-09-robot-krolik-iz-kartona.md                    # Робот кролик из картона: вопросы по проекту
│   ├── 2026-03-10-robot-krolik-iz-kartona.md                    # Робот кролик из картона: вид и движение
│   ├── 2026-03-11-robot-krolik-iz-kartona.md                    # Робот кролик из картона: самодельный редуктор
│   ├── 2026-03-13-plavnoe-zazhiganie-svetodioda.md              # Эффект плавного зажигания светодиода: галерея
│   ├── 2026-03-14-plavnoe-zazhiganie-svetodioda.md              # Эффект плавного зажигания светодиода: вопросы по проекту
│   ├── 2026-03-15-plavnoe-zazhiganie-svetodioda.md              # Эффект плавного зажигания светодиода: макет эксперимента
│   ├── 2026-03-16-plavnoe-zazhiganie-svetodioda.md              # Эффект плавного зажигания светодиода: время зажигания и гашения
│   ├── 2026-04-03-pano-uslovnye-oboznacheniya.md                # Условные обозначения: галерея
│   ├── 2026-04-04-pano-uslovnye-oboznacheniya.md                # Условные обозначения: вопросы по проекту
│   ├── 2026-04-06-avtomobil-s-polnym-privodom-iz-kartona.md     # Автомобиль 4wd из картона: галерея
│   ├── 2026-04-07-avtomobil-s-polnym-privodom-iz-kartona.md     # Автомобиль 4wd из картона: вопросы по проекту
│   ├── 2026-04-08-avtomobil-s-polnym-privodom-iz-kartona.md     # Автомобиль 4wd из картона: вид и движение
│   ├── 2026-04-10-podstavka-dlya-oscillografa.md                # Подставка для осциллографа: галерея
│   ├── 2026-04-11-podstavka-dlya-oscillografa.md                # Подставка для осциллографа: вопросы по проекту
│   ├── 2026-04-12-podstavka-dlya-oscillografa.md                # Подставка для осциллографа: общий вид
│   ├── 2026-04-14-muzykalnyj-karandash.md                       # Музыкальный карандаш: галерея
│   ├── 2026-04-15-muzykalnyj-karandash.md                       # Музыкальный карандаш: вопросы по проекту
│   ├── 2026-04-16-muzykalnyj-karandash.md                       # Музыкальный карандаш: общий вид
│   ├── 2026-04-17-muzykalnyj-karandash.md                       # Музыкальный карандаш: сборка
│   ├── 2026-04-18-muzykalnyj-karandash.md                       # Музыкальный карандаш: описание работы
│   ├── 2026-04-19-muzykalnyj-karandash.md                       # Музыкальный карандаш: тестирование
│   ├── 2026-04-20-muzykalnyj-karandash.md                       # Музыкальный карандаш: применение
│   ├── 2026-05-11-metronom-signalnyj.md                         # Метроном сигнальный: галерея
│   ├── 2026-05-12-metronom-signalnyj.md                         # Метроном сигнальный: вопросы по проекту
│   ├── 2026-05-13-metronom-signalnyj.md                         # Метроном сигнальный: изделие №1
│   ├── 2026-05-14-metronom-signalnyj.md                         # Метроном сигнальный: этапы создания
│   ├── 2026-05-15-metronom-signalnyj.md                         # Метроном сигнальный: общий вид
│   ├── 2026-06-05-robot-krolik-iz-kartona.md                    # Робот кролик из картона: модель с разворотом
│   └── 2026-06-10-multivibrator-nesimmetrichnyj.md              # Мультивибратор несимметричный
├── _process/
│   ├── 2026-creative-proces-regular.md          # Черновик регулярного творческого процесса; публикация отключена.
│   ├── 2026-creative-process-regular-techlab.md # Инженерные занятия: 2026 [TechLab]
│   └── 2026-creative-process-regular-valery.md  # Инженерные занятия: 2026 – Валерий Р.
├── _reference/
├── assets/
│   ├── batchfiles/
│   │   ├── generate_readme.bat   # Скрипт автоматического сбора описаний и документирования файлов папки.
│   │   ├── README.md
│   │   ├── structure_tree.bat    # Скрипт автоматической генерации интерактивной структуры дерева репозитория.
│   │   └── webm_optimization.bat # Скрипт для оптимизации видео в формате webm сайта Лаборатории.
│   ├── css/
│   │   ├── biblio.css             # Модуль стилей для отображения карточек книг электронной библиотеки сайта.
│   │   ├── comment-builder.css    # Модуль стилей веб-страницы формы комментариев.
│   │   ├── diary.css              # Модуль стилей для отображения карточек Дневника инженера.
│   │   ├── faire.css              # Модуль изолированных стилей раздела Ярмарки поделок
│   │   ├── footnotes.css          # Модуль стилей для оформления блока примечаний и академических сносок.
│   │   ├── giscus.css             # Модуль адаптивной верстки интерактивного виджета комментариев Giscus.
│   │   ├── giscus-gallery.css     # Модуль изолированных стилей страницы дискусий Галерея раздела Ярмарка поделок
│   │   ├── giscus-process.css     # Модуль изолированных стилей страницы дискусий раздела Творческий процесс
│   │   ├── giscus-v1.0.css        # Первая версия пользовательского оформления комментариев Giscus.
│   │   ├── giscus-v1.1-0.css      # Версия пользовательского оформления Giscus для раздела творческого процесса.
│   │   ├── header-classic.css     # Модуль стилей глобальной шапки и элементов брендинга главной страницы.
│   │   ├── header-desktop.css     # Модуль тестовой интерактивной шапки сайта с имитацией псевдоконсоли
│   │   ├── header-panel.css       # Модуль стилей интерактивной панели управления и консольной шапки сайта.
│   │   ├── images.css             # Модуль изображений.
│   │   ├── journal-attendance.css # Модуль стилей веб-страницы журнала посещений.
│   │   ├── pagination.css         # Модуль универсальной пагинации, крошек навигации и лент обновлений
│   │   ├── projects.css           # Модуль стилей двухмерной сетки для раздела Учебные проекты.
│   │   ├── README.md
│   │   ├── style.css              # Ядро главных стилей сайта Лаборатории.
│   │   ├── tools.css              # Модуль стилей для отображения карточек используемого инструментария и инженерного ПО.
│   │   ├── video.css              # Модуль стилей для отображения видеоплееров, оптимизации загрузки и антипрыжка контента.
│   │   ├── video-figure.css       # Стили одиночных видеоблоков с подписями.
│   │   ├── video-figure-v.css     # Стили вертикальных видеоблоков.
│   │   ├── video-gallery.css      # Стили галерейных рядов видеороликов без подписей.
│   │   └── zoom.css               # Модуль центрированного модального зума (Лайтбокса) для картинок.
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
│   │   │   ├── 01-comment-notify.js      # Модуль уведомлений и статусов конструктора.
│   │   │   ├── 02-comment-auth.js        # Модуль авторизации и проверки доступа к Конструктору.
│   │   │   ├── 03-comment-form.js        # Модуль инициализации и сброса формы конструктора.
│   │   │   ├── 04-drafts-parser.js       # Модуль разбора структуры черновиков Markdown.
│   │   │   ├── 05-drafts-loader.js       # Модуль загрузки списка черновиков из GitHub.
│   │   │   ├── 06-drafts-injector.js     # Модуль восстановления выбранного черновика в конструкторе.
│   │   │   ├── 07-drafts-delete.js       # Модуль управления удалением черновиков.
│   │   │   ├── 08-comment-validation.js  # Модуль проверки данных комментария.
│   │   │   ├── 09-comment-lock.js        # Модуль блокировки формы конструктора.
│   │   │   ├── 10-media-blocks.js        # Модуль создания и удаления медиаблоков.
│   │   │   ├── 11-media-files.js         # Модуль управления данными медиафайлов.
│   │   │   ├── 12-media-files-ui.js      # Модуль интерфейса списка медиафайлов.
│   │   │   ├── 13-media-upload.js        # Модуль загрузки медиафайлов в буферный репозиторий.
│   │   │   ├── 14-comment-markdown.js    # Модуль формирования и кодирования Markdown комментария.
│   │   │   ├── 15-comment-github-save.js # Модуль сохранения Markdown-файлов через GitHub API.
│   │   │   ├── 16-comment-submit.js      # Модуль обработки отправки комментария и сохранения черновика.
│   │   │   └── README.md
│   │   ├── journal-attendance/
│   │   │   ├── 01-core-auth.js           # Модуль авторизации и контроля доступа.
│   │   │   ├── 02-students-loader.js     # Модуль сетевой загрузки базы расписания.
│   │   │   ├── 03-yaml-parser.js         # Модуль объектного парсинга и валидации синтаксиса.
│   │   │   ├── 04-journal-ui.js          # Модуль динамической отрисовки интерфейса.
│   │   │   ├── 05-attendance-commands.js # Модуль сбора посещаемости и обработки системных команд.
│   │   │   ├── 06-status-and-repair.js   # Модуль управления состояниями и опроса сервера.
│   │   │   ├── 07-validation.js          # Модуль контроля безопасности строк.
│   │   │   └── README.md
│   │   ├── image-lazy-load.js  # Модуль лези-лоада картинок.
│   │   ├── pagination-logic.js # Модуль пагинации.
│   │   ├── posts-page-list.js  # Модуль фильтрации и зачистки ленты медиа.
│   │   ├── posts-page-nav.js   # Модуль локальной пагинации проектов.
│   │   ├── README.md
│   │   ├── tags-search.js      # Модуль js-фильтрации страницы поиска по тегам.
│   │   ├── video-lazy-load.js  # Профессиональный модуль ленивой предзагрузки нативных видеоплееров.
│   │   └── zoom.js             # Модуль идеального центрированного модального зума (Лайтбокса) для картинок.
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
│   ├── borisov-v-g-enciklopediya-yunogo-radiolyubitelya-konstruktora-2001.md # Энциклопедия юного радиолюбителя-конструктора
│   ├── chernenko-g-t-puteshestvie-v-stranu-robotov-1977.md                   # Путешествие в страну роботов
│   ├── index.md                                                              # Список литературы
│   ├── kiselyov-l-kniga-yunogo-tekhnika-1948.md                              # Книга юного техника
│   ├── materialy-dlya-samostoyatelnogo-izucheniya-osnov-elektroniki.md       # Материалы для самостоятельного изучения основ электроники
│   ├── pchyolko-a-s-arifmetika-dlya-nachalnoj-shkoly-1955.md                 # Книги по арифметике, сборники задач и упражнений к ним
│   ├── rostovcev-n-n-risovanie-1957.md                                       # Рисование, 1-4 класс
│   ├── svoren-r-a-elektronika-shag-za-shagom-1991.md                         # Электроника шаг за шагом
│   └── zak-a-z-intellektika-2024.md                                          # Интеллектика. Тетрадь для развития мыслительных способностей
├── bin/
│   ├── feed.py       # Изолированный монолитный сборщик единой ленты обновлений из Источника Правды.
│   ├── images.py     # Монолитный объединенный модуль предобработки изображений для Obsidian -> Jekyll.
│   ├── pathlinks.py  # Модуль глобальной очистки путей, конвертации Wiki-ссылок и текстовых связей Obsidian.
│   ├── postpage.py   # Изолированный автономный генератор физических md-страниц архивов проектов.
│   ├── preprocess.py # Главный менеджер автоматической предобработки контента Obsidian перед сборкой Jekyll.
│   ├── sitemap.py    # Главный диспетчер и общий купол конвейера
│   ├── smLinks.py    # Геометрия каркаса и связей сайта.
│   ├── smPropsIn.py  # Обогащение карты и расчет инвариантных дат
│   ├── smPropsOut.py # Расчет тегов, категорий контура и сохранение файлов
│   ├── vault.py      # Автономный сквозной точечный сейф исключений для защиты примеров кода.
│   └── videos.py     # Модуль предобработки видео-ссылок для Obsidian -> Jekyll с поддержкой ленивой загрузки.
├── diary/
│   ├── index.md           # Дневник инженера
│   └── note-schematics.md # Заметки по схемотехнике
├── faire/
│   ├── avtomobil-s-polnym-privodom-iz-kartona/
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona.md # Автомобиль с полным приводом из картона
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona.webp # Общий вид: картонный автомобиль с полным приводом
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-01.webm # Сборка и проверка картонного автомобиля с полным приводом
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-01.webp # Картонный автомобиль с полным приводом: ракурс 1
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-02.webm # Испытание движения полноприводной модели на полу
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-02.webp # Картонный автомобиль с полным приводом: ракурс 2
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-03.webm # Заезд самодельного автомобиля по ровной поверхности
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-03.webp # Картонный автомобиль с полным приводом: ракурс 3
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-04.webm # Проверка управления и привода картонного автомобиля
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-04.webp # Картонный автомобиль с полным приводом: ракурс 4
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-05.webp # Картонный автомобиль с полным приводом: ракурс 5
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-06.webp # Картонный автомобиль с полным приводом: ракурс 6
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-07.webp # Картонный автомобиль с полным приводом: ракурс 7
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-08.webp # Картонный автомобиль с полным приводом: ракурс 8
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-09.webp # Картонный автомобиль с полным приводом: ракурс 9
│   │   ├── avtomobil-s-polnym-privodom-iz-kartona-10.webp # Картонный автомобиль с полным приводом: ракурс 10
│   │   └── avtomobil-s-polnym-privodom-iz-kartona-11.webp # Картонный автомобиль с полным приводом: ракурс 11
│   ├── besprovodnoj-telegraf/
│   │   ├── besprovodnoj-telegraf.md # Беспроводной телеграф
│   │   ├── besprovodnoj-telegraf.webp # Общий вид: макеты беспроводного телеграфа
│   │   ├── besprovodnoj-telegraf-01.webm # Передача сигнала между блоками беспроводного телеграфа
│   │   ├── besprovodnoj-telegraf-01.webp # Макеты беспроводного телеграфа: ракурс 1
│   │   └── besprovodnoj-telegraf-02.webp # Макеты беспроводного телеграфа: ракурс 2
│   ├── blaster-elektroakusticheskij/
│   │   ├── blaster-elektroakusticheskij.md # Бластер электроакустический
│   │   ├── blaster-elektroakusticheskij.webp # Общий вид: электроакустический бластер
│   │   ├── blaster-elektroakusticheskij-01.webm # Проверка электроакустического бластера с цифровой индикацией
│   │   ├── blaster-elektroakusticheskij-01.webp # Электроакустический бластер: ракурс 1
│   │   ├── blaster-elektroakusticheskij-02.webp # Электроакустический бластер: ракурс 2
│   │   ├── blaster-elektroakusticheskij-03.webp # Электроакустический бластер: ракурс 3
│   │   ├── blaster-elektroakusticheskij-ad.dxf
│   │   ├── blaster-elektroakusticheskij-ad.pdf
│   │   ├── blaster-elektroakusticheskij-esd.pdf
│   │   └── blaster-elektroakusticheskij-esd.spl8
│   ├── detektor-pereliva/
│   │   ├── detektor-pereliva.md # Детектор перелива
│   │   ├── detektor-pereliva.webp # Общий вид: детектор перелива
│   │   ├── detektor-pereliva-01.webm # Сборка и проверка электронного датчика перелива
│   │   ├── detektor-pereliva-01.webp # Детектор перелива: ракурс 1
│   │   ├── detektor-pereliva-02.webm # Демонстрация работы датчика перелива на макете
│   │   ├── detektor-pereliva-02.webp # Детектор перелива: ракурс 2
│   │   ├── detektor-pereliva-03.webp # Детектор перелива: ракурс 3
│   │   ├── detektor-pereliva-04.webp # Детектор перелива: ракурс 4
│   │   ├── detektor-pereliva-05.webp # Детектор перелива: ракурс 5
│   │   ├── detektor-pereliva-06.webp # Детектор перелива: ракурс 6
│   │   ├── detektor-pereliva-07.webp # Детектор перелива: ракурс 7
│   │   ├── detektor-pereliva-08.webp # Детектор перелива: ракурс 8
│   │   ├── detektor-pereliva-09.webp # Детектор перелива: ракурс 9
│   │   ├── detektor-pereliva-10.webp # Детектор перелива: ракурс 10
│   │   ├── detektor-pereliva-11.webp # Детектор перелива: ракурс 11
│   │   ├── detektor-pereliva-12.webp # Детектор перелива: ракурс 12
│   │   ├── detektor-pereliva-13.webp # Детектор перелива: ракурс 13
│   │   ├── detektor-pereliva-14.webp # Детектор перелива: ракурс 14
│   │   ├── detektor-pereliva-15.webp # Детектор перелива: ракурс 15
│   │   ├── detektor-pereliva-16.webp # Принципиальная схема звукового сигнализатора с контактным датчиком
│   │   ├── detektor-pereliva-17.webp # Схема работы транзисторного узла, этап 1
│   │   ├── detektor-pereliva-18.webp # Схема работы транзисторного узла, этап 2
│   │   ├── detektor-pereliva-19.webp # Схема работы трансформатора и звукового излучателя
│   │   ├── detektor-pereliva-20.webp # Схема формирования звукового сигнала
│   │   ├── detektor-pereliva-21.webp # Схема завершающего этапа цикла работы устройства
│   │   ├── detektor-pereliva-22.webp # Последовательность этапов работы звукового сигнализатора
│   │   ├── detektor-pereliva-23.webp # Пошаговая схема подключения датчика к контактам А и Б
│   │   ├── detektor-pereliva-esd.pdf
│   │   ├── detektor-pereliva-esd.spl8
│   │   ├── detektor-perelivaj-ad.dxf
│   │   └── detektor-perelivaj-ad.pdf
│   ├── elektronnyj-organ/
│   │   ├── elektronnyj-organ.md # Электронный орган
│   │   ├── elektronnyj-organ.webp # Общий вид: электронный орган
│   │   ├── elektronnyj-organ-01.webm # Демонстрация самодельного электронного органа с громкоговорителем
│   │   ├── elektronnyj-organ-01.webp # Электронный орган: ракурс 1
│   │   ├── elektronnyj-organ-02.webm # Проверка звучания электронного органа
│   │   ├── elektronnyj-organ-02.webp # Электронный орган: ракурс 2
│   │   ├── elektronnyj-organ-03.webm # Испытание клавиш и звукового модуля электронного органа
│   │   ├── elektronnyj-organ-03.webp # Электронный орган: ракурс 3
│   │   ├── elektronnyj-organ-04.webm # Настройка электронного органа на рабочем столе
│   │   ├── elektronnyj-organ-04.webp # Электронный орган: ракурс 4
│   │   ├── elektronnyj-organ-05.webm # Игра на собранном электронном органе
│   │   ├── elektronnyj-organ-05.webp # Электронный орган: ракурс 5
│   │   ├── elektronnyj-organ-06.webp # Электронный орган: ракурс 6
│   │   ├── elektronnyj-organ-07.webp # Электронный орган: ракурс 7
│   │   ├── elektronnyj-organ-08.webp # Электронный орган: ракурс 8
│   │   ├── elektronnyj-organ-09.webp # Электронный орган: ракурс 9
│   │   ├── elektronnyj-organ-10.webp # Электронный орган: ракурс 10
│   │   ├── elektronnyj-organ-11.webp # Электронный орган: ракурс 11
│   │   ├── elektronnyj-organ-12.webp # Электронный орган: ракурс 12
│   │   ├── elektronnyj-organ-13.webp # Электронный орган: ракурс 13
│   │   ├── elektronnyj-organ-14.webp # Эскиз корпуса и компоновки электронного органа
│   │   ├── elektronnyj-organ-15.webp # Деревянная основа клавишного механизма и отдельные платы кнопок
│   │   ├── elektronnyj-organ-16.webp # Подготовленные детали корпуса, клавиш и соединительных проводов
│   │   ├── elektronnyj-organ-17.webp # Фотошаблоны печатных плат электронного органа
│   │   ├── elektronnyj-organ-18.webp # Печатные платы после травления
│   │   ├── elektronnyj-organ-19.webp # Печатная плата с маркировкой электронного органа
│   │   ├── elektronnyj-organ-20.webp # Крупный план печатной платы с маркировкой
│   │   ├── elektronnyj-organ-21.webp # Две платы с маркировкой после обработки
│   │   ├── elektronnyj-organ-22.webp # Печатные платы с проявленными медными дорожками
│   │   ├── elektronnyj-organ-23.webp # Две платы с рисунком дорожек и маркировкой
│   │   ├── elektronnyj-organ-24.webp # Сравнение двух вариантов изготовленных печатных плат
│   │   ├── elektronnyj-organ-25.webp # Печатная плата с маркировкой и контактными площадками
│   │   ├── elektronnyj-organ-26.webp # Крупный план платы с дорожками и обозначениями компонентов
│   │   ├── elektronnyj-organ-27.webp # Печатная плата с маркировкой органа и таймера NE555
│   │   ├── elektronnyj-organ-28.webp # Плата с надписями на фоне рабочего стола
│   │   ├── elektronnyj-organ-29.webp # Электронный орган: ракурс 29
│   │   ├── elektronnyj-organ-30.webp # Электронный орган: ракурс 30
│   │   ├── elektronnyj-organ-31.webp # Электронный орган: ракурс 31
│   │   ├── elektronnyj-organ-32.webp # Электронный орган: ракурс 32
│   │   ├── elektronnyj-organ-33.webp # Электронный орган: ракурс 33
│   │   ├── elektronnyj-organ-34.webp # Электронный орган: ракурс 34
│   │   ├── elektronnyj-organ-35.webp # Электронный орган: ракурс 35
│   │   ├── elektronnyj-organ-36.webp # Электронный орган: ракурс 36
│   │   ├── elektronnyj-organ-37.webp # Электронный орган: ракурс 37
│   │   ├── elektronnyj-organ-38.webp # Электронный орган: ракурс 38
│   │   ├── elektronnyj-organ-39.webp # Электронный орган: ракурс 39
│   │   ├── elektronnyj-organ-40.webp # Электронный орган: ракурс 40
│   │   ├── elektronnyj-organ-41.webp # Экран осциллографа с прямоугольным сигналом генератора
│   │   ├── elektronnyj-organ-42.webp # Рукописные схемы и расчёты электронного органа
│   │   └── elektronnyj-organ-pcb.lay6
│   ├── fonarik-svetodiodnyj-bumazhnyj/
│   │   ├── fonarik-svetodiodnyj-bumazhnyj.md # Фонарик светодиодный бумажный
│   │   ├── fonarik-svetodiodnyj-bumazhnyj.pdf
│   │   ├── fonarik-svetodiodnyj-bumazhnyj.spl8
│   │   ├── fonarik-svetodiodnyj-bumazhnyj.webp # Общий вид: бумажный светодиодный фонарик
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-01.webm # Включение светодиода в самодельном бумажном фонарике
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-01.webp # Бумажный светодиодный фонарик: ракурс 1
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-02.webp # Бумажный светодиодный фонарик: ракурс 2
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-03.webp # Принципиальная схема светодиодного фонарика
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-04.webp # Учебная иллюстрация с фонарём
│   │   ├── fonarik-svetodiodnyj-bumazhnyj-05.webp # Схематичное изображение полярности подключения светодиода
│   │   └── fonarik-svetodiodnyj-bumazhnyj-trafaret.pdf
│   ├── metronom-signalnyj/
│   │   ├── metronom-signalnyj.md # Метроном сигнальный
│   │   ├── metronom-signalnyj.webp # Общий вид: сигнальный метроном
│   │   ├── metronom-signalnyj-01.webm # Демонстрация корпуса и работы сигнального метронома
│   │   ├── metronom-signalnyj-01.webp # Сигнальный метроном: ракурс 1
│   │   ├── metronom-signalnyj-02.webm # Проверка электронной схемы сигнального метронома
│   │   ├── metronom-signalnyj-02.webp # Сигнальный метроном: ракурс 2
│   │   ├── metronom-signalnyj-03.webm # Настройка и проверка схемы сигнального метронома
│   │   ├── metronom-signalnyj-03.webp # Сигнальный метроном: ракурс 3
│   │   ├── metronom-signalnyj-04.webm # Демонстрация световой индикации сигнального метронома
│   │   ├── metronom-signalnyj-04.webp # Сигнальный метроном: ракурс 4
│   │   ├── metronom-signalnyj-05.webm # Проверка переключателей и режимов сигнального метронома
│   │   ├── metronom-signalnyj-05.webp # Сигнальный метроном: ракурс 5
│   │   ├── metronom-signalnyj-06.webm # Работа метронома в затемнённом помещении
│   │   ├── metronom-signalnyj-06.webp # Сигнальный метроном: ракурс 6
│   │   ├── metronom-signalnyj-07.webm # Световая индикация метронома в темноте
│   │   ├── metronom-signalnyj-07.webp # Сигнальный метроном: ракурс 7
│   │   ├── metronom-signalnyj-08.webp # Сигнальный метроном: ракурс 8
│   │   ├── metronom-signalnyj-09.webp # Сигнальный метроном: ракурс 9
│   │   ├── metronom-signalnyj-10.webp # Сигнальный метроном: ракурс 10
│   │   ├── metronom-signalnyj-11.webp # Сигнальный метроном: ракурс 11
│   │   ├── metronom-signalnyj-12.webp # Сигнальный метроном: ракурс 12
│   │   ├── metronom-signalnyj-13.webp # Сигнальный метроном: ракурс 13
│   │   ├── metronom-signalnyj-14.webp # Сигнальный метроном: ракурс 14
│   │   ├── metronom-signalnyj-15.webp # Сигнальный метроном: ракурс 15
│   │   ├── metronom-signalnyj-16.webp # Сигнальный метроном: ракурс 16
│   │   ├── metronom-signalnyj-17.webp # Сигнальный метроном: ракурс 17
│   │   ├── metronom-signalnyj-18.webp # Сигнальный метроном: ракурс 18
│   │   ├── metronom-signalnyj-19.webp # Сигнальный метроном: ракурс 19
│   │   ├── metronom-signalnyj-20.webp # Сигнальный метроном: ракурс 20
│   │   ├── metronom-signalnyj-21.webp # Сигнальный метроном: ракурс 21
│   │   ├── metronom-signalnyj-22.webp # Сигнальный метроном: ракурс 22
│   │   ├── metronom-signalnyj-23.webp # Сигнальный метроном: ракурс 23
│   │   ├── metronom-signalnyj-24.webp # Сигнальный метроном: ракурс 24
│   │   ├── metronom-signalnyj-25.webp # Сигнальный метроном: ракурс 25
│   │   ├── metronom-signalnyj-26.webp # Сигнальный метроном: ракурс 26
│   │   ├── metronom-signalnyj-27.webp # Сигнальный метроном: ракурс 27
│   │   ├── metronom-signalnyj-28.webp # Сигнальный метроном: ракурс 28
│   │   ├── metronom-signalnyj-29.webp # Сигнальный метроном: ракурс 29
│   │   ├── metronom-signalnyj-30.webp # Сигнальный метроном: ракурс 30
│   │   ├── metronom-signalnyj-31.webp # Сигнальный метроном: ракурс 31
│   │   ├── metronom-signalnyj-esd.pdf
│   │   └── metronom-signalnyj-esd.spl8
│   ├── muzykalnyj-karandash/
│   │   ├── muzykalnyj-karandash.md # Музыкальный карандаш
│   │   ├── muzykalnyj-karandash.webp # Общий вид: музыкальный карандаш
│   │   ├── muzykalnyj-karandash-01.webm # Игра на бумажной клавиатуре музыкальным карандашом
│   │   ├── muzykalnyj-karandash-01.webp # Музыкальный карандаш: ракурс 1
│   │   ├── muzykalnyj-karandash-02.webm # Проверка музыкального карандаша с измерительным прибором
│   │   ├── muzykalnyj-karandash-02.webp # Музыкальный карандаш: ракурс 2
│   │   ├── muzykalnyj-karandash-03.webm # Наблюдение сигнала музыкального карандаша на осциллографе
│   │   ├── muzykalnyj-karandash-03.webp # Электрическая схема музыкального карандаша на таймере TLC555
│   │   ├── muzykalnyj-karandash-04.webm # Рисование схемы музыкального карандаша на бумаге
│   │   ├── muzykalnyj-karandash-04.webp # Музыкальный карандаш: ракурс 4
│   │   ├── muzykalnyj-karandash-05.webm # Проверка бумажной клавиатуры музыкального карандаша
│   │   ├── muzykalnyj-karandash-05.webp # Музыкальный карандаш: ракурс 5
│   │   ├── muzykalnyj-karandash-06.webm # Подготовка рисунка для музыкального карандаша
│   │   ├── muzykalnyj-karandash-06.webp # Музыкальный карандаш: ракурс 6
│   │   ├── muzykalnyj-karandash-07.webm # Проверка работы музыкального карандаша на бумажной схеме
│   │   ├── muzykalnyj-karandash-07.webp # Музыкальный карандаш: ракурс 7
│   │   ├── muzykalnyj-karandash-08.webm # Нанесение проводящих линий на рисунок музыкального устройства
│   │   ├── muzykalnyj-karandash-08.webp # Музыкальный карандаш: ракурс 8
│   │   ├── muzykalnyj-karandash-09.webm # Соединение бумажных клавиш проводящими линиями
│   │   ├── muzykalnyj-karandash-09.webp # Музыкальный карандаш: ракурс 9
│   │   ├── muzykalnyj-karandash-10.webm # Испытание бумажной клавиатуры музыкального карандаша
│   │   ├── muzykalnyj-karandash-10.webp # Музыкальный карандаш: ракурс 10
│   │   ├── muzykalnyj-karandash-11.webm # Рисование элементов музыкальной схемы карандашом
│   │   ├── muzykalnyj-karandash-11.webp # Музыкальный карандаш: ракурс 11
│   │   ├── muzykalnyj-karandash-12.webm # Игра на самодельной бумажной клавиатуре
│   │   ├── muzykalnyj-karandash-12.webp # Музыкальный карандаш: ракурс 12
│   │   ├── muzykalnyj-karandash-13.webm # Проверка клавиш музыкального карандаша на бумажной панели
│   │   ├── muzykalnyj-karandash-13.webp # Музыкальный карандаш: ракурс 13
│   │   ├── muzykalnyj-karandash-14.webm # Нанесение графических элементов схемы музыкального карандаша
│   │   ├── muzykalnyj-karandash-14.webp # Музыкальный карандаш: ракурс 14
│   │   ├── muzykalnyj-karandash-15.webm # Сборка и проверка электронного блока музыкального карандаша
│   │   ├── muzykalnyj-karandash-15.webp # Музыкальный карандаш: ракурс 15
│   │   ├── muzykalnyj-karandash-16.webm # Испытание музыкального карандаша с бумажными контактами
│   │   ├── muzykalnyj-karandash-16.webp # Музыкальный карандаш: ракурс 16
│   │   ├── muzykalnyj-karandash-17.webm # Проверка срабатывания контактов бумажной клавиатуры
│   │   ├── muzykalnyj-karandash-17.webp # Музыкальный карандаш: ракурс 17
│   │   ├── muzykalnyj-karandash-18.webm # Тестирование бумажных клавиш музыкального устройства
│   │   ├── muzykalnyj-karandash-18.webp # Музыкальный карандаш: ракурс 18
│   │   ├── muzykalnyj-karandash-19.webm # Настройка контактов музыкального карандаша
│   │   ├── muzykalnyj-karandash-19.webp # Музыкальный карандаш: ракурс 19
│   │   ├── muzykalnyj-karandash-20.webm # Проверка контактной клавиатуры музыкального карандаша
│   │   ├── muzykalnyj-karandash-20.webp # Музыкальный карандаш: ракурс 20
│   │   ├── muzykalnyj-karandash-21.webp # Музыкальный карандаш: ракурс 21
│   │   ├── muzykalnyj-karandash-22.webp # Музыкальный карандаш: ракурс 22
│   │   ├── muzykalnyj-karandash-23.webp # Принципиальная схема музыкального карандаша
│   │   ├── muzykalnyj-karandash-24.webp # Описание работы и расчёт частоты генератора музыкального карандаша
│   │   ├── muzykalnyj-karandash-esd.jpg # Электрическая схема музыкального карандаша в формате ESD
│   │   ├── muzykalnyj-karandash-esd.pdf
│   │   ├── muzykalnyj-karandash-trafaret.pdf
│   │   └── muzykalnyj-karandash-trafaret.spl8
│   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem/
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem 1.webp # Настольная лампа с растением на прозрачном фоне
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem.md # Настольная светодиодная лампа с растением
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem.webp # Общий вид: настольная лампа для растения
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-01.webm # Демонстрация настольной светодиодной лампы с декоративным растением
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-01.webp # Настольная лампа для растения: ракурс 1
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-02.webp # Настольная лампа для растения: ракурс 2
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-03.webp # Настольная лампа для растения: ракурс 3
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniem-04.webp # Настольная лампа для растения: ракурс 4
│   │   ├── nastolnaya-svetodiodnaya-lampa-s-rasteniemj-ad.dxf
│   │   └── nastolnaya-svetodiodnaya-lampa-s-rasteniemj-ad.pdf
│   ├── pano-uslovnye-oboznacheniya/
│   │   ├── pano-uslovnye-oboznacheniya.md # Условные обозначения
│   │   ├── pano-uslovnye-oboznacheniya.webp # Общий вид: панно с условными обозначениями
│   │   ├── pano-uslovnye-oboznacheniya-01.webm # Обзор панно с условными обозначениями
│   │   ├── pano-uslovnye-oboznacheniya-01.webp # Панно с условными обозначениями: ракурс 1
│   │   └── pano-uslovnye-oboznacheniya-02.webp # Панно с условными обозначениями: ракурс 2
│   ├── plavnoe-zazhiganie-svetodioda/
│   │   ├── plavnoe-zazhiganie-svetodioda.md # Эффект плавного зажигания светодиода
│   │   ├── plavnoe-zazhiganie-svetodioda.webp # Общий вид: устройство плавного включения светодиода
│   │   ├── plavnoe-zazhiganie-svetodioda-01.webm # Проверка плавного включения светодиода на электронной плате
│   │   ├── plavnoe-zazhiganie-svetodioda-01.webp # Устройство плавного включения светодиода: ракурс 1
│   │   ├── plavnoe-zazhiganie-svetodioda-02.webm # Изменение яркости светодиода в схеме плавного зажигания
│   │   ├── plavnoe-zazhiganie-svetodioda-02.webp # Устройство плавного включения светодиода: ракурс 2
│   │   ├── plavnoe-zazhiganie-svetodioda-03.webm # Демонстрация плавного включения светодиода
│   │   ├── plavnoe-zazhiganie-svetodioda-03.webp # Устройство плавного включения светодиода: ракурс 3
│   │   ├── plavnoe-zazhiganie-svetodioda-04.webm # Проверка светодиодной схемы с регулировкой яркости
│   │   ├── plavnoe-zazhiganie-svetodioda-04.webp # Устройство плавного включения светодиода: ракурс 4
│   │   ├── plavnoe-zazhiganie-svetodioda-05.webm # Испытание электронного устройства плавного зажигания светодиода
│   │   ├── plavnoe-zazhiganie-svetodioda-05.webp # Принципиальная схема устройства плавного включения светодиода
│   │   ├── plavnoe-zazhiganie-svetodioda-06.webp # Схема транзисторного узла и регулировки времени свечения
│   │   ├── plavnoe-zazhiganie-svetodioda-07.webp # Сравнение обычного и инверсного включения светодиода
│   │   ├── plavnoe-zazhiganie-svetodioda-08.webp # Устройство плавного включения светодиода: ракурс 8
│   │   ├── plavnoe-zazhiganie-svetodioda-09.webp # Устройство плавного включения светодиода: ракурс 9
│   │   ├── plavnoe-zazhiganie-svetodioda-esd.jpg # Принципиальная схема устройства в формате ESD
│   │   └── plavnoe-zazhiganie-svetodioda-esd.pdf
│   ├── podstavka-dlya-oscillografa/
│   │   ├── podstavka-dlya-oscillografa.md # Подставка для осциллографа
│   │   ├── podstavka-dlya-oscillografa.webp # Общий вид: подставка для осциллографа
│   │   ├── podstavka-dlya-oscillografa-01.webp # Подставка для осциллографа: ракурс 1
│   │   ├── podstavka-dlya-oscillografa-02.webp # Подставка для осциллографа: ракурс 2
│   │   ├── podstavka-dlya-oscillografa-03.webp # Подставка для осциллографа: ракурс 3
│   │   ├── podstavka-dlya-oscillografa-04.webp # Подставка для осциллографа: ракурс 4
│   │   ├── podstavka-dlya-oscillografa-05.webp # Подставка для осциллографа: ракурс 5
│   │   ├── podstavka-dlya-oscillografa-06.webp # Подставка для осциллографа: ракурс 6
│   │   ├── podstavka-dlya-oscillografa-07.webp # Подставка для осциллографа: ракурс 7
│   │   ├── podstavka-dlya-oscillografa-08.webp # Подставка для осциллографа: ракурс 8
│   │   ├── podstavka-dlya-oscillografa-09.webp # Подставка для осциллографа: ракурс 9
│   │   └── podstavka-dlya-oscillografa-10.webp # Подставка для осциллографа: ракурс 10
│   ├── prazdnichnyj-domik/
│   │   ├── prazdnichnyj-domik.md # Праздничный домик
│   │   ├── prazdnichnyj-domik.webp # Общий вид: праздничный домик с электроникой
│   │   ├── prazdnichnyj-domik-01.webm # Обзор самодельного праздничного домика с подсветкой
│   │   ├── prazdnichnyj-domik-01.webp # Праздничный домик с электроникой: ракурс 1
│   │   ├── prazdnichnyj-domik-02.webm # Установка световых элементов в картонный праздничный домик
│   │   ├── prazdnichnyj-domik-02.webp # Праздничный домик с электроникой: ракурс 2
│   │   ├── prazdnichnyj-domik-03.webm # Декорирование праздничного домика светодиодами
│   │   ├── prazdnichnyj-domik-03.webp # Праздничный домик с электроникой: ракурс 3
│   │   ├── prazdnichnyj-domik-04.webm # Демонстрация разноцветной подсветки праздничного домика
│   │   ├── prazdnichnyj-domik-04.webp # Праздничный домик с электроникой: ракурс 4
│   │   ├── prazdnichnyj-domik-05.webm # Проверка светодиодной подсветки макета праздничного домика
│   │   ├── prazdnichnyj-domik-05.webp # Праздничный домик с электроникой: ракурс 5
│   │   ├── prazdnichnyj-domik-06.webm # Обзор конструкции праздничного домика с подсветкой
│   │   ├── prazdnichnyj-domik-06.webp # Праздничный домик с электроникой: ракурс 6
│   │   ├── prazdnichnyj-domik-07.webm # Демонстрация праздничного домика с включёнными огнями
│   │   ├── prazdnichnyj-domik-07.webp # Праздничный домик с электроникой: ракурс 7
│   │   ├── prazdnichnyj-domik-08.webp # Праздничный домик с электроникой: ракурс 8
│   │   └── prazdnichnyj-domik-09.webp # Праздничный домик с электроникой: ракурс 9
│   ├── robot-korova-iz-kartona/
│   │   ├── robot-korova-iz-kartona.md # Робот корова из картона
│   │   ├── robot-korova-iz-kartona.webp # Общий вид: картонный шагающий робот
│   │   ├── robot-korova-iz-kartona-01.webm # Обзор картонного робота-коровы с подвижными ногами
│   │   ├── robot-korova-iz-kartona-01.webp # Картонный шагающий робот: ракурс 1
│   │   ├── robot-korova-iz-kartona-02.webm # Испытание механизма движения картонного робота-коровы
│   │   ├── robot-korova-iz-kartona-02.webp # Картонный шагающий робот: ракурс 2
│   │   ├── robot-korova-iz-kartona-03.webm # Проверка ходовой конструкции робота-коровы
│   │   ├── robot-korova-iz-kartona-03.webp # Картонный шагающий робот: ракурс 3
│   │   ├── robot-korova-iz-kartona-04.webm # Демонстрация движения самодельного робота-коровы
│   │   ├── robot-korova-iz-kartona-04.webp # Картонный шагающий робот: ракурс 4
│   │   ├── robot-korova-iz-kartona-05.webp # Картонный шагающий робот: ракурс 5
│   │   ├── robot-korova-iz-kartona-06.webp # Картонный шагающий робот: ракурс 6
│   │   ├── robot-korova-iz-kartona-07.webp # Картонный шагающий робот: ракурс 7
│   │   ├── robot-korova-iz-kartona-08.webp # Картонный шагающий робот: ракурс 8
│   │   ├── robot-korova-iz-kartona-09.webp # Картонный шагающий робот: ракурс 9
│   │   └── robot-korova-iz-kartona-10.webp # Картонный шагающий робот: ракурс 10
│   ├── robot-krolik-iz-kartona/
│   │   ├── robot-krolik-iz-kartona.md # Робот кролик из картона
│   │   ├── robot-krolik-iz-kartona.webp # Общий вид: картонный робот-кролик
│   │   ├── robot-krolik-iz-kartona-.webp # Робот-кролик с отдельным блоком управления на прозрачном фоне
│   │   ├── robot-krolik-iz-kartona--.webp # Вариант изображения робота-кролика на прозрачном фоне
│   │   ├── robot-krolik-iz-kartona-01.webm # Обзор картонного робота-кролика с подвижными деталями
│   │   ├── robot-krolik-iz-kartona-01.webp # Картонный робот-кролик: ракурс 1
│   │   ├── robot-krolik-iz-kartona-02.webm # Проверка механизма движения робота-кролика
│   │   ├── robot-krolik-iz-kartona-02.webp # Картонный робот-кролик: ракурс 2
│   │   ├── robot-krolik-iz-kartona-03.webm # Испытание картонного робота-кролика на поверхности
│   │   ├── robot-krolik-iz-kartona-03.webp # Картонный робот-кролик: ракурс 3
│   │   ├── robot-krolik-iz-kartona-04.webm # Демонстрация работы механизма робота-кролика
│   │   ├── robot-krolik-iz-kartona-04.webp # Картонный робот-кролик: ракурс 4
│   │   ├── robot-krolik-iz-kartona-05.webm # Проверка движения самодельного робота-кролика
│   │   ├── robot-krolik-iz-kartona-05.webp # Картонный робот-кролик: ракурс 5
│   │   ├── robot-krolik-iz-kartona-06.webp # Картонный робот-кролик: ракурс 6
│   │   ├── robot-krolik-iz-kartona-07.webp # Картонный робот-кролик: ракурс 7
│   │   ├── robot-krolik-iz-kartona-08.webp # Картонный робот-кролик: ракурс 8
│   │   ├── robot-krolik-iz-kartona-09.webp # Картонный робот-кролик: ракурс 9
│   │   ├── robot-krolik-iz-kartona-10.webp # Картонный робот-кролик: ракурс 10
│   │   ├── robot-krolik-iz-kartona-11.webp # Картонный робот-кролик: ракурс 11
│   │   ├── robot-krolik-iz-kartona-12.webp # Картонный робот-кролик: ракурс 12
│   │   ├── robot-krolik-iz-kartona-13.webp # Картонный робот-кролик: ракурс 13
│   │   ├── robot-krolik-iz-kartona-14.webp # Картонный робот-кролик: ракурс 14
│   │   ├── robot-krolik-iz-kartona-15.webp # Картонный робот-кролик: ракурс 15
│   │   ├── robot-krolik-iz-kartona-16.webp # Картонный робот-кролик: ракурс 16
│   │   ├── robot-krolik-iz-kartona-17.webp # Картонный робот-кролик: ракурс 17
│   │   ├── robot-krolik-iz-kartona-18.webp # Картонный робот-кролик: ракурс 18
│   │   ├── robot-krolik-iz-kartona-19.webp # Картонный робот-кролик: ракурс 19
│   │   ├── robot-krolik-iz-kartona-20.webp # Картонный робот-кролик: ракурс 20
│   │   ├── robot-krolik-iz-kartona-21.webp # Картонный робот-кролик: ракурс 21
│   │   ├── robot-krolik-iz-kartona-22.webp # Картонный робот-кролик: ракурс 22
│   │   ├── robot-krolik-iz-kartona-23.webp # Картонный робот-кролик: ракурс 23
│   │   ├── robot-krolik-iz-kartona-24.webp # Картонный робот-кролик: ракурс 24
│   │   └── robot-krolik-iz-kartona-25.webp # Картонный робот-кролик: ракурс 25
│   ├── robot-strannik/
│   │   ├── robot-strannik.md # Робот странник
│   │   ├── robot-strannik.webp # Общий вид: робот-странник и игрушка-робот
│   │   ├── robot-strannik-01.webm # Испытание шагающего робота-странника на полу
│   │   ├── robot-strannik-01.webp # Робот-странник и игрушка-робот: ракурс 1
│   │   ├── robot-strannik-02.webm # Демонстрация ходьбы шагающего робота-странника
│   │   ├── robot-strannik-02.webp # Робот-странник и игрушка-робот: ракурс 2
│   │   ├── robot-strannik-03.webm # Проверка устойчивости и движения робота-странника
│   │   ├── robot-strannik-03.webp # Робот-странник и игрушка-робот: ракурс 3
│   │   ├── robot-strannik-04.webm # Короткий тест шагающего робота-странника
│   │   ├── robot-strannik-04.webp # Робот-странник и игрушка-робот: ракурс 4
│   │   ├── robot-strannik-05.webp # Робот-странник и игрушка-робот: ракурс 5
│   │   ├── robot-strannik-06.webp # Робот-странник и игрушка-робот: ракурс 6
│   │   ├── robot-strannik-07.webp # Робот-странник и игрушка-робот: ракурс 7
│   │   ├── robot-strannik-08.webp # Робот-странник и игрушка-робот: ракурс 8
│   │   ├── robot-strannik-09.webp # Робот-странник и игрушка-робот: ракурс 9
│   │   ├── robot-strannik-10.webp # Робот-странник и игрушка-робот: ракурс 10
│   │   ├── robot-strannik-11.webp # Робот-странник и игрушка-робот: ракурс 11
│   │   ├── robot-strannik-12.webp # Робот-странник и игрушка-робот: ракурс 12
│   │   └── robot-strannik-13.webp # Этикетка советской игрушки «Робот» с данными производителя
│   ├── simple-cardboard-walking-robot/
│   │   ├── simple-cardboard-walking-robot.md # Робот двуногий шагающий из картона
│   │   ├── simple-cardboard-walking-robot.webp # Общий вид: картонный шагающий робот
│   │   ├── simple-cardboard-walking-robot-01.webm # Испытание простого шагающего робота из картона
│   │   ├── simple-cardboard-walking-robot-01.webp # Картонный шагающий робот: ракурс 1
│   │   ├── simple-cardboard-walking-robot-02.webm # Проверка движения самодельного картонного робота
│   │   ├── simple-cardboard-walking-robot-02.webp # Картонный шагающий робот: ракурс 2
│   │   ├── simple-cardboard-walking-robot-03.webp # Картонный шагающий робот: ракурс 3
│   │   ├── simple-cardboard-walking-robot-04.webp # Картонный шагающий робот: ракурс 4
│   │   ├── simple-cardboard-walking-robotj-ad.dxf
│   │   └── simple-cardboard-walking-robotj-ad.pdf
│   ├── sputnik-1/
│   │   ├── sputnik-1.md # Спутник-1
│   │   ├── sputnik-1.webp # Общий вид: модель спутника-1
│   │   ├── sputnik-1-01.webp # Модель спутника-1: ракурс 1
│   │   ├── sputnik-1-02.webp # Модель спутника-1: ракурс 2
│   │   ├── sputnik-1-03.webp # Модель спутника-1: ракурс 3
│   │   ├── sputnik-1-04.webp # Модель спутника-1: ракурс 4
│   │   ├── sputnik-1-05.webp # Модель спутника-1: ракурс 5
│   │   └── sputnik-1-06.webp # Модель спутника-1: ракурс 6
│   ├── vibrohod-iz-zubnoj-shchetki/
│   │   ├── vibrohod-iz-zubnoj-shchetki.md # Виброход из зубной щетки
│   │   ├── vibrohod-iz-zubnoj-shchetki.webp # Общий вид: виброход из зубной щётки
│   │   ├── vibrohod-iz-zubnoj-shchetki-01.webm # Демонстрация виброхода на основе зубной щётки
│   │   ├── vibrohod-iz-zubnoj-shchetki-01.webp # Виброход из зубной щётки: ракурс 1
│   │   ├── vibrohod-iz-zubnoj-shchetki-02.webm # Проверка движения миниатюрного виброхода
│   │   ├── vibrohod-iz-zubnoj-shchetki-02.webp # Виброход из зубной щётки: ракурс 2
│   │   ├── vibrohod-iz-zubnoj-shchetki-03.webm # Испытание виброхода на ровной поверхности
│   │   ├── vibrohod-iz-zubnoj-shchetki-03.webp # Виброход из зубной щётки: ракурс 3
│   │   ├── vibrohod-iz-zubnoj-shchetki-04.webm # Настройка и проверка вибрационного привода
│   │   ├── vibrohod-iz-zubnoj-shchetki-04.webp # Виброход из зубной щётки: ракурс 4
│   │   ├── vibrohod-iz-zubnoj-shchetki-05.webm # Демонстрация перемещения виброхода из зубной щётки
│   │   ├── vibrohod-iz-zubnoj-shchetki-05.webp # Виброход из зубной щётки: ракурс 5
│   │   ├── vibrohod-iz-zubnoj-shchetki-06.webm # Проверка вибрационного механизма мини-робота
│   │   ├── vibrohod-iz-zubnoj-shchetki-06.webp # Виброход из зубной щётки: ракурс 6
│   │   ├── vibrohod-iz-zubnoj-shchetki-07.webm # Испытание виброхода с установленным мотором
│   │   └── vibrohod-iz-zubnoj-shchetki-08.webm # Обзор деталей и сборки виброхода из зубной щётки
│   └── yablonevoe-derevo/
│       ├── yablonevoe-derevo.md # Яблоневое дерево
│       ├── yablonevoe-derevo.webp # Общий вид: светодиодное декоративное дерево
│       ├── yablonevoe-derevo-01.webm # Демонстрация декоративного светодиодного яблоневого дерева
│       ├── yablonevoe-derevo-01.webp # Светодиодное декоративное дерево: ракурс 1
│       ├── yablonevoe-derevo-02.webp # Светодиодное декоративное дерево: ракурс 2
│       ├── yablonevoe-derevo-03.webp # Декоративное дерево с разноцветным узором на кроне
│       ├── yablonevoe-derevo-04.webp # Обратная сторона дерева с цветным рисунком
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
│   ├── aluminum-electrolytic-capacitor.md # Алюминиевый электролитический конденсатор
│   ├── analog-panel-meter.md              # Аналоговый стрелочный измерительный прибор
│   ├── carbon-film-resistor.md            # Углеродный пленочный резистор
│   ├── ceramic-disc-capacitor.md          # Керамический дисковый конденсатор
│   ├── index.md                           # Техническое вдохновение
│   ├── magnetic-buzzer.md                 # Магнитный зуммер
│   ├── our-dream.md                       # Наша мечта ...
│   ├── strontium-atom.md                  # Одиночный атом стронция в ионной ловушке
│   └── through-hole-red-led.md            # Красный светодиод с выводами для сквозного монтажа
├── projects/
│   ├── index.md                # Учебные проекты
│   └── novyj-robot-shagohod.md # Робот новый
├── test/
│   ├── folder/
│   │   ├── test.webp
│   │   ├── test-v.webp
│   │   └── test-vertical.webm
│   ├── -figure-single.md # Тестирование модуля одиночных журнальных блоков (fig)
│   ├── img-base.md       # Тестирование модуля базовых изображений (img_base.py)
│   ├── img-figure.md     # Тестирование модуля групповых журнальных блоков (img_figure.py)
│   ├── links.md          # Tест с преобразованием ссылок фото и видео
│   ├── -row-photo.md     # Tесты с групповыми фото
│   ├── -single-photo.md  # Tесты с одиночными фото
│   ├── vault.md          # Тестирование изолированных зон безопасности (vault.py)
│   ├── -video.md         # Tест с видео
│   └── Без названия 1.md # Тестовый документ с примерами одиночных и групповых медиаблоков.
├── tools/
│   ├── files/
│   │   ├── fritzing-led-sketch.fzz
│   │   ├── pianino-elektronnoe-proekt-uchebnyj.lay6
│   │   └── sprintlayout.zip
│   ├── img/
│   │   ├── fritzing-workflow-1-0-5.webp
│   │   └── sprintlayout-6-0-workflow.webp
│   ├── fritzing.md     # Fritzing
│   ├── index.md        # Полезные инструменты
│   └── sprintlayout.md # Sprint Layout
├── .gitignore         # Файл исключений системы контроля версий Git
├── _config.yml        # Основные настройки Jekyll: параметры сайта, сборки, темы и подключаемых расширений.
├── 404.html           # Страница ошибки 404 с сообщением о ненайденном адресе и ссылкой на главную.
├── CHANGELOG.md       # Журнал изменений проекта
├── CODE_OF_CONDUCT.md # Правила поведения участников и соавторов проекта.
├── CONTRIBUTING.md    # Соавторство и вклад в развитие проекта.
├── giscus.json        # Настройки виджета Giscus для домена сайта и порядка отображения комментариев.
├── index.md           # Творческая лаборатория познавательного развития
├── LICENSE.txt        # Условия лицензии Creative Commons Attribution 4.0 International (CC BY 4.0).
├── README.md
├── ROADMAP.md         # Дорожная карта проекта
├── robots.txt         # Инструкции поисковым роботам по обходу сайта и адрес карты сайта.
├── STRUCTURE.md       # Документ с деревом каталогов и файлов репозитория и краткими описаниями их назначения.
└── tags.md            # Поиск по тегам
```
