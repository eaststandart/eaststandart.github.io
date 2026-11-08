/**
 * @module 05-drafts-injector.js
 * @about   Модуль восстановления черновиков в интерфейсе.
 * @purpose Синхронизация полей и восстановление медиаблоков.
 * @author  TechLab
 * @version 2.0.0
 */

console.log("[TEST 05] Модуль injector загружен");

/**
 * Перерисовка выпадающего списка
 */
function refreshDraftSelect() {
  const select = document.getElementById("draft-select");
  const isDraftMode = document.getElementById("is-draft-mode")?.checked;
  if (!select) return;

  select.replaceChildren();

  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = isDraftMode
    ? "-- Сохраненный черновик --"
    : "Выберите черновик -->";
  select.appendChild(placeholder);

  if (isDraftMode) {
    mockDrafts.forEach(draft => {
      const option = document.createElement("option");
      option.value = draft.id;

      const title = String(draft.title || "").trim() || "Без заголовка";
      option.textContent = `[${draft.date}] ${title}`;

      select.appendChild(option);
    });

    select.disabled = false;
  } else {
    select.disabled = true;
  }
}

/**
 * Переключение режима черновиков
 */
function toggleDraftBehavior() {
  const isDraftMode = document.getElementById("is-draft-mode").checked;
  const select = document.getElementById("draft-select");
  const publishFlag = document.getElementById("publish-now-flag");
  currentCommentDraft = null;
  currentCommentSession = null;

  if (isDraftMode) {
    if (publishFlag) publishFlag.checked = false;
    if (typeof updatePublishLabel === "function") updatePublishLabel();
    if (typeof loadCommentDraftsFromApi === "function") loadCommentDraftsFromApi();

  } else {
    if (select) {
      select.innerHTML = `<option value="">Выберите черновик --></option>`;
      select.disabled = true;
      select.value = "";
    }

    if (publishFlag) publishFlag.checked = true;
    if (typeof updatePublishLabel === "function") updatePublishLabel();

    const localToday = new Date();
    const offset = localToday.getTimezoneOffset();
    const correctedDate = new Date(localToday.getTime() - offset * 60000);
    const defaultDateStr = correctedDate.toISOString().split("T")[0];

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

    if (typeof initCommentInterface === "function") {
      initCommentInterface();
    }
  }
}

/**
 * Создание безопасной ссылки на вложение
 */
function createDraftFileLink(fileName) {
  const baseUrl =
    `https://github.com/${repo_owner}/${repo_name}/blob/main/_input/`;

  const encodedPath = fileName
    .split("/")
    .map(part => encodeURIComponent(part))
    .join("/");

  const link = document.createElement("a");
  link.href = baseUrl + encodedPath;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = `[${fileName}]`;

  return link;
}

/**
 * Восстановление одного медиаблока
 */
function restoreMediaBlock(container, blockData, type) {
  console.log("[TEST 05] restoreMediaBlock вызвана", blockData.title);

  console.log("[INJECTOR 1] Получены данные:", {
    type: type,
    title: blockData.title,
    titleJSON: JSON.stringify(blockData.title)
  });

  const addFunction = type === "photo"
    ? addPhotoBlock
    : addVideoBlock;

  const blockElement = addFunction("", blockData.description);

  if (!blockElement) return;

  const titleInput = blockElement.querySelector(
    type === "photo" ? ".photo-h3-title" : ".video-h3-title"
  );

  if (titleInput) {
    titleInput.value = (blockData.title || "")
      .split("<!--")[0]
      .trim();

    console.log("[INJECTOR 2] Значение поля:", {
      value: titleInput.value,
      valueJSON: JSON.stringify(titleInput.value),
      html: titleInput.outerHTML
    });
  }

  // Восстанавливаем вложения черновика
  if (typeof registerExistingMediaFiles === "function") {
    registerExistingMediaFiles(
      blockElement,
      blockData.files || [],
      type
    );
  }
}

/**
 * Восстановление выбранного черновика
 */

// Текущий редактируемый черновик
let currentCommentDraft = null;

function loadDraftData(draftId) {
  if (!draftId) return;

  const selectedDraft = mockDrafts.find(d => d.id === draftId);
  if (!selectedDraft) return;

  currentCommentDraft = selectedDraft;

  console.log("[ИНЪЕКТОР] Восстановление черновика:", draftId);

  // 1. Параметры комментария
  const dateInput = document.getElementById("target-date");
  if (dateInput) dateInput.value = selectedDraft.date || "";

  document.getElementById("discussion-combo").value =
    selectedDraft.discussion || "";

  document.getElementById("commit-id").value =
    selectedDraft.commit || "";

  // 2. Очищаем медиаконтейнеры
  const containerPhotos = document.getElementById("photos-meta-container");
  const containerVideos = document.getElementById("videos-meta-container");

  if (containerPhotos) containerPhotos.innerHTML = "";
  if (containerVideos) containerVideos.innerHTML = "";

  photoBlockIdx = 0;
  videoBlockIdx = 0;

  // 3. Разделяем основной текст и подвал
  let bodyText = selectedDraft.text || "";
  let postMainText = "";
  let postFooterText = "";

  if (bodyText.includes("\n---")) {
    const parts = bodyText.split(/\r?\n---\s*(?:\r?\n|$)/);
    postMainText = parts[0].trim();
    postFooterText = parts.slice(1).join("\n---\n").trim();
  } else {
    postMainText = bodyText.trim();
  }

  // 4. Заполняем поля Блока 2
  const titleInput = document.getElementById("post-title");
  const textInput = document.getElementById("post-text");
  const footerInput = document.getElementById("post-footer");

  if (titleInput) titleInput.value = selectedDraft.title || "";
  if (textInput) textInput.value = postMainText;
  if (footerInput) footerInput.value = postFooterText;

  // 5. Восстанавливаем фотоблоки
  selectedDraft.photos.forEach(blockData => {
    restoreMediaBlock(containerPhotos, blockData, "photo");
  });

  // 6. Восстанавливаем видеоблоки
  selectedDraft.videos.forEach(blockData => {
    restoreMediaBlock(containerVideos, blockData, "video");
  });

  // 7. Если блоков не было — создаём пустые
  if (!selectedDraft.photos.length) {
    addPhotoBlock();
  }

  if (!selectedDraft.videos.length) {
    addVideoBlock();
  }

  console.log("[ИНЪЕКТОР] Черновик восстановлен");

  showNotify(
    `Черновик от ${selectedDraft.date} успешно развернут!`,
    "success"
  );
}