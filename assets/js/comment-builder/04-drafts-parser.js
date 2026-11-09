/**
 * @module 04-drafts-parser.js
 * @about   Парсер черновиков новой структуры Markdown.
 * @version 2.0.0
 */

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

function getMarkdownField(content, fieldName) {
  const fields = getMarkdownSections(content, 3);
  const field = fields.find(item => item.title === fieldName);
  return field ? field.content.trim() : "";
}

function parseNewManifestBody(body) {
  const sections = getMarkdownSections(body, 2);
  const mainSection = sections.find(section => section.title === "Структура комментария");

  if (!mainSection) return null;

  const title = getMarkdownField(mainSection.content, "Заголовок комментария");
  const mainText = getMarkdownField(mainSection.content, "Основной текст");
  const footer = getMarkdownField(mainSection.content, "Подвал комментария");

  const photos = [];
  const videos = [];

  sections.forEach(section => {
    const normalizedType = section.title.replace(/\s+/g, " ").trim();
    let type = null;

    if (normalizedType === "📸 Фотоматериалы") type = "photo";
    if (normalizedType === "🎥 Видеоматериалы") type = "video";
    if (!type) return;

    const fields = getMarkdownSections(section.content, 3);
    const blockTitle = fields.length ? fields[0].title : "";
    const blockContent = fields.length ? fields[0].content : section.content;

    const files = [...blockContent.matchAll(/!\[\[([^\]]+)\]\]/g)]
      .map(file => file[1].split("|")[0].trim());

    const description = blockContent
      .replace(/!\[\[[^\]]+\]\]/g, "")
      .replace(/!\[[^\]]*\]\([^)]*\)/g, "")
      .trim();

    const target = type === "photo" ? photos : videos;
    target.push({
      index: target.length + 1,
      title: blockTitle,
      description,
      files
    });
  });

  return { title, text: mainText, footer, photos, videos };
}

function parseLegacyManifestBody(body) {
  const titleMatch = body.match(/^##[ \t]+(.+?)[ \t]*#*[ \t]*$/m);

  const mediaRegex =
    /^###\s+(.+?)\s*<!--\s*\[блок\s+(фото|видео)\]\s*-->[ \t]*$/gim;

  const matches = [...body.matchAll(mediaRegex)];
  const photos = [];
  const videos = [];

  let photoIndex = 0;
  let videoIndex = 0;

  const cleanBodyText = (
    matches.length ? body.substring(0, matches[0].index) : body
  )
    .replace(titleMatch ? titleMatch[0] : "", "")
    .replace(/\r\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();

  matches.forEach((match, position) => {
    const type = match[2].toLowerCase();
    const contentStart = match.index + match[0].length;
    const contentEnd = position + 1 < matches.length
      ? matches[position + 1].index
      : body.length;
    const content = body.substring(contentStart, contentEnd).trim();

    const files = [...content.matchAll(/!\[\[([^\]]+)\]\]/g)]
      .map(file => file[1].split("|")[0].trim());

    const description = content
      .replace(/!\[\[[^\]]+\]\]/g, "")
      .replace(/!\[[^\]]*\]\([^)]*\)/g, "")
      .trim();

    const index = type === "фото" ? ++photoIndex : ++videoIndex;
    const block = {
      index,
      title: match[1].replace(/<!--.*?-->/g, "").trim(),
      description,
      files
    };

    if (type === "фото") photos.push(block);
    else videos.push(block);
  });

  return {
    title: titleMatch ? titleMatch[1].trim() : "",
    text: cleanBodyText,
    footer: "",
    photos,
    videos
  };
}

function parseManifestContent(fileName, text, sha) {
  try {
    const parsed = parseManifestYaml(text, fileName, sha);
    const meta = parsed.meta;
    const body = parsed.body;

    const newContent = parseNewManifestBody(body);
    const content = newContent || parseLegacyManifestBody(body);

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
      structured: Boolean(newContent),
      photos: content.photos,
      videos: content.videos,
      timestamp: meta.timestamp || "",
      published: meta.published || "false",
      teacher: meta.teacher || ""
    };
  } catch (error) {
    console.error("[ПАРСЕР] Ошибка:", fileName, error);
    return null;
  }
}
