---
layout: home
title: Творческая лаборатория познавательного развития
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
            <h2>Что нового в уголке конструктора?</h2>
        </div>    
        <ul id="posts-list" style="list-style: none; padding: 0; margin: 0;">
            <!-- УНИФИЦИРОВАННЫЙ ВЫЗОВ ЦИКЛА ДЛЯ ГЛАВНОЙ СТРАНИЦЫ -->
            {% include news-loop.liquid type="home" %}
        </ul>
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
