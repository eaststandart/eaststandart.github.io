/**
 * @module  07-validation.js
 * @about   Модуль контроля безопасности строк.
 * @purpose Проверка баланса кавычек и блокировка опасных ломающих спецсимволов в полях ручного ввода.
 * @author  TechLab
 * @version 1.0.0
 */

// Возвращает текст ошибки, если найден брак, или null, если строка чиста
function validateRawText(cleanText) {
  // 1. Проверка на несбалансированные или лишние кавычки
  const doubleQuotesCount = cleanText.split('"').length - 1;
  const singleQuotesCount = cleanText.split("'").length - 1;
  if (doubleQuotesCount > 2 || singleQuotesCount > 2 || doubleQuotesCount % 2 !== 0 || singleQuotesCount % 2 !== 0) {
    return "обнаружены лишние или несбалансированные кавычки.";
  }

  // 2. Проверка на опасные ломающие спецсимволы
  const forbiddenChars = ["[", "]", "\\", "=", ";"];
  for (let char of forbiddenChars) {
    if (cleanText.includes(char)) {
      return "обнаружен запрещённый спецсимвол '" + char + "'.";
    }
  }

  return null; // Строка полностью соответствует стандарту безопасности
}
