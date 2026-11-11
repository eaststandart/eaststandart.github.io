/**
 * @module  10-comment-save.js
 * @about   Модуль формирования и сохранения комментариев.
 * @purpose Сборка Markdown с Front Matter, загрузка медиафайлов и сохранение черновика или комментария в GitHub.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: commentYamlQuote
// НАЗНАЧЕНИЕ: Безопасно оформляет строковое значение для YAML.
function commentYamlQuote(value) {
  return JSON.stringify(String(value ?? ""));
}

// ФУНКЦИЯ: commentToBase64
// НАЗНАЧЕНИЕ: Кодирует текст в Base64 с поддержкой UTF-8.
function commentToBase64(value) {
  const bytes = new TextEncoder().encode(value);
  let binary = "";
  const chunkSize = 0x8000;

  for (let i = 0; i < bytes.length; i += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
  }

  return btoa(binary);
}

// ФУНКЦИЯ: collectCommentMedia
// НАЗНАЧЕНИЕ: Собирает данные заполненных медиаблоков выбранного типа.
function collectCommentMedia(containerId, type) {
  const container = document.getElementById(containerId);
  if (!container) return [];

  return Array.from(container.querySelectorAll(".media-sub-block"))
    .map(block => {
      const titleSelector = type === "photo"
        ? ".photo-h3-title"
        : ".video-h3-title";

      const descSelector = type === "photo"
        ? ".photo-block-desc"
        : ".video-block-desc";

      const title = block.querySelector(titleSelector)?.value.trim() || "";
      const description = block.querySelector(descSelector)?.value.trim() || "";
      const files = Array.isArray(block.mediaFiles)
        ? block.mediaFiles
            .filter(file => file.missingName || file.uploadName || file.name)
            .map(file => {
              const fileName = file.missingName || file.uploadName || file.name;
              const uploadNameMatch = fileName.match(
                /^\d{4}-\d{2}-\d{2}-\d+_discussion_.*_(photo|video)_(\d+\.[^.]+)$/i
              );
              const shortName = file.shortName ||
                (uploadNameMatch
                  ? uploadNameMatch[1] + "_" + uploadNameMatch[2]
                  : fileName);
              // Новые файлы с компьютера получают пару имён.
              // Восстановленные ссылки сохраняют прежнюю подпись.
              const displayName = file.originalName
                ? file.originalName + " | " + shortName
                : file.sourceFormat === "obsidian"
                  ? "MediaWiki | " + shortName
                  : file.displayName || shortName;

              return {
                name: fileName,
                displayName,
                embed: file.embed === true || file.kind === "local"
              };
            })
        : [];

      if (!files.length) return null;

      return {
        title,
        description,
        files
      };
    })
    .filter(Boolean);
}

// ФУНКЦИЯ: buildCommentMarkdown
// НАЗНАЧЕНИЕ: Формирует полный Markdown-документ комментария и его Front Matter.
function buildCommentMarkdown(session) {
  const title = document.getElementById("post-title")?.value.trim() || "";
  const mainText = document.getElementById("post-text")?.value.trim() || "";
  const footer = document.getElementById("post-footer")?.value.trim() || "";
  const commit = document.getElementById("commit-id")?.value.trim() || "";
  const deleteRequested = document.getElementById("delete-draft-flag")?.checked === true;
  const published = !deleteRequested && document.getElementById("publish-now-flag")?.checked === true;
  const publishAsBot = document.getElementById("publish-as-bot-flag")?.checked === true;

  const photos = collectCommentMedia("photos-meta-container", "photo");
  const videos = collectCommentMedia("videos-meta-container", "video");

  if (!currentCommentDraft && !title && !mainText && !footer && !photos.length && !videos.length) {
    throw new Error("Комментарий пустой. Добавьте текст или медиаматериалы.");
  }

  const frontMatter = [
    "---",
    `publish_as_bot: ${publishAsBot}`,
    `discussion_number: ${session.discussion}`,
    ...(commit ? [`discussion_comment: ${commit}`] : []),
    `date: ${session.date}`,
    `timestamp: ${session.frontMatterTimestamp || session.timestamp}`,
    `published: ${deleteRequested ? "delete" : published}`,
    `title: ${commentYamlQuote(title)}`,
    `teacher: ${commentYamlQuote(session.teacher)}`,
    "---"
  ];

  const body = [
    published ? "# Комментарий для публикации" : "# Черновик комментария"
  ];

  const commentFields = [];
  if (title) commentFields.push("### Заголовок комментария\n\n" + title);
  if (mainText) commentFields.push("### Основной текст\n\n" + mainText);
  if (footer) commentFields.push("### Подвал комментария\n\n" + footer);

  body.push("## Структура комментария", ...commentFields);

  photos.forEach(block => {
    const section = ["## 📸 Фотоматериалы"];
    if (block.title) section.push("### Заголовок блока", block.title);
    if (block.description) section.push("### Описание блока", block.description);
    section.push("### Медиафайлы");
    block.files.forEach(file => {
      section.push(`${file.embed ? "!" : ""}[${file.displayName}](${file.name})`);
    });
    body.push(section.join("\n\n"));
  });

  videos.forEach(block => {
    const section = ["## 🎥 Видеоматериалы"];
    if (block.title) section.push("### Заголовок блока", block.title);
    if (block.description) section.push("### Описание блока", block.description);
    section.push("### Медиафайлы");
    block.files.forEach(file => {
      section.push(`${file.embed ? "!" : ""}[${file.displayName}](${file.name})`);
    });
    body.push(section.join("\n\n"));
  });

  return `${frontMatter.join("\n")}\n\n${body.join("\n\n")}\n`;
}

// ФУНКЦИЯ: decodeGithubContent
// НАЗНАЧЕНИЕ: Декодирует содержимое файла GitHub из Base64 в UTF-8.
function decodeGithubContent(content) {
  const binary = atob(content.replace(/\s/g, ""));
  const bytes = Uint8Array.from(binary, char => char.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}

// ФУНКЦИЯ: waitBeforeRetry
// НАЗНАЧЕНИЕ: Ожидает перед повторной попыткой сохранения после временной ошибки.
function waitBeforeRetry(seconds, attempt) {
  return new Promise(resolve => {
    let remaining = seconds;

    showNotify(
      `Ошибка сети. Повтор ${attempt}/3 через ${remaining} сек.`,
      "error"
    );

    const timer = setInterval(() => {
      remaining--;

      if (remaining <= 0) {
        clearInterval(timer);
        resolve();
        return;
      }

      showNotify(
        `Ошибка сети. Повтор ${attempt}/3 через ${remaining} сек.`,
        "error"
      );
    }, 1000);
  });
}

// ФУНКЦИЯ: saveCommentMarkdownOnce
// НАЗНАЧЕНИЕ: Выполняет одну попытку создания или обновления Markdown-файла в GitHub.
async function saveCommentMarkdownOnce(url, headers, fileName, markdown, knownSha = null) {
  // ФУНКЦИЯ: getCurrentFile
  // НАЗНАЧЕНИЕ: Получает актуальную версию Markdown-файла и его SHA.
  async function getCurrentFile() {
    const response = await fetch(`${url}?ref=main&_=${Date.now()}`, {
      method: "GET",
      headers,
      cache: "no-store"
    });

    if (response.status === 404) return null;

    if (!response.ok) {
      const error = new Error(`Ошибка проверки файла: HTTP ${response.status}`);
      error.status = response.status;
      throw error;
    }

    return await response.json();
  }

  // ФУНКЦИЯ: putFile

  // НАЗНАЧЕНИЕ: Создаёт или обновляет Markdown-файл через GitHub Contents API.
  async function putFile(sha) {
    const payload = {
      message: `${sha ? "Update" : "Create"} comment: ${fileName}`,
      content: commentToBase64(markdown),
      branch: "main"
    };

    if (sha) payload.sha = sha;

    return await fetch(url, {
      method: "PUT",
      headers,
      body: JSON.stringify(payload)
    });
  }

  const existingFile = knownSha ? { sha: knownSha } : await getCurrentFile();
  let sha = existingFile?.sha || null;

  if (
    existingFile?.content &&
    decodeGithubContent(existingFile.content) === markdown
  ) {
    return {
      fileName,
      result: existingFile,
      alreadySaved: true
    };
  }

  let response = await putFile(sha);

  if (response.status === 409) {
    const latestFile = await getCurrentFile();

    if (!latestFile) {
      response = await putFile(null);
    } else {
      if (latestFile.content &&
          decodeGithubContent(latestFile.content) === markdown) {
        return {
          fileName,
          result: latestFile,
          alreadySaved: true
        };
      }

      response = await putFile(latestFile.sha);
    }
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const error = new Error(
      errorData.message || `Комментарий не сохранён: HTTP ${response.status}`
    );
    error.status = response.status;
    throw error;
  }

  return {
    fileName,
    result: await response.json()
  };
}

// ФУНКЦИЯ: saveCommentMarkdown
// НАЗНАЧЕНИЕ: Сохраняет Markdown-файл с повторными попытками при временных ошибках.
async function saveCommentMarkdown(session, markdown, knownSha = null) {
  const fileName = currentCommentDraft
    ? currentCommentDraft.id
    : `${session.date}-${session.timestamp}_discussion_${session.discussion}_${session.teacher}.md`;

  const url =
    `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_input/${encodeURIComponent(fileName)}`;

  const headers = {
    Authorization: `Bearer ${accessToken}`,
    Accept: "application/vnd.github+json",
    "Content-Type": "application/json"
  };

  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return await saveCommentMarkdownOnce(
        url, headers, fileName, markdown,
        attempt === 1 ? knownSha : null
      );

    } catch (error) {
      const isNetworkError =
        error instanceof TypeError ||
        (error.status >= 500 && error.status <= 599);

      if (!isNetworkError || attempt === 3) {
        throw error;
      }

      await waitBeforeRetry(60, attempt + 1);
    }
  }
}

// ФУНКЦИЯ: handleCommentSubmit
// НАЗНАЧЕНИЕ: Проверяет форму, загружает медиафайлы и сохраняет комментарий или черновик.
async function handleCommentSubmit() {
  if (window.commentFormLocked) return;

  let markdownSaved = false;
  let mediaUploadCompleted = false;
  let uploadedMediaCount = 0;
  let mediaUploadErrorCount = 0;
  let keepFormLocked = false;

  try {
    if (!accessToken) {
      throw new Error("Нет активного токена!");
    }

    const session = getCommentUploadSession();

    if (!session?.date || !/^\d{4}-\d{2}-\d{2}$/.test(session.date)) {
      throw new Error("Проверьте дату комментария");
    }

    if (!session.discussion || !/^\d+$/.test(session.discussion)) {
      throw new Error("Укажите номер обсуждения");
    }

    if (!session.teacher) {
      throw new Error("Преподаватель не определён");
    }

    const validationError = validateCommentForm();
    if (validationError) {
      throw new Error(validationError);
    }

    setCommentOperationLock(true);
    setFormLock(true, "Подготовка комментария...");

    // При каждом сохранении обновляем только timestamp Front Matter.
    // Идентификатор сессии для имён файлов остаётся постоянным.
    const previousTimestamp = Number(
      currentCommentDraft?.timestamp || session.frontMatterTimestamp || 0
    );
    session.frontMatterTimestamp = String(
      Math.max(Math.floor(Date.now() / 1000), previousTimestamp + 1)
    );

    // Сначала назначаем имена новым файлам и сохраняем ссылки на них в Markdown.
    prepareLocalMediaFileNames(session);
    const markdown = buildCommentMarkdown(session);

    showNotify("Сохранение Markdown...", "success");
    const saved = await saveCommentMarkdown(session, markdown);
    markdownSaved = true;
    if (typeof commitDraftDeleteState === "function") commitDraftDeleteState();

    if (currentCommentDraft) {
      currentCommentDraft.timestamp = session.frontMatterTimestamp;
    }

    // После сохранения манифеста загружаем физические файлы.
    showNotify("Загрузка новых медиафайлов...", "success");
    const uploadResult = await uploadLocalMediaFiles(session);
    uploadedMediaCount = uploadResult.uploaded;
    mediaUploadErrorCount = uploadResult.errors.length;
    mediaUploadCompleted = true;

    // После загрузки файлов обновляем Front Matter ещё раз:
    // это запускает workflow повторно, когда комплект уже собран.
    if (uploadResult.uploaded > 0) {
      const uploadedTimestamp = Number(session.frontMatterTimestamp || 0);
      session.frontMatterTimestamp = String(
        Math.max(Math.floor(Date.now() / 1000), uploadedTimestamp + 1)
      );

      if (currentCommentDraft) {
        currentCommentDraft.timestamp = session.frontMatterTimestamp;
      }

      const completedMarkdown = buildCommentMarkdown(session);
      const latestSha = saved.result?.content?.sha || null;
      await saveCommentMarkdown(session, completedMarkdown, latestSha);
    }

    const unresolvedMediaCount = [
      document.getElementById("photos-meta-container"),
      document.getElementById("videos-meta-container")
    ].filter(Boolean).reduce((total, container) => {
      const blocks = Array.from(container.querySelectorAll(".media-sub-block"));
      return total + blocks.reduce((count, block) => {
        const files = Array.isArray(block.mediaFiles) ? block.mediaFiles : [];
        return count + files.filter(file => file.kind === "missing").length;
      }, 0);
    }, 0);

    const deleteRequested = document.getElementById("delete-draft-flag")?.checked === true;
    const published = !deleteRequested && document.getElementById("publish-now-flag")?.checked === true;
    const saveMessage = published ? "Комментарий сохранён!" : "Черновик сохранён!";

    // Убираем опубликованный комментарий из списка только после полной комплектации.
    if (published && unresolvedMediaCount === 0 && currentCommentDraft && Array.isArray(mockDrafts)) {
      mockDrafts = mockDrafts.filter(draft => draft.id !== saved.fileName);
      if (typeof refreshDraftSelect === "function") refreshDraftSelect();
    }

    if (uploadResult.errors.length || unresolvedMediaCount > 0) {
      showNotify(
        `Markdown сохранён | Медиа: загружены ${uploadResult.uploaded}, ошибок ${uploadResult.errors.length}`,
        "error"
      );
      if (uploadResult.errors.length) {
        console.warn("[COMMENT SAVE] Не загружены медиафайлы:", uploadResult.errors);
      }
    } else {
      showNotify(saveMessage, "success");

      console.log("[COMMENT SAVE] Файл сохранён:", saved.fileName);
      console.log("[COMMENT SAVE] Загружено новых медиафайлов:", uploadResult.uploaded);

      keepFormLocked = true;
      finishCommentFormOperation(true);
    }

  } catch (error) {
    console.error("[COMMENT SAVE] Ошибка:", error);
    let message = error.message || "Ошибка сохранения комментария.";
    if (message === "Failed to fetch") message = "Загрузка не удалась!";

    if (markdownSaved && !mediaUploadCompleted) {
      mediaUploadErrorCount = Math.max(mediaUploadErrorCount, 1);
      message = `Markdown сохранён | Медиа: загружены ${uploadedMediaCount}, ошибок ${mediaUploadErrorCount}`;
    } else if (markdownSaved && mediaUploadCompleted) {
      message = `Markdown не обновлён | Медиа: загружены ${uploadedMediaCount}, ошибок ${mediaUploadErrorCount}`;
    }

    showNotify(message, "error");

  } finally {
    if (!keepFormLocked) setFormLock(false);
    setCommentOperationLock(false);
  }
}
