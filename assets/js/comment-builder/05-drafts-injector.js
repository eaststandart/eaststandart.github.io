/**
 * @module  05-drafts-injector.js
 * @about   Модуль инъекции данных черновиков в интерфейс.
 * @purpose Отрисовка селекта Линии 2, жесткая синхронизация полей, автоматическое восстановление структуры медиа-блоков и вывод скрепок-ссылок.
 * @author  TechLab
 * @version 1.0.0
 */

/**
 * Функция перерисовки выпадающего списка на Линии 2
 */
function refreshDraftSelect() {
  const select = document.getElementById("draft-select");
  const isDraftMode = document.getElementById("is-draft-mode")?.checked;
  
  if (!select) return;

  if (isDraftMode) {
    let html = `<option value="">-- Сохраненный черновик --</option>`;
    mockDrafts.forEach(draft => {
      html += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
    });
    select.innerHTML = html;
    select.disabled = false;
  } else {
    select.innerHTML = `<option value="">Выберите черновик --></option>`;
    select.disabled = true;
  }
}

/**
 * ЛИНИЯ 2 В ДЕЙСТВИИ: Включение и отключение селекта Линии 2
 */
function toggleDraftBehavior() {
  const isDraftMode = document.getElementById("is-draft-mode").checked;
  const select = document.getElementById("draft-select");
  const publishFlag = document.getElementById("publish-now-flag");

  if (isDraftMode) {
    if (publishFlag) publishFlag.checked = false;
    if (typeof updatePublishLabel === "function") updatePublishLabel();
    if (typeof loadCommentDraftsFromApi === "function") loadCommentDraftsFromApi();
  } else {
    if (select) {
      select.innerHTML = `<option value="">Выберите черновик --></option>`;
      select.disabled = true;
    }
    if (publishFlag) publishFlag.checked = true;
    if (typeof updatePublishLabel === "function") updatePublishLabel();
    
    // Вычисляем текущую дату без хардкода (1 в 1 из Журнала)
    const localToday = new Date();
    const offset = localToday.getTimezoneOffset();
    const correctedDate = new Date(localToday.getTime() - (offset * 60 * 1000));
    const defaultDateStr = correctedDate.toISOString().split('T')[0];

    const dateInput = document.getElementById("target-date");
    if (dateInput) dateInput.value = defaultDateStr;
    
    const postTitle = document.getElementById("post-title");
    const postText = document.getElementById("post-text");
    const postFooter = document.getElementById("post-footer");
    
    if (postTitle) postTitle.value = "";
    if (postText) postText.value = "";
    if (postFooter) postFooter.value = "";
    
    document.getElementById("discussion-combo").value = "";
    document.getElementById("commit-id").value = "";

    // Сбрасываем медиа-блоки в дефолтное состояние (по 1 пустому блоку)
    if (typeof initCommentInterface === "function") {
      initCommentInterface();
    }
  }
}

/**
 * ЖЕСТКАЯ СИНХРОНИЗАЦИЯ: Наполнение всех полей и блоков 2, 3 и 4 при выборе из списка
 */
function loadDraftData(draftId) {
  if (!draftId) return;
  const selectedDraft = mockDrafts.find(d => d.id === draftId);
  if (!selectedDraft) return;

  // 1. Наполнение Линии 1 шапки
  const dateInput = document.getElementById("target-date");
  if (dateInput) dateInput.value = selectedDraft.date;
  
  document.getElementById("discussion-combo").value = selectedDraft.discussion;
  document.getElementById("commit-id").value = selectedDraft.commit || "";
  
  // 2. Очищаем старые контейнеры медиа-блоков на экране перед восстановлением структуры
  const containerPhotos = document.getElementById("photos-meta-container");
  const containerVideos = document.getElementById("videos-meta-container");
  if (containerPhotos) containerPhotos.innerHTML = "";
  if (containerVideos) containerVideos.innerHTML = "";
  
  // Сбрасываем глобальные индексы блочного генератора
  photoBlockIdx = 0;
  videoBlockIdx = 0;

  let bodyText = selectedDraft.text;
  let postTitleText = selectedDraft.title !== "Без заголовка" ? selectedDraft.title : "";
  let postMainText = "";
  let postFooterText = "";

  // Вырезаем подвал, если он отделен через черту ---
  if (bodyText.includes("---")) {
    const parts = bodyText.split("---");
    postMainText = parts[0].trim();
    postFooterText = parts.slice(1).join("---").trim();
  } else {
    postMainText = bodyText.trim();
  }

  // 4. ПАРСИНГ И ИНТЕЛЛЕКТУАЛЬНОЕ ВОССТАНОВЛЕНИЕ ДИНАМИЧЕСКИХ МЕДИА-БЛОКОВ
  const sections = postMainText.split(/(?=### )/);
  let cleanDescriptionText = "";

  sections.forEach(section => {
    if (!section.trim()) return;

    // Ссылка на скачивание контента с GitHub raw для скрепки
    const baseUrl = `https://raw.githubusercontent.com/${repo_owner}/${repo_name}/main/_input/`;

    // Восстановление блоков ФОТО
    if (section.includes("![[photo_") || section.includes("![photo_")) {
      const titleMatch = section.match(/###\s*(.*?)\n/);
      const title = titleMatch ? titleMatch[1].trim() : "📸 Фотоматериалы";
      let desc = section.replace(/###.*?\n/, "").replace(/!\[\[.*?\]\]/, "").replace(/!\[.*?\]\(.*?\)/, "").trim();
      
      const fileMatch = section.match(/!\[\[(.*?)\]\]/) || section.match(/!\[.*?\]\((.*?)\)/);
      
      if (typeof addPhotoBlock === "function") {
        const block = addPhotoBlock(title, desc);
        if (block && fileMatch) {
          const fileName = fileMatch[1].split("|")[0].trim();
          const indicator = block.querySelector(".file-link-indicator");
          if (indicator) {
            indicator.style.display = "block";
            indicator.innerHTML = `📎 <a href="${baseUrl}${fileName}" target="_blank">[${fileName}]</a>`;
          }
        }
      }
    }
    // Восстановление блоков ВИДЕО
    else if (section.includes("![[video_") || section.includes("![video_")) {
      const titleMatch = section.match(/###\s*(.*?)\n/);
      const title = titleMatch ? titleMatch[1].trim() : "🎥 Видеоматериалы";
      let desc = section.replace(/###.*?\n/, "").replace(/!\[\[.*?\]\]/, "").replace(/!\[.*?\]\(.*?\)/, "").trim();
      
      const fileMatch = section.match(/!\[\[(.*?)\]\]/) || section.match(/!\[.*?\]\((.*?)\)/);
      
      if (typeof addVideoBlock === "function") {
        const block = addVideoBlock(title, desc);
        if (block && fileMatch) {
          const fileName = fileMatch[1].split("|")[0].trim();
          const indicator = block.querySelector(".file-link-indicator");
          if (indicator) {
            indicator.style.display = "block";
            indicator.innerHTML = `📎 <a href="${baseUrl}${fileName}" target="_blank">[${fileName}]</a>`;
          }
        }
      }
    }
    else {
      cleanDescriptionText += section + "\n";
    }
  });

  // Наполняем контекст полей Блока 2
  const titleInput = document.getElementById("post-title");
  const textInput = document.getElementById("post-text");
  const footerInput = document.getElementById("post-footer");

  if (titleInput) titleInput.value = postTitleText;
  if (textInput) textInput.value = cleanDescriptionText.replace(/##.*?\n/, "").trim();
  if (footerInput) footerInput.value = postFooterText;

  // Возврат дефолтных блоков, если секции оказались пустыми
  if (document.querySelectorAll("#photos-meta-container .media-sub-block").length === 0) {
    if (typeof addPhotoBlock === "function") addPhotoBlock();
  }
  if (document.querySelectorAll("#videos-meta-container .media-sub-block").length === 0) {
    if (typeof addVideoBlock === "function") addVideoBlock();
  }

  showNotify(`Черновик успешно развернут!`, "success");
}
