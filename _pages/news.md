---
layout: news
title: Что нового?
permalink: /news/
per_page: 10
folder: ""
pinned_url: ""
---
{% comment %} 
СТРАНИЦА: ОБЩИЙ АРХИВ НОВОСТЕЙ (\_pages/news.md)
Назначение: Указывает шаблону news.html выводить ВСЕ новости по 10 штук.
Параметры: folder: "" (пусто, значит выводим всё без фильтра по папкам).
{% endcomment %}
<style>
  /* ТЕСТОВЫЙ CSS ДЛЯ ПРОВЕРКИ ПЕРЕНОСА СТРОК КОЛОНКАМИ В АРХИВЕ */
  
  /* 1. Превращаем строку списка в гибкую невидимую мини-таблицу */
  .updates-feed #posts-list .update-item {
      display: table !important;
      width: 100% !important;
      box-sizing: border-box !important;
      margin-bottom: 12px !important;
      border-bottom: 1px solid #f0f0f0 !important;
      padding-bottom: 8px !important;
  }

  /* 2. Превращаем дату в левый плотный фиксированный столбик */
  .updates-feed #posts-list .update-item small {
      display: table-cell !important;
      width: 95px !important;           /* Фиксированная ширина колонки даты */
      min-width: 95px !important;
      color: #888 !important;
      vertical-align: top !important;    /* Выравнивание букв строго по верхней линии */
      line-height: 1.4 !important;
  }

  /* 3. Превращаем ссылку в правый независимый столбик контента */
  .updates-feed #posts-list .update-item .item-link {
      display: table-cell !important;
      vertical-align: top !important;    /* Жесткая защита от уплывания текста вниз */
      line-height: 1.4 !important;
      text-decoration: none !important;
      margin-left: 0 !important;         /* Обнуляем маргин, так как зазор теперь задается шириной левой ячейки */
      padding-left: 8px !important;      /* Делаем аккуратный отступ текста от даты внутри колонки */
  }
</style>
