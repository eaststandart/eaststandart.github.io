/**
 * @module  07-media-files.js
 * @about   Управление вложениями медиаблоков.
 * @purpose Выбор, проверка, отображение и точечное удаление фото и видео.
 * @author  TechLab
 * @version 1.0.0
 */

let mediaFileId = 0;

const MEDIA_FILE_RULES = {
  photo: {
    extensions: [".jpg", ".jpeg", ".png"],
    mimeTypes: ["image/jpeg", "image/png"],
    accept: ".jpg,.jpeg,.png"
  },
  video: {
    extensions: [".mp4", ".mov", ".avi", ".mkv"],
    mimeTypes: [
      "video/mp4",
      "video/quicktime",
      "video/x-msvideo",
      "video/avi",
      "video/x-matroska"
    ],
    accept: ".mp4,.mov,.avi,.mkv"
  }
};

/**
 * Определение расширения файла
 */
function getMediaFileExtension(fileName) {
  const dotIndex = fileName.lastIndexOf(".");
  return dotIndex >= 0
    ? fileName.slice(dotIndex).toLowerCase()
    : "";
}

/**
 * Проверка расширения и MIME-типа
 */
function validateMediaFile(file, type) {
  const rules = MEDIA_FILE_RULES[type];

  if (!rules) return false;

  const extension = getMediaFileExtension(file.name);

  if (!rules.extensions.includes(extension)) {
    return false;
  }

  // Некоторые браузеры не определяют MIME или возвращают общий тип.
  if (
    file.type &&
    file.type !== "application/octet-stream" &&
    !rules.mimeTypes.includes(file.type)
  ) {
    return false;
  }

  return true;
}

/**
 * Получение списка вложений медиаблока
 */
function getMediaFilesForBlock(block) {
  return block && Array.isArray(block.mediaFiles)
    ? [...block.mediaFiles]
    : [];
}

/**
 * Создание поля выбора файлов
 */
function createMediaFileInput(block, type) {
  let input = block.querySelector(".media-file-input");

  if (input) return input;

  input = document.createElement("input");
  input.type = "file";
  input.className = "media-file-input";
  input.accept = MEDIA_FILE_RULES[type].accept;
  input.multiple = true;
  input.style.display = "none";

  input.addEventListener("change", () => {
    addMediaFiles(block, Array.from(input.files || []), type);
    input.value = "";
  });

  block.appendChild(input);

  return input;
}

/**
 * Добавление новых файлов в медиаблок
 */
function addMediaFiles(block, files, type) {
  if (!block || !MEDIA_FILE_RULES[type]) return;

  if (!Array.isArray(block.mediaFiles)) {
    block.mediaFiles = [];
  }

  const rejectedFiles = [];
  let addedCount = 0;

  files.forEach(file => {
    if (!validateMediaFile(file, type)) {
      rejectedFiles.push(file.name);
      return;
    }

    block.mediaFiles.push({
      id: ++mediaFileId,
      name: file.name,
      kind: "local",
      file: file
    });

    addedCount++;
  });

  renderMediaFiles(block);

  if (rejectedFiles.length) {
    showNotify(
      `Недопустимый формат файла: ${rejectedFiles.join(", ")}`,
      "error"
    );
  } else if (addedCount > 0) {
    showNotify(
      `Добавлено файлов: ${addedCount}. Ожидают загрузки.`,
      "info"
    );
  }
}

/**
 * Регистрация файлов, восстановленных из черновика
 */
function registerExistingMediaFiles(block, fileNames, type) {
  if (!block || !Array.isArray(fileNames)) return;

  block.mediaFiles = [];

  const rejectedFiles = [];

  fileNames.forEach(fileName => {
    const file = { name: fileName };

    if (!validateMediaFile(file, type)) {
      rejectedFiles.push(fileName);
      return;
    }

    block.mediaFiles.push({
      id: ++mediaFileId,
      name: fileName,
      kind: "existing",
      file: null
    });
  });

  renderMediaFiles(block);

  if (rejectedFiles.length) {
    showNotify(
      `В черновике обнаружены неподдерживаемые вложения: ${rejectedFiles.join(", ")}`,
      "error"
    );
  }
}

/**
 * Отрисовка актуального списка вложений
 */
function renderMediaFiles(block) {
  const indicator = block.querySelector(".file-link-indicator");

  if (!indicator) return;

  indicator.innerHTML = "";

  const files = getMediaFilesForBlock(block);

  indicator.style.display = files.length ? "block" : "none";

  files.forEach(mediaFile => {
    const row = document.createElement("div");
    row.className = "media-file-row";

    const name = document.createElement("span");
    name.className = "media-file-name";

    if (mediaFile.kind === "existing" &&
        typeof createDraftFileLink === "function") {
      name.appendChild(createDraftFileLink(mediaFile.name));
    } else {
      name.textContent = mediaFile.name;
    }

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "media-file-remove";
    removeButton.dataset.fileId = String(mediaFile.id);
    removeButton.setAttribute("aria-label", `Удалить ${mediaFile.name}`);
    removeButton.textContent = "×";

    row.appendChild(name);
    row.appendChild(removeButton);

    indicator.appendChild(row);
  });
}

/**
 * Точечное удаление одного вложения
 */
function removeMediaFile(block, fileId) {
  if (!block || !Array.isArray(block.mediaFiles)) return;

  const previousCount = block.mediaFiles.length;

  block.mediaFiles = block.mediaFiles.filter(
    file => String(file.id) !== String(fileId)
  );

  renderMediaFiles(block);

  if (block.mediaFiles.length < previousCount) {
    showNotify("Файл удалён.", "info");
  }
}

/**
 * Определение типа медиаблока
 */
function getMediaBlockType(block) {
  if (!block) return null;

  if (block.querySelector(".photo-h3-title")) return "photo";
  if (block.querySelector(".video-h3-title")) return "video";

  return null;
}

/**
 * Обработка нажатий на зону выбора и кнопки удаления
 */
document.addEventListener("click", event => {
  const removeButton = event.target.closest(".media-file-remove");

  if (removeButton) {
    const block = removeButton.closest(".media-sub-block");

    removeMediaFile(block, removeButton.dataset.fileId);
    return;
  }

  const dropZone = event.target.closest(".drop-zone");

  if (!dropZone) return;

  const block = dropZone.closest(".media-sub-block");
  const type = getMediaBlockType(block);

  if (!type) return;

  createMediaFileInput(block, type).click();
});

/**
 * Обработка перетаскивания файлов
 */
document.addEventListener("dragover", event => {
  const dropZone = event.target.closest(".drop-zone");

  if (!dropZone) return;

  event.preventDefault();
  dropZone.classList.add("is-dragover");
});

document.addEventListener("dragleave", event => {
  const dropZone = event.target.closest(".drop-zone");

  if (!dropZone) return;

  dropZone.classList.remove("is-dragover");
});

document.addEventListener("drop", event => {
  const dropZone = event.target.closest(".drop-zone");

  if (!dropZone) return;

  event.preventDefault();
  dropZone.classList.remove("is-dragover");

  const block = dropZone.closest(".media-sub-block");
  const type = getMediaBlockType(block);

  if (!type) return;

  addMediaFiles(
    block,
    Array.from(event.dataTransfer.files || []),
    type
  );
});