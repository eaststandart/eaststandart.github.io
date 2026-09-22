/**
 * @about Модуль пагинации (ЧЕСТНЫЙ СЕТЕВОЙ КОНТУР JSON).
 * @purpose Физически скачивает с сервера строго по 10 постов в формате JSON (статус 200 ОК)
 *          при переключении страниц, полностью сохраняя оригинальные цвета и классы CSS.
 * @author TechLab
 * @version 8.0.0-pure-json-network
 */

function runPagination(listId, controlsId, itemsPerPage, basketName) {
  var list = document.getElementById(listId);
  if (!list) return;

  var controls = document.getElementById(controlsId);
  if (!controls) return;

  // Железный автомат имени корзины напрямую из параметра вызова Liquid
  var currentSection = (basketName || 'news').trim().toLowerCase();
  
  var currentPage = 1;
  var totalPages = 1;

  // 1. ЧЕСТНЫЙ СЕТЕВОЙ ЗАПРОС К КОНКРЕТНОМУ МИКРО-ФАЙЛУ ПОРЦИИ
  function loadPortion(page) {
    // Формируем прямой физический адрес порции в открытой папке assets/feed/
    var portionUrl = window.location.origin + '/assets/feed/' + currentSection + '-page' + page + '.json';
    
    fetch(portionUrl)
      .then(function(response) {
        if (!response.ok) {
          throw new Error('Сетевой сбой при подкачке порции: ' + response.status);
        }
        return response.json(); // Нативно парсим JSON без тяжелых библиотек
      })
      .then(function(portionData) {
        totalPages = portionData.total_pages || 1;
        currentPage = page;
        renderPage(portionData.items);
      })
      .catch(function(error) {
        console.error('[PAGINATION-ERROR] Не удалось подкачать сетевую порцию:', error);
      });
  }

  // 2. СБОРКА HTML СТРОК СТРОГО ПО ЭТАЛОНУ ВАШЕГО CSS
  function renderPage(items) {
    list.innerHTML = '';
    var isHome = (controlsId === "home-news-pagination");

    items.forEach(function(item) {
      var li = document.createElement('li');
      var pinnedClass = item.pinned ? ' pinned-item' : '';
      
      // Переводим дату из YYYY-MM-DD в канонический формат DD.MM.YYYY
      var dateParts = item.date.split('-');
      var dateStr = dateParts.length === 3 ? dateParts[2] + '.' + dateParts[1] + '.' + dateParts[0] : item.date;

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
        // ВАРИАНТ Б: Точный клон вёрстки для Журнала, Вопросов и Медиатеки
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

  // 3. ВСПОМОГАТЕЛЬНЫЕ КНОПКИ УПРАВЛЕНИЯ С ЧЕСТНОЙ СЕТЕВОЙ ПОДКАЧКОЙ ПРИ КЛИКЕ
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
        // 🌟 ЧЕСТНЫЙ СЕТЕВОЙ КЛИК: Скачиваем строго нужный файл-порцию с сервера по сети
        loadPortion(targetPage);
        
    if (!isDisabled && !isCurrent) {
      btn.addEventListener('click', function() {
        // 🌟 ЧЕСТНЫЙ СЕТЕВОЙ КЛИК: Переключаем порции без шевеления и прыжков экрана!
        loadPortion(targetPage);
      });
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

  // 4. ГЕНЕРАЦИЯ КНОПОК ПАГИНАЦИИ НА ОСНОВЕ ТЕКУЩЕГО МИКРО-JSON
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

  // 🌟 СТАРТОВЫЙ ЗАПУСК: При загрузке страницы честно качаем первую порцию с сервера
  loadPortion(currentPage);
}
