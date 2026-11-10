/**
 * @module  04-drafts-parser.js
 * @about   Модуль разбора структуры черновиков Markdown.
 * @purpose Разбор Front Matter и содержимого Markdown, извлечение полей комментария и медиаблоков.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: parseManifestYaml
// НАЗНАЧЕНИЕ: Разбирает Front Matter и извлекает метаданные комментария.
function parseManifestYaml(text, fileName, sha) {
  const yamlMatch = text.match(/^---\s*\r?\n([\s\S]*?)\r?\n---\s*(?:\r?\n|$)/);

  if (!yamlMatch) {
    throw new Error("Не найден Front Matter");
  }

  const meta = { id: fileName, sha: sha };

  yamlMatch[1].split(/\r?\n/).forEach(line => {
    const separator = line.indexOf(":");
    if (separator === -1) return;

    const key = line.substring(0, separator).trim().toLowerCase();
    const value = line.substring(separator + 1)
      .trim()
      .replace(/^["']|["']$/g, "");

    meta[key] = value;
  });

  return {
    meta,
    body: text.substring(yamlMatch[0].length)
  };
}

// ФУНКЦИЯ: getMarkdownSections
// НАЗНАЧЕНИЕ: Разделяет Markdown-документ на именованные разделы.
function getMarkdownSections(text, level) {
  const regex = new RegExp("^" + "#".repeat(level) + "[ \t]+(.+?)[ \t]*#*[ \t]*$", "gm");
  const matches = [...text.matchAll(regex)];

  return matches.map((match, index) => ({
    title: match[1].trim(),
    content: text.substring(
      match.index + match[0].length,
      index + 1 < matches.length ? matches[index + 1].index : text.length
    ).trim()
  }));
}

// ФУНКЦИЯ: getMarkdownField
// НАЗНАЧЕНИЕ: Извлекает содержимое указанного поля Markdown.
function getMarkdownField(content, fieldName) {
  const lines = content.split(/\r?\n/);
  const marker = "### " + fieldName;
  const startIndex = lines.findIndex(line => line.trim() === marker);

  if (startIndex === -1) return "";

  const knownFields = [
    "### Заголовок комментария",
    "### Основной текст",
    "### Подвал комментария",
    "### Заголовок блока",
    "### Описание блока",
    "### Медиафайлы"
  ];

  let endIndex = lines.length;

  for (let index = startIndex + 1; index < lines.length; index++) {
    if (knownFields.includes(lines[index].trim())) {
      endIndex = index;
      break;
    }
  }

  return lines.slice(startIndex + 1, endIndex).join("\n").trim();
}
// ФУНКЦИЯ: parseNewManifestBody
// НАЗНАЧЕНИЕ: Разбирает тело комментария в новой структуре Markdown.
function parseNewManifestBody(body) {
  const sections = getMarkdownSections(body, 2);
  const mainSection = sections.find(section => section.title === "Структура комментария");
  const hasMediaSections = sections.some(section =>
    section.title === "📸 Фотоматериалы" || section.title === "🎥 Видеоматериалы"
  );

  if (!mainSection && !hasMediaSections) return null;

  const title = mainSection
    ? getMarkdownField(mainSection.content, "Заголовок комментария")
    : "";
  const mainText = mainSection
    ? getMarkdownField(mainSection.content, "Основной текст")
    : "";
  const footer = mainSection
    ? getMarkdownField(mainSection.content, "Подвал комментария")
    : "";

  const photos = [];
  const videos = [];

  sections.forEach(section => {
    const normalizedType = section.title.replace(/\s+/g, " ").trim();
    let type = null;

    if (normalizedType === "📸 Фотоматериалы") type = "photo";
    if (normalizedType === "🎥 Видеоматериалы") type = "video";
    if (!type) return;

    const blockTitle = getMarkdownField(section.content, "Заголовок блока");
    const description = getMarkdownField(section.content, "Описание блока");

    const mediaExtensions = type === "photo"
      ? /\.(jpg|jpeg|png|webp)$/i
      : /\.(mp4|webm)$/i;

    const files = [];
    const displayNames = [];
    const embedFlags = [];

    // Формат Obsidian: поддерживаем embed ![[...]] и обычную ссылку [[...]].
    for (const match of section.content.matchAll(/(!?)\[\[([^\]]+)\]\]/g)) {
      const fileName = match[2].split("|")[0].trim();
      if (!mediaExtensions.test(fileName)) continue;
      files.push(fileName);
      displayNames.push("");
      embedFlags.push(match[1] === "!");
    }

    // Стандартный Markdown: поддерживаем ссылки с ! и без него.
    for (const match of section.content.matchAll(/(!?)\[([^\]]*)\]\(([^)]+)\)/g)) {
      const embed = match[1] === "!";
      const displayName = match[2].trim();
      let fileName = match[3].trim();

      if (fileName.startsWith("<") && fileName.endsWith(">")) {
        fileName = fileName.slice(1, -1);
      }

      // В манифесте ожидаются локальные имена файлов, а не внешние URL.
      if (/^[a-z][a-z0-9+.-]*:/i.test(fileName) || fileName.startsWith("//")) continue;
      if (!mediaExtensions.test(fileName)) continue;

      files.push(fileName);
      displayNames.push(displayName);
      embedFlags.push(embed);
    }

    const target = type === "photo" ? photos : videos;
    target.push({
      index: target.length + 1,
      title: blockTitle,
      description,
      files,
      displayNames,
      embedFlags
    });
  });

  return { title, text: mainText, footer, photos, videos };
}

// ФУНКЦИЯ: parseManifestContent
// НАЗНАЧЕНИЕ: Формирует объект черновика из имени файла и содержимого Markdown.
function parseManifestContent(fileName, text, sha) {
  try {
    const parsed = parseManifestYaml(text, fileName, sha);
    const meta = parsed.meta;
    const body = parsed.body;

    const content = parseNewManifestBody(body);
    if (!content) {
      throw new Error("Неподдерживаемая структура черновика");
    }

    // YAML title остаётся совместимым с существующей логикой черновиков.
    // Если он отсутствует, используем заголовок из Markdown.
    const articleTitle = meta.title !== undefined
      ? meta.title
      : content.title;

    return {
      id: fileName,
      sha,
      date: meta.date || "",
      discussion: meta.discussion_number || "",
      commit: meta.discussion_comment || meta.comment_id || "",
      title: articleTitle,
      text: content.text,
      footer: content.footer,
      structured: true,
      photos: content.photos,
      videos: content.videos,
      timestamp: meta.timestamp || "",
      published: meta.published || "false",
      publishAsBot: String(meta.publish_as_bot || "false").toLowerCase() === "true",
      teacher: meta.teacher || ""
    };
  } catch (error) {
    console.error("[ПАРСЕР] Ошибка:", fileName, error);
    return null;
  }
}
