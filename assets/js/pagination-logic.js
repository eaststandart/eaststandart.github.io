/**
 * @about Модуль пагинации (ГИБРИДНЫЙ ЧИСТЫЙ КОНТУР).
 * @purpose Скачивает плоскую базу feed.yml и рендерит порции строго по 10 штук,
 *          копируя структуру классов вашего оригинального Liquid-файла.
 * @author TechLab
 * @version 9.0.0-pure-hybrid
 */

function runPagination(listId, controlsId, itemsPerPage, basketName) {
  var list = document.getElementById(listId);
  if (!list) return;

  var controls = document.getElementById(controlsId);
  if (!controls) return;

  // Железный автомат имени корзины напрямую из параметра вызова Liquid
  var currentSection = (basketName || 'news').trim().toLowerCase();
  
  var currentPage = 1;
  var fullPool = [];
  var totalPages = 1;

  // 1. ПОДХВАТ ДАННЫХ ИЗ ОПЕРАТИВНОЙ ПАМЯТИ ИЛИ СЕТИ
  if (window.site_feed_data && window.site_feed_data[currentSection]) {
    // Если Jekyll уже пробросил базу данных в память сайта
    var rawData = window.site_feed_data[currentSection];
    fullPool = Array.isArray(rawData) ? rawData : (rawData.items || rawData.pages || []);
    initPagination();
  } else {
    // Резервный сетевой запрос к плоскому файлу базы данных feed.yml
    var feedUrl = window.location.origin + '/_data/feed.yml';
    fetch(feedUrl)
      .then(function(response) { return response.text(); })
      .then(function(yamlText) {
        if (window.site_feed_data && window.site_feed_data[currentSection]) {
          fullPool = window.site_feed_data[currentSection];
          initPagination();
        }
      });
  }

  function initPagination() {
    if (!Array.isArray(fullPool) || fullPool.length === 0) return;
    totalPages = Math.ceil(fullPool.length / itemsPerPage);
    renderPage(currentPage);
  }

  // 2. СБОРКА СТРОК СТРОГО ПО КЛАССАМ И ТЕГАМ ВАШЕГО LIQUID-ФАЙЛА
  function renderPage(page) {
    list.innerHTML = '';
    var isHome = (controlsId === "home-news-pagination");

    // Вырезаем порцию строго по 10 штук для текущей страницы
    var start = (page - 1) * itemsPerPage;
    var end = start + itemsPerPage;
    var pageItems = fullPool.slice(start, end);

    pageItems.forEach(function(item) {
      var li = document.createElement('li');
      var pinnedClass = item.pinned ? ' pinned-item' : '';
      
      // Переводим дату из YYYY-MM-DD в канонический формат DD.MM.YYYY
      var dateStr = item.date;
      if (item.date && item.date.indexOf('-') !== -1) {
        dateStr = item.date.split('-').reverse().join('.');
      }

      if (isHome) {
        // ВАРИАНТ А: Точный клон вёрстки для Главной страницы (Карточка "Что нового?")
        li.className = 'news-item news-item-compact' + pinnedClass;
        li.setAttribute('data-date', item.date);
        li.setAttribute('data-is-post', item.is_post);
        
        var emojiStr = item.emoji ? ' ' + item.emoji : '';
        li.innerHTML = '<div><span>' + dateStr + '&nbsp;»&nbsp;</span><span>' +
                       '<a href="' + item.url + '" class="item-link">' + item.title + emojiStr + '</a>' +
                       '</span></div>';
        li.style.setProperty('display', 'flex', 'important');
      } else {
        // ВАРИАНТ Б: Точный клон вёрстки для Журнала, Вопросов и частных лент
        li.className = 'news-item' + pinnedClass;
        li.setAttribute('data-date', item.date);
        li.setAttribute('data-is-post', item.is_post);
        li.style.cssText = 'margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;';
        
        var personalEmojiStr = item.personal_emoji ? ' ' + item.personal_emoji : '';
        li.innerHTML = '<div><span>' + dateStr + '&nbsp;»&nbsp;</span><span>' +
                       '<a href="' + item.url + '" class="item-link" style="text-decoration: none;">' + item.title + personalEmojiStr + '</a>' +
                       '</span></div>';
        li.style.setProperty('display', 'block', 'important');
      }

      list.appendChild(li);
    });

    renderControls();
  }

  // 3. ВСПОМОГАТЕЛЬНЫЕ КНОПКИ УПРАВЛЕНИЯ С ФИКСАЦИЕЙ ЭКРАНА СТРОГО ПО КОНТЕКСТУ
  function createButton(text, targetPage, isCurrent, isDisabled) {
    var btn = document.createElement('button');
    btn.innerText = text;
    btn.className = 'page-btn';
    if (isCurrent) btn.classList.add('active');
    if (isDisabled) {
      btn.style.opacity = '0.4';
      btn.style.cursor = 'default';
    }
    if (!isDisabled && !isCurrent) {
      btn.addEventListener('click', function() {
        currentPage = targetPage;
        renderPage(currentPage);
        
        // ФИКСАЦИЯ ЭКРАНА: Если мы на Главной — экран стоит как влитой.
        // Если в Журнале / Вопросах — плавно возвращаем фокус к началу блока постов.
        var isHome = (controlsId === "home-news-pagination");
        if (!isHome) {
          var feedContainer = document.querySelector('.news-feed');
          if (feedContainer) {
            feedContainer.scrollIntoView({ behavior: 'smooth' });
          } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
        }
      });
    }
    return btn;
  }

  function createSeparator() {
    var span = document.createElement('span');
    span.innerText = '...';
    span.style.padding = '6px 4px';
    span.style.color = '#6a737d';
    span.style.fontSize = '0.9rem';
    span.style.fontWeight = '600';
    span.style.userSelect = 'none';
    return span;
  }

  // 4. ГЕНЕРАЦИЯ КНОПОК ПАГИНАЦИИ НА ОСНОВЕ ДАННЫХ ВЫБРАННОЙ КОРЗИНЫ
  function renderControls() {
    controls.innerHTML = '';
    
    if (controlsId === "home-news-pagination") {
      var archiveBtn = document.createElement('button');
      archiveBtn.innerText = '»»';
      archiveBtn.className = 'page-btn home-news-all-btn';
      archiveBtn.addEventListener('click', function() {
        window.location.href = '/news/';
      });
      controls.appendChild(archiveBtn);
    }

    if (totalPages <= 1) return;

    controls.appendChild(createButton('«', currentPage - 1, false, currentPage === 1));

    var maxVisible = 5;
    if (totalPages <= maxVisible) {
      for (var i = 1; i <= totalPages; i++) {
        controls.appendChild(createButton(i, i, i === currentPage, false));
      }
    } else {
      var startPage = Math.max(1, currentPage - 1);
      var endPage = Math.min(totalPages, currentPage + 1);

      if (currentPage <= 2) { endPage = 3; }
      if (currentPage >= totalPages - 1) { startPage = totalPages - 2; }

      if (startPage > 1) {
        controls.appendChild(createButton('1', 1, currentPage === 1, false));
        if (startPage > 2) controls.appendChild(createSeparator());
      }

      for (var i = startPage; i <= endPage; i++) {
        controls.appendChild(createButton(i, i, i === currentPage, false));
      }

      if (endPage < totalPages) {
        if (endPage < totalPages - 1) controls.appendChild(createSeparator());
        controls.appendChild(createButton(totalPages, totalPages, currentPage === totalPages, false));
      }
    }

    controls.appendChild(createButton('»', currentPage + 1, false, currentPage === totalPages));
  }
}
