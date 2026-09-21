/**
 * @about Модуль пагинации (НАДЁЖНЫЙ ЧИСТЫЙ КОНТУР).
 * @purpose Управляет видимостью порций по 10 штук из уже набитой базы Питона,
 *          полностью исключая fetch-запросы и ошибки скачивания файлов.
 * @author TechLab
 * @version 4.2.0-switcher-fixed
 */

function runPagination(listId, controlsId, itemsPerPage, basketName) {
  var list = document.getElementById(listId);
  if (!list) return;

  var controls = document.getElementById(controlsId);
  if (!controls) return;

  // Железно определяем имя секции напрямую из вызова Liquid без угадывания адресов
  var currentSection = (basketName || 'news').trim().toLowerCase();

  var currentPage = 1;
  var feedData = null;

  // Мгновенно подхватываем квантованный объект Питона из памяти сайта
  if (window.site_feed_data && window.site_feed_data[currentSection]) {
    feedData = window.site_feed_data[currentSection];
    renderPage(currentPage);
  } else {
    console.error("Ожидание проброса глобального объекта site_feed_data для секции: " + currentSection);
    return;
  }

  // СБОРКА СТРОК СТРОГО ПО КЛАССАМ И ТЕГАМ ВАШЕГО LIQUID-ФАЙЛА
  function renderPage(page) {
    list.innerHTML = '';
    var pageItems = feedData.pages[page] || [];
    var isHome = (controlsId === "home-news-pagination");

    pageItems.forEach(function(item) {
      var li = document.createElement('li');
      var pinnedClass = item.pinned ? ' pinned-item' : '';
      
      var dateParts = item.date.split('-');
      var dateStr = dateParts.length === 3 ? dateParts + '.' + dateParts + '.' + dateParts : item.date;

      if (isHome) {
        // ВАРИАНТ А: Ваша оригинальная верстка для Главной страницы
        li.className = 'news-item news-item-compact' + pinnedClass;
        var emojiStr = item.emoji ? ' ' + item.emoji : '';
        li.innerHTML = '<div><span>' + dateStr + '&nbsp;»&nbsp;</span><span>' +
                       '<a href="' + item.url + '" class="item-link">' + item.title + emojiStr + '</a>' +
                       '</span></div>';
        li.style.setProperty('display', 'flex', 'important');
      } else {
        // ВАРИАНТ Б: Ваша оригинальная верстка для Журнала, Вопросов и т.д.
        li.className = 'news-item' + pinnedClass;
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
