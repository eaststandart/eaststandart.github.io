function runMediaArchiveFilter() {
    var urlParams = new URLSearchParams(window.location.search);
    var project = urlParams.get('project'); 

    if (!project) return; 

    // Удаляем чужие блоки сразу по атрибуту data-project
    document.querySelectorAll('.media-archive-list-wrapper .media-entry').forEach(function(item) {
        var cats = item.getAttribute('data-project') || "";
        if (cats.includes(project)) { 
          item.style.display = 'block'; 
        } else {
          item.remove(); // Физически стираем чужой проект
        }
    });

    // Зачищаем линии у последнего оставшегося поста
    var visibleEntries = Array.from(document.querySelectorAll('.media-archive-list-wrapper .media-entry'));
    if (visibleEntries.length > 0) {
      var lastItem = visibleEntries[visibleEntries.length - 1];
      lastItem.style.setProperty('margin-bottom', '0px', 'important');
      var hr = lastItem.querySelector('.media-entry-hr');
      if (hr) hr.style.setProperty('display', 'none', 'important');
    }
}
