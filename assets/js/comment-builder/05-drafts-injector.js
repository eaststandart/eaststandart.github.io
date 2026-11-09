/**
 * @module  05-drafts-injector.js
 * @about   Модуль восстановления черновиков в интерфейсе.
 * @purpose Заполнение полей конструктора данными выбранного черновика и восстановление его медиаблоков.
 * @author  TechLab
 * @version 1.0.0
 */

console.log("[TEST 05] Модуль injector загружен");

// ФУНКЦИЯ: refreshDraftSelect
// НАЗНАЧЕНИЕ: Перерисовка выпадающего списка
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
      const isIncomplete = draft.missingFiles?.length > 0;
      option.textContent = "[" + draft.date + "] " + title;

      if (isIncomplete) {
        option.classList.add("is-incomplete");
      }

      select.appendChild(option);
    });

    select.disabled = false;
  } else {
    select.disabled = true;
  }
}

// ФУНКЦИЯ: toggleDraftBehavior
// НАЗНАЧЕНИЕ: Переключение режима черновиков
async function toggleDraftBehavior() {
  const draftModeCheckbox = document.getElementById("is-draft-mode");
  const isDraftMode = draftModeCheckbox.checked;
  const select = document.getElementById("draft-select");
  currentCommentDraft = null;
  currentCommentSession = null;

  if (isDraftMode) {
    if (typeof updatePublishLabel === "function") updatePublishLabel();

    setFormLock(true);

    let loaded = false;

    try {
      loaded = typeof loadCommentDraftsFromApi === "function"
        ? await loadCommentDraftsFromApi()
        : false;
    } finally {
      if (!loaded) {
        draftModeCheckbox.checked = false;
        mockDrafts = [];
      }

      setFormLock(false);

      if (typeof refreshDraftSelect === "function") {
        refreshDraftSelect();
      }
    }

  } else {
    if (select) {
      select.innerHTML = `<option value="">Выберите черновик --></option>`;
      select.disabled = true;
      select.value = "";
    }

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

    const userLogin = localStorage.getItem("github_comment_logged_user");
    if (userLogin) {
      showNotify("👨‍🎓 Преподаватель: " + userLogin, "info");
    }
  }
}

// ФУНКЦИЯ: createDraftFileLink
// НАЗНАЧЕНИЕ: Создание безопасной ссылки на вложение
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

// ФУНКЦИЯ: restoreMediaBlock
// НАЗНАЧЕНИЕ: Восстановление одного медиаблока
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
      type,
      currentCommentDraft?.missingFiles || []
    );
  }
}

// НАЗНАЧЕНИЕ: Текущий редактируемый черновик.

// Текущий редактируемый черновик
let currentCommentDraft = null;

// ФУНКЦИЯ: loadDraftData
// НАЗНАЧЕНИЕ: Восстановление выбранного черновика в форме конструктора.
function loadDraftData(draftId) {
  if (!draftId) return;

  const selectedDraft = mockDrafts.find(d => d.id === draftId);
  if (!selectedDraft) return;

  currentCommentDraft = selectedDraft;

  const publishFlag = document.getElementById("publish-now-flag");
  if (publishFlag) {
    publishFlag.checked = String(selectedDraft.published).toLowerCase() === "true";
  }
  if (typeof updatePublishLabel === "function") updatePublishLabel();
  const publishAsBotFlag = document.getElementById("publish-as-bot-flag");
  if (publishAsBotFlag) {
    publishAsBotFlag.checked = selectedDraft.publishAsBot === true;
  }

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

  // 3. Получаем основной текст и подвал.
  // Новая структура хранит их отдельно; старые черновики требуют прежнего разделения.
  let postMainText = selectedDraft.text || "";
  let postFooterText = selectedDraft.footer || "";

  if (!selectedDraft.structured && postMainText.includes("\n---")) {
    const parts = postMainText.split(/\r?\n---\s*(?:\r?\n|$)/);
    postMainText = parts[0].trim();
    postFooterText = parts.slice(1).join("\n---\n").trim();
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

  console.log("[ИНЪЕКТОР] Черновик восстановлен");

  showNotify(
    "Черновик успешно развернут!",
    "success"
  );
}