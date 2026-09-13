/**
 * @about Модуль пагинации (С ВЕЧНЫМ ЗАКРЕПЛЕНИЕМ НА ВСЕХ СТРАНИЦАХ).
 * @purpose Разбивает список на страницы, удерживая закрепленные посты на самом верху.
 * @author TechLab
 * @version 2.1.0-multi-page-pin
 */

function runPagination(listId, controlsId, itemsPerPage, pinnedUrl, showEmoji) {
  var list = document.getElementById(listId);
  if (!list) return;

  var controls = document.getElementById(controlsId);
  if (!controls) return;

  var allElements = Array.from(list.children);
  
  # ➔ РАЗДЕЛЯЕМ ГОТОВЫЙ СПИСОК НА ДВЕ ОЧЕРЕДИ СРАЗУ ПРИ ЗАГРУЗКЕ
  var pinnedItems = allElements.filter(function(el) {
    return el.classList.contains('pinned-item');
  });
  
  var regularItems = allElements.filter(function(el) {
    return !el.classList.contains('pinned-item');
  });

  var currentPage = 1;
  
  # Динамический расчет лимита страниц: если есть закрепленный пост, обычных выводим на 1 меньше (9 вместо 10)
  var dynamicLimit = pinnedItems.length > 0 ? (itemsPerPage - pinnedItems.length) : itemsPerPage;
  if (dynamicLimit < 1) dynamicLimit = 1; # Предохранитель от деления на ноль
  
  var totalPages = Math.ceil(regularItems.length / dynamicLimit);

  # 1. ОТРИСОВКА ВЫБРАННОЙ СТРАНИЦЫ
  function renderPage(page) {
    list.innerHTML = '';
    var isArchive = window.location.pathname.includes('/news/') || window.location.pathname.includes('/journal/');

    # Шаг А: Первыми ВСЕГДА выводим закрепленные посты на абсолютно любой странице
    pinnedItems.forEach(function(pinnedEl) {
      # Принудительно обрабатываем эмодзи для закрепленного поста
      var pEmoji = pinnedEl.getAttribute('data-emoji');
      var pLink = pinnedEl.querySelector('.item-link');
      if (showEmoji === 'Y' && pLink && pEmoji && !pLink.innerHTML.includes(pEmoji)) {
        pLink.innerHTML += ' ' + pEmoji;
      }
      pinnedEl.style.setProperty('display', isArchive ? 'block' : 'flex', 'important');
      list.appendChild(pinnedItems);
    });

    # Шаг Б: Ниже дописываем порцию обычных постов для текущей страницы
    var start = (page - 1) * dynamicLimit;
    var end = start + dynamicLimit;
    
    regularItems.slice(start, end).forEach(function(el) {
      var emoji = el.getAttribute('data-emoji');
      var link = el.querySelector('.item-link');
      if (showEmoji === 'Y' && link && emoji && !link.innerHTML.includes(emoji)) {
        link.innerHTML += ' ' + emoji;
      }
      el.style.setProperty('display', isArchive ? 'block' : 'flex', 'important'); 
      list.appendChild(el);
    });

    renderControls();
  }

  # 2. ВСПОМОГАТЕЛЬНЫЕ КНОПКИ УПРАВЛЕНИЯ
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
        if (window.location.pathname.includes('/news/')) {
          window.scrollTo(0, 0); 
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

  # 3. ГЕНЕРАЦИЯ КНОПОК СКОЛЬЗЯЩЕГО ОКНА
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

  renderPage(currentPage);
}
