/**
 * @about Модуль фильтрации и зачистки ленты медиа.
 * @purpose Управляет отображением контента в зависимости от выбранного режима.
 * @author TechLab
 * @version 1.0.0
 */

function runMediaArchiveFilter() {
    // 1. Получаем слаг проекта из адресной строки браузера
    var urlParams = new URLSearchParams(window.location.search);
    var targetProject = urlParams.get('project');
    
    if (!targetProject) return;

    // 2. Находим все блоки публикаций на странице
    var entries = document.querySelectorAll('#media-container .media-entry');
    var visibleEntries = [];

    entries.forEach(function(entry) {
        var projectSlug = entry.getAttribute('data-project');
        
        // Если слаг поста совпадает с запрошенным проектом — открываем его
        if (projectSlug === targetProject) {
            entry.style.display = 'block';
            visibleEntries.push(entry);
        } else {
            entry.style.display = 'none';
        }
    });

    // 3. Зачистка разделительных линий (hr) у последнего поста в ленте
    if (visibleEntries.length > 0) {
        var lastEntry = visibleEntries[visibleEntries.length - 1];
        var hr = lastEntry.querySelector('.media-entry-hr');
        if (hr) {
            hr.style.display = 'none';
        }
    }
}
