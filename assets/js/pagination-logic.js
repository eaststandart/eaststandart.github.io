/* ==========================================================================
   УНИВЕРСАЛЬНЫЙ МОДУЛЬ ПАГИНАЦИИ СТРАНИЦ И СКОЛЬЗЯЩЕГО ОКНА (pagination-logic.js)
   ========================================================================== */

(function() {
  // Набор для отслеживания уже обработанных элементов, чтобы избежать дублирования
  var initializedControls = new Set();

  function initSinglePagination(controls) {
    if (initializedControls.has(controls)) return;
    initializedControls.add(controls);

    var listId = controls.getAttribute('data-list-id');
    var itemsPerPage = parseInt(controls.getAttribute('data-per-page') || "10", 10);
    var pinnedUrl = controls.getAttribute('data-pinned-url') || "";
    var showEmoji = controls.getAttribute('data-show-emoji') || "Y";
    var controlsId = controls.getAttribute('id');

    // Железная подстраховка: кнопка »» на Главной выводится в любом случае
    if (controlsId === "home-news-pagination") {
      controls.innerHTML = '';
      var archiveBtn = document.createElement('button');
      archiveBtn.innerText = '»»';
      archiveBtn.className = 'page-btn home-news-all-btn';
      archiveBtn.addEventListener('click', function() {
        window.location.href = '/news/';
      });
      controls.appendChild(archiveBtn);
    }

    var list = document.getElementById(listId);
    if (!list) return;

    var items = Array.from(list.children);
    if (items.length === 0) return;

    var currentPage = 1;
    var pinnedItem = null;

    // 1. ХРОНОЛОГИЧЕСКАЯ СОРТИРОВКА СПИСКА
    items.sort(function(a, b) {
      var dateA = a.getAttribute('data-date');
      var dateB = b.getAttribute('data-date');
      if (dateA && dateB) {
        return new Date(dateB) - new Date(dateA);
      }
      return 0; 
    });

    // 2. ИЗОЛИРОВАННАЯ РОКИРОВКА ЗАКРЕПЛЕННОГО ПОСТА (PINNED)
    if (pinnedUrl !== "") {
      var targetIndex = -1;
      for (var i = 0; i < items.length; i++) {
        var aTag = items[i].querySelector('.item-link');
        if (aTag && aTag.getAttribute('href') && aTag.getAttribute('href').includes(pinnedUrl)) {
          targetIndex = i;
          break;
        }
      }

      if (targetIndex > -1) {
        pinnedItem = items[targetIndex];
        pinnedItem.classList.add('pinned-item');
        items.splice(targetIndex, 1); 
      }
    }

    var totalPages = Math.ceil(items.length / itemsPerPage);

    // 3. ФУНКЦИЯ ОТРИСОВКИ ТЕКУЩЕЙ СТРАНИЦЫ КОНТЕНТА
    function renderPage(page) {
      list.innerHTML = '';
      
      var isArchive = window.location.pathname.includes('/news/') || window.location.pathname.includes('/journal/');
      var currentLimit = itemsPerPage;

      if (pinnedItem) {
        pinnedItem.style.setProperty('display', isArchive ? 'block' : 'flex', 'important');
        
        var pinnedLink = pinnedItem.querySelector('.item-link');
        var pinnedEmoji = pinnedItem.getAttribute('data-emoji');
        
        if (showEmoji === 'Y' && pinnedLink && pinnedEmoji && !pinnedLink.innerHTML.includes(pinnedEmoji)) {
          pinnedLink.innerHTML += ' ' + pinnedEmoji;
        }
        
        list.appendChild(pinnedItem);
        currentLimit = itemsPerPage - 1;
      }

      var start = (page - 1) * currentLimit;
      var end = start + currentLimit;
      
      items.slice(start, end).forEach(function(el) {
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

    // 4. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ГЕНЕРАЦИИ ЭЛЕМЕНТОВ ИНТЕРФЕЙСА
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

    // 5. ГЕНЕРАЦИЯ БЛОКА КНОПОК ПО СХЕМЕ "СКОЛЬЗЯЩЕГО ОКНА"
    function renderControls() {
      // Для Главной страницы очищаем только старые цифровые кнопки, сохраняя кнопку »»
      if (controlsId === "home-news-pagination") {
        var existingBtns = controls.querySelectorAll('.page-btn:not(.home-news-all-btn), span');
        existingBtns.forEach(function(btn) { btn.remove(); });
      } else {
        controls.innerHTML = '';
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

  // Запуск логики для уже существующих на странице элементов
  function scanExisting() {
    var controlDivs = document.querySelectorAll('.pagination-controls');
    controlDivs.forEach(function(controls) {
      initSinglePagination(controls);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scanExisting);
  } else {
    scanExisting();
  }

  // Обучаем скрипт динамически перехватывать появление блоков ( MutationObserver )
  var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      mutation.addedNodes.forEach(function(node) {
        if (node.nodeType === Node.ELEMENT_NODE) {
          if (node.classList.contains('pagination-controls')) {
            initSinglePagination(node);
          }
          var childControls = node.querySelectorAll('.pagination-controls');
          childControls.forEach(function(controls) {
            initSinglePagination(controls);
          });
        }
      });
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });
})();
