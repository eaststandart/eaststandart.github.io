/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ХЛЕБНЫХ КРОШЕК НАВИГАЦИИ (navigation-crumbs.js)
   ========================================================================== */

function runNavigationCrumbs(navDir, prj, projectTitle) {
    if (prj && navDir) {
      var bb = document.getElementById('dynamic-nav-back');
      if (bb) {
        // Добавляем пробел перед span и внутри span вокруг палочки, как это делает Jekyll
        bb.innerHTML = ' <span class="nav-separator">|</span> ' +
                       '<a href="/' + navDir + '/' + prj + '/" class="back-link nav-header-link nav-ellipsis-link">' + projectTitle + '</a>';
      }
    }
}
