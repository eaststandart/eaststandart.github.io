/**
 * @module journal-attendance.js
 * @about Клиентский скрипт отправки данных Журнала посещений
 * @purpose Сбор отметок посещаемости на сайте и отправка PUT-запросов JSON в репозиторий GitHub
 * @author TechLab
 * @version 10.0.0
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

  const instr = document.getElementById("instructions-section");
  if (instr) instr.classList.add("hidden");

  loadStudentsFromYaml();
}

function logoutTeacher() {
  if (confirm("Вы уверены, что хотите выйти из журнала и сменить ключ доступа?")) {
    localStorage.removeItem("github_journal_token");
    accessToken = null;

    const instr = document.getElementById("instructions-section");
    if (instr) instr.classList.remove("hidden");

    window.location.reload();
  }
}

// Чтение базы детей с правильным парсером, два поля ввода и отправка порций
function loadStudentsFromYaml() {
  showNotify("Идентификация пользователя...", "success");
  
  fetch("https://api.github.com/user", {
    headers: { "Authorization": `token ${accessToken}` }
  })
  .then(r => r.json())
  .then(userData => {
    const userLogin = userData.login;
    localStorage.setItem("github_journal_logged_user", userLogin);
    showNotify(`Загрузка журнала для ${userLogin}...`, "success");
    
    return fetch(`https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/journal-attendance-${userLogin}.yml`, {
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
      
      daysContainer.innerHTML += `
        <button id="${btnId}" class="btn-big btn-day btn-day-transition day-border-${dayInfo.key}" ${disabledAttr} 
                onclick="selectDynamicDay('${dayInfo.key}')">
          ${dayInfo.label}
        </button>`;
    });

    daysContainer.innerHTML += `
      <button class="btn-big btn-day btn-logout" onclick="logoutTeacher()">
        ВЫХОД
      </button>`;

    showNotify("Журнал успешно загружен!", "success");
    setTimeout(() => { document.getElementById("notification").classList.add("hidden"); }, 2000);
  })
  .catch(err => {
    console.error(err);
    const enteredLogin = localStorage.getItem("github_journal_logged_user") || "";
    
    if (allowedTeachers.includes(enteredLogin)) {
      showNotify("Ошибка загрузки личного журнала. Проверьте наличие файла на GitHub.", "error");
    } else {
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

// Обновленный объектный парсер YAML под новую древовидную структуру базы расписания
function parseSimpleYaml(text) {
  let result = {};
  let currentDay = "";
  let currentGroup = "";
  let currentKidObj = null;
  
  const lines = text.split('\n');

  lines.forEach(line => {
    const trimmed = line.trimEnd();
    if (!trimmed || trimmed.startsWith('#')) return;

    const indent = line.search(/\S/);
    const cleanText = trimmed.trim();
    
    if (indent === 0 && cleanText.endsWith(':')) {
      currentDay = cleanText.slice(0, -1).toLowerCase().trim();
      result[currentDay] = {};
    } 
   else if (indent === 2 && cleanText.endsWith(':')) {
     // Просто забираем чистое время из строки YAML без ломающихся матчей
     currentGroup = cleanText.slice(0, -1).replace(/"/g, '').replace(/'/g, '').trim();
     result[currentDay][currentGroup] = [];
   }
    // Считывание начала объекта ученика (- name:)
    else if (indent === 4 && cleanText.startsWith('- name:')) {
      let rawName = cleanText.substring(cleanText.indexOf(':') + 1).trim();
      if (rawName.startsWith('"') && rawName.endsWith('"')) rawName = rawName.slice(1, -1).trim();
      if (rawName.startsWith("'") && rawName.endsWith("'")) rawName = rawName.slice(1, -1).trim();
      
      currentKidObj = {
        name: rawName.replace(/\s+/g, " ").trim(),
        direction: "",
        tag: ""
      };
      
      if (currentDay && currentGroup && currentKidObj.name) {
        result[currentDay][currentGroup].push(currentKidObj);
      }
    }
    // Считывание полей direction и tag внутри объекта ученика
    else if (indent === 6 && currentKidObj) {
      const colonIndex = cleanText.indexOf(':');
      if (colonIndex !== -1) {
        const key = cleanText.substring(0, colonIndex).trim().toLowerCase();
        let val = cleanText.substring(colonIndex + 1).trim();
        
        if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1).trim();
        if (val.startsWith("'") && val.endsWith("'")) val = val.slice(1, -1).trim();
        
        if (key === 'direction') {
          currentKidObj.direction = val.trim();
        } else if (key === 'tag') {
          currentKidObj.tag = val.trim();
        }
      }
    }
  });
  return result;
}

function selectDynamicDay(day) {
  const allDayButtons = document.querySelectorAll('[id^="btn-day-"]');
  allDayButtons.forEach(btn => {
    btn.classList.remove("active");
  });

  const activeBtn = document.getElementById("btn-day-" + day);
  if (activeBtn) {
    activeBtn.classList.add("active");
  }
  
  const localToday = new Date();
  const offset = localToday.getTimezoneOffset();
  const correctedDate = new Date(localToday.getTime() - (offset * 60 * 1000));
  const defaultDateStr = correctedDate.toISOString().split('T')[0];

  document.getElementById("global-date-container").innerHTML = 
    "📅 Дата проведения занятий: " +
    "<input type='text' id='global-journal-date' value='" + defaultDateStr + "' class='global-date-input'>";

  const container = document.getElementById("groups-container");
  container.innerHTML = "";

  if (!studentsData[day] || Object.keys(studentsData[day]).length === 0) {
    container.innerHTML = "<p class='empty-group-msg'>В этот день групп нет.</p>";
    return;
  }

  Object.keys(studentsData[day]).sort().forEach(time => {
    const kids = studentsData[day][time];
    
    let groupHtml = "<div class='group-block' id='block-" + time.replace(':', '-') + "'>" +
      "<div class='group-header-flex'>" +
        "<h3 class='group-title-clean'>⏰ Группа " + time + "</h3>" +
      "</div>";
    
    kids.forEach((kidObj, index) => {
      const id = "kid-" + time.replace(':', '-') + "-" + index;
      const displayName = kidObj.name;
      const serializedKid = encodeURIComponent(JSON.stringify(kidObj));

      groupHtml += 
        "<div class='kid-row'>" +
          "<label class='lbl-big'>" +
            "<input type='checkbox' id='" + id + "' class='chk-big' value='" + serializedKid + "'>" +
            displayName +
          "</label>" +
        "</div>";
    });

    let cleanBtnTextTime = time;
    const timeParts = time.split(':');
    if (timeParts.length === 2) {
      const hh = timeParts[0].trim();
      const mm = timeParts[1].trim();
      if (hh && mm) {
        cleanBtnTextTime = hh + ":" + mm;
      }
    }

    groupHtml += 
      "<div class='margin-top-15'>" +
        "<label class='field-label'>➕ Новые постоянные ученики (войдут в базу):</label>" +
        "<input type='text' id='newbies-" + time + "' class='input-text' placeholder='Имена через запятую'>" +
        
        "<label class='field-label-probation'>⏳ Временные ученики (только на сегодня):</label> + " +
        "<input type='text' id='probation-" + time + "' class='input-text input-probation' placeholder='Имена через запятую'>" +
      "</div>" +
      "<button class='btn-big btn-save' id='btn-save-" + time.replace(':', '-') + "' onclick=\"saveGroupAttendance('" + day + "', '" + time + "')\">💾 Отправить группу " + cleanBtnTextTime + "</button>" +
    "</div>";
  
    container.innerHTML += groupHtml;
  });
}

  // Валидатор и объектный конвертер ручного ввода (Белый список ключей с полными именами)
  const convertAndValidateInputs = (inputStr, fieldLabel, isProbation = false) => {
    if (!inputStr) return [];
    
    let isErrorFound = false;
    let errorMessage = "";

    const cleanList = inputStr.split(',').map(item => {
      let rawKid = item.trim();
      if (!rawKid) return "";

      // Шаг 1: Жесткая блокировка мусора. Запрещены скобки, кавычки и точка с запятой
      if (rawKid.includes('[') || rawKid.includes(']') || rawKid.includes("'") || rawKid.includes('"') || rawKid.includes('\\') || rawKid.includes(';')) {
        isErrorFound = true;
        errorMessage = "В поле '" + fieldLabel + "' у ученика '" + rawKid + "' обнаружен запрещённый символ. Ввод квадратных скобок [, ], кавычек и точек с запятой строго запрещён!";
        return null;
      }

      // Шаг 2: Проверка на бесхозные знаки решётки (без слэша разрешено только внутри #techlab-)
      if (rawKid.includes('#') && !rawKid.includes('#techlab-')) {
        // Проверяем, что перед решёткой нет слэша
        const checkIndex = rawKid.indexOf('#');
        if (checkIndex === 0 || rawKid.charAt(checkIndex - 1) !== '/') {
          isErrorFound = true;
          errorMessage = "В поле '" + fieldLabel + "' у ученика '" + rawKid + "' обнаружен недопустимый символ '#'. Вводить решётку без слэша разрешено только внутри слова '#techlab-'! Для автогенерации используйте ключ '/#'";
          return null;
        }
      }

      let directionValue = "";
      let tagValue = "";
      let hasAutoHash = false;

      // Шаг 3: Анализируем и вырезаем ключ автогенерации /#
      if (rawKid.includes('/#')) {
        hasAutoHash = true;
        rawKid = rawKid.replace('/#', '').trim();
      }

      // Шаг 4: Вытаскиваем готовые интернет-теги
      if (rawKid.includes('@')) {
        const parts = rawKid.split(' ');
        for (let p of parts) {
          if (p.startsWith('@')) {
            tagValue = p.trim();
            rawKid = rawKid.replace(tagValue, '').trim();
            break;
          }
        }
      } 
      
      if (rawKid.includes('#techlab-')) {
        const parts = rawKid.split(' ');
        for (let p of parts) {
          if (p.startsWith('#techlab-')) {
            tagValue = p.trim();
            rawKid = rawKid.replace(tagValue, '').trim();
            break;
          }
        }
      } else if (hasAutoHash) {
        tagValue = "#";
      }

      // Шаг 5: Вытаскиваем и сопоставляем ключи направлений
      if (rawKid.includes('/')) {
        const parts = rawKid.split(' ');
        for (let p of parts) {
          if (p.startsWith('/')) {
            const lowerKey = p.toLowerCase().trim();
            if (lowerKey === '/э' || lowerKey === '/e') {
              directionValue = "электронное конструирование";
              rawKid = rawKid.replace(p, '').trim();
            } else if (lowerKey === '/с' || lowerKey === '/c') {
              directionValue = "столярное дело";
              rawKid = rawKid.replace(p, '').trim();
            } else {
              isErrorFound = true;
              errorMessage = "В поле '" + fieldLabel + "' обнаружен недопустимый ключ '" + p + "' у ученика '" + rawKid + "'. Разрешены строго одиночные ключи: /э, /e, /с, /c, /#";
              return null;
            }
            break;
          }
        }
      }

      // Шаг 6: Если направление не указано — это жесткая ошибка для новичков
      if (!directionValue) {
        isErrorFound = true;
        errorMessage = "В поле '" + fieldLabel + "' у ученика '" + rawKid + "' не указано направление занятия! Допишите ключ курса через косую черту (например: /э или /с)";
        return null;
      }

      // Очищаем имя от лишних внутренних пробелов
      const cleanName = rawKid.replace(/\s+/g, ' ').trim();

      // Собираем чистый объект ученика
      let kidObj = {
        name: cleanName,
        direction: directionValue
      };
      
      if (tagValue) {
        kidObj.tag = tagValue;
      }

      return kidObj;
    }).filter(n => n !== null && n !== "");

    if (isErrorFound) {
      alert("⚠️ СБОЙ ВАЛИДАЦИИ:\n" + errorMessage);
      return null;
    }
    return cleanList;
  };

  // Прогоняем оба поля ввода через наш новый объектный валидатор
  let newbiesList = convertAndValidateInputs(newbiesInput, "Новые постоянные ученики");
  if (newbiesList === null) return; 

  let probationList = convertAndValidateInputs(probationInput, "Временные ученики", true);
  if (probationList === null) return; 

  showNotify("Подготовка объектного отчета для группы " + time + "...", "success");

  // Шаг 3: Отправка сформированного объектного Payload на GitHub через официальный API
  fetch("https://api.github.com/user", {
    headers: { "Authorization": "token " + accessToken }
  })
  .then(r => r.json())
  .then(userData => {
    const teacherUsername = userData.name || userData.login || "Преподаватель";
    const teacherLogin = userData.login;

    // КРИСТАЛЬНО ЧИСТЫЙ ОБЪЕКТНЫЙ ПАКЕТ ДАННЫХ СМЕНЫ ПЕРЕД ОТПРАВКОЙ В СЕТЬ
    const currentGroupPayload = {
      date: dateStr,
      day: day,
      time: time,
      teacher_username: teacherUsername,
      teacher_login: teacherLogin,
      present_permanent: presentKids, 
      newbies: newbiesList,           
      probation: probationList        
    };

    const filePath = `_input/${dateStr}-${timeId}-journal-attendance-${teacherLogin}.json`;
    const targetUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/${filePath}`;

    return fetch(targetUrl, {
      headers: { "Authorization": "token " + accessToken }
    })
    .then(checkRes => {
      if (checkRes.ok) {
        return checkRes.json().then(existingFile => existingFile.sha);
      }
      return null; 
    })
    .then(sha => {
      let commitBody = {
        message: "Отчет: объектная группа " + time + " (" + day + ") от " + teacherUsername,
        content: btoa(unescape(encodeURIComponent(JSON.stringify(currentGroupPayload, null, 2))))
      };

      if (sha) {
        commitBody.sha = sha;
      }

      return fetch(targetUrl, {
        method: "PUT",
        headers: {
          "Authorization": "token " + accessToken,
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
    showNotify("Объектная группа " + time + " успешно отправлена в общую сборку дня!", "success");
    
    const block = document.getElementById("block-" + timeId);
    if (block) block.style.opacity = "0.6";
    
    const btn = document.getElementById("btn-save-" + timeId);
    if (btn) {
      btn.innerText = "✅ Группа " + time + " сохранена";
      btn.disabled = true;
    }
  })
  .catch(err => {
    console.error(err);
    showNotify("Не удалось сохранить группу. Ошибка синхронизации данных.", "error");
  });
}

function showNotify(text, type) {
  const el = document.getElementById("notification");
  if (el) {
    el.classList.remove("hidden", "notify-success", "notify-error");
    el.classList.add(type === "success" ? "notify-success" : "notify-error");
    el.innerText = text;
  }
}
