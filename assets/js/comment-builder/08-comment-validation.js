/**
 * @module  06-comment-validation.js
 * @about   Модуль проверки пользовательского текста.
 * @purpose Проверка текста комментария и медиаблоков перед сохранением.
 * @author  TechLab
 * @version 1.0.0
 */

// ЕДИНЫЕ НАСТРОЙКИ ОГРАНИЧЕНИЙ ДЛИНЫ ТЕКСТА.
window.COMMENT_TEXT_LIMITS = Object.freeze({
  block2Title: 50,
  block2Description: 1000,
  mediaTitle: 50,
  mediaDescription: 500
});

// ФУНКЦИЯ: countVisibleCharacters
// НАЗНАЧЕНИЕ: Считает видимые символы, включая составные эмодзи, как один символ.
function countVisibleCharacters(value) {
  const text = String(value ?? "");

  if (typeof Intl.Segmenter === "function") {
    const segmenter = new Intl.Segmenter("ru", { granularity: "grapheme" });
    return Array.from(segmenter.segment(text)).length;
  }

  return Array.from(text).length;
}

// ФУНКЦИЯ: validateCommentText
// НАЗНАЧЕНИЕ: Проверяет текст на управляющие символы и установленное ограничение длины.
function validateCommentText(value, fieldName, maxLength = null) {
  const text = String(value ?? "");

  // Разрешены табуляция и переносы строк. Остальные управляющие символы запрещены.
  if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F]/.test(text)) {
    return `Поле «${fieldName}» содержит недопустимые управляющие символы.`;
  }

  if (maxLength !== null && countVisibleCharacters(text) > maxLength) {
    return `Поле «${fieldName}»: не более ${maxLength} символов.`;
  }

  return null;
}

// Не допускаем ввод, превышающий лимит. Вставка и замена выделенного текста учитываются.
document.addEventListener("beforeinput", event => {
  const field = event.target;
  const limitType = field?.dataset?.limitType;
  const maxLength = window.COMMENT_TEXT_LIMITS[limitType];

  if (!maxLength || event.isComposing || !event.inputType?.startsWith("insert")) return;

  let insertedText = event.data;

  if (insertedText === null && event.dataTransfer) {
    insertedText = event.dataTransfer.getData("text/plain");
  }

  // Если браузер не предоставляет вставляемый текст, окончательная проверка сработает при сохранении.
  if (typeof insertedText !== "string") return;

  const start = field.selectionStart ?? field.value.length;
  const end = field.selectionEnd ?? start;
  const nextValue =
    field.value.slice(0, start) + insertedText + field.value.slice(end);

  if (countVisibleCharacters(nextValue) > maxLength) {
    event.preventDefault();
  }
});

// ФУНКЦИЯ: validateCommentForm
// НАЗНАЧЕНИЕ: Проверяет все текстовые поля формы перед загрузкой файлов и сохранением.
function validateCommentForm() {
  const fields = [
    { selector: "#post-title", name: "Заголовок комментария" },
    { selector: "#post-text", name: "Основной текст" },
    { selector: "#post-footer", name: "Подвал комментария" }
  ];

  for (const fieldInfo of fields) {
    const field = document.querySelector(fieldInfo.selector);
    if (!field) continue;

    const error = validateCommentText(field.value, fieldInfo.name);
    if (error) return error;
  }

  const block2Fields = [
    { selector: "#post-title", name: "Заголовок комментария" },
    { selector: "#post-text", name: "Описание комментария" }
  ];

  for (const fieldInfo of block2Fields) {
    const field = document.querySelector(fieldInfo.selector);
    if (!field) continue;

    const error = validateCommentText(
      field.value,
      fieldInfo.name,
      window.COMMENT_TEXT_LIMITS[field.dataset.limitType]
    );
    if (error) return error;
  }

  const mediaFields = [
    { selector: ".photo-h3-title, .video-h3-title", name: "Заголовок медиаблока", limitType: "mediaTitle" },
    { selector: ".photo-block-desc, .video-block-desc", name: "Описание медиаблока", limitType: "mediaDescription" }
  ];

  for (const fieldInfo of mediaFields) {
    const fields = document.querySelectorAll(fieldInfo.selector);

    for (const field of fields) {
      if (field.disabled) continue;

      const error = validateCommentText(
        field.value,
        fieldInfo.name,
        window.COMMENT_TEXT_LIMITS[fieldInfo.limitType]
      );

      if (error) return error;
    }
  }

  return null;
}
