/**
 * @module journal-attendance.js
 * @about Клиентский скрипт отправки данных Журнала посещений
 * @purpose Сбор отметок посещаемости на сайте и отправка PUT-запросов JSON в репозиторий GitHub
 * @author TechLab
 * @version 1.0.0
 */

// Настройки репозитория и проверка пароля преподавателя
const repo_owner = "eaststandart";
const repo_name = "techlab-journal-attendance";
const allowedTeachers = ["eaststandart", "eastemitting"];

let accessToken = localStorage.getItem("github_journal_token");
let studentsData = {};

// Автоматический вход, если ключ уже сохранен в браузере
document.addEventListener("DOMContentLoaded", () => {
  if (accessToken) {
    showJournal();
  }
});

// Функция проверки введенного пароля
function submitToken() {
  const tokenValue = document.getElementById("token-input").value.trim();
  if (!tokenValue) {
    alert("Пожалуйста, введите ключ доступа!");
    return;
  }

  document.getElementById("btn-login").disabled = true;
  document.getElementById("btn-login").innerText = "Проверка пароля...";

  // Ссылка запроса: https://github.com
  fetch("https://api.github.com/user", {
    headers: { "Authorization": `token ${tokenValue}` }
  })
  .then(response => {
    if (response.ok) {
      localStorage.setItem("github_journal_token", tokenValue);
      accessToken = tokenValue;
      showJournal();
    } else {
      alert("Неверный ключ доступа! Проверьте символы.");
      document.getElementById("btn-login").disabled = false;
      document.getElementById("btn-login").innerText = "🔓 Подключить журнал";
    }
  })
  .catch(err => {
    console.error(err);
    alert("Ошибка сети. Проверьте интернет-соединение.");
    document.getElementById("btn-login").disabled = false;
    document.getElementById("btn-login").innerText = "🔓 Подключить журнал";
  });
}

function showJournal() {
  document.getElementById("auth-section").classList.add("hidden");
  document.getElementById("journal-section").classList.remove("hidden");

  // СКРЫВАЕМ ИНСТРУКЦИЮ ПОСЛЕ УСПЕШНОГО ВХОДА
  const instr = document.getElementById("instructions-section");
  if (instr) instr.classList.add("hidden");

  loadStudentsFromYaml();
}

function logoutTeacher() {
  if (confirm("Вы уверены, что хотите выйти из журнала и сменить ключ доступа?")) {
    localStorage.removeItem("github_journal_token");
    accessToken = null;

    // ПОКАЗЫВАЕМ ИНСТРУКЦИЮ ПРИ ВЫХОДЕ
    const instr = document.getElementById("instructions-section");
    if (instr) instr.classList.remove("hidden");

    window.location.reload();
  }
}

// Чтение базы детей с правильным парсером, два поля ввода и отправка порций
function loadStudentsFromYaml() {
  showNotify("Идентификация пользователя...", "success");
  
  // Сначала узнаем логин учителя, чтобы понять какой личный файл скачивать
  fetch("https://api.github.com/user", {
    headers: { "Authorization": `token ${accessToken}` }
  })
  .then(r => r.json())
  .then(userData => {
    const userLogin = userData.login; // Например, "TechLab"
    localStorage.setItem("github_journal_logged_user", userLogin);
    showNotify(`Загрузка журнала для ${userLogin}...`, "success");
    
    // Динамический адрес личного файла с жестким кэш-брейкером
    const yamlUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/journal-attendance-${userLogin}.yml?nocache=${new Date().getTime()}`;
    return fetch(yamlUrl, {
      headers: { "Authorization": `token ${accessToken}` }
    });
  })
  .then(response => {
    if (!response.ok) throw new Error("Личный файл журнала не найден в папке _data");
    return response.json();
  })
  .then(data => {
    const yamlText = decodeURIComponent(atob(data.content).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    
    studentsData = parseSimpleYaml(yamlText);
    
    // Генерация сетки дней недели + 8-я кнопка ВЫХОД
    const daysContainer = document.getElementById("days-buttons-container");
    daysContainer.innerHTML = "";
    
    const calendarOrder = [
      { key: "понедельник", label: "ПН" },
      { key: "вторник", label: "ВТ" },
      { key: "среда", label: "СР" },
      { key: "четверг", label: "ЧТ" },
      { key: "пятница", label: "ПТ" },
      { key: "суббота", label: "СБ" },
      { key: "воскресенье", label: "ВС" }
    ];
    
    calendarOrder.forEach(dayInfo => {
      const btnId = `btn-day-${dayInfo.key}`;
      const isAvailable = studentsData[dayInfo.key] && Object.keys(studentsData[dayInfo.key]).length > 0;
      const disabledAttr = isAvailable ? "" : "disabled";
      
      // ТОТАЛЬНО ОЧИЩЕНО: Параметр цвета удален, вызываем только имя дня недели
      daysContainer.innerHTML += `
        <button id="${btnId}" class="btn-big btn-day btn-day-transition day-border-${dayInfo.key}" ${disabledAttr} 
                onclick="selectDynamicDay('${dayInfo.key}')">
          ${dayInfo.label}
        </button>`;
    });

    // ДОБАВЛЯЕМ 8-Ю КНОПКУ ВЫХОД С КЛАССОМ btn-logout
    daysContainer.innerHTML += `
      <button class="btn-big btn-day btn-logout" onclick="logoutTeacher()">
        ВЫХОД
      </button>`;

    showNotify("Журнал успешно загружен!", "success");
    setTimeout(() => { document.getElementById("notification").classList.add("hidden"); }, 2000);
  })
  .catch(err => {
    console.error(err);
    
    // ПРОВЕРКА: Извлекаем сохранённый логин и сверяем с белым списком
    const enteredLogin = localStorage.getItem("github_journal_logged_user") || "";
    
    if (allowedTeachers.includes(enteredLogin)) {
      // СИТУАЦИЯ 1: Это наш официальный преподаватель, но у него отсутствует файл базы.
      // Поведение строго как в старом коде: оставляем в журнале и просто пишем ошибку!
      showNotify("Ошибка загрузки личного журнала. Проверьте наличие файла на GitHub.", "error");
    } else {
      // СИТУАЦИЯ 2: Это посторонний человек с левым токеном.
      // Только в этом случае жестко выкидываем на экран ввода ключа и блокируем!
      document.getElementById("auth-section").classList.remove("hidden");
      document.getElementById("journal-section").classList.add("hidden");
      
      const instr = document.getElementById("instructions-section");
      if (instr) instr.classList.remove("hidden");
      
      document.getElementById("btn-login").disabled = false;
      document.getElementById("btn-login").innerText = "🔓 Подключить журнал";
      
      showNotify("❌ Доступ заблокирован. Ваш аккаунт не зарегистрирован в базе преподавателей. Обратитесь к администратору.", "error");
    }
  });
}

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

    // Фиксация выхода из config:, если начался реальный день недели с отступом 0
    if (indent === 0 && cleanText.endsWith(':') && cleanText.toLowerCase() !== 'config:') {
      isInsideConfig = false;
    }

    // =========================================================================
    // 🛑 МНОГОУРОВНЕВЫЙ ЕДИНЫЙ БЛОК ВАЛИДАЦИИ СИНТАКСИСА И СТРУКТУРЫ СТРОКИ
    // =========================================================================
    // Если мы находимся внутри секции config:, проверки синтаксиса расписания полностью игнорируются!
    if (!isInsideConfig) {
      
      // Проверка 1: Несбалансированные или лишние кавычки в строке данных
      const doubleQuotesCount = cleanText.split('"').length - 1;
      const singleQuotesCount = cleanText.split("'").length - 1;
      if (doubleQuotesCount > 2 || singleQuotesCount > 2 || doubleQuotesCount % 2 !== 0 || singleQuotesCount % 2 !== 0) {
        triggerEmergencyBlock(i + 1, cleanText, "обнаружены лишние или несбалансированные кавычки в данных.");
        return {};
      }

      // Проверка 2: Наличие опасных ломающих спецсимволов в строке данных
      const forbiddenChars = ["[", "]", "\\", "=", ";", "/"];
      for (let char of forbiddenChars) {
        if (cleanText.includes(char)) {
          triggerEmergencyBlock(i + 1, cleanText, "обнаружен запрещённый спецсимвол '" + char + "' в структуре данных.");
          return {};
        }
      }

      // Проверка 3: Жесткий контроль формата времени группы (отступ строго 2 пробела)
      if (indent === 2 && cleanText.endsWith(':')) {
        let rawTimeStr = cleanText.slice(0, -1).replace(/"/g, '').replace(/'/g, '').trim();
        if (rawTimeStr.length !== 5 || rawTimeStr.charAt(2) !== ':') {
          triggerEmergencyBlock(i + 1, cleanText, "неверный формат времени группы. Требуется строго стандарт ЧЧ:ММ (например, 10:00).");
          return {};
        }
      }
    }
    
    // =========================================================================
    // 🧱 БЛОК ИСПОЛНИТЕЛЬНОЙ СБОРКИ ОБЪЕКТА (СИНТАКСИС ГАРАНТИРОВАННО ЧИСТ)
    // =========================================================================
    if (!isInsideConfig) {
      // 1. Фиксация дня недели
      if (indent === 0 && cleanText.endsWith(':')) {
        currentDay = cleanText.slice(0, -1).toLowerCase().trim();
        result[currentDay] = {};
      } 
      // 2. Фиксация времени группы
      else if (indent === 2 && cleanText.endsWith(':')) {
        currentGroup = cleanText.slice(0, -1).replace(/"/g, '').replace(/'/g, '').trim();
        result[currentDay][currentGroup] = [];
      } 
      // 3. Извлечение голого имени постоянного ученика
      else if (indent === 4 && cleanText.startsWith('- name:')) {
        let rawName = cleanText.substring(cleanText.indexOf(':') + 1).trim();
        
        if (rawName.startsWith('"') && rawName.endsWith('"')) rawName = rawName.slice(1, -1).trim();
        if (rawName.startsWith("'") && rawName.endsWith("'")) rawName = rawName.slice(1, -1).trim();
        
        const cleanName = rawName.replace(/\s+/g, " ").trim();
        
        if (currentDay && currentGroup && cleanName) {
          result[currentDay][currentGroup].push(cleanName);
        }
      }
    }
  }
  return result;
}

function selectDynamicDay(day) {
  // 1. Сбрасываем CSS-класс active у абсолютно всех кнопок дней
  const allDayButtons = document.querySelectorAll(`[id^="btn-day-"]`);
  allDayButtons.forEach(btn => {
    btn.classList.remove("active");
  });

  // 2. Подсвечиваем выбранную кнопку, добавляя чистый CSS-класс active
  const activeBtn = document.getElementById(`btn-day-${day}`);
  if (activeBtn) {
    activeBtn.classList.add("active");
  }
  
  // 3. Выводим ОДНО ЕДИНСТВЕННОЕ общее поле даты под календарь
  const localToday = new Date();
  const offset = localToday.getTimezoneOffset();
  const correctedDate = new Date(localToday.getTime() - (offset * 60 * 1000));
  const defaultDateStr = correctedDate.toISOString().split('T')[0];

  document.getElementById("global-date-container").innerHTML = `
    📅 Дата проведения занятий: 
    <input type="text" id="global-journal-date" value="${defaultDateStr}" class="global-date-input">
  `;

  // 4. Генерируем группы для выбранного дня недели
  const container = document.getElementById("groups-container");
  container.innerHTML = "";

  if (!studentsData[day] || Object.keys(studentsData[day]).length === 0) {
    container.innerHTML = `<p class="empty-group-msg">В этот день групп нет.</p>`;
    return;
  }

  Object.keys(studentsData[day]).sort().forEach(time => {
    const kids = studentsData[day][time];
    
    // Чистый заголовок группы использует класс макета вместо инлайн-стилей
    let groupHtml = `<div class="group-block" id="block-${time.replace(':', '-')}">
      <div class="group-header-flex">
        <h3 class="group-title-clean">⏰ Группа ${time}</h3>
      </div>`;
    
    kids.forEach((kid, index) => {
      const id = `kid-${time.replace(':', '-')}-${index}`;
      
      // Зряче отсекаем для экрана всё, что идёт после скобок или интернет-тегов
      let displayName = kid;
      const cutIndex = kid.search(/\[|@|#/);
      if (cutIndex !== -1) {
        displayName = kid.substring(0, cutIndex).trim();
      }
      
      groupHtml += `
        <div class="kid-row">
          <label class="lbl-big">
            <input type="checkbox" id="${id}" class="chk-big" value="${kid}">
            ${displayName}
          </label>
        </div>`;
    });

    // Локальный фильтр всеядности времени для вывода идеального текста на саму кнопку занятия
    let matchBtnTime = time.match(/(\d{1,2})\D*(\d{2})/);
    let cleanBtnTextTime = (matchBtnTime && matchBtnTime[1] && matchBtnTime[2]) ? `${matchBtnTime[1]}:${matchBtnTime[2]}` : time;

    // Текстовые блоки разметки переведены на чистые классы отступов и цветов
    groupHtml += `
      <div class="margin-top-15">
        <label class="field-label">➕ Новые постоянные ученики (войдут в базу):</label>
        <input type="text" id="newbies-${time}" class="input-text" placeholder="Имена через запятую">
        
        <label class="field-label-probation">⏳ Временные ученики (только на сегодня):</label>
        <input type="text" id="probation-${time}" class="input-text input-probation" placeholder="Имена через запятую">
      </div>
      <!-- ИСПРАВЛЕНО НАМЕРТВО: Текст кнопки полностью защищен от знаков равенства, дефисов и слэшей! -->
      <button class="btn-big btn-save" id="btn-save-${time.replace(':', '-')}" onclick="saveGroupAttendance('${day}', '${time}')">💾 Отправить группу ${cleanBtnTextTime}</button>
    </div>`;
  
    container.innerHTML += groupHtml;
  });
}

function saveGroupAttendance(day, time) {
  const dateStr = document.getElementById("global-journal-date").value.trim(); 
  const timeId = time.replace(':', '-');

  let presentKids = [];
  const checkboxes = document.querySelectorAll(`[id^="kid-${time.replace(':', '-')}-"]`);
  checkboxes.forEach(chk => {
    if (chk.checked) presentKids.push(chk.value);
  });

  const newbiesInput = document.getElementById(`newbies-${time}`).value.trim();
  const probationInput = document.getElementById(`probation-${time}`).value.trim();

  // Функция-обработчик: выполняет сквозной перевод комбинаций ключей по белому списку
  const convertAndValidateInputs = (inputStr, fieldLabel) => {
    if (!inputStr) return [];
    
    let isErrorFound = false;
    let errorMessage = "";

    const cleanList = inputStr.split(',').map(item => {
      let rawKid = item.trim();
      if (!rawKid) return "";

      // Шаг 1: Приводим множественные пробелы к одному (кавычки, скобки и слэши НЕ ТРОГАЕМ для валидации)
      rawKid = rawKid.replace(/\s+/g, ' ').trim();

      // Шаг 2: ТОТАЛЬНАЯ БЛОКИРОВКА МУСОРА И ЛОЖНЫХ СИМВОЛОВ НА СТАРТЕ
      // 1. Запрет на квадратные скобки [ ], кавычки ' ", обратный слэш \ и точку с запятой ;
      const forbiddenCharsMatch = rawKid.match(/[\[\]'"\\;]/);
      if (forbiddenCharsMatch) {
        isErrorFound = true;
        errorMessage = `В поле "${fieldLabel}" у ученика "${rawKid}" обнаружен запрещённый символ "${forbiddenCharsMatch[0]}". Ввод квадратных скобок, кавычек, обратных слэшей и точек с запятой строго запрещён! Используйте легитимные ключи: /э, /e, /с, /c, /#`;
        return "";
      }

      // 2. Запрет на бесхозные решётки (разрешено только внутри слова #techlab-)
      const badHashes = rawKid.match(/(?<!\/)#(?!techlab-)/g);
      if (badHashes) {
        isErrorFound = true;
        errorMessage = `В поле "${fieldLabel}" у ученика "${rawKid}" обнаружен недопустимый символ "#". Вводить знак решётки без слэша разрешено только внутри системного слова "#techlab-"! Для автогенерации используйте ключ "/#"`;
        return "";
      }

      // 3. Запрет на левые и грязные ключи после слэша (разрешены строго одиночные: /э, /e, /с, /c, /#)
      const slashMatches = rawKid.match((/\/\S*/g));
      if (slashMatches) {
        for (let sMatch of slashMatches) {
          const lowerKey = sMatch.toLowerCase();
          if (lowerKey !== '/э' && lowerKey !== '/e' && lowerKey !== '/с' && lowerKey !== '/c' && lowerKey !== '/#') {
            isErrorFound = true;
            errorMessage = `В поле "${fieldLabel}" обнаружен недопустимый ключ "${sMatch}" у ученика "${rawKid}". Разрешены строго одиночные ключи: /э, /e, /с, /c, /#`;
            return "";
          }
        }
      }

      // Шаг 3: Сквозная последовательная замена легитимных ключей на временные маркеры
      rawKid = rawKid.replace(/\/([eеЕЭ])/g, ' [э]');
      rawKid = rawKid.replace(/\/([cсСC])/g, ' [с]');

      // Шаг 4: Схлопывание дубликатов решёток (если ввели несколько законных /#)
      rawKid = rawKid.replace(/\/#(\s*\/#)+/g, '/#');

      // Шаг 5: ИЗОЛИРОВАНИЕ И ХИРУРГИЧЕСКАЯ СБОРКА СТРОКИ ПО ПРАВИЛУ (Имя ➔ Направление ➔ Тег)
      let directionMarker = "";
      let systemTag = "";
      let hasAutoHash = false;

      // Вытаскиваем маркер направления
      if (rawKid.includes('[э]')) { directionMarker = "[э]"; rawKid = rawKid.replace('[э]', ''); }
      else if (rawKid.includes('[с]')) { directionMarker = "[с]"; rawKid = rawKid.replace('[с]', ''); }

      // Вытаскиваем ключ автогенерации /#
      if (rawKid.includes('/#')) {
        hasAutoHash = true;
        rawKid = rawKid.replace(/\/#/g, '');
      }

      // Вытаскиваем готовые интернет-теги Гитхаба
      const githubLoginMatch = rawKid.match(/@([a-zA-Z0-9_\-]+)/);
      const techlabTagMatch = rawKid.match(/#techlab-([a-zA-Z0-9_\-]+)/);

      if (githubLoginMatch) {
        systemTag = githubLoginMatch[0];
        rawKid = rawKid.replace(githubLoginMatch[0], '');
      } else if (techlabTagMatch) {
        systemTag = techlabTagMatch[0];
        rawKid = rawKid.replace(techlabTagMatch[0], '');
      } else if (hasAutoHash) {
        systemTag = "#";
      }

      // Очищаем оставшееся имя ученика от лишних пробелов
      const cleanName = rawKid.replace(/\s+/g, ' ').trim();

      // АППАРАТНЫЙ ЩИТ: Если имя ученика оказалось пустым после извлечения тегов/ключей — блок ввода!
      if (!cleanName) {
        isErrorFound = true;
        errorMessage = `В поле "${fieldLabel}" обнаружена строка без имени ученика! Ввод одиночных ключей (например, "/#") без указания самого имени строго запрещён.`;
        return "";
      }

      // Собираем идеальную строку строго по цепочке: Имя ➔ Направление ➔ Тег
      let finalRow = cleanName;
      if (directionMarker) finalRow += ` ${directionMarker}`;
      if (systemTag) finalRow += ` ${systemTag}`;

      return finalRow.replace(/\s+/g, ' ').trim();
    }).filter(n => n !== "");

    if (isErrorFound) {
      alert(`⚠️ СБОЙ ВАЛИДАЦИИ:\n${errorMessage}`);
      return null;
    }
    return cleanList;
  };

  // Прогоняем оба поля ввода через наш зрячий валидатор
  let newbiesList = convertAndValidateInputs(newbiesInput, "Новые постоянные ученики");
  if (newbiesList === null) return; // Жестко прерываем отправку формы при ошибке ключа!

  let probationList = convertAndValidateInputs(probationInput, "Временные ученики");
  if (probationList === null) return; // Жестко прерываем отправку формы при ошибке ключа!

  showNotify(`Подготовка отчета для группы ${time}...`, "success");

  // Шаг 1: Узнаем логин преподавателя
  fetch("https://api.github.com/user", {
    headers: { "Authorization": `token ${accessToken}` }
  })
  .then(r => r.json())
  .then(userData => {
    const teacherUsername = userData.name || userData.login || "Преподаватель";
    const teacherLogin = userData.login; // Используем оригинальную переменную логина

    // Функция-трансформатор текстовых строк Журнала в объектный формат JSON
    const objectifyList = (list, isPermanent = false) => {
      return list.map(kidStr => {
        let name = kidStr;
        let direction = "";
        let tag = "";

        // 1. Извлекаем маркер направления
        if (name.includes('[э]')) { 
          direction = "электронное конструирование"; 
          name = name.replace('[э]', ''); 
        } else if (name.includes('[с]')) { 
          direction = "столярное дело"; 
          name = name.replace('[с]', ''); 
        } else if (isPermanent) { 
          // Дефолт-предохранитель для постоянных учеников
          direction = "электронное конструирование"; 
        }

        // 2. Извлекаем интернет-теги
        const parts = name.split(' ');
        for (let p of parts) {
          const trimmedPart = p.trim();
          if (trimmedPart.indexOf('@') === 0 || trimmedPart.indexOf('#techlab-') === 0 || trimmedPart === '#') {
            tag = trimmedPart;
            name = name.replace(tag, '');
            break;
          }
        }

        // 3. Сборка объекта ученика новой эпохи
        let kidObj = {
          name: name.replace(/\s+/g, ' ').trim(),
          direction: direction
        };
        
        // Поле tag добавляется строго при его физическом наличии
        if (tag) {
          kidObj.tag = tag;
        }

        return kidObj;
      });
    };

    // Собираем пакет данных смены
    const currentGroupPayload = {
      date: dateStr,
      day: day,
      time: time,
      teacher_username: teacherUsername,
      teacher_login: teacherLogin,
      present_permanent: presentKids,
      newbies: objectifyList(newbiesList),           // Новички пакуются объектами
      probation: objectifyList(probationList)        // Временные пакуются объектами
    };

    const filePath = `_input/${dateStr}-${timeId}-journal-attendance-${teacherLogin}.json`;
    const targetUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/${filePath}`;

    // АВТОМАТИЧЕСКАЯ ПЕРЕЗАПИСЬ: Сначала проверяем файл на GitHub, чтобы забрать SHA при его наличии
    return fetch(targetUrl, {
      headers: { "Authorization": `token ${accessToken}` }
    })
    .then(checkRes => {
      if (checkRes.ok) {
        // Файл уже существует на сервере! Извлекаем его sha маркера
        return checkRes.json().then(existingFile => existingFile.sha);
      }
      return null; // Файла нет, создаем с чистого листа
    })
    .then(sha => {
      let commitBody = {
        message: `Отчет: группа ${time} (${day}) от ${teacherUsername}`,
        content: btoa(unescape(encodeURIComponent(JSON.stringify(currentGroupPayload, null, 2))))
      };

      // Если маркер sha найден, обязательно прикрепляем его к запросу для перезаписи мусора!
      if (sha) {
        commitBody.sha = sha;
      }

      // Отправляем чистый PUT-запрос (создание или безопасное обновление поверх старого)
      return fetch(targetUrl, {
        method: "PUT",
        headers: {
          "Authorization": `token ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(commitBody)
      });
    });
  })
  .then(response => {
    if (!response.ok) throw new Error("Ошибка записи файла на GitHub");
    return response.json();
  })
  .then(data => {
    showNotify(`Группа ${time} успешно отправлена в общую сборку дня!`, "success");
    
    const block = document.getElementById(`block-${timeId}`);
    block.style.opacity = "0.6";
    const btn = document.getElementById(`btn-save-${timeId}`);
    btn.innerText = `✅ Группа ${time} сохранена`;
    btn.disabled = true;
  })
  .catch(err => {
    console.error(err);
    showNotify("Не удалось сохранить группу. Ошибка синхронизации данных.", "error");
  });
}

function showNotify(text, type) {
  const el = document.getElementById("notification");
  el.classList.remove("hidden", "notify-success", "notify-error");
  el.classList.add(type === "success" ? "notify-success" : "notify-error");
  el.innerText = text;
}

// Финальная двухфайловая функция запуска адресного ремонта расписания преподавателя
function sendTargetedRepairSignal() {
  const btn = document.getElementById("btn-force-repair");
  if (btn) {
    btn.disabled = true;
    btn.innerText = "⏳ Запуск проверки на сервере...";
  }

  const currentTeacher = localStorage.getItem("github_journal_logged_user") || repo_owner;
  
  const statusUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/repair-status.json`;
  const signalUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/signal-repair.json`;

  const statusPayload = { status: "on", timestamp: new Date().toISOString() };
  const statusBody = {
    message: "chore: сброс светофора в положение on [skip ci]",
    content: btoa(unescape(encodeURIComponent(JSON.stringify(statusPayload, null, 2))))
  };

  fetch(statusUrl, { headers: { "Authorization": "token " + accessToken } })
  .then(res => res.ok ? res.json() : null)
  .then(existingStatus => {
    if (existingStatus && existingStatus.sha) statusBody.sha = existingStatus.sha;
    return fetch(statusUrl, {
      method: "PUT",
      headers: { "Authorization": "token " + accessToken, "Content-Type": "application/json" },
      body: JSON.stringify(statusBody)
    });
  })
  .then(res => {
    if (!res.ok) throw new Error("Не удалось сбросить файл статуса");
    
    const signalPayload = { teacher_login: currentTeacher };
    const signalBody = {
      message: "chore: запрос адресного исправления расписания для " + currentTeacher,
      content: btoa(unescape(encodeURIComponent(JSON.stringify(signalPayload, null, 2))))
    };
    
    return fetch(signalUrl, { headers: { "Authorization": "token " + accessToken } })
    .then(r => r.ok ? r.json() : null)
    .then(existingSignal => {
      if (existingSignal && existingSignal.sha) signalBody.sha = existingSignal.sha;
      return fetch(signalUrl, {
        method: "PUT",
        headers: { "Authorization": "token " + accessToken, "Content-Type": "application/json" },
        body: JSON.stringify(signalBody)
      });
    });
  })
  .then(res => {
    if (!res.ok) throw new Error("Ошибка отправки сигнала");
    showNotify("🟢 Запрос отправлен! Сервер выполняет исправление файла расписания...", "success");
    startRepairStatusPolling();
  })
  .catch(err => {
    console.error(err);
    showNotify("❌ Не удалось связаться с сервером.", "error");
    if (btn) {
      btn.disabled = false;
      btn.innerText = "🛠️ Попробуй запустить ремонт снова";
    }
  });
}

// Функция зрячего 5-секундного опроса файла статуса
function startRepairStatusPolling() {
  const btn = document.getElementById("btn-force-repair");
  const statusUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/repair-status.json`;

  const intervalId = setInterval(() => {
    fetch(statusUrl + "?nocache=" + new Date().getTime(), {
      headers: { "Authorization": "token " + accessToken }
    })
    .then(res => {
      if (!res.ok) throw new Error("Ожидание файла...");
      return res.json();
    })
    .then(data => {
      const jsonText = decodeURIComponent(atob(data.content).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      
      const payload = JSON.parse(jsonText);
      if (btn) btn.innerText = "⏳ Сервер обрабатывает файл расписания...";

      if (payload.status === "off") {
        clearInterval(intervalId);
        showNotify("🟢 База данных успешно исправлена сервером!", "success");
        setTimeout(() => { window.location.reload(); }, 2000);
      }
      
      if (payload.status === "error") {
        clearInterval(intervalId);
        showNotify("❌ Ошибка. Исправьте файл расписания вручную.", "error");
        if (btn) {
          btn.disabled = false;
          btn.innerText = "❌ Сбой ремонта. Исправьте вручную";
        }
      }
    })
    .catch(err => { console.warn("Опрос статуса:", err.message); });
  }, 5000);
}

// Единая функция для вывода баннера аварийной блокировки и кнопки ремонта сервера
function triggerEmergencyBlock(lineNum, cleanText, errorDetails) {
  document.getElementById("groups-container").innerHTML = 
    "<div class='notify-error' style='padding:20px; border-radius:6px; margin-top:20px; font-weight:bold; font-size:16px; background-color:#ffeef0; color:#d73a49; border:1px solid #ced4da;'>" +
      "⚠️ АВАРИЙНАЯ БЛОКИРОВКА: КРИТИЧЕСКИЙ СБОЙ СТРУКТУРЫ РАСПИСАНИЯ!<br>" +
      "<span style='font-size:14px; font-weight:normal; margin-top:10px; display:block;'>" +
        "В строке №" + lineNum + " обнаружена ошибка: " + errorDetails + "<br>Проблемный текст базы: <code style='background:#fff; padding:2px 4px; border-radius:4px;'>" + cleanText + "</code>.<br><br>" +
        "<b>Генерация отчетов полностью заблокирована!</b> Вы можете запустить автоматическое исправление на сервере Гитхаб:<br><br>" +
        "<button id='btn-force-repair' class='btn-big btn-save' style='background-color:#d73a49;' onclick='sendTargetedRepairSignal()'>🛠️ Исправить базу данных на сервере</button>" +
      "</span>" +
    "</div>";
  
  const allDayButtons = document.querySelectorAll('[id^="btn-day-"]');
  allDayButtons.forEach(function(btn) { btn.disabled = true; btn.classList.remove("active"); });
  
  showNotify("❌ Обнаружена критическая ошибка синтаксиса в файле!", "error");
}
