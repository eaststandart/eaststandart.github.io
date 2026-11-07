
/**
 * @module 09-media-upload.js
 * @about   Загрузка новых медиафайлов в буферный репозиторий.
 * @purpose Загрузка local-файлов через GitHub Contents API с сохранением имен.
 * @author  TechLab
 * @version 1.0.0
 */

/**
 * Преобразование File в Base64
 */

// Текущая сессия загрузки
let currentCommentSession = null;

/**
 * Получение параметров текущей сессии
 */

function getCommentUploadSession() {
  // Редактирование существующего черновика
  if (currentCommentDraft) {
    const draft = currentCommentDraft;

    return {
      date: draft.date,
      timestamp: draft.timestamp,
      discussion: draft.discussion,
      teacher: draft.teacher
    };
  }

  // Создание нового комментария
  if (!currentCommentSession) {
    currentCommentSession = {
      date: document.getElementById("target-date")?.value.trim(),
      timestamp: String(Math.floor(Date.now() / 1000)),
      discussion: document.getElementById("discussion-combo")?.value.trim(),
      teacher: localStorage.getItem("github_comment_logged_user")
    };
  }

  return currentCommentSession;
}

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

/**
 * Формирование имени нового медиафайла
 */
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

/**
 * Загрузка одного файла в _input
 */
async function uploadSingleMediaFile(file, fileName) {
  const url =
    `https://api.github.com/repos/${repo_owner}/${repo_name}` +
    `/contents/_input/${encodeURIComponent(fileName)}`;

  const content = await mediaFileToBase64(file);

  console.log("UPLOAD AUTH CHECK", {
    tokenExists: !!accessToken,
    tokenLength: accessToken?.length,
    tokenMatchesStorage: accessToken === localStorage.getItem("github_comment_token")
  });

  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Authorization": `token ${accessToken}`,
      "Accept": "application/vnd.github+json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: `Upload media: ${fileName}`,
      content: content
    })
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      error.message || `Ошибка загрузки ${fileName}: HTTP ${response.status}`
    );
  }

  return response.json();
}

/**
 * Загрузка всех новых медиафайлов конструктора
 *
 * session:
 * {
 *   date: "YYYY-MM-DD",
 *   timestamp: "секундная метка",
 *   discussion: "номер обсуждения",
 *   teacher: "логин преподавателя"
 * }
 */
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

  const counters = {
    photo: 0,
    video: 0
  };

  const uploads = [];

  blocks.forEach(block => {
    const type = getMediaBlockType(block);

    if (!type || !Array.isArray(block.mediaFiles)) return;

    block.mediaFiles.forEach(mediaFile => {
      if (mediaFile.kind !== "local") return;

      counters[type]++;

      uploads.push({
        block,
        mediaFile,
        type,
        index: counters[type]
      });
    });
  });

  if (!uploads.length) {
    return {
      success: true,
      uploaded: 0
    };
  }

  let uploaded = 0;

  for (const item of uploads) {
    const fileName = createMediaUploadName(
      item.mediaFile.file,
      item.type,
      session,
      item.index
    );

    const result = await uploadSingleMediaFile(
      item.mediaFile.file,
      fileName
    );

    // После успешной загрузки сохраняем новое имя.
    // При повторном запуске этот файл уже не загрузится повторно.
    item.mediaFile.name = result.content.name;
    item.mediaFile.kind = "existing";
    item.mediaFile.file = null;

    uploaded++;
    renderMediaFiles(item.block);
  }

  return {
    success: true,
    uploaded: uploaded
  };
}
