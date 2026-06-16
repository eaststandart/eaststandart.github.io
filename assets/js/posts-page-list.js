/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЖЕСТКОЙ ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Например, "robot-korova-iz-kartona"

    // Создаем массив, куда будем складывать элементы для полного удаления
    var nodesToRemove = [];

    // 1. Цикл фильтрации постов по текущему проекту
    document.querySelectorAll('.media-archive-list-wrapper .media-entry').forEach(function(item) {
      if (project) {
        var cats = item.getAttribute('data-project') || "";
        
        // Если пост принадлежит нашему проекту — открываем его
        if (cats.split(' ').indexOf(project) !== -1) { 
          item.style.display = 'block'; 
        } else {
          // Если пост чужой — отправляем его в список на жесткое удаление
          nodesToRemove.push(item);
        }
      } else {
        item.style.display = 'block';
      }
    });

    // ВЫПОЛНЯЕМ ЗАЧИСТКУ: Физически стираем все чужие блоки из HTML-кода страницы
    nodesToRemove.forEach(function(node) {
        node.parentNode.removeChild(node);
    });

    // 2. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ: Находим последний ВИДИМЫЙ пост на экране
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry')).filter(function(el) {
      return el.style.display === 'block';
    });

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      // Полностью обнуляем маргин и прячем разделительную линию у финишного поста
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      var hr = lastItem.querySelector('.media-entry-hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
    }
}
