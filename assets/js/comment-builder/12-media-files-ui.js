/**
 * @module  12-media-files-ui.js
 * @about   Модуль интерфейса списка медиафайлов.
 * @purpose Отображение вложенных файлов в медиаблоках и обработка действий пользователя по удалению, замене и выбору файлов, включая перетаскивание.
 * @author  TechLab
 * @version 1.0.0
 */

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
      } else if (mediaFile.originalName) {
        name.append("[");
        link.textContent = originalName + " | " + shortName;
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