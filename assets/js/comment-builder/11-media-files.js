/**
 * @module  11-media-files.js
 * @about   Модуль управления данными медиафайлов.
 * @purpose Создание элементов выбора файлов, проверка типов и дубликатов, формирование имён файлов и регистрация файлов в медиаблоках.
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
  const physicalNamePattern = new RegExp(
    "^\\d{4}-\\d{2}-\\d{2}-\\d+_discussion_.*_" + type + "_(\\d+)\\.[^.]+$",
    "i"
  );
  const shortNamePattern = new RegExp(
    "^" + type + "_(\\d+)\\.[^.]+$",
    "i"
  );

  document.querySelectorAll(".media-sub-block").forEach(block => {
    if (getMediaBlockType(block) !== type || !Array.isArray(block.mediaFiles)) return;

    block.mediaFiles.forEach(mediaFile => {
      // Учитываем физические имена существующих файлов и короткие имена
      // всех записей, включая локальные файлы, уже добавленные в форму.
      [
        mediaFile.name,
        mediaFile.uploadName,
        mediaFile.missingName,
        mediaFile.shortName
      ].filter(Boolean).forEach(name => {
        const value = String(name).trim();
        const match = value.match(physicalNamePattern)
          || value.match(shortNamePattern);

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

      // Для файлов, ранее добавленных через форму, берём исходное имя до " | ".
      // Для остальных ссылок берём физическое имя из круглых скобок.
      const displayName = String(mediaFile.displayName || "").trim();
      const isFormCreatedName =
        mediaFile.sourceFormat === "markdown" &&
        displayName.includes(" | ");
      const comparisonName = isFormCreatedName
        ? displayName.split(" | ")[0].trim()
        : mediaFile.name;

      return typeof mediaFile.fileSize === "number" &&
        Number.isFinite(mediaFile.fileSize) &&
        mediaFile.fileSize === file.size &&
        String(comparisonName || "").trim().toLowerCase() === selectedName;
    });

    if (!duplicate && match) duplicate = match;
  });

  return duplicate;
}

// ФУНКЦИЯ: askDuplicateMediaFile
// НАЗНАЧЕНИЕ: Запрос подтверждения повторного прикрепления файла.
function askDuplicateMediaFile(fileName) {
  return new Promise(resolve => {
    const dialog = document.createElement("dialog");
    dialog.setAttribute("aria-label", "Повторное прикрепление файла");
    dialog.style.cssText = "padding:24px;border:1px solid #ccc;border-radius:8px;max-width:420px;width:calc(100% - 40px);box-shadow:0 8px 32px rgba(0,0,0,.25);";
    const message = document.createElement("p");
    message.textContent = `Файл ${fileName} прикреплен. Загрузить повторно?`;
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
    if (duplicate && !(await askDuplicateMediaFile(file.name))) continue;
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
      fileSize: fileSizes[index] !== null &&
        fileSizes[index] !== undefined &&
        fileSizes[index] !== "" &&
        Number.isFinite(Number(fileSizes[index]))
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


// ФУНКЦИЯ: getMediaBlockType
// НАЗНАЧЕНИЕ: Определение типа медиаблока
function getMediaBlockType(block) {
  if (!block) return null;

  if (block.querySelector(".photo-h3-title")) return "photo";
  if (block.querySelector(".video-h3-title")) return "video";

  return null;
}