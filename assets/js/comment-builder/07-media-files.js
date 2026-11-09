/**
 * @module  07-media-files.js
 * @about   Модуль управления вложениями медиаблоков.
 * @purpose Выбор, проверка, отображение, восстановление и удаление фото- и видеофайлов.
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

// ФУНКЦИЯ: getMediaFileExtension
// НАЗНАЧЕНИЕ: Определение расширения файла
function getMediaFileExtension(fileName) {
  const dotIndex = fileName.lastIndexOf(".");
  return dotIndex >= 0
    ? fileName.slice(dotIndex).toLowerCase()
    : "";
}

// ФУНКЦИЯ: validateMediaFile
// НАЗНАЧЕНИЕ: Проверка расширения и MIME-типа
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

// ФУНКЦИЯ: getMediaFilesForBlock
// НАЗНАЧЕНИЕ: Получение списка вложений медиаблока
function getMediaFilesForBlock(block) {
  return block && Array.isArray(block.mediaFiles)
    ? [...block.mediaFiles]
    : [];
}

// ФУНКЦИЯ: createMediaFileInput
// НАЗНАЧЕНИЕ: Создание поля выбора файлов
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

// ФУНКЦИЯ: addMediaFiles
// НАЗНАЧЕНИЕ: Добавление новых файлов в медиаблок
function addMediaFiles(block, files, type) {
  if (!block || !MEDIA_FILE_RULES[type]) return;

  if (!Array.isArray(block.mediaFiles)) {
    block.mediaFiles = [];
  }

  const rejectedFiles = [];

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
  });

  renderMediaFiles(block);

  if (rejectedFiles.length) {
    showNotify(
      `Недопустимый формат файла: ${rejectedFiles.join(", ")}`,
      "error"
    );
  } else {
    const pendingCount = document.querySelectorAll(
      ".media-sub-block"
    );

    const totalPending = Array.from(pendingCount).reduce(
      (total, item) => total + (item.mediaFiles || []).filter(
        file => file.kind === "local"
      ).length,
      0
    );

    if (totalPending > 0) {
      showNotify(
        `Добавлено файлов: ${totalPending}. Ожидают загрузки.`,
        "info"
      );
    }
  }
}

// ФУНКЦИЯ: registerExistingMediaFiles
// НАЗНАЧЕНИЕ: Регистрация файлов, восстановленных из черновика
function registerExistingMediaFiles(block, fileNames, type, missingFileNames = []) {
  if (!block || !Array.isArray(fileNames)) return;

  const missing = new Set(missingFileNames);

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
      kind: missing.has(fileName) ? "missing" : "existing",
      file: null,
      uploadName: fileName
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

// ФУНКЦИЯ: renderMediaFiles
// НАЗНАЧЕНИЕ: Отрисовка актуального списка вложений
function renderMediaFiles(block) {
  const indicator = block.querySelector(".file-link-indicator");

  if (!indicator) return;

  indicator.innerHTML = "";

  const files = getMediaFilesForBlock(block);

  const type = getMediaBlockType(block);
  const fields = type === "photo"
    ? [".photo-h3-title", ".photo-block-desc"]
    : [".video-h3-title", ".video-block-desc"];

  fields.forEach(selector => {
    const field = block.querySelector(selector);
    if (!field) return;

    field.disabled = files.length === 0;

    if (!files.length) {
      field.value = "";
    }
  });

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
      name.textContent = mediaFile.kind === "missing"
        ? mediaFile.name + " (файл отсутствует)"
        : mediaFile.name;
    }

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "media-file-remove";
    removeButton.dataset.fileId = String(mediaFile.id);
    removeButton.setAttribute("aria-label", `Удалить ${mediaFile.name}`);
    removeButton.textContent = "×";

    row.appendChild(name);

    if (mediaFile.kind === "missing") {
      const replaceButton = document.createElement("button");
      replaceButton.type = "button";
      replaceButton.className = "media-file-replace";
      replaceButton.dataset.fileId = String(mediaFile.id);
      replaceButton.textContent = "Выбрать файл";
      row.appendChild(replaceButton);
    }

    row.appendChild(removeButton);
    indicator.appendChild(row);
  });
}

// ФУНКЦИЯ: removeMediaFile
// НАЗНАЧЕНИЕ: Точечное удаление одного вложения
function removeMediaFile(block, fileId) {
  if (!block || !Array.isArray(block.mediaFiles)) return;

  const previousCount = block.mediaFiles.length;

  block.mediaFiles = block.mediaFiles.filter(
    file => String(file.id) !== String(fileId)
  );

  renderMediaFiles(block);

  if (block.mediaFiles.length < previousCount) {
    const totalPending = Array.from(
      document.querySelectorAll(".media-sub-block")
    ).reduce((total, item) => {
      const files = Array.isArray(item.mediaFiles)
        ? item.mediaFiles
        : [];

      return total + files.filter(
        file => file.kind === "local"
      ).length;
    }, 0);

    if (totalPending > 0) {
      showNotify(
        `Осталось файлов: ${totalPending}. Ожидают загрузки.`,
        "info"
      );
    } else {
      showNotify(
        "Новых медиафайлов для загрузки нет.",
        "info"
      );
    }
  }
}

// ФУНКЦИЯ: getMediaBlockType
// НАЗНАЧЕНИЕ: Определение типа медиаблока
function getMediaBlockType(block) {
  if (!block) return null;

  if (block.querySelector(".photo-h3-title")) return "photo";
  if (block.querySelector(".video-h3-title")) return "video";

  return null;
}

// НАЗНАЧЕНИЕ: Обработка нажатий на зону выбора и кнопки удаления
document.addEventListener("click", event => {
  const replaceButton = event.target.closest(".media-file-replace");

  if (replaceButton) {
    const block = replaceButton.closest(".media-sub-block");
    const fileId = replaceButton.dataset.fileId;
    const type = getMediaBlockType(block);
    const input = document.createElement("input");

    input.type = "file";
    input.accept = MEDIA_FILE_RULES[type].accept;
    input.style.display = "none";

    input.addEventListener("change", () => {
      const selectedFile = input.files?.[0];
      const target = block.mediaFiles?.find(
        file => String(file.id) === String(fileId)
      );

      if (selectedFile && target) {
        if (!validateMediaFile(selectedFile, type)) {
          showNotify("Недопустимый формат файла: " + selectedFile.name, "error");
        } else {
          target.kind = "local";
          target.file = selectedFile;
          target.uploadName = target.name;
          renderMediaFiles(block);
        }
      }

      input.remove();
    }, { once: true });

    block.appendChild(input);
    input.click();
    return;
  }

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

// НАЗНАЧЕНИЕ: Обработка перетаскивания файлов
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