/**
 * @module  03-comment-form.js
 * @about   Модуль инициализации и сброса формы конструктора.
 * @purpose Инициализация интерфейса, управление состоянием полей формы и сброс данных формы.
 * @author  TechLab
 * @version 1.0.0
 */

let photoBlockIdx = 0;
let videoBlockIdx = 0;
let commentInterfaceInitialized = false;

// ФУНКЦИЯ: initCommentInterface
// НАЗНАЧЕНИЕ: ФУНКЦИЯ №2: Главная инициализация интерфейса Конструктора Вызывается строго из модуля 01-comment-auth.js после успешной авторизации.
function initCommentInterface() {
  const commentTitle = document.getElementById("post-title");
  const commentDescription = document.getElementById("post-text");
  if (commentTitle) commentTitle.dataset.limitType = "block2Title";
  if (commentDescription) commentDescription.dataset.limitType = "block2Description";

  const publishFlag = document.getElementById("publish-now-flag");
  const publishAsBotFlag = document.getElementById("publish-as-bot-flag");
  if (!commentInterfaceInitialized) {
    if (publishFlag) publishFlag.checked = false;
    if (publishAsBotFlag) publishAsBotFlag.checked = false;
    commentInterfaceInitialized = true;
  }

  const containerPhotos = document.getElementById("photos-meta-container");
  const containerVideos = document.getElementById("videos-meta-container");
  
  if (containerPhotos) containerPhotos.innerHTML = "";
  if (containerVideos) containerVideos.innerHTML = "";
  
  photoBlockIdx = 0;
  videoBlockIdx = 0;

  // Медиаблоки создаются только по нажатию кнопок добавления.

  // Настраиваем дефолтное состояние Линии 2 шапки
  const select = document.getElementById("draft-select");
  if (select) {
    select.innerHTML = `<option value="">Выберите черновик →</option>`;
    select.disabled = true;
  }

  // Автоматический расчет текущей даты при первой загрузке (1 в 1 из Журнала)
  const localToday = new Date();
  const offset = localToday.getTimezoneOffset();
  const correctedDate = new Date(localToday.getTime() - (offset * 60 * 1000));
  const defaultDateStr = correctedDate.toISOString().split('T')[0];

  const dateInput = document.getElementById("target-date");
  if (dateInput) dateInput.value = defaultDateStr;

  const discussionInput = document.getElementById("discussion-combo");
  if (discussionInput) discussionInput.value = "";

  updatePublishLabel();

  // Статус готовности и разблокировка выполняются после завершения инициализации авторизации.
}

// ФУНКЦИЯ: resetCommentForm
// НАЗНАЧЕНИЕ: Очищает поля формы и возвращает конструктор в исходное состояние.
function resetCommentForm() {
  currentCommentDraft = null;
  currentCommentSession = null;
  if (typeof setDraftDeleteState === "function") setDraftDeleteState(null);

  document.getElementById("post-title").value = "";
  document.getElementById("post-text").value = "";
  document.getElementById("post-footer").value = "";

  document.getElementById("discussion-combo").value = "";
  document.getElementById("commit-id").value = "";

  const today = new Date();
  const offset = today.getTimezoneOffset();
  const localDate = new Date(today.getTime() - offset * 60000)
    .toISOString()
    .split("T")[0];

  document.getElementById("target-date").value = localDate;

  document.getElementById("is-draft-mode").checked = false;
  document.getElementById("publish-now-flag").checked = false;
  const publishAsBotFlag = document.getElementById("publish-as-bot-flag");
  if (publishAsBotFlag) publishAsBotFlag.checked = false;

  const select = document.getElementById("draft-select");
  select.innerHTML = `<option value="">Выберите черновик →</option>`;
  select.disabled = true;
  if (window.commentFormLocked) select.dataset.lockDisabled = "1";
  select.value = "";

  document.getElementById("photos-meta-container").innerHTML = "";
  document.getElementById("videos-meta-container").innerHTML = "";

  photoBlockIdx = 0;
  videoBlockIdx = 0;

  updatePublishLabel();

  showNotify("Очистка формы...", "success");

  console.log("[COMMENT SAVE] Форма сброшена");
}

// ФУНКЦИЯ: updatePublishLabel
// НАЗНАЧЕНИЕ: ДИНАМИЧЕСКИЙ ПЕРЕКЛЮЧАТЕЛЬ ТЕКСТА КНОПКИ ПРИ СМЕНЕ ФЛАГОВ (Из монолитного скрипта)
function updatePublishLabel() {
  const publishFlag = document.getElementById("publish-now-flag");
  const deleteFlag = document.getElementById("delete-draft-flag");
  const labelText = document.getElementById("publish-label-text");
  
  if (!publishFlag) return;
  const isChecked = publishFlag.checked;
  const isDeleteRequested = deleteFlag?.checked === true;

  const submitBtn = document.getElementById("submit-btn");
  if (submitBtn) {
    submitBtn.textContent = isDeleteRequested
      ? "✖️ Удалить черновик"
      : isChecked
        ? "💾 Сохранить комментарий"
        : "💾 Сохранить черновик";
    submitBtn.classList.toggle("is-delete-requested", isDeleteRequested);
    submitBtn.classList.toggle("is-publish-requested", isChecked && !isDeleteRequested);
  }
  
  if (labelText) labelText.innerText = "Опубликовать";

  // Флаги публикации и удаления заранее присутствуют в HTML.
}
