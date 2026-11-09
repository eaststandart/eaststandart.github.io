/**
 * @module  06-comment-validation.js
 * @about   Модуль проверки пользовательского текста.
 * @purpose Проверка текста комментария и медиаблоков перед сохранением.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: validateCommentText
// НАЗНАЧЕНИЕ: Проверяет текст на управляющие символы и установленное ограничение длины.
function validateCommentText(value, fieldName, maxLength = null) {
  const text = String(value ?? "");

  // Разрешены табуляция и переносы строк. Остальные управляющие символы запрещены.
  if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F]/.test(text)) {
    return `Поле «${fieldName}» содержит недопустимые управляющие символы.`;
  }

  if (maxLength !== null && text.length > maxLength) {
    return `Поле «${fieldName}»: не более ${maxLength} символов.`;
  }

  return null;
}

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

  const mediaFields = [
    { selector: ".photo-h3-title", name: "Заголовок фотоблока", maxLength: 50 },
    { selector: ".photo-block-desc", name: "Описание фотоблока", maxLength: 500 },
    { selector: ".video-h3-title", name: "Заголовок видеоблока", maxLength: 50 },
    { selector: ".video-block-desc", name: "Описание видеоблока", maxLength: 500 }
  ];

  for (const fieldInfo of mediaFields) {
    const fields = document.querySelectorAll(fieldInfo.selector);

    for (const field of fields) {
      if (field.disabled) continue;

      const error = validateCommentText(
        field.value,
        fieldInfo.name,
        fieldInfo.maxLength
      );

      if (error) return error;
    }
  }

  return null;
}
