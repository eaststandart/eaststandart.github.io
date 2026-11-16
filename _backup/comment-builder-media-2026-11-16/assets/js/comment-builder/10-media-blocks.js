/**
 * @module  10-media-blocks.js
 * @about   Модуль создания и удаления медиаблоков.
 * @purpose Добавление и удаление фото- и видеоблоков, а также обновление доступности кнопок их удаления.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: updatePhotoDeleteButtons
// НАЗНАЧЕНИЕ: АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ФОТО
function updatePhotoDeleteButtons() {
  const blocks = document.querySelectorAll("#photos-meta-container .media-sub-block");
  blocks.forEach((block) => {
    const deleteContainer = block.querySelector(".btn-delete-container");
    if (deleteContainer) {
      deleteContainer.classList.add("is-visible");
    }
  });
}

// ФУНКЦИЯ: updateVideoDeleteButtons
// НАЗНАЧЕНИЕ: АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ВИДЕО
function updateVideoDeleteButtons() {
  const blocks = document.querySelectorAll("#videos-meta-container .media-sub-block");
  blocks.forEach((block) => {
    const deleteContainer = block.querySelector(".btn-delete-container");
    if (deleteContainer) {
      deleteContainer.classList.add("is-visible");
    }
  });
}

// ФУНКЦИЯ: addPhotoBlock
// НАЗНАЧЕНИЕ: ДОБАВЛЕНИЕ БЛОКА ФОТО С ОРИГИНАЛЬНЫМИ КЛАССАМИ ОФОРМЛЕНИЯ
function addPhotoBlock(initialTitle = "", initialDesc = "") {
  photoBlockIdx++;

  const container = document.getElementById("photos-meta-container");
  if (!container) return null;

  const subBlock = document.createElement("div");
  subBlock.className = "media-sub-block";
  subBlock.id = `photo-sub-block-${photoBlockIdx}`;

  subBlock.innerHTML = `
    <input type="text" class="photo-h3-title" data-limit-type="mediaTitle" placeholder="Заголовок для фотоматериалов" disabled>
    <textarea class="photo-block-desc" data-limit-type="mediaDescription" rows="2" placeholder="Краткое описание блока..." disabled></textarea>
    <div class="drop-zone" data-media-type="photo">Нажмите для выбора или перенесите фото в этот блок</div>
    <div class="file-link-indicator"></div>
    <div class="btn-delete-container">
      <button class="btn-delete-block" type="button" onclick="deletePhotoBlock('${subBlock.id}')">[Удалить блок]</button>
    </div>
  `;

  subBlock.querySelector(".photo-h3-title").value = initialTitle;
  subBlock.querySelector(".photo-block-desc").value = initialDesc;

  container.appendChild(subBlock);
  updatePhotoDeleteButtons();

  return subBlock;
}

// ФУНКЦИЯ: deletePhotoBlock
// НАЗНАЧЕНИЕ: Удаляет выбранный фотоблок из формы.
function deletePhotoBlock(blockId) {
  const block = document.getElementById(blockId);
  if (block) {
    block.remove();
    updatePhotoDeleteButtons();
  }
}

// ФУНКЦИЯ: addVideoBlock
// НАЗНАЧЕНИЕ: ДОБАВЛЕНИЕ БЛОКА ВИДЕО С ОРИГИНАЛЬНЫМИ КЛАССАМИ ОФОРМЛЕНИЯ
function addVideoBlock(initialTitle = "", initialDesc = "") {
  videoBlockIdx++;
  const container = document.getElementById("videos-meta-container");
  if (!container) return null;
  
  const subBlock = document.createElement("div");
  subBlock.className = "media-sub-block video-block-border";
  subBlock.id = `video-sub-block-${videoBlockIdx}`;
  
  subBlock.innerHTML = `
    <input type="text" class="video-h3-title" data-limit-type="mediaTitle" placeholder="Заголовок для видеоматериалов" disabled>
    <textarea class="video-block-desc" data-limit-type="mediaDescription" rows="2" placeholder="Краткое описание блока..." disabled></textarea>
    <div class="drop-zone" data-media-type="video">Нажмите для выбора или перенесите видео в этот блок</div>
    <div class="file-link-indicator"></div>
    <div class="btn-delete-container">
      <button class="btn-delete-block" type="button" onclick="deleteVideoBlock('${subBlock.id}')">[Удалить блок]</button>
    </div>
  `;

  subBlock.querySelector(".video-h3-title").value = initialTitle;
  subBlock.querySelector(".video-block-desc").value = initialDesc;

  container.appendChild(subBlock);
  updateVideoDeleteButtons();
  return subBlock;
}

// ФУНКЦИЯ: deleteVideoBlock
// НАЗНАЧЕНИЕ: Удаляет выбранный видеоблок из формы.
function deleteVideoBlock(blockId) {
  const block = document.getElementById(blockId);
  if (block) {
    block.remove();
    updateVideoDeleteButtons();
  }
}

