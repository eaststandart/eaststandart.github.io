/* ==========================================================================
   ДЕБАГ-ДВИЖОК ФИЛЬТРАЦИИ И ТОТАЛЬНОЙ ЗАЧИСТКИ ЛЕНТЫ МЕДИА (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Например, "robot-korova-iz-kartona"

    console.log("=== ДЕБАГ: Запуск фильтрации для проекта:", project);

    if (!project) {
        console.log("=== ДЕБАГ: Параметр проекта не найден в URL. Отмена удаления.");
        // Если параметра нет, просто показываем всё
        document.querySelectorAll('.media-archive-list-wrapper .media-entry').forEach(function(item) {
            item.style.display = 'block';
        });
        return;
    }

    // 1. Делаем изолированный снимок ВСЕХ блоков до того, как их начнет менять скрипт видео
    var allEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));
    console.log("=== ДЕБАГ: Всего найдено блоков на странице перед очисткой:", allEntries.length);

    var removedCount = 0;
    var keptCount = 0;

    // 2. Пробегаемся по снимку и ЖЕСТКО ВЫРЕЗАЕМ все чужое по атрибуту data-project
    allEntries.forEach(function(item) {
        var cats = item.getAttribute('data-project') || "";
        
        // Проверяем, содержит ли строка категорий имя нашего проекта
        if (cats.includes(project)) { 
            item.style.setProperty('display', 'block', 'important'); // Наш проект — открываем
            keptCount++;
        } else {
            // Чужой проект — полностью стираем из HTML-кода до запуска видео-скрипта
            item.remove(); 
            removedCount++;
        }
    });

    console.log("=== ДЕБАГ: Очистка завершена. Оставлено постов:", keptCount, "| Удалено лишних блоков:", removedCount);

    // 3. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ: Работаем с уже идеально чистым деревом
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));

    if (visibleEntries.length > 0) {
        var lastItem = visibleEntries[visibleEntries.length - 1];
        lastItem.style.setProperty('margin-bottom', '0px', 'important');
        var hr = lastItem.querySelector('.media-entry-hr');
        if (hr) {
            hr.style.setProperty('display', 'none', 'important');
        }
    }
}
