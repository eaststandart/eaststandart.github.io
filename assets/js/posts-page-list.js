/* ==========================================================================
   ОРИГИНАЛЬНЫЙ ДВИЖОК ФИЛЬТРАЦИИ И ЖЕСТКОЙ ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Получаем, например, "robot-korova-iz-kartona"

    if (!project) return; // Если параметр проекта не передан в URL, ничего не трогаем

    // 1. Находим вообще все блоки медиа-постов на странице
    var allEntries = document.querySelectorAll('.media-archive-list-wrapper .media-entry');
    
    allEntries.forEach(function(item) {
        var cats = item.getAttribute('data-project') || "";
        
        // Жесткая проверка: содержит ли строка категорий наш слаг проекта
        if (cats.includes(project)) { 
            item.style.setProperty('display', 'block', 'important'); 
        } else {
            // Если проект чужой — ФИЗИЧЕСКИ вырезаем его из HTML-кода страницы
            item.remove();
        }
    });

    // 2. ЗАЧИСТКА ХВОСТОВ: Корректируем стили для последнего оставшегося поста
    var visibleEntries = document.querySelectorAll('.media-archive-list-wrapper .media-entry');
    
    if (visibleEntries.length > 0) {
        var lastItem = visibleEntries[visibleEntries.length - 1];
        lastItem.style.setProperty('margin-bottom', '0px', 'important');
        
        var hr = lastItem.querySelector('.media-entry-hr');
        if (hr) {
            hr.style.setProperty('display', 'none', 'important');
        }
    }
}
