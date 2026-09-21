/**
 * @about Модуль пагинации (БАЗОВЫЙ ЭКСПЕРИМЕНТАЛЬНЫЙ КОНТУР).
 * @purpose Гарантированно выводит новости порциями по 10 штук с бэкенда Питона,
 *          полностью исключая сложные условия переключения дизайнов.
 * @author TechLab
 * @version 7.0.0-experimental-pure
 */

function runPagination(listId, controlsId, itemsPerPage) {
  var list = document.getElementById(listId);
  if (!list) return;

  var controls = document.getElementById(controlsId);
  if (!controls) return;

  // Автоматически определяем имя текущей ленты по интернет-адресу страницы
  var pathClean = window.location.pathname.replace(/^\/|\/$/g, '');
  var currentSection = pathClean.split('/').pop() || 'news';
  if (window.location.pathname === '/' || currentSection === '') {
    currentSection = 'news';
  }

  var currentPage = 1;
  var feedData = null;

  // Подхватываем квантованную базу данных из оперативной памяти сервера Jekyll
  if (window.site_feed_data && window.site_feed_data[currentSection]) {
    feedData = window.site_feed_data[currentSection];
    renderPage(currentPage);
  } else {
    console.error("Ожидание проброса глобального объекта site_feed_data...");
    return;
  }

  // 1. МАКСИМАЛЬНО ПРОСТОЙ СКВОЗНОЙ ВЫВОД СТРОК ОБНОВЛЕНИЙ
  function renderPage(page) {
    list.innerHTML = '';
    var pageItems = feedData.pages[page] || [];

    pageItems.forEach(function(item) {
      var li = document.createElement('li');
      var pinnedClass = item.pinned ? ' pinned-item' : '';
      
      // ИСПРАВЛЕНО: Безупречная склейка даты формата DD.MM.YYYY из строки Питона
      var dateParts = item.date.split('-');
      var dateStr = (dateParts.length === 3) ? dateParts[2] + '.' + dateParts[1] + '.' + dateParts[0] : item.date;

      // Базовые универсальные классы строки контура
      li.className = 'news-item' + pinnedClass;
      li.setAttribute('data-date', item.date);
      li.setAttribute('data-is-post', item.is_post);
      
      var emojiStr = item.emoji ? ' ' + item.emoji : '';
      
      // Чистый сквозной HTML без инлайн-стилей и тяжелых конструкций
      li.innerHTML = '<div><span>' + dateStr + '&nbsp;»&nbsp;</span><span>' +
                     '<a href="' + item.url + '" class="item-link">' + item.title + emojiStr + '</a>' +
                     '</span></div>';
      
      li.style.setProperty('display', 'flex', 'important');
      list.appendChild(li);
    });

    renderControls();
  }

  // 2. БАЗОВЫЕ КНОПКИ УПРАВЛЕНИЯ ЭКСПЕРИМЕНТОМ
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

  // 3. СЛЕПАЯ ГЕНЕРАЦИЯ КНОПОК НА ОСНОВЕ ДАННЫХ ПИТОНА
  function renderControls() {
    controls.innerHTML = '';
    var totalPages = feedData.total_pages || 1;
    
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
