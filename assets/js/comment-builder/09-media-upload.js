/**
 * @module  09-media-upload.js
 * @about   Модуль загрузки медиафайлов в буферный репозиторий.
 * @purpose Загрузка новых локальных файлов через GitHub Contents API и обработка результатов загрузки.
 * @author  TechLab
 * @version 1.0.0
 */

// НАЗНАЧЕНИЕ: Преобразование File в Base64

// Текущая сессия загрузки
let currentCommentSession = null;

// ФУНКЦИЯ: getCommentUploadSession
// НАЗНАЧЕНИЕ: Получение параметров текущей сессии
function getCommentUploadSession() {
  // Редактирование существующего черновика
  if (currentCommentDraft) {
    const draft = currentCommentDraft;
    const identityMatch = String(draft.id || "").match(/^\d{4}-\d{2}-\d{2}-(\d+)_discussion_/);
    return {
      date: draft.date,
      timestamp: identityMatch ? identityMatch[1] : draft.timestamp,
      frontMatterTimestamp: draft.timestamp,
      discussion: draft.discussion,
      teacher: draft.teacher
    };
  }

  // Текущие значения формы
  const date = document.getElementById("target-date")?.value.trim();
  const discussion = document.getElementById("discussion-combo")?.value.trim();
  const teacher = localStorage.getItem("github_comment_logged_user");

  // Создание новой сессии
  if (!currentCommentSession) {
    currentCommentSession = {
      date,
      timestamp: String(Math.floor(Date.now() / 1000)),
      discussion,
      teacher
    };
  } else {
    // Заполняем отсутствующие параметры, не меняя уже сохранённые
    if (!currentCommentSession.date && date) {
      currentCommentSession.date = date;
    }
    if (!currentCommentSession.discussion && discussion) {
      currentCommentSession.discussion = discussion;
    }
    if (!currentCommentSession.teacher && teacher) {
      currentCommentSession.teacher = teacher;
    }
  }

  return currentCommentSession;
}

// ФУНКЦИЯ: prepareLocalMediaFileNames
// НАЗНАЧЕНИЕ: Назначает новые имена с учётом номеров всех записей, включая отсутствующие.
function prepareLocalMediaFileNames(session) {
  const containers = [
    document.getElementById("photos-meta-container"),
    document.getElementById("videos-meta-container")
  ].filter(Boolean);

  const blocks = containers.flatMap(container =>
    Array.from(container.querySelectorAll(".media-sub-block"))
  );

  const counters = { photo: 0, video: 0 };

  blocks.forEach(block => {
    const type = getMediaBlockType(block);
    if (!type || !Array.isArray(block.mediaFiles)) return;

    block.mediaFiles.forEach(mediaFile => {
      [
        mediaFile.missingName,
        mediaFile.uploadName,
        mediaFile.kind === "local" ? null : mediaFile.name
      ].filter(Boolean).forEach(name => {
        const match = name.match(new RegExp("_" + type + "_(\\d+)\\.[^.]+$", "i"));
        if (match) counters[type] = Math.max(counters[type], Number(match[1]));
      });
    });
  });

  blocks.forEach(block => {
    const type = getMediaBlockType(block);
    if (!type || !Array.isArray(block.mediaFiles)) return;

    block.mediaFiles.forEach(mediaFile => {
      if (mediaFile.kind !== "local" || mediaFile.uploadName) return;
      counters[type]++;
      mediaFile.uploadName = createMediaUploadName(
        mediaFile.file,
        type,
        session,
        counters[type]
      );
    });
  });
}

// ФУНКЦИЯ: mediaFileToBase64
// НАЗНАЧЕНИЕ: Преобразует содержимое медиафайла в строку Base64.
async function mediaFileToBase64(file) {
  const buffer = await file.arrayBuffer();
  const bytes = new Uint8Array(buffer);

  let binary = "";
  const chunkSize = 0x8000;

  for (let i = 0; i < bytes.length; i += chunkSize) {
    binary += String.fromCharCode(
      ...bytes.subarray(i, i + chunkSize)
    );
  }

  return btoa(binary);
}

// ФУНКЦИЯ: createMediaUploadName
// НАЗНАЧЕНИЕ: Формирование имени нового медиафайла
function createMediaUploadName(file, type, session, index) {
  const extension = getMediaFileExtension(file.name);

  return (
    `${session.date}-${session.timestamp}` +
    `_discussion_${session.discussion}` +
    `_${session.teacher}` +
    `_${type}_${String(index).padStart(2, "0")}` +
    extension
  );
}

// ФУНКЦИЯ: waitMediaUploadRetry
// НАЗНАЧЕНИЕ: Ожидает перед повторной попыткой загрузки медиафайла.
function waitMediaUploadRetry(seconds, attempt) {
  return new Promise(resolve => {
    let remaining = seconds;

    showNotify(
      `Ошибка сети. Повтор загрузки ${attempt}/3 через ${remaining} сек.`,
      "info"
    );

    const timer = setInterval(() => {
      remaining--;

      if (remaining <= 0) {
        clearInterval(timer);
        resolve();
        return;
      }

      showNotify(
        `Ошибка сети. Повтор загрузки ${attempt}/3 через ${remaining} сек.`,
        "info"
      );
    }, 1000);
  });
}

// ФУНКЦИЯ: uploadSingleMediaFileOnce
// НАЗНАЧЕНИЕ: Выполняет одну попытку загрузки файла в _input.
async function uploadSingleMediaFileOnce(file, fileName) {
  const url =
    `https://api.github.com/repos/${repo_owner}/${repo_name}` +
    `/contents/_input/${encodeURIComponent(fileName)}`;

  const content = await mediaFileToBase64(file);

  const headers = {
    "Authorization": `Bearer ${accessToken}`,
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json"
  };

  // Проверяем, существует ли файл.
  const checkResponse = await fetch(`${url}?ref=main`, {
    method: "GET",
    headers
  });

  let sha;

  if (checkResponse.ok) {
    const existingFile = await checkResponse.json();
    sha = existingFile.sha;
  } else if (checkResponse.status !== 404) {
    const errorData = await checkResponse.json().catch(() => ({}));
    const error = new Error(errorData.message || `Ошибка проверки ${fileName}: HTTP ${checkResponse.status}`);
    error.status = checkResponse.status;
    throw error;
  }

  const body = {
    message: `${sha ? "Replace" : "Upload"} media: ${fileName}`,
    content
  };

  if (sha) body.sha = sha;

  const response = await fetch(url, {
    method: "PUT",
    headers,
    body: JSON.stringify(body)
  });

  console.log("UPLOAD RESPONSE CHECK", {
    status: response.status,
    statusText: response.statusText,
    requestId: response.headers.get("x-github-request-id"),
    fileName,
    replaced: !!sha
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const error = new Error(errorData.message || `Ошибка загрузки ${fileName}: HTTP ${response.status}`);
    error.status = response.status;
    throw error;
  }

  return response.json();
}

// ФУНКЦИЯ: uploadSingleMediaFile
// НАЗНАЧЕНИЕ: Загружает файл с повторными попытками при временных ошибках.
async function uploadSingleMediaFile(file, fileName) {
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return await uploadSingleMediaFileOnce(file, fileName);
    } catch (error) {
      const isTemporaryError =
        error instanceof TypeError ||
        (error.status >= 500 && error.status <= 599);

      if (!isTemporaryError || attempt === 3) {
        throw error;
      }

      await waitMediaUploadRetry(60, attempt + 1);
    }
  }
}

// ФУНКЦИЯ: uploadLocalMediaFiles
// НАЗНАЧЕНИЕ: Загружает новые файлы, неудачные оставляет в форме как отсутствующие.
async function uploadLocalMediaFiles(session) {
  if (!accessToken) {
    throw new Error("Нет активного токена GitHub.");
  }

  if (
    !session ||
    !session.date ||
    !session.timestamp ||
    !session.discussion ||
    !session.teacher
  ) {
    throw new Error("Не переданы все параметры сессии загрузки.");
  }

  const containers = [
    document.getElementById("photos-meta-container"),
    document.getElementById("videos-meta-container")
  ].filter(Boolean);

  const blocks = containers.flatMap(container =>
    Array.from(container.querySelectorAll(".media-sub-block"))
  );

  const counters = { photo: 0, video: 0 };
  const uploads = [];

  // Учитываем индексы всех записей, включая отсутствующие.
  blocks.forEach(block => {
    const type = getMediaBlockType(block);
    if (!type || !Array.isArray(block.mediaFiles)) return;

    block.mediaFiles.forEach(mediaFile => {
      [
        mediaFile.missingName,
        mediaFile.uploadName,
        mediaFile.kind === "local" ? null : mediaFile.name
      ].filter(Boolean).forEach(name => {
        const match = name.match(new RegExp(`_${type}_(\\d+)\\.[^.]+$`, "i"));
        if (match) counters[type] = Math.max(counters[type], Number(match[1]));
      });
    });
  });

  // Новые файлы получают следующие свободные номера.
  blocks.forEach(block => {
    const type = getMediaBlockType(block);
    if (!type || !Array.isArray(block.mediaFiles)) return;

    block.mediaFiles.forEach(mediaFile => {
      if (mediaFile.kind !== "local") return;

      if (!mediaFile.uploadName) {
        counters[type]++;
        mediaFile.uploadName = createMediaUploadName(
          mediaFile.file,
          type,
          session,
          counters[type]
        );
      }

      uploads.push({ block, mediaFile, type });
    });
  });

  if (!uploads.length) {
    return { success: true, uploaded: 0, errors: [] };
  }

  let uploaded = 0;
  const errors = [];

  for (const item of uploads) {
    const fileName = item.mediaFile.uploadName;

    try {
      const result = await uploadSingleMediaFile(item.mediaFile.file, fileName);

      item.mediaFile.name = result.content.name;
      item.mediaFile.uploadName = result.content.name;
      item.mediaFile.kind = "existing";
      item.mediaFile.missingName = null;
      item.mediaFile.file = null;
      uploaded++;
    } catch (error) {
      errors.push({ fileName, message: error.message });
      item.mediaFile.name = item.mediaFile.missingName || fileName;
      item.mediaFile.uploadName = null;
      item.mediaFile.kind = "missing";
      item.mediaFile.file = null;
    }

    renderMediaFiles(item.block);
  }

  return {
    success: errors.length === 0,
    uploaded,
    errors
  };
}

// ФУНКЦИЯ: handleMediaUpload
// НАЗНАЧЕНИЕ: Обработчик кнопки загрузки медиафайлов
async function handleMediaUpload() {
  if (window.commentFormLocked) return;

  let message = "";
  let type = "success";

  try {
    setCommentOperationLock(true);
    setFormLock(true, "Загрузка медиафайлов...");

    const session = getCommentUploadSession();
    const result = await uploadLocalMediaFiles(session);

    message = result.errors.length
      ? `Загружено: ${result.uploaded}. Не загружено: ${result.errors.length}. Отсутствующие файлы оставлены в списке.`
      : result.uploaded > 0
        ? `Загрузка завершена. Файлов загружено: ${result.uploaded}.`
        : "Новых медиафайлов для загрузки нет.";

    if (result.errors.length) {
      type = "error";
      console.warn("[MEDIA UPLOAD] Не загружены файлы:", result.errors);
    }
  } catch (error) {
    message = error.message || "Ошибка загрузки медиафайлов.";
    type = "error";
  } finally {
    setFormLock(false);
    setCommentOperationLock(false);
  }

  showNotify(message, type);
}
