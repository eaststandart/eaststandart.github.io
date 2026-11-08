/**
 * @module  02-comment-ui.js
 * @about   Модуль динамического управления интерфейсом и блочным конструктором.
 * @purpose Генерация полей ввода, добавление/удаление блоков медиа, сквозной пересчет счетчиков.
 * @author  TechLab
 * @version 1.0.0
 */

let photoBlockIdx = 0;
let videoBlockIdx = 0;

/**
 * ФУНКЦИЯ №2: Главная инициализация интерфейса Конструктора
 * Вызывается строго из модуля 01-comment-auth.js после успешной авторизации.
 */
function initCommentInterface() {
  const containerPhotos = document.getElementById("photos-meta-container");
  const containerVideos = document.getElementById("videos-meta-container");
  
  if (containerPhotos) containerPhotos.innerHTML = "";
  if (containerVideos) containerVideos.innerHTML = "";
  
  photoBlockIdx = 0;
  videoBlockIdx = 0;

  // Генерируем по одному дефолтному пустому блоку 1 в 1 как в монолитном скрипте
  addPhotoBlock();
  addVideoBlock();

  // Настраиваем дефолтное состояние Линии 2 шапки
  const select = document.getElementById("draft-select");
  if (select) {
    select.innerHTML = `<option value="">Выберите черновик --></option>`;
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

  showNotify("Интерфейс конструктора готов!", "success");
  
  const userLogin = localStorage.getItem("github_comment_logged_user") || "Преподаватель";
  setTimeout(() => { showNotify("👨‍🎓 Преподаватель: " + userLogin, "info"); }, 1500);
}

/**
 * АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ФОТО
 */
function updatePhotoDeleteButtons() {
  const blocks = document.querySelectorAll("#photos-meta-container .media-sub-block");
  blocks.forEach((block) => {
    const deleteContainer = block.querySelector(".btn-delete-container");
    if (deleteContainer) {
      // Если блок единственный на экране — прячем кнопку удаления
      deleteContainer.style.display = (blocks.length > 1) ? "block" : "none";
    }
  });
}

/**
 * АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ВИДЕО
 */
function updateVideoDeleteButtons() {
  const blocks = document.querySelectorAll("#videos-meta-container .media-sub-block");
  blocks.forEach((block) => {
    const deleteContainer = block.querySelector(".btn-delete-container");
    if (deleteContainer) {
      // Если блок единственный на экране — прячем кнопку удаления
      deleteContainer.style.display = (blocks.length > 1) ? "block" : "none";
    }
  });
}

/**
 * ДОБАВЛЕНИЕ БЛОКА ФОТО С ОРИГИНАЛЬНЫМИ КЛАССАМИ ОФОРМЛЕНИЯ
 */
function addPhotoBlock(initialTitle = "", initialDesc = "") {
  photoBlockIdx++;

  const container = document.getElementById("photos-meta-container");
  if (!container) return null;

  const subBlock = document.createElement("div");
  subBlock.className = "media-sub-block";
  subBlock.id = `photo-sub-block-${photoBlockIdx}`;

  subBlock.innerHTML = `
    <input type="text" class="photo-h3-title" placeholder="Заголовок для фотоматериалов">
    <textarea class="photo-block-desc" rows="2" placeholder="Краткое описание блока..."></textarea>
    <div class="drop-zone" data-media-type="photo">Нажмите для выбора или перетащите фото в этот блок</div>
    <div class="file-link-indicator" style="margin-top: 5px; font-size: 13px; font-family: monospace; display: none;"></div>
    <div class="btn-delete-container" style="display: none;">
      <button class="btn-delete-block" type="button" onclick="deletePhotoBlock('${subBlock.id}')">[Удалить блок]</button>
    </div>
  `;

  subBlock.querySelector(".photo-h3-title").value = initialTitle;
  subBlock.querySelector(".photo-block-desc").value = initialDesc;

  container.appendChild(subBlock);
  updatePhotoDeleteButtons();

  return subBlock;
}

function deletePhotoBlock(blockId) {
  const block = document.getElementById(blockId);
  if (block) {
    block.remove();
    updatePhotoDeleteButtons();
  }
}

/**
 * ДОБАВЛЕНИЕ БЛОКА ВИДЕО С ОРИГИНАЛЬНЫМИ КЛАССАМИ ОФОРМЛЕНИЯ
 */
function addVideoBlock(initialTitle = "", initialDesc = "") {
  videoBlockIdx++;
  const container = document.getElementById("videos-meta-container");
  if (!container) return null;
  
  const subBlock = document.createElement("div");
  subBlock.className = "media-sub-block video-block-border";
  subBlock.id = `video-sub-block-${videoBlockIdx}`;
  
  subBlock.innerHTML = `
    <input type="text" class="video-h3-title" placeholder="Заголовок для видеоматериалов" value="${initialTitle}">
    <textarea class="video-block-desc" rows="2" placeholder="Краткое описание блока...">${initialDesc}</textarea>
    <div class="drop-zone" data-media-type="video">Нажмите для выбора или перетащите видео в этот блок</div>
    <div class="file-link-indicator" style="margin-top: 5px; font-size: 13px; font-family: monospace; display: none;"></div>
    <div class="btn-delete-container" style="display: none;">
      <button class="btn-delete-block" type="button" onclick="deleteVideoBlock('${subBlock.id}')">[Удалить блок]</button>
    </div>
  `;
  container.appendChild(subBlock);
  updateVideoDeleteButtons();
  return subBlock;
}

function deleteVideoBlock(blockId) {
  const block = document.getElementById(blockId);
  if (block) {
    block.remove();
    updateVideoDeleteButtons();
  }
}

/**
 * ДИНАМИЧЕСКИЙ ПЕРЕКЛЮЧАТЕЛЬ ТЕКСТА КНОПКИ ПРИ СМЕНЕ ФЛАГОВ (Из монолитного скрипта)
 */
function updatePublishLabel() {
  const publishFlag = document.getElementById("publish-now-flag");
  const labelText = document.getElementById("publish-label-text");
  
  if (!publishFlag) return;
  const isChecked = publishFlag.checked;

  const submitBtn = document.getElementById("submit-btn");
  if (submitBtn) {
    submitBtn.textContent = isChecked
      ? "Создать комментарий"
      : "Сохранить черновик";
  }
  
  if (isChecked) {
    if (labelText) labelText.innerText = "🔥 Опубликовать сейчас (published: true)";
  } else {
    if (labelText) labelText.innerText = "🔥 Опубликовать сейчас (published: false)";
  }
}
