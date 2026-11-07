/**
 * @module 04-drafts-parser.js
 * @about   Парсер черновиков.
 * @version 1.0.0
 */

function parseManifestContent(fileName, text, sha) {
  try {
    const yamlMatch = text.match(/^---\s*\r?\n([\s\S]*?)\r?\n---\s*(?:\r?\n|$)/);

    if (!yamlMatch) {
      throw new Error("Не найден Front Matter");
    }

    const meta = {
      id: fileName,
      sha: sha
    };

    yamlMatch[1].split(/\r?\n/).forEach(line => {
      const separator = line.indexOf(":");
      if (separator === -1) return;

      const key = line.substring(0, separator).trim().toLowerCase();
      const value = line.substring(separator + 1)
        .trim()
        .replace(/^["']|["']$/g, "");

      meta[key] = value;
    });

    const body = text.substring(yamlMatch[0].length);
    const titleMatch = body.match(/^##[ \t]+(.+?)[ \t]*#*[ \t]*$/m);

    const articleTitle =
      meta.title ||
      (titleMatch ? titleMatch[1].trim() : "Без заголовка");

    const mediaRegex =
      /^###\s+(.+?)\s*<!--\s*\[блок\s+(фото|видео)\]\s*-->[ \t]*$/gim;

    const matches = [...body.matchAll(mediaRegex)];
    const photos = [];
    const videos = [];

    let photoIndex = 0;
    let videoIndex = 0;

    const cleanBodyText = (
      matches.length
        ? body.substring(0, matches[0].index)
        : body
    )
      .replace(titleMatch ? titleMatch[0] : "", "")
      .replace(/\r\n/g, "\n")
      .replace(/\n{3,}/g, "\n\n")
      .trim();

    matches.forEach((match, position) => {
      const title = match[1].replace(/<!--.*?-->/g, "").trim();

      console.log("[PARSER] Заголовок медиаблока:", {
        rawMatch: match[0],
        capturedTitle: match[1],
        finalTitle: title,
        type: match[2]
      });

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
        title,
        description,
        files
      };

      if (type === "фото") {
        photos.push(block);
      } else {
        videos.push(block);
      }
    });

    return {
      id: fileName,
      sha,
      date: meta.date || "",
      discussion: meta.discussion_number || "",
      commit: meta.discussion_comment || meta.comment_id || "",
      title: articleTitle,
      text: cleanBodyText,
      photos,
      videos,
      timestamp: meta.timestamp || "",
      published: meta.published || "false",
      teacher: meta.teacher || ""
    };

  } catch (error) {
    console.error("[ПАРСЕР] Ошибка:", fileName, error);
    return null;
  }
}
