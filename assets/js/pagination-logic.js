/**
 * @about Модуль пагинации (ЧИСТЫЙ СВИТЧЕР СТРАНИЦ).
 * @purpose Только переключает видимость готовых блоков feed-page-block.
 *          Внутри скрипта нет генерации HTML-строк и скрытия ссылок.
 * @author TechLab
 * @version 5.0.0-switcher
 */

function runPagination(listId, controlsId, itemsPerPage) {
  var list = document.getElementById(listId);
  if (!list) return;

  var controls = document.getElementById(controlsId);
  if (!controls) return;

  // Находим все готовые постраничные блоки, которые сервер Liquid уже создал со всеми стилями
  var pageBlocks = Array.from(list.getElementsByClassName('feed-page-block'));
  if (pageBlocks.length === 0) return;

  var currentPage = 1;
  var totalPages = pageBlocks.length;

  // 1. ПЕРЕКЛЮЧЕНИЕ ВИДИМОСТИ ГОТОВЫХ СЕРВЕРНЫХ БЛОКОВ
  function showPage(pageToBlock) {
    pageBlocks.forEach(function(block) {
      var blockPageNum = parseInt(block.getAttribute('data-page'), 10);
      if (blockPageNum === pageToBlock) {
        block.style.setProperty('display', 'block', 'important');
      } else {
        block.style.setProperty('display', 'none', 'important');
      }
    });
    renderControls();
  }

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
        showPage(currentPage);
        
        // ФИКСАЦИЯ ПРЫЖКОВ: На Главной экран стоит на месте, в Журнале — плавно фокусирует начало
        if (controlsId !== "home-news-pagination") {
          list.scrollIntoView({ behavior: 'smooth' });
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
    return span;
  }

  // 2. ОТРИСОВКА КНОПОК НА ОСНОВЕ ФИЗИЧЕСКОГО КОЛИЧЕСТВА СТРАНИЦ
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

  // Запуск стартовой отрисовки первой страницы
  showPage(currentPage);
}
