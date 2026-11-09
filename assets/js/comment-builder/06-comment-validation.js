/**
 * @module  06-comment-validation.js
 * @about   Модуль проверки пользовательского текста.
 * @purpose Проверка вводимых строк на недопустимые символы и конструкции, способные нарушить структуру данных.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: validateRawText
// НАЗНАЧЕНИЕ: Возвращает текст ошибки, если найден брак, или null, если строка чиста (1 в 1 из Журнала)
function validateRawText(cleanText) {
  // 1. Проверка на несбалансированные или лишние кавычки
  const doubleQuotesCount = cleanText.split('"').length - 1;
  const singleQuotesCount = cleanText.split("'").length - 1;
  if (doubleQuotesCount > 2 || singleQuotesCount > 2 || doubleQuotesCount % 2 !== 0 || singleQuotesCount % 2 !== 0) {
    return "обнаружены лишние или несбалансированные кавычки.";
  }

  // 2. Проверка на опасные ломающие спецсимволы (1 в 1 из Журнала, кроме квадратных скобок)
  const forbiddenChars = ["\\", "=", ";"];
  for (let char of forbiddenChars) {
    if (cleanText.includes(char)) {
      return "обнаружен запрещённый спецсимвол '" + char + "'.";
    }
  }

  return null; // Строка полностью соответствует стандарту безопасности
}
