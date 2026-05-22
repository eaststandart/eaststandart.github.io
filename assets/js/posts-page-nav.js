/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ЛОКАЛЬНОЙ ПАГИНАЦИИ ПРОЕКТОВ (posts-page-nav.js)
   ========================================================================== */

function runPostsPageNav(containerId, ctrlId, perPage, archiveUrl, includeType, projectSlugLast, sectionSlug, navTitle) {
    var ul = document.getElementById(containerId);
    var ctrlDiv = document.getElementById(ctrlId);
    if (!ul || !ctrlDiv) return;

    // Извлекаем элементы списка и настраиваем лимиты страниц
    var allItems = Array.from(ul.querySelectorAll('.local-post-item'));
    var itemsPerPage = parseInt(perPage, 10) || 5; 
    var totalPages = Math.ceil(allItems.length / itemsPerPage);
    var currentPage = 1;

    var targetArchiveUrl = archiveUrl;

    // Функция переключения страниц контента
    function showPage(page) {
      if (page < 1 || page > totalPages) return;
      currentPage = page;
      
      var start = (page - 1) * itemsPerPage;
      var end = start + itemsPerPage;

      allItems.forEach(function(el, index) {
        if (index >= start && index < end) {
          el.style.setProperty('display', 'block', 'important');
        } else {
          el.style.setProperty('display', 'none', 'important');
        }
      });

      renderButtons();
    }

    // Вспомогательная функция сборки кликабельной кнопки на чистом теге <button>
    function createBtn(text, targetPage, isCurrent, isDisabled, btnType) {
      var btn = document.createElement('button');
      btn.className = 'posts-page-btn'; 
      btn.innerText = text;

      // Если это кнопка специального архива (ёлочки или ноль) — красим её в синий
      if (btnType === 'archive' || btnType === 'full') {
        btn.classList.add('posts-page-all-btn');
        
        btn.addEventListener('click', function() {
          if (btnType === 'archive') {
            // Две ёлочки уводят на стандартный постраничный архив
            window.location.href = targetArchiveUrl;
          } else if (btnType === 'full') {
            // Кнопка "0" уводит на раскрытую ленту твоего media-archive.liquid
            var fullArchiveType = includeType;     
            window.location.href = '/' + fullArchiveType + '-posts-page/?project=' + projectSlugLast +
                                   '&nav=' + sectionSlug + 
                                   '&title=' + navTitle;
          }
        });
      } else {
        // Логика работы обычных цифровых кнопок пагинации проекта
        if (isCurrent) {
          btn.classList.add('active'); 
        } else if (isDisabled) {
          btn.style.opacity = '0.4'; 
          btn.style.cursor = 'default';
        } else {
          btn.addEventListener('click', function() {
            showPage(targetPage);
          });
        }
      }
      return btn;
    }

    // Динамический рендеринг навигационной ленты кнопок
    function renderButtons() {
      ctrlDiv.innerHTML = '';
      
      // Кнопка 1: Твои две ёлочки (передаем маркер 'archive', чтобы кнопка стала синей)
      ctrlDiv.appendChild(createBtn('»»', null, false, false, 'archive'));

      // Кнопка 2: Синяя кнопка "0" (передаем маркер 'full', чтобы она тоже нативно стала синей)
      ctrlDiv.appendChild(createBtn('0', null, false, false, 'full'));

      // Если страниц больше одной — рендерим стандартный цифровой блок пагинации
      if (totalPages > 1) {
        ctrlDiv.appendChild(createBtn('«', currentPage - 1, false, currentPage === 1, null));
        for (var i = 1; i <= totalPages; i++) {
          ctrlDiv.appendChild(createBtn(i, i, i === currentPage, false, null));
        }
        ctrlDiv.appendChild(createBtn('»', currentPage + 1, false, currentPage === totalPages, null));
      }
    }

    // Первичный запуск отрисовки первой страницы при загрузке карточки проекта
    showPage(1);
}
