/**
 * @module  14-comment-markdown.js
 * @about   Модуль формирования и кодирования Markdown комментария.
 * @purpose Сбор данных формы и медиафайлов, формирование Markdown с Front Matter, а также кодирование и декодирование содержимого для работы с GitHub.
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
                  ? "WikiLink | " + shortName
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
    ...(commit ? [`discussion_comment: ${commentYamlQuote(commit)}`] : []),
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