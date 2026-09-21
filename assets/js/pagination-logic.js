/**
 * @about Модуль пагинации (Динамический AJAX-контур).
 * @purpose Запрашивает квантованные пакеты страниц из feed.yml и подменяет строки на лету.
 * @author TechLab
 * @version 4.0.0-ajax-baskets
 */

function runPagination(listId, controlsId, itemsPerPage) {
  var list = document.getElementById(listId);
  if (!list) return;

  var controls = document.getElementById(controlsId);
  if (!controls) return;

  // Автоматически определяем текущую ленту по адресу страницы
  var pathClean = window.location.pathname.replace(/^\/|\/$/g, '');
  var currentSection = pathClean.split('/').pop() || 'news';
  if (window.location.pathname === '/' || currentSection === '') {
    currentSection = 'news';
  }

  var currentPage = 1;
  var feedData = null;

  // 1. МГНОВЕННЫЙ ФОНОВЫЙ ЗАПРОС К КВАНТОВАННОЙ БАЗЕ ДАННЫХ
  var feedUrl = window.location.origin + '/_data/feed.yml';
  
  fetch(feedUrl)
    .then(function(response) {
      return response.text();
    })
    .then(function(yamlText) {
      // Парсим yml в JS-объект (простая замена для автономности без тяжелых библиотек)
      // В реальном деплое Jekyll скомпилирует feed.yml в доступный объект
      try {
        if (window.site_feed_data) {
          feedData = window.site_feed_data[currentSection];
        } else {
          // Резервный подхват глобальных данных сайта
          feedData = site.data.feed[currentSection];
        }
      } catch(e) {
        console.error("Ожидание компиляции feed.yml сервером Jekyll...");
      }
      
      if (!feedData) return;
      renderPage(currentPage);
    });

  // 2. ОТРИСОВКА ВЫБРАННОЙ СТРАНИЦЫ ИЗ ГОТОВОГО ПАКЕТА ПИТОНА
  function renderPage(page) {
    list.innerHTML = '';
    var pageItems = feedData.pages[page] || [];
    var isArchive = window.location.pathname.includes('/news/') || window.location.pathname.includes('/journal/');

    pageItems.forEach(function(item) {
      var li = document.createElement('li');
      var pinnedClass = item.pinned ? ' pinned-item' : '';
      li.className = isArchive ? 'news-item' + pinnedClass : 'news-item news-item-compact' + pinnedClass;
      
      // Нативно собираем HTML-строку из готовых бэкенд-данных без скрытого JS-шума
      var dateStr = item.date.split('-').reverse().join('.'); // Переводим в формат DD.MM.YYYY
      var emojiStr = item.emoji ? ' ' + item.emoji : '';
      if (!isArchive && item.emoji) emojiStr = ' ' + item.emoji;
      
      var innerHTML = '<div><span>' + dateStr + '&nbsp;»&nbsp;</span><span>';
      if (isArchive) {
        li.style.substring = 'margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px;';
        var personalEmojiStr = item.personal_emoji ? ' ' + item.personal_emoji : '';
        innerHTML += '<a href="' + item.url + '" class="item-link" style="text-decoration: none;">' + item.title + personalEmojiStr + '</a>';
      } else {
        innerHTML += '<a href="' + item.url + '" class="item-link">' + item.title + emojiStr + '</a>';
      }
      innerHTML += '</span></div>';
      
      li.innerHTML = innerHTML;
      li.style.setProperty('display', isArchive ? 'block' : 'flex', 'important');
      list.appendChild(li);
    });

    renderControls();
  }

  // 3. ВСПОМОГАТЕЛЬНЫЕ КНОПКИ УПРАВЛЕНИЯ
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
        window.scrollTo(0, 0); 
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

  // 4. ГЕНЕРАЦИЯ КНОПОК СКОЛЬЗЯЩЕГО ОКНА НА ОСНОВЕ TOTAL_PAGES БАЗЫ ДАННЫХ
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

