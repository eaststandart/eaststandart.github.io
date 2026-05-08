---
layout: default
title: Фотографии работ участников
permalink: /photos/
---

<script>
  const urlParams = new URLSearchParams(window.location.search);
  const selectedProject = urlParams.get('project');

  if (selectedProject) {
    // 1. Вставляем кнопку "Назад" прямо в строку навигации
    const navContainer = document.getElementById('dynamic-back');
    if (navContainer) {
      navContainer.innerHTML = '<span style="color: #ccc; margin: 0 5px;">|</span><a href="javascript:history.back()" class="back-link" style="margin-bottom: 0;">Назад</a>';
    }

    // 2. Фильтруем фото (как и раньше)
    document.querySelectorAll('.photo-entry').forEach(item => {
      if (item.getAttribute('data-project') === selectedProject) {
        item.style.display = 'block';
      }
    });
  } else {
    // Если параметра нет — показываем всё
    document.querySelectorAll('.photo-entry').forEach(item => {
        item.style.display = 'block';
    });
  }
</script>

