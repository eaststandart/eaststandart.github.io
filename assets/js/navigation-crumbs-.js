/**
 * @about Модуль навигации.
 * @purpose Автоматически строит цепочку пути для удобного возврата в родительские разделы.
 * @author TechLab
 * @version 1.0.0
 */

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
