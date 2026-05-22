/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ЛОКАЛЬНОЙ ПАГИНАЦИИ ПРОЕКТОВ (posts-page-nav.js)
   ========================================================================== */

function runPostsPageNav(containerId, ctrlId, perPage, archiveUrl, includeType, projectSlugLast, sectionSlug, navTitle) {
    var ul = document.getElementById(containerId);
    var ctrlDiv = document.getElementById(ctrlId);
    if (!ul || !ctrlDiv) return;

    var allItems = Array.from(ul.querySelectorAll('.local-post-item'));
    var itemsPerPage = parseInt(perPage, 10) || 5; 
    var totalPages = Math.ceil(allItems.length / itemsPerPage);
    var currentPage = 1;

    var targetArchiveUrl = archiveUrl;

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

    function createBtn(text, targetPage, isCurrent, isDisabled, btnType) {
      var btn = document.createElement('button');
      btn.className = 'posts-page-btn'; 
      btn.innerText = text;

      if (btnType === 'archive' || btnType === 'full') {
        btn.classList.add('posts-page-all-btn');
        btn.addEventListener('click', function() {
          if (btnType === 'archive') {
            window.location.href = targetArchiveUrl;
          } else if (btnType === 'full') {
            window.location.href = '/' + includeType + '-posts-page/?project=' + projectSlugLast +
                                   '&nav=' + sectionSlug + 
                                   '&title=' + navTitle;
          }
        });
      } else {
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

    function renderButtons() {
      ctrlDiv.innerHTML = '';
      ctrlDiv.appendChild(createBtn('»»', null, false, false, 'archive'));
      ctrlDiv.appendChild(createBtn('0', null, false, false, 'full'));

      if (totalPages > 1) {
        ctrlDiv.appendChild(createBtn('«', currentPage - 1, false, currentPage === 1, null));
        for (var i = 1; i <= totalPages; i++) {
          ctrlDiv.appendChild(createBtn(i, i, i === currentPage, false, null));
        }
        ctrlDiv.appendChild(createBtn('»', currentPage + 1, false, currentPage === totalPages, null));
      }
    }

    showPage(1);
}
