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
    
    // Автоматически рассчитываем текущую календарную дату смены (1 в 1 из Журнала)
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

    // Наглухо сбрасываем интерфейс медиа-блоков в стартовое состояние (по 1 пустому блоку)
    if (typeof initCommentInterface === "function") {
      initCommentInterface();
    }
  }
}

/**
 * ЖЕСТКАЯ СИНХРОНИЗАЦИЯ: Наполнение всех полей шапки и Блока 2 при выборе черновика
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
  
  // 2. Очищаем пустые стартовые медиа-контейнеры на экране перестройки
  const containerPhotos = document.getElementById("photos-meta-container");
  const containerVideos = document.getElementById("videos-meta-container");
  if (containerPhotos) containerPhotos.innerHTML = "";
  if (containerVideos) containerVideos.innerHTML = "";
  
  // Аппаратно сбрасываем индексы блочного генератора
  photoBlockIdx = 0;
  videoBlockIdx = 0;

  // 3. Вырезаем подвал, если он отделен через черту ---
  let bodyText = selectedDraft.text;
  let postMainText = "";
  let postFooterText = "";

  if (bodyText.includes("---")) {
    const parts = bodyText.split("---");
    postMainText = parts[0].trim();
    postFooterText = parts.slice(1).join("---").trim();
  } else {
    postMainText = bodyText.trim();
  }

  // 4. ВОССТАНОВЛЕНИЕ СТРУКТУРЫ И ВЫВОД КЛИКАБЕЛЬНЫХ СКРЕПОК
  // Наша правильная базовая ссылка для JavaScript без лишних слов repos (1 в 1 как согласовали)
  const baseUrl = `https://githubusercontent.com{repo_owner}/${repo_name}/main/_input/`;

  // Восстановление блоков ФОТОМАТЕРИАЛОВ
  selectedDraft.photos.forEach(photoBlockData => {
    const rawSection = photoBlockData.rawContent;

    // Вытаскиваем заголовок любого уровня (#) из секции
    const titleMatch = rawSection.match(/#+\s*(.*?)\n/);
    const title = titleMatch ? titleMatch[1].trim() : "📸 Фотоматериалы";

    // Описание — это текст между заголовком и первой картинкой ![[...]]
    let desc = rawSection.replace(/#+.*?\n/, "").replace(/!\[\[.*?\]\]/g, "").replace(/!\[.*?\]\(.*?\)/g, "").trim();

    if (typeof addPhotoBlock === "function") {
      const blockElement = addPhotoBlock(title, desc);
      if (blockElement) {
        const indicator = blockElement.querySelector(".file-link-indicator");
        
        // Регулярным выражением вытаскиваем ВСЕ файлы картинок из этого блока
        const fileMatches = rawSection.match(/!\[\[(.*?)\]\]/g) || [];
        if (fileMatches.length > 0 && indicator) {
          indicator.style.display = "block";
          indicator.innerHTML = ""; // Очищаем контейнер под список скрепок
          
          fileMatches.forEach(matchStr => {
            const fileName = matchStr.replace("![[", "").replace("]]", "").split("|")[0].trim();
            indicator.innerHTML += `<div style="margin-bottom: 2px;">📎 <a href="${baseUrl}${fileName}" target="_blank">[${fileName}]</a></div>`;
          });
        }
      }
    }
  });

  // Восстановление блоков ВИДЕОМАТЕРИАЛОВ
  selectedDraft.videos.forEach(videoBlockData => {
    const rawSection = videoBlockData.rawContent;

    const titleMatch = rawSection.match(/#+\s*(.*?)\n/);
    const title = titleMatch ? titleMatch[1].trim() : "🎥 Видеоматериалы";

    let desc = rawSection.replace(/#+.*?\n/, "").replace(/!\[\[.*?\]\]/g, "").replace(/!\[.*?\]\(.*?\)/g, "").trim();

    if (typeof addVideoBlock === "function") {
      const blockElement = addVideoBlock(title, desc);
      if (blockElement) {
        const indicator = blockElement.querySelector(".file-link-indicator");
        
        // Регулярным выражением вытаскиваем ВСЕ видеофайлы из этого блока
        const fileMatches = rawSection.match(/!\[\[(.*?)\]\]/g) || [];
        if (fileMatches.length > 0 && indicator) {
          indicator.style.display = "block";
          indicator.innerHTML = "";
          
          fileMatches.forEach(matchStr => {
            const fileName = matchStr.replace("![[", "").replace("]]", "").split("|")[0].trim();
            indicator.innerHTML += `<div style="margin-bottom: 2px;">📎 <a href="${baseUrl}${fileName}" target="_blank">[${fileName}]</a></div>`;
          });
        }
      }
    }
  });

  // 5. Заполнение контекста полей Блока 2
  const titleInput = document.getElementById("post-title");
  const textInput = document.getElementById("post-text");
  const footerInput = document.getElementById("post-footer");

  if (titleInput) titleInput.value = postTitleText;
  if (textInput) textInput.value = postMainText.replace(/##.*?\n/, "").trim(); // Убираем возможные h2 заголовки
  if (footerInput) footerInput.value = postFooterText;

  // Если вдруг в черновике не было медиа-блоков, принудительно возвращаем по 1 дефолтному пустому
  if (document.querySelectorAll("#photos-meta-container .media-sub-block").length === 0) {
    if (typeof addPhotoBlock === "function") addPhotoBlock();
  }
  if (document.querySelectorAll("#videos-meta-container .media-sub-block").length === 0) {
    if (typeof addVideoBlock === "function") addVideoBlock();
  }

  showNotify(`Черновик от ${selectedDraft.date} успешно развернут!`, "success");
}
