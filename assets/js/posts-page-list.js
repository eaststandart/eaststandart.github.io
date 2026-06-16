/* ==========================================================================
   ДВИЖОК ФИЛЬТРАЦИИ, АКТИВАЦИИ МЕДИА И ТОТАЛЬНОЙ ЗАЧИСТКИ (posts-page-list.js)
   ========================================================================== */

function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); // Например, "robot-korova-iz-kartona"

    console.log("=== ЗАПУСК: Фильтрация и активация медиа для проекта:", project);

    if (!project) {
        // Если параметра нет в URL, просто делаем все посты видимыми и активируем в них медиа
        document.querySelectorAll('.media-archive-list-wrapper .media-entry').forEach(function(item) {
            item.style.display = 'block';
            item.querySelectorAll('[data-src]').forEach(function(mediaElement) {
                mediaElement.setAttribute('src', mediaElement.getAttribute('data-src'));
                mediaElement.removeAttribute('data-src');
            });
        });
        return;
    }

    // 1. Делаем изолированный снимок всех блоков, чтобы удаление чужих не ломало цикл
    var allEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));
    
    var removedCount = 0;
    var keptCount = 0;

    // 2. Пробегаемся по снимку: наш проект активируем, чужие — стираем под корень
    allEntries.forEach(function(item) {
        var cats = item.getAttribute('data-project') || "";
        
        // Проверяем принадлежность поста к текущему проекту через includes
        if (cats.includes(project)) { 
            item.style.setProperty('display', 'block', 'important'); // Открываем наш проект
            
            // АКТИВАЦИЯ МЕДИА: Подгружаем картинки и видео ТОЛЬКО для нашего проекта
            item.querySelectorAll('[data-src]').forEach(function(mediaElement) {
                mediaElement.setAttribute('src', mediaElement.getAttribute('data-src'));
                mediaElement.removeAttribute('data-src'); // Удаляем временный атрибут
            });
            
            keptCount++;
        } else {
            // Чужой проект — полностью вырезаем текстовый мусор из HTML-кода страницы
            item.remove(); 
            removedCount++;
        }
    });

    console.log("=== ОЧИСТКА ЗАВЕРШЕНА. Оставлено проектов:", keptCount, "| Удалено лишних текстовых блоков:", removedCount);

    // 3. ЖЕЛЕЗОБЕТОННАЯ ЗАЧИСТКА ХВОСТОВ: Корректируем линию у последнего оставшегося поста
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
