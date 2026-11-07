/**
 * @module  04-drafts-parser.js
 * @about   Модуль объектного парсинга и валидации структуры черновиков.
 * @purpose Построчный разбор Front Matter и подготовка текстовых массивов для инъекции.
 * @author  TechLab
 * @version 1.0.0
 */

/**
 * Изолированный разбор контента .md черновика для извлечения Front Matter
 * Вызывается строго из модуля 03-drafts-loader.js при обработке потока API.
 */
function parseManifestContent(fileName, text, sha) {
  try {
    const yamlMatch = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
    if (!yamlMatch) return null;

    const yamlBlock = yamlMatch[1];
    // Извлекаем остаток тела строго со следующего символа после закрывающих дефисов шапки
    const rawBodyText = text.substring(yamlMatch[0].length);
    
    let meta = { id: fileName, sha: sha };
    
    // Построчно вытаскиваем ключевые YAML параметры
    yamlBlock.split('\n').forEach(line => {
      if (line.includes(':')) {
        const parts = line.split(':');
        const key = parts[0].trim().toLowerCase();
        // Склеиваем обратно значение на случай, если внутри текста тоже были двоеточия
        const value = parts.slice(1).join(':').trim().replace(/^["']|["']$/g, '');
        meta[key] = value;
      }
    });

    // Возвращаем детерминированный плоский объект данных
    return {
      id: fileName,
      sha: sha,
      date: meta.date || "",
      discussion: meta.discussion_number || "",
      commit: meta.discussion_comment || meta.comment_id || "",
      title: meta.title || "Без заголовка",
      text: rawBodyText, // Чистый остаток markdown-тела для инжектора блоков
      timestamp: meta.timestamp || "",
      published: meta.published || "false",
      teacher: meta.teacher || ""
    };
  } catch (e) {
    console.error("[ПАРСЕР] ⚠️ Ошибка регулярного разбора Front Matter черновика: ", e);
    return null;
  }
}
