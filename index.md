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
            <!-- КНОПКИ СВЯЗИ: Встраиваются прямо внутрь вашего родного .card-header -->
            <div class="social-badge-wrapper">
                <!-- Круглый GitHub (Форум) -->
                <a href="https://github.com" title="Форум проекта" class="social-badge-click">
                    <svg viewBox="0 0 24 24" width="30" height="30"><circle cx="12" cy="12" r="12" fill="#24292e"/><path d="M12 2.5a9.5 9.5 0 0 0-3 18.5c.5.1.6-.2.6-.5v-1.7c-2.6.6-3.2-1.3-3.2-1.3-.4-1.1-1-1.4-1-1.4-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .8 1.5 2.3 1 2.9.8.1-.6.3-1 .6-1.2-2.1-.2-4.3-1-4.3-4.7 0-1 .4-1.9 1-2.6 0-.3-.4-1.2.1-2.5 0 0 .8-.3 2.7 1a9.5 9.5 0 0 1 5 0c1.9-1.3 2.7-1 2.7-1 .5 1.3.2 2.2.1 2.5.6.7 1 1.6 1 2.6 0 3.7-2.2 4.5-4.3 4.7.3.3.6.9.6 1.9v2.8c0 .3.1.6.6.5A9.5 9.5 0 0 0 12 2.5z" fill="#ffffff"/></svg>
                </a>
                <!-- Круглый Telegram (Канал) -->
				<a href="https://t.me" title="Телеграм-канал" class="social-badge-click">
				    <svg viewBox="0 0 24 24" width="30" height="30"><circle cx="12" cy="12" r="12" fill="#0088cc"/><path d="M16.8 8.1l-1.4 6.8c-.1.5-.4.6-.8.3l-2.2-1.6-1.1 1c-.1.1-.2.2-.4.2l.2-2.4 4.4-4c.2-.2 0-.3-.3-.1l-5.5 3.5-2.3-.7c-.5-.1-.5-.5.1-.7l9-3.5c.4-.1.8.2.7.9z" fill="#ffffff"/></svg>
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
