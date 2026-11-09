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
        title,
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

  if (!currentCommentDraft && !title && !mainText && !footer && !photos.length && !videos.length) {
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
    block.files.forEach(file => section.push(`![[${file}]]`));
    body.push(section.join("\n\n"));
  });

  videos.forEach(block => {
    const section = ["## 🎥 Видеоматериалы"];
    if (block.title) section.push("### Заголовок блока", block.title);
    if (block.description) section.push("### Описание блока", block.description);
    section.push("### Медиафайлы");
    block.files.forEach(file => section.push(`![[${file}]]`));
    body.push(section.join("\n\n"));
  });

  return `${frontMatter.join("\n")}\n\n${body.join("\n\n")}\n`;
}

function decodeGithubContent(content) {
  const binary = atob(content.replace(/\s/g, ""));
  const bytes = Uint8Array.from(binary, char => char.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}

function waitBeforeRetry(seconds, attempt) {
  return new Promise(resolve => {
    let remaining = seconds;

    showNotify(
      `Ошибка сети. Повтор ${attempt}/3 через ${remaining} сек.`,
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
        `Ошибка сети. Повтор ${attempt}/3 через ${remaining} сек.`,
        "info"
      );
    }, 1000);
  });
}

async function saveCommentMarkdownOnce(url, headers, fileName, markdown) {
  async function getCurrentFile() {
    const response = await fetch(`${url}?ref=main`, {
      method: "GET",
      headers
    });

    if (response.status === 404) return null;

    if (!response.ok) {
      const error = new Error(`Ошибка проверки файла: HTTP ${response.status}`);
      error.status = response.status;
      throw error;
    }

    return await response.json();
  }

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

  const existingFile = await getCurrentFile();
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
      errorData.message || `Не удалось сохранить комментарий: HTTP ${response.status}`
    );
    error.status = response.status;
    throw error;
  }

  return {
    fileName,
    result: await response.json()
  };
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

  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return await saveCommentMarkdownOnce(url, headers, fileName, markdown);

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

    setTimeout(() => {
      resetCommentForm();
    }, 2000);

  } catch (error) {
    console.error("[COMMENT SAVE] Ошибка:", error);
    showNotify(error.message || "Ошибка сохранения комментария.", "error");

  } finally {
    setFormLock(false);
  }
}
