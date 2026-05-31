---
layout: home
title: Творческая лаборатория познавательного развития
description: "[ для тех, кто хочет знать как всё устроено и создавать технологии своими руками ]"
header_theme: classic
---

<div class="grid-container"> 
    <!-- БЛОК 1 -->
    <section class="category-card my-projects">
        <div class="card-header">
            <img src="/assets/icons/ugolok-mladshego-konstruktora.svg" alt="✈️" class="section-icon">
            <h2>Уголок младшего конструктора</h2>
        </div>
        <ul class="project-list">
            <li><a href="/biblio/">📚 Список литературы</a></li>
            <li><a href="/diary/">📝 Дневник инженера</a></li>
            <li><a href="/projects/">🗂️ Учебные проекты</a></li>
            <li><a href="/faire/">🔥 Ярмарка поделок</a></li>
            <li><a href="/inspiration/">🚀 Техническое вдохновение</a></li>
            <li><a href="/tools/">🛠 Полезные инструменты</a></li>
        </ul>
    </section>

    <!-- БЛОК 2: ЧТО НОВОГО -->
    <section class="category-card site-news">
        <div class="card-header">
            <img src="/assets/icons/chto-novogo.svg" alt="🔥" class="section-icon">
            <h2>Что нового?</h2>
            
            <!-- КНОПКИ СВЯЗИ -->

<div class="social-badge-wrapper">
<a href="https://github.com" class="github-badge"> <!-- Современный SVG силуэт кота (Invertocat) --> <svg viewBox="0 0 98 96" xmlns="http://w3.org"> <path fill-rule="evenodd" clip-rule="evenodd" d="M48.854 0C21.839 0 0 22 0 49.217c0 21.756 13.993 40.172 33.4 46.642 2.442.447 3.332-1.072 3.332-2.375 0-1.172-.043-4.275-.066-8.39-13.59 2.975-16.457-6.6-16.457-6.6-2.222-5.688-5.424-7.2-5.424-7.2-4.436-3.055.336-2.995.336-2.995 4.904.348 7.485 5.076 7.485 5.076 4.36 7.527 11.435 5.352 14.22 4.092.442-3.187 1.702-5.354 3.097-6.585-10.85-1.243-22.257-5.467-22.257-24.342 0-5.378 1.905-9.774 5.033-13.22-.504-1.243-2.18-6.255.48-13.038 0 0 4.106-1.325 13.447 5.052a46.213 46.213 0 0 1 24.448 0C71.18 10.912 75.28 12.237 75.28 12.237c2.666 6.783.99 11.795.487 13.038 3.134 3.446 5.029 7.842 5.029 13.22 0 18.922-11.424 23.085-22.308 24.303 1.754 1.523 3.322 4.52 3.322 9.11 0 6.58-.06 11.88-.06 13.5 0 1.314.88 2.845 3.35 2.365C84.015 89.37 98 70.96 98 49.217 98 22 76.16 0 48.854 0z"/> </svg> </a>

    <a href="https://t.me" title="Telegram" class="social-badge-click social-telegram">
        <img src="/assets/icons/logo-telegram.svg" alt="Telegram" class="social-img-brand">
    </a>
</div>



        </div>
        <!-- Смысловой контейнер для изоляции стилей обновлений Главной -->
        <div class="home-news-feed">
            <ul id="posts-list" style="list-style: none; padding: 0; margin: 0;">
                {% include news-loop.liquid type="home" %}
            </ul>
        </div>
        <div id="home-news-pagination"></div>
    </section>

    <!-- БЛОК 3: РЕЗЕРВ -->
    <section class="category-card tech-creative">
        <div class="card-header">
            <img src="/assets/icons/detskij-inzhenernyj-klub.svg" alt="✈️" class="section-icon">
            <h2>Информация юным техникам</h2>
        </div>
        <ul class="project-list">
            <li><a href="#">✨ Деятельность клуба</a></li>
            <li><a href="#">🎓 Регулярные занятия</a></li>
            <li><a href="#">🪁 Детско-юношеский лагерь</a></li>
            <li><a href="#">🎨 Творческий процесс</a></li>
            <li><a href="#">💥 Работы юных инженеров</a></li>
        </ul>
    </section>
</div>

{% include pagination.liquid list_id="posts-list" controls_id="home-news-pagination" per_page=10 pinned_url="/people/fran-blanche/" %}
