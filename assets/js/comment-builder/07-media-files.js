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
    extensions: [".jpg", ".jpeg", ".png", ".webp"],
    mimeTypes: ["image/jpeg", "image/png", "image/webp"],
    accept: ".jpg,.jpeg,.png,.webp"
  },
  video: {
    extensions: [".mp4", ".webm"],
    mimeTypes: ["video/mp4", "video/webm"],
    accept: ".mp4,.webm"
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

// ФУНКЦИЯ: getMediaShortNameFromUploadName
// НАЗНАЧЕНИЕ: Получение сокращённого имени из имени загруженного файла.
function getMediaShortNameFromUploadName(fileName) {
  const match = String(fileName || "").match(/(?:^|_)(photo|video)_(\d+)(\.[^.]+)$/i);
  return match ? match[1].toLowerCase() + "_" + match[2] + match[3] : "";
}

// ФУНКЦИЯ: getNextMediaShortName
// НАЗНАЧЕНИЕ: Назначение следующего свободного сокращённого имени.
function getNextMediaShortName(type, extension) {
  let maxIndex = 0;
  document.querySelectorAll(".media-sub-block").forEach(block => {
    if (getMediaBlockType(block) !== type || !Array.isArray(block.mediaFiles)) return;
    block.mediaFiles.forEach(mediaFile => {
      [mediaFile.shortName, mediaFile.uploadName, mediaFile.missingName,
       mediaFile.kind === "local" ? null : mediaFile.name].filter(Boolean).forEach(name => {
        const match = String(name).match(new RegExp("(?:^|_)" + type + "_(\\d+)(\\.[^.]+)$", "i"));
        if (match) maxIndex = Math.max(maxIndex, Number(match[1]));
      });
    });
  });
  return type + "_" + String(maxIndex + 1).padStart(2, "0") + extension;
}

// ФУНКЦИЯ: findDuplicateMediaFile
// НАЗНАЧЕНИЕ: Поиск ранее прикреплённого в текущей форме того же файла.
function findDuplicateMediaFile(file) {
  let duplicate = null;
  const selectedName = String(file.name || "").trim().toLowerCase();

  document.querySelectorAll(".media-sub-block").forEach(block => {
    if (!Array.isArray(block.mediaFiles)) return;

    const match = block.mediaFiles.find(mediaFile => {
      // Для файлов, добавленных в текущей сессии, сохраняем точную проверку.
      if (mediaFile.originalName) {
        return mediaFile.originalName === file.name &&
          mediaFile.fileSize === file.size &&
          mediaFile.fileLastModified === file.lastModified &&
          mediaFile.fileType === file.type;
      }

      // Для вики-ссылок сравниваем полное имя из адреса ссылки.
      // Для ссылок формы — исходное имя из подписи до разделителя " | ".
      const displayName = String(mediaFile.displayName || "").trim();
      const isWikiLink = mediaFile.sourceFormat === "obsidian" ||
        mediaFile.sourceFormat === "mediawiki" ||
        (mediaFile.sourceFormat === "markdown" && /^MediaWiki\s*\|/i.test(displayName)) ||
        (mediaFile.sourceFormat === "markdown" && !displayName.includes(" | "));
      const comparisonName = isWikiLink
        ? mediaFile.name
        : displayName.split(" | ")[0].trim();

      return Number.isFinite(Number(mediaFile.fileSize)) &&
        Number(mediaFile.fileSize) === file.size &&
        String(comparisonName || "").trim().toLowerCase() === selectedName;
    });

    if (!duplicate && match) duplicate = match;
  });

  return duplicate;
}

// ФУНКЦИЯ: askDuplicateMediaFile
// НАЗНАЧЕНИЕ: Запрос подтверждения повторного прикрепления файла.
function askDuplicateMediaFile() {
  return new Promise(resolve => {
    const dialog = document.createElement("dialog");
    dialog.setAttribute("aria-label", "Повторное прикрепление файла");
    dialog.style.cssText = "padding:24px;border:1px solid #ccc;border-radius:8px;max-width:420px;width:calc(100% - 40px);box-shadow:0 8px 32px rgba(0,0,0,.25);";
    const message = document.createElement("p");
    message.textContent = "Файл прикреплен. Загрузить повторно?";
    message.style.margin = "0 0 20px";
    const buttons = document.createElement("div");
    buttons.style.cssText = "display:flex;justify-content:flex-end;gap:10px;";
    const yesButton = document.createElement("button");
    yesButton.type = "button";
    yesButton.textContent = "Да";
    const noButton = document.createElement("button");
    noButton.type = "button";
    noButton.textContent = "Нет";
    const finish = value => {
      if (dialog.open) dialog.close();
      dialog.remove();
      resolve(value);
    };
    yesButton.addEventListener("click", () => finish(true));
    noButton.addEventListener("click", () => finish(false));
    dialog.addEventListener("cancel", event => {
      event.preventDefault();
      finish(false);
    });
    buttons.append(yesButton, noButton);
    dialog.append(message, buttons);
    document.body.appendChild(dialog);
    dialog.showModal();
    noButton.focus();
  });
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

  input.addEventListener("change", () => {
    addMediaFiles(block, Array.from(input.files || []), type);
    input.value = "";
  });

  block.appendChild(input);

  return input;
}

// ФУНКЦИЯ: addMediaFiles
// НАЗНАЧЕНИЕ: Добавление новых файлов в медиаблок
// ФУНКЦИЯ: addMediaFiles
// НАЗНАЧЕНИЕ: Добавление новых файлов в медиаблок с подтверждением дубликатов.
async function addMediaFiles(block, files, type) {
  if (!block || !MEDIA_FILE_RULES[type]) return;
  if (!Array.isArray(block.mediaFiles)) block.mediaFiles = [];
  const rejectedFiles = [];
  let addedCount = 0;
  for (const file of files) {
    if (!validateMediaFile(file, type)) {
      rejectedFiles.push(file.name);
      continue;
    }
    const duplicate = findDuplicateMediaFile(file);
    if (duplicate && !(await askDuplicateMediaFile())) continue;
    block.mediaFiles.push({
      id: ++mediaFileId,
      name: file.name,
      originalName: file.name,
      shortName: getNextMediaShortName(type, getMediaFileExtension(file.name)),
      fileSize: file.size,
      fileLastModified: file.lastModified,
      fileType: file.type,
      embed: true,
      kind: "local",
      file: file
    });
    addedCount++;
  }
  renderMediaFiles(block);
  if (rejectedFiles.length) {
    showNotify("Неподдерживаемые вложения!", "error");
  } else if (addedCount > 0) {
    const pendingCount = document.querySelectorAll(".media-sub-block");
    const totalPending = Array.from(pendingCount).reduce(
      (total, item) => total + (item.mediaFiles || []).filter(file => file.kind === "local").length,
      0
    );
    if (totalPending > 0) {
      showNotify("Добавлено файлов: " + totalPending + ". Ожидают загрузки.", "success");
    }
  }
}

// ФУНКЦИЯ: registerExistingMediaFiles
// НАЗНАЧЕНИЕ: Регистрация файлов, восстановленных из черновика
function registerExistingMediaFiles(
  block,
  fileNames,
  type,
  missingFileNames = [],
  displayNames = [],
  embedFlags = [],
  sourceFormats = [],
  fileSizes = []
) {
  if (!block || !Array.isArray(fileNames)) return;

  const missing = new Set(missingFileNames);

  block.mediaFiles = [];

  const rejectedFiles = [];

  fileNames.forEach((fileName, index) => {
    const file = { name: fileName };

    if (!validateMediaFile(file, type)) {
      rejectedFiles.push(fileName);
      return;
    }

    block.mediaFiles.push({
      id: ++mediaFileId,
      name: fileName,
      displayName: displayNames[index] || "",
      sourceFormat: sourceFormats[index] || "obsidian",
      fileSize: Number.isFinite(Number(fileSizes[index]))
        ? Number(fileSizes[index])
        : null,
      shortName: getMediaShortNameFromUploadName(fileName) || fileName,
      embed: embedFlags[index] === true,
      kind: missing.has(fileName) ? "missing" : "existing",
      file: null,
      uploadName: fileName
    });
  });

  renderMediaFiles(block);

  if (rejectedFiles.length) {
    showNotify(
      "Неподдерживаемые вложения!",
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

  indicator.classList.toggle("is-visible", files.length > 0);

  files.forEach(mediaFile => {
    const row = document.createElement("div");
    row.className = "media-file-row";

    const name = document.createElement("span");
    name.className = "media-file-name";

    const hasOriginalName = Boolean(mediaFile.originalName || mediaFile.displayName);
    const originalName = mediaFile.originalName || mediaFile.displayName || "";
    const shortName = mediaFile.shortName
      || getMediaShortNameFromUploadName(mediaFile.uploadName || mediaFile.name)
      || mediaFile.name;

    const isMediaWiki = mediaFile.sourceFormat === "obsidian" ||
      mediaFile.sourceFormat === "mediawiki";

    if (mediaFile.kind === "existing" &&
        typeof createDraftFileLink === "function") {
      const link = createDraftFileLink(mediaFile.name);
      if (isMediaWiki) {
        name.append("[");
        link.textContent = "MediaWiki | " + shortName;
        name.appendChild(link);
        name.append("]");
      } else {
        name.append("[");
        if (mediaFile.sourceFormat === "markdown") {
          link.textContent = mediaFile.displayName;
        } else {
          if (hasOriginalName) {
            name.append(originalName);
            name.append(" | ");
          }
          link.textContent = shortName;
        }
        name.appendChild(link);
        name.append("]");
      }
    } else {
      let displayName;
      if (isMediaWiki) {
        displayName = "[MediaWiki | " + shortName + "]";
      } else {
        displayName = "[" + (mediaFile.sourceFormat === "markdown"
          ? mediaFile.displayName
          : hasOriginalName
            ? originalName + " | " + shortName
            : shortName) + "]";
      }
      name.textContent = displayName
        + (mediaFile.kind === "missing" ? " (отсутствует)" : "");
    }

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "media-file-remove";
    removeButton.dataset.fileId = String(mediaFile.id);
    removeButton.setAttribute("aria-label", "Удалить " + originalName);
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
        "success"
      );
    } else {
      showNotify(
        "Новых медиафайлов для загрузки нет.",
        "success"
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
    input.className = "media-file-input";
    input.accept = MEDIA_FILE_RULES[type].accept;
  
    input.addEventListener("change", () => {
      const selectedFile = input.files?.[0];
      const target = block.mediaFiles?.find(
        file => String(file.id) === String(fileId)
      );

      if (selectedFile && target) {
        if (!validateMediaFile(selectedFile, type)) {
          showNotify("Неподдерживаемые вложения!", "error");
        } else {
          target.missingName = target.name;
          target.originalName = selectedFile.name;
          target.fileSize = selectedFile.size;
          target.fileLastModified = selectedFile.lastModified;
          target.fileType = selectedFile.type;
          target.kind = "local";
          target.file = selectedFile;
          target.name = selectedFile.name;
          target.uploadName = null;
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