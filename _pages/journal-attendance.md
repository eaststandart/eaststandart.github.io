---
layout: page
title: Журнал посещаемости
permalink: /journal-attendance/
---

<!-- Часть 1: Обновленные стили и интерфейс с двумя раздельными полями ввода -->
<style>
  .admin-container { font-family: system-ui, sans-serif; max-width: 600px; margin: 0 auto; padding: 15px; }
  .btn-big { display: block; width: 100%; padding: 15px; margin: 10px 0; font-size: 16px; font-weight: bold; text-align: center; border: none; border-radius: 8px; cursor: pointer; }
  .btn-auth { background-color: #24292e; color: white; }
  .btn-day { background-color: #f1f3f5; color: #495057; border: 1px solid #ced4da; padding: 10px 5px; margin: 0; font-size: 14px; flex: 1; min-width: 40px; text-align: center; border-radius: 6px; font-weight: bold; }
  .btn-day:disabled { background-color: #e9ecef; color: #adb5bd; border-color: #dee2e6; cursor: not-allowed; opacity: 0.6; border-left: none !important; }
  .btn-day.active-sat { background-color: #2b8a3e; color: white; }
  .btn-day.active-sun { background-color: #1c7ed6; color: white; }
  .btn-save { background-color: #37b24d; color: white; margin-top: 15px; }
  .group-block { border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 20px 0; background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
  .group-title { font-size: 18px; margin-top: 0; color: #212529; border-bottom: 2px solid #e9ecef; padding-bottom: 5px; }
  .kid-row { display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f3f5; }
  .kid-row:last-child { border-bottom: none; }
  .chk-big { width: 24px; height: 24px; margin-right: 15px; cursor: pointer; }
  .lbl-big { font-size: 16px; cursor: pointer; user-select: none; flex-grow: 1; }
  .input-text { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ced4da; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
  .hidden { display: none; }
  .notify { padding: 12px; margin: 10px 0; border-radius: 6px; font-size: 14px; text-align: center; font-weight: bold; }
  .notify-success { background-color: #d3f9d8; color: #2b8a3e; }
  .notify-error { background-color: #ffe3e3; color: #c92a2a; }
  .auth-box { background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; border-radius: 8px; }
  .field-label { font-size: 14px; font-weight: bold; color: #495057; display: block; margin-top: 10px; }
</style>

<div class="admin-container">
  <!-- БЛОК АВТОРИЗАЦИИ ЧЕРЕЗ ТОКЕН-ПАРОЛЬ -->
  <div id="auth-section" class="auth-box">
    <h3 style="margin-top: 0; color: #24292e;">🔑 Доступ к журналу</h3>
    <p style="font-size: 14px; color: #6c757d; margin-bottom: 15px;">Вставьте ваш личный персональный ключ доступа (github_pat), чтобы открыть журнал:</p>
    <input type="password" id="token-input" class="input-text" placeholder="github_pat_...">
    <button id="btn-login" class="btn-big btn-auth" onclick="submitToken()">🔓 Подключить журнал</button>
  </div>

  <!-- РАБОЧАЯ ЗОНА ЖУРНАЛА -->
  <div id="journal-section" class="hidden">
    <!-- Выбор дня недели -->
    <!-- Контейнер для динамических кнопок дней недели -->
    <div id="days-buttons-container" style="display: flex; gap: 10px; flex-wrap: wrap;"></div>

	<div id="notification" class="notify hidden"></div>

    <!-- Контейнер для динамических групп детей -->
    <div id="groups-container"></div>
  </div>
</div>
<script>
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

    // Ссылка запроса: https://api . github . com/user
    fetch(" https://api.github.com/user", {
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
    loadStudentsFromYaml();
  }

  function logoutTeacher() {
    if (confirm("Вы уверены, что хотите выйти из журнала и сменить ключ доступа?")) {
      localStorage.removeItem("github_journal_token");
      accessToken = null;
      window.location.reload();
    }
  }

  // Часть 3: Чтение базы детей с правильным парсером, два поля ввода и отправка порций
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
        { key: "понедельник", label: "ПН", color: "#e63946" },
        { key: "вторник", label: "ВТ", color: "#d9480f" },
        { key: "среда", label: "СР", color: "#f59f00" },
        { key: "четверг", label: "ЧТ", color: "#2b8a3e" },
        { key: "пятница", label: "ПТ", color: "#0c8599" },
        { key: "суббота", label: "СБ", color: "#2b8a3e" },
        { key: "воскресенье", label: "ВС", color: "#1c7ed6" }
      ];
      
      calendarOrder.forEach(dayInfo => {
        const btnId = `btn-day-${dayInfo.key}`;
        const isAvailable = studentsData[dayInfo.key] && Object.keys(studentsData[dayInfo.key]).length > 0;
        const disabledAttr = isAvailable ? "" : "disabled";
        const borderStyle = isAvailable ? `border-left: 4px solid ${dayInfo.color};` : "";
        
        daysContainer.innerHTML += `
          <button id="${btnId}" class="btn-big btn-day" ${disabledAttr} 
                  style="${borderStyle} transition: 0.2s;" 
                  onclick="selectDynamicDay('${dayInfo.key}', '${dayInfo.color}')">
            ${dayInfo.label}
          </button>`;
      });

      // ДОБАВЛЯЕМ 8-Ю КНОПКУ ВЫХОД В ЭТОТ ЖЕ РЯД
      daysContainer.innerHTML += `
        <button class="btn-big btn-day" 
                style="border-left: none; background-color: #c92a2a; color: white;" 
                onclick="logoutTeacher()">
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

    function selectDynamicDay(day, activeColor) {
    // 1. Сбрасываем стили у абсолютно всех кнопок дней, делая их стандартными
    const allDayButtons = document.querySelectorAll(`[id^="btn-day-"]`);
    allDayButtons.forEach(btn => {
      btn.style.backgroundColor = "#f1f3f5";
      btn.style.color = "#495057";
    });

    // 2. Подсвечиваем выбранную кнопку её уникальным цветом
    const activeBtn = document.getElementById(`btn-day-${day}`);
    if (activeBtn) {
      activeBtn.style.backgroundColor = activeColor;
      activeBtn.style.color = "white";
    }
    
    // 3. Генерируем группы для выбранного дня недели
    const container = document.getElementById("groups-container");
    container.innerHTML = "";

    if (!studentsData[day] || Object.keys(studentsData[day]).length === 0) {
      container.innerHTML = "<p style='text-align:center; color:#868e96;'>В этот день групп нет.</p>";
      return;
    }

    Object.keys(studentsData[day]).sort().forEach(time => {
      const kids = studentsData[day][time];
      let groupHtml = `<div class="group-block" id="block-${time.replace(':', '-')}">
        <h3 class="group-title">⏰ Группа ${time}</h3>`;
      
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

      groupHtml += `
        <div style="margin-top: 15px;">
          <label class="field-label">➕ Новые постоянные ученики (войдут в базу навсегда):</label>
          <input type="text" id="newbies-${time}" class="input-text" placeholder="Имена через запятую">
          
          <label class="field-label" style="color: #1c7ed6;">⏳ Временные / Пробные ученики (только на сегодня):</label>
          <input type="text" id="probation-${time}" class="input-text" placeholder="Имена через запятую" style="border-color: #a5d8ff;">
        </div>
        <button class="btn-big btn-save" id="btn-save-${time.replace(':', '-')}" onclick="saveGroupAttendance('${day}', '${time}')">💾 Отправить группу ${time}</button>
      </div>`;
      
      container.innerHTML += groupHtml;
    });
  }

   function saveGroupAttendance(day, time) {
    const today = new Date();
    // Чистая дата в формате ГГГГ-ММ-ДД
    const dateStr = today.toISOString().split('T')[0]; 
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
      const teacherLogin = userData.login.toLowerCase().trim(); // ДОБАВЛЕНО: Объявляем переменную логина!

      const currentGroupPayload = {
        date: dateStr,
        day: day,
        time: time,
        teacher_username: teacherUsername,
        teacher_login: teacherLogin, // ДОБАВЛЕНО: Записываем логин в JSON
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
</script>
