
/**
 * @module 04-drafts-parser.js
 * @about   Парсер и валидатор структуры черновиков.
 * @purpose Извлечение заголовка, основного текста, фотоблоков и видеоблоков.
 * @author  TechLab
 * @version 1.1.0
 */

function parseManifestContent(fileName, text, sha) {
  try {
    console.log("[ПАРСЕР] Начало разбора:", fileName);

    // 1. Извлекаем Front Matter
    const yamlMatch = text.match(
      /^---\s*\r?\n([\s\S]*?)\r?\n---\s*(?:\r?\n|$)/
    );

    if (!yamlMatch) {
      throw new Error("Не найден Front Matter");
    }

    const yamlBlock = yamlMatch[1];
    let body = text.substring(yamlMatch[0].length);

    const meta = {
      id: fileName,
      sha: sha
    };

    yamlBlock.split(/\r?\n/).forEach(line => {
      const separator = line.indexOf(":");

      if (separator === -1) return;

      const key = line.substring(0, separator).trim().toLowerCase();
      const value = line
        .substring(separator + 1)
        .trim()
        .replace(/^["']|["']$/g, "");

      meta[key] = value;
    });

    // 2. Извлекаем заголовок статьи
    const titleMatch = body.match(/^##\s+(.+?)\s*#*\s*$/m);

    const articleTitle = titleMatch
      ? titleMatch[1].trim()
      : (meta.title || "Без заголовка");

    if (titleMatch) {
      body = body.replace(titleMatch[0], "");
    }

    // 3. Извлекаем основной текст
    const mainRegex =
      /<!--\s*main-start\s*-->([\s\S]*?)<!--\s*main-end\s*-->/i;

    const mainMatch = body.match(mainRegex);

    if (!mainMatch) {
      throw new Error(
        "Не найдены маркеры основного текста main-start / main-end"
      );
    }

    const cleanBodyText = mainMatch[1].trim();

    body = body.replace(mainRegex, "");

    // 4. Извлекаем фотоблоки и видеоблоки
    const extractedPhotos = [];
    const extractedVideos = [];

    const mediaRegex =
      /<!--\s*media-(photo|video)-(\d+)-start\s*-->([\s\S]*?)<!--\s*media-(photo|video)-(\d+)-end\s*-->/gi;

    let match;

    while ((match = mediaRegex.exec(body)) !== null) {
      const type = match[1].toLowerCase();
      const index = parseInt(match[2], 10);
      const content = match[3].trim();

      const endType = match[4].toLowerCase();
      const endIndex = parseInt(match[5], 10);

      // Проверяем соответствие открывающего и закрывающего маркеров
      if (type !== endType || index !== endIndex) {
        throw new Error(
          `Несоответствие маркеров медиаблока: ${type}-${index}`
        );
      }

      // Извлекаем заголовок блока
      const headingMatch = content.match(/^#{1,6}\s+(.+)$/m);

      const title = headingMatch
        ? headingMatch[1].trim()
        : (type === "photo" ? "Фотоматериалы" : "Видеоматериалы");

      // Извлекаем Obsidian-вложения
      const fileMatches = [...content.matchAll(/!\[\[([^\]]+)\]\]/g)];

      const files = fileMatches.map(fileMatch => {
        return fileMatch[1].split("|")[0].trim();
      });

      // Формируем описание без заголовка и вложений
      let description = content;

      if (headingMatch) {
        description = description.replace(headingMatch[0], "");
      }

      description = description
        .replace(/!\[\[[^\]]+\]\]/g, "")
        .replace(/!\[[^\]]*\]\([^)]*\)/g, "")
        .trim();

      const block = {
        index,
        title,
        description,
        files,
        rawContent: match[0]
      };

      if (type === "photo") {
        extractedPhotos.push(block);
      } else {
        extractedVideos.push(block);
      }

      console.log(
        `[ПАРСЕР] Найден блок ${type} №${index}:`,
        files.length,
        "файлов"
      );
    }

    // 5. Проверяем, не остались ли необработанные маркеры
    const remainingMarkers = body.match(
      /<!--\s*media-(?:photo|video)-\d+-(?:start|end)\s*-->/gi
    );

    if (remainingMarkers) {
      throw new Error(
        "Обнаружены незакрытые или некорректные маркеры медиаблоков: " +
        remainingMarkers.join(", ")
      );
    }

    // 6. Сортируем блоки по номерам
    extractedPhotos.sort((a, b) => a.index - b.index);
    extractedVideos.sort((a, b) => a.index - b.index);

    // 7. Выводим результаты
    console.log("[ПАРСЕР] Заголовок:", articleTitle);
    console.log("[ПАРСЕР] Основной текст:", cleanBodyText);
    console.log("[ПАРСЕР] Фото:", extractedPhotos);
    console.log("[ПАРСЕР] Видео:", extractedVideos);

    // 8. Возвращаем объект черновика
    return {
      id: fileName,
      sha: sha,
      date: meta.date || "",
      discussion: meta.discussion_number || "",
      commit: meta.discussion_comment || meta.comment_id || "",
      title: articleTitle,
      text: cleanBodyText,
      photos: extractedPhotos,
      videos: extractedVideos,
      timestamp: meta.timestamp || "",
      published: meta.published || "false",
      teacher: meta.teacher || ""
    };

  } catch (e) {
    console.error("[ПАРСЕР] Ошибка разбора:", fileName, e);
    return null;
  }
}
