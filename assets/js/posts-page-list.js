/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    // Находим последний видимый пост на экране (он тут и так один, вашей категории)
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));

    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      // Полностью обнуляем маргин и прячем разделительную линию у финишного поста
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      var hr = lastItem.querySelector('.media-entry-hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
    }
}
