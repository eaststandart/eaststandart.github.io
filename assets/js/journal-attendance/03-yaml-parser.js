/**
 * @module  03-yaml-parser.js
 * @about   Разбор и проверка YAML.
 * @purpose Разбор и проверка YAML.
 * @author  TechLab
 * @version 1.0.0
 */

// Объектный парсер YAML с монолитным Блоком Валидации и защитой от секции config
function parseSimpleYaml(text) {
  let result = {};
  let currentDay = "";
  let currentGroup = "";
  let isInsideConfig = false; // Зрячий предохранитель секции конфигурации
  
  const lines = text.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trimEnd();
    
    // Игнорируем законные пустые строки и строки комментариев
    if (!trimmed || trimmed.trim().startsWith('#')) continue;

    // Считаем количество отступов пробелами
    let indent = 0;
    while (indent < line.length && line.charAt(indent) === ' ') {
      indent++;
    }
    const cleanText = trimmed.trim();

    // Перехват входа в секцию конфигурации config:
    if (indent === 0 && cleanText.toLowerCase() === 'config:') {
      isInsideConfig = true;
      continue;
    }

    // Фиксация выхода из config:, если начался реальный день недели (даже со сдвигом пробелов)
    const checkConfigDays = ["понедельник:", "вторник:", "среда:", "четверг:", "пятница:", "суббота:", "воскресенье:"];
    if (checkConfigDays.includes(cleanText.toLowerCase())) {
      isInsideConfig = false;
    }

    // =========================================================================
    // 🛑 МНОГОУРОВНЕВЫЙ ЕДИНЫЙ БЛОК ВАЛИДАЦИИ СИНТАКСИСА И СТРУКТУРЫ СТРОКИ
    // =========================================================================
    // Если мы находимся внутри секции config:, проверки синтаксиса расписания полностью игнорируются!
    if (!isInsideConfig) {

      // ПЕРЕХВАТ ОШИБОК ПРОБЕЛОВ С ВЫДАЧЕЙ СТАТУСА "space"
      if (cleanText.includes("  ") || (cleanText.includes("tag:") && cleanText.replace("tag:", "").trim().includes(" "))) {
        const spaceMsg = "множественные пробелы подряд. Допускается строго один пробел между словами.";
        triggerEmergencyBlock(i + 1, cleanText, spaceMsg, "space", currentDay);
        return {};
      }
      
      // Вызов Единого Монолитного Щита Валидации
      const structureError = validateRawText(cleanText);
      if (structureError) {
        triggerEmergencyBlock(i + 1, cleanText, structureError, "manual", currentDay);
        return {};
      }
      // Упреждающе обновляем имя дня, если прошли строку отступа 0
      const checkDaysInline = ["понедельник:", "вторник:", "среда:", "четверг:", "пятница:", "суббота:", "воскресенье:"];
      if (indent === 0 && checkDaysInline.includes(cleanText.toLowerCase())) {
        currentDay = cleanText.slice(0, -1).toLowerCase().trim();
      }

      // Проверка 3: Всеядный контроль геометрии и формата времени группы при любом количестве пробелов
      const cleanTimeContent = cleanText.replace(/[\"']/g, '').trim().replace(/:\s*$/, '').trim();
      const timeMatch = cleanTimeContent.match(/^(\d{1,2})\s*[:\/ .=–—-]?\s*(\d{2})$/);
      if (cleanText.endsWith(':') && timeMatch) {
        
        // Фильтр геометрии отступов расписания TechLab
        if (indent !== 2) {
          triggerEmergencyBlock(i + 1, cleanText, "сдвиг времени группы! Время группы должно иметь отступ строго 2 пробела (обнаружено: " + indent + " пробелов).", "repair", currentDay);
          return {};
        }

        // Математический фильтр реальности часов и минут
        const h = parseInt(timeMatch[1], 10);
        const m = parseInt(timeMatch[2], 10);
        
        if (isNaN(h) || isNaN(m) || h < 0 || h > 23 || m < 0 || m > 59) {
          triggerEmergencyBlock(i + 1, cleanText, "несуществующее время суток! Часы должны быть от 00 до 23, минуты от 00 до 59 (обнаружено: " + (currentDay || "неизвестный день") + " " + cleanTimeContent + ").", "modify_time", currentDay);
          return {};
        }
      }

    }
    
    // =========================================================================
    // 🧱 БЛОК ИСПОЛНИТЕЛЬНОЙ СБОРКИ ОБЪЕКТА И ГЕОМЕТРИЧЕСКОГО КОНТРОЛЯ
    // =========================================================================
    if (!isInsideConfig) {
      const validYamlDays = ["понедельник:", "вторник:", "среда:", "четверг:", "пятница:", "суббота:", "воскресенье:"];
      const isDayLine = validYamlDays.includes(cleanText.toLowerCase());
      const isTimeLine = cleanText.endsWith(':') && /^(["']?)\d{1,2}\s*[:\/ .=–—-]?\s*\d{2}\1:$/.test(cleanText);

      // 1. Фиксация и тотальный контроль сдвига Дней недели (Строго отступ 0)
      if (isDayLine) {
        if (indent !== 0) {
          triggerEmergencyBlock(i + 1, cleanText, "сдвиг дня недели! Название дня недели обязано стоять в самом начале строки (отступ 0 пробелов).", "repair", currentDay);
          return {};
        }
        currentDay = cleanText.slice(0, -1).toLowerCase().trim();
        result[currentDay] = {};
      } 
      // 2. Фиксация и тотальный контроль сдвига Времени группы (Строго отступ 2)
      else if (isTimeLine) {
        if (indent !== 2) {
          triggerEmergencyBlock(i + 1, cleanText, "сдвиг времени группы! Время группы (например, \"10:00\":) должно иметь отступ строго 2 пробела.", "repair", currentDay);
          return {};
        }
        currentGroup = cleanText.slice(0, -1).replace(/"/g, '').replace(/'/g, '').trim();
        result[currentDay][currentGroup] = [];
      } 
      // 3. Извлечение и тотальный контроль сдвига Имени ученика (Строго отступ 4)
      else if (cleanText.startsWith('- name:')) {
        if (indent !== 4) {
          triggerEmergencyBlock(i + 1, cleanText, "сдвиг строки ученика! Поле '- name:' должно иметь отступ строго 4 пробела.", "repair", currentDay);
          return {};
        }
        let rawName = cleanText.substring(cleanText.indexOf(':') + 1).trim();
        
        if (rawName.startsWith('"') && rawName.endsWith('"')) rawName = rawName.slice(1, -1).trim();
        if (rawName.startsWith("'") && rawName.endsWith("'")) rawName = rawName.slice(1, -1).trim();
      
        if (currentDay && currentGroup && rawName) {
          result[currentDay][currentGroup].push(rawName);
        }
      } 
      // Точечный контроль сдвига параметров ученика direction и tag (Строго отступ 6)
      else if (cleanText.startsWith('direction:') || cleanText.startsWith('tag:')) {
        if (indent !== 6) {
          triggerEmergencyBlock(i + 1, cleanText, `сдвиг параметра ученика! Поле должно иметь отступ строго 6 пробелов.`, "repair", currentDay);
          return {};
        }
      }
    }
  }
  return result;
}
