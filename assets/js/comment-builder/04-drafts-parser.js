/**
 * @module  04-drafts-parser.js
 * @about   Модуль объектного парсинга и валидации структуры черновиков.
 * @purpose Построчный разбор Front Matter и выделение контента медиа-блоков по русским семафорам-маркерам.
 * @author  TechLab
 * @version 1.0.0
 */

/**
 * Изолированный разбор контента .md черновика.
 * Вызывается строго из модуля 03-drafts-loader.js при обработке потока API.
 */
function parseManifestContent(fileName, text, sha) {
  try {
    // 1. Отделяем блок Front Matter от тела markdown-статьи
    const yamlMatch = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
    if (!yamlMatch) return null;

    const yamlBlock = yamlMatch[1];
    const rawBodyText = text.substring(yamlMatch[0].length);
    
    let meta = { id: fileName, sha: sha };
    
    // Построчно парсим параметры YAML-шапки
    yamlBlock.split('\n').forEach(line => {
      if (line.includes(':')) {
        const parts = line.split(':');
        const key = parts[0].trim().toLowerCase();
        const value = parts.slice(1).join(':').trim().replace(/^["']|["']$/g, '');
        meta[key] = value;
      }
    });

    // 2. Инициализируем массивы под извлекаемые динамические блоки
    let extractedPhotos = [];
    let extractedVideos = [];

    // Регулярные выражения сквозного поиска контента внутри русских семафоров блоков
    const photoRegex = /<!--\s*блок-(\d+)-фотоматериалы-начало\s*-->([\s\S]*?)<!--\s*блок-\1-фотоматериалы-конец\s*-->/g;
    const videoRegex = /<!--\s*блок-(\d+)-видеоматериалы-начало\s*-->([\s\S]*?)<!--\s*блок-\1-видеоматериалы-конец\s*-->/g;

    let match;
    let cleanBodyText = rawBodyText;

    // 3. Вырезаем все блоки ФОТОМАТЕРИАЛОВ из основного текста
    while ((match = photoRegex.exec(rawBodyText)) !== null) {
      const blockIndex = match[1];
      const blockContent = match[2];
      
      // Удаляем этот кусок из основного текста отчета, чтобы он не дублировался в описании
      cleanBodyText = cleanBodyText.replace(match[0], "");
      
      extractedPhotos.push({
        index: parseInt(blockIndex, 10),
        rawContent: blockContent
      });
    }

    // 4. Вырезаем все блоки ВИДЕОМАТЕРИАЛОВ из основного текста
    while ((match = videoRegex.exec(rawBodyText)) !== null) {
      const blockIndex = match[1];
      const blockContent = match[2];
      
      cleanBodyText = cleanBodyText.replace(match[0], "");
      
      extractedVideos.push({
        index: parseInt(blockIndex, 10),
        rawContent: blockContent
      });
    }

    // Сортируем массивы блоков строго по возрастанию их порядковых индексов (1, 2, 3...)
    extractedPhotos.sort((a, b) => a.index - b.index);
    extractedVideos.sort((a, b) => a.index - b.index);

    // 5. Возвращаем детерминированный структурированный объект данных
    return {
      id: fileName,
      sha: sha,
      date: meta.date || "",
      discussion: meta.discussion_number || "",
      commit: meta.discussion_comment || meta.comment_id || "",
      title: meta.title || "Без заголовка",
      text: cleanBodyText.trim(), // Сюда уходит чистый остаток текста Блока 2 без разметки медиа
      photos: extractedPhotos,    // Изолированный массив блоков фото
      videos: extractedVideos,    // Изолированный массив блоков видео
      timestamp: meta.timestamp || "",
      published: meta.published || "false",
      teacher: meta.teacher || ""
    };
  } catch (e) {
    console.error("[ПАРСЕР] ⚠️ Ошибка регулярного разбора Front Matter черновика: ", e);
    return null;
  }
}
