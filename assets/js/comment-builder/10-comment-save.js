/**
 * @module 10-comment-save.js
 * @about Сборка Markdown и сохранение комментария в _input.
 */

function commentYamlQuote(value) {
  return JSON.stringify(String(value ?? ""));
}

function commentToBase64(value) {
  const bytes = new TextEncoder().encode(value);
  let binary = "";
  const chunkSize = 0x8000;

  for (let i = 0; i < bytes.length; i += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
  }

  return btoa(binary);
}

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
            .filter(file => file.kind === "existing" && file.name)
            .map(file => file.name)
        : [];

      if (!files.length) return null;

      return {
        title: title || (type === "photo" ? "Фотоматериалы" : "Видеоматериалы"),
        description,
        files
      };
    })
    .filter(Boolean);
}

function buildCommentMarkdown(session) {
  const title = document.getElementById("post-title")?.value.trim() || "";
  const mainText = document.getElementById("post-text")?.value.trim() || "";
  const footer = document.getElementById("post-footer")?.value.trim() || "";
  const commit = document.getElementById("commit-id")?.value.trim() || "";
  const published = document.getElementById("publish-now-flag")?.checked === true;

  const photos = collectCommentMedia("photos-meta-container", "photo");
  const videos = collectCommentMedia("videos-meta-container", "video");

  if (!title && !mainText && !footer && !photos.length && !videos.length) {
    throw new Error("Комментарий пустой. Добавьте текст или медиаматериалы.");
  }

  const frontMatter = [
    "---",
    "publish_as_bot: true",
    `discussion_number: ${session.discussion}`,
    ...(commit ? [`discussion_comment: ${commit}`] : []),
    `date: ${session.date}`,
    `timestamp: ${session.timestamp}`,
    `published: ${published}`,
    `title: ${commentYamlQuote(title)}`,
    `teacher: ${commentYamlQuote(session.teacher)}`,
    "---"
  ];

  const body = [];

  if (title) body.push(`## ${title}`);
  if (mainText) body.push(mainText);

  if (footer) {
    body.push("---");
    body.push(footer);
  }

  photos.forEach(block => {
    const section = [
      `### ${block.title} <!-- [блок фото] -->`
    ];

    if (block.description) section.push(block.description);
    block.files.forEach(file => section.push(`![[${file}]]`));

    body.push(section.join("\n\n"));
  });

  videos.forEach(block => {
    const section = [
      `### ${block.title} <!-- [блок видео] -->`
    ];

    if (block.description) section.push(block.description);
    block.files.forEach(file => section.push(`![[${file}]]`));

    body.push(section.join("\n\n"));
  });

  return `${frontMatter.join("\n")}\n\n${body.join("\n\n")}\n`;
}

async function saveCommentMarkdown(session, markdown) {
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

  // Проверяем, существует ли файл, чтобы при повторном сохранении обновить его.
  const checkResponse = await fetch(`${url}?ref=main`, {
    method: "GET",
    headers
  });

  let sha = null;

  if (checkResponse.ok) {
    const existingFile = await checkResponse.json();
    sha = existingFile.sha;
  } else if (checkResponse.status !== 404) {
    const error = await checkResponse.json().catch(() => ({}));
    throw new Error(error.message || `Не удалось проверить файл: HTTP ${checkResponse.status}`);
  }

  const payload = {
    message: `${sha ? "Update" : "Create"} comment: ${fileName}`,
    content: commentToBase64(markdown),
    branch: "main"
  };

  if (sha) payload.sha = sha;

  const response = await fetch(url, {
    method: "PUT",
    headers,
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || `Не удалось сохранить комментарий: HTTP ${response.status}`);
  }

  return {
    fileName,
    result: await response.json()
  };
}

async function handleCommentSubmit() {
  if (window.commentFormLocked) return;

  try {
    if (!accessToken) {
      throw new Error("Нет активного токена GitHub.");
    }

    const session = getCommentUploadSession();

    if (!session?.date || !/^\d{4}-\d{2}-\d{2}$/.test(session.date)) {
      throw new Error("Проверьте дату комментария.");
    }

    if (!session.discussion || !/^\d+$/.test(session.discussion)) {
      throw new Error("Укажите номер обсуждения.");
    }

    if (!session.teacher) {
      throw new Error("Не определён преподаватель.");
    }

    setFormLock(true, "Подготовка комментария...");

    // Сначала загружаем все новые медиафайлы.
    showNotify("Загрузка новых медиафайлов...", "info");
    const uploadResult = await uploadLocalMediaFiles(session);

    // Markdown формируем только после успешной загрузки всех файлов.
    const markdown = buildCommentMarkdown(session);

    showNotify("Сохранение комментария...", "info");
    const saved = await saveCommentMarkdown(session, markdown);

    const published = document.getElementById("publish-now-flag")?.checked === true;
    const saveMessage = published ? "Комментарий сохранён" : "Черновик сохранён";

    showNotify(
      `${saveMessage}: ${saved.fileName}. Загружено новых медиафайлов: ${uploadResult.uploaded}.`,
      "success"
    );

    console.log("[COMMENT SAVE] Файл сохранён:", saved.fileName);

  } catch (error) {
    console.error("[COMMENT SAVE] Ошибка:", error);
    showNotify(error.message || "Ошибка сохранения комментария.", "error");

  } finally {
    setFormLock(false);
  }
}
