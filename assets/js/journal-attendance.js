// Часть 2: Настройки репозитория и проверка пароля преподавателя
const repo_owner = "eaststandart";
const repo_name = "eaststandart.github.io";

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
    showNotify(`Загрузка журнала для ${userLogin}...`, "success");
    
    // Динамический адрес личного файла: journal-attendance-ЛОГИН.yml
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
    showNotify("Ошибка загрузки личного журнала. Проверьте наличие файла на GitHub.", "error");
  });
}

// Обновленный парсер YAML под структуру с правильными отступами
function parseSimpleYaml(text) {
  let result = {};
  let currentDay = "";
  let currentGroup = "";
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
      currentGroup = cleanText.slice(0, -1).replace(/"/g, '').replace(/'/g, '').trim();
      result[currentDay][currentGroup] = [];
    } 
    else if (indent === 4 && cleanText.startsWith('-')) {
      const name = cleanText.substring(cleanText.indexOf('-') + 1).trim();
      if (currentDay && currentGroup) {
        result[currentDay][currentGroup].push(name);
      }
    }
  });
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
      groupHtml += `
        <div class="kid-row">
          <label class="lbl-big">
            <input type="checkbox" id="${id}" class="chk-big" value="${kid}">
            ${kid}
          </label>
        </div>`;
    });

    // Текстовые блоки разметки переведены на чистые классы отступов и цветов
    groupHtml += `
      <div class="margin-top-15">
        <label class="field-label">➕ Новые постоянные ученики (войдут в базу):</label>
        <input type="text" id="newbies-${time}" class="input-text" placeholder="Имена через запятую">
        
        <label class="field-label-probation">⏳ Временные ученики (только на сегодня):</label>
        <input type="text" id="probation-${time}" class="input-text input-probation" placeholder="Имена через запятую">
      </div>
      <button class="btn-big btn-save" id="btn-save-${time.replace(':', '-')}" onclick="saveGroupAttendance('${day}', '${time}')">💾 Отправить группу ${time}</button>
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

  let newbiesList = [];
  if (newbiesInput !== "") {
    newbiesList = newbiesInput.split(',').map(n => n.trim()).filter(n => n !== "");
  }

  let probationList = [];
  if (probationInput !== "") {
    probationList = probationInput.split(',').map(n => n.trim()).filter(n => n !== "");
  }

  showNotify(`Подготовка отчета для группы ${time}...`, "success");

  // Шаг 1: Узнаем логин преподавателя
  fetch("https://api.github.com/user", {
    headers: { "Authorization": `token ${accessToken}` }
  })
  .then(r => r.json())
  .then(userData => {
    const teacherUsername = userData.name || userData.login || "Преподаватель";
    const teacherLogin = userData.login.toLowerCase().trim();

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

    // Шаг 2: Формируем имя файла индивидуально для каждой группы
    const filePath = `_data/${dateStr}-${timeId}-journal-attendance-${teacherLogin}.json`;

    let commitBody = {
      message: `Отчет группы: Группа ${time} (${day}) от ${teacherUsername}`,
      content: btoa(unescape(encodeURIComponent(JSON.stringify(currentGroupPayload, null, 2))))
    };

    // Шаг 3: Отправляем файл напрямую на GitHub без склейки в браузере
    return fetch(`https://api.github.com/repos/${repo_owner}/${repo_name}/contents/${filePath}`, {
      method: "PUT",
      headers: {
        "Authorization": `token ${accessToken}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(commitBody)
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

