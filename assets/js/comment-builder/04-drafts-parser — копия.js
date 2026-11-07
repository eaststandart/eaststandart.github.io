/**
 * @module  04-drafts-parser.js
 * @about   Модуль объектного парсинга и валидации структуры черновиков.
 * @purpose Построчный разбор Front Matter и выделение контента медиа-блоков по русским семафорам-маркерам с подробным логированием.
 * @author  TechLab
 * @version 2.1.0
 */

function parseManifestContent(fileName, text, sha) {
  try {
    console.log("[ПАРСЕР] === Старт разбора файла ===", fileName);

    // 1. Отделяем блок Front Matter от тела markdown-статьи
    const yamlMatch = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
    if (!yamlMatch) {
      console.error("[ПАРСЕР] ❌ Критическая ошибка: Не найден Front Matter (шапка ---)");
      return null;
    }

    const yamlBlock = yamlMatch[1];
    const rawBodyText = text.substring(yamlMatch[0].length);
    console.log("[ПАРСЕР] ✅ Шапка YAML и сырое тело успешно разделены");
    
    let meta = { id: fileName, sha: sha };
    
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

    // Всеядные регулярные выражения с поддержкой любых флагов переноса строк
    const photoRegex = /<!--\s*(?:блок|block)-(\d+)-фото[а-я]*?-начало\s*-->([\s\S]*?)<!--\s*(?:блок|block)-\1-фото[а-я]*?-конец\s*-->/gi;
    const videoRegex = /<!--\s*(?:блок|block)-(\d+)-видео[а-я]*?-начало\s*-->([\s\S]*?)<!--\s*(?:блок|block)-\1-видео[а-я]*?-конец\s*-->/gi;

    let match;
    let cleanBodyText = rawBodyText;

    console.log("[ПАРСЕР] Тестируем регулярное выражение фото на сыром тексте...");
    // 3. Вырезаем все блоки ФОТОМАТЕРИАЛОВ
    while ((match = photoRegex.exec(rawBodyText)) !== null) {
      console.log(`[ПАРСЕР] 📸 НАЙДЕН блок фото №${match[1]}! Длина совпадения: ${match[0].length} символов.`);
      
      // ГАРАНТИРОВАННОЕ УДАЛЕНИЕ: Режем текст по точному совпадению, полностью исключая сбои replace
      cleanBodyText = cleanBodyText.split(match[0]).join("");
      
      extractedPhotos.push({
        index: parseInt(match[1], 10),
        rawContent: match[0] // Передаем блок целиком, включая маркеры, для корректной инъекции
      });
    }

    console.log("[ПАРСЕР] Тестируем регулярное выражение видео на сыром тексте...");
    // 4. Вырезаем все блоки ВИДЕОМАТЕРИАЛОВ
    while ((match = videoRegex.exec(rawBodyText)) !== null) {
      console.log(`[ПАРСЕР] 🎥 НАЙДЕН блок видео №${match[1]}! Длина совпадения: ${match[0].length} символов.`);
      
      cleanBodyText = cleanBodyText.split(match[0]).join("");
      
      extractedVideos.push({
        index: parseInt(match[1], 10),
        rawContent: match[0]
      });
    }

    extractedPhotos.sort((a, b) => a.index - b.index);
    extractedVideos.sort((a, b) => a.index - b.index);

    console.log("[ПАРСЕР] Всего успешно вырезано блоков фото:", extractedPhotos.length);
    console.log("[ПАРСЕР] Всего успешно вырезано блоков видео:", extractedVideos.length);
    console.log("[ПАРСЕР] Итоговый очищенный текст Описания Блока 2, подготовленный к выводу:\n", cleanBodyText.trim());

    // 5. Возвращаем структурированный объект данных
    return {
      id: fileName,
      sha: sha,
      date: meta.date || "",
      discussion: meta.discussion_number || "",
      commit: meta.discussion_comment || meta.comment_id || "",
      title: meta.title || "Без заголовка",
      text: cleanBodyText.trim(), 
      photos: extractedPhotos,    
      videos: extractedVideos,    
      timestamp: meta.timestamp || "",
      published: meta.published || "false",
      teacher: meta.teacher || ""
    };
  } catch (e) {
    console.error("[ПАРСЕР] ❌ Критическая ошибка внутри исполняемого контура: ", e);
    return null;
  }
}
