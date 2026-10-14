// ФУНКЦИЯ №2: Контур многократной загрузки расписания и работы с роботом сервера
function loadStudentsFromYaml() {
  const userLogin = localStorage.getItem("github_journal_logged_user") || repo_owner;

  // --- ЭТАП №3: ОТРИСОВКА И ЗАГРУЗКА ДАННЫХ РАСПИСАНИЯ ПРЕПОДАВАТЕЛЯ НАПРЯМУЮ ---
  showNotify("Загрузка данных расписания...", "success");
  const yamlUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/journal-attendance-${userLogin}.yml?nocache=${new Date().getTime()}`;
  
  fetch(yamlUrl, { headers: { "Authorization": `token ${accessToken}` } })
  .then(response => {
    if (!response.ok) throw new Error("Личный файл журнала не найден в папке _data");
    return response.json();
  })
  .then(data => {
    const yamlText = decodeURIComponent(atob(data.content).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    
    studentsData = parseSimpleYaml(yamlText);
    if (!studentsData || Object.keys(studentsData).length === 0) return;
    
    const daysContainer = document.getElementById("days-buttons-container");
    daysContainer.innerHTML = "";
    
    const calendarOrder = [
      { key: "понедельник", label: "ПН" }, { key: "вторник", label: "ВТ" },
      { key: "среда", label: "СР" }, { key: "четверг", label: "ЧТ" },
      { key: "пятница", label: "ПТ" }, { key: "суббота", label: "СБ" },
      { key: "воскресенье", label: "ВС" }
    ];
    
    calendarOrder.forEach(dayInfo => {
      const btnId = `btn-day-${dayInfo.key}`;
      const isAvailable = studentsData[dayInfo.key] && Object.keys(studentsData[dayInfo.key]).length > 0;
      const disabledAttr = isAvailable ? "" : "disabled";
      daysContainer.innerHTML += `
        <button id="${btnId}" class="btn-big btn-day btn-day-transition day-border-${dayInfo.key}" ${disabledAttr} onclick="selectDynamicDay('${dayInfo.key}')">
          ${dayInfo.label}
        </button>`;
    });

    showNotify("Журнал успешно загружен!", "success");
    setTimeout(() => { showNotify("👨‍🎓 Преподаватель: " + userLogin, "info"); }, 2000);
  })
  .catch(err => {
    console.error(err);
    showNotify("Ошибка загрузки личного файла журнала расписания.", "error");
  });
}

// Изолированная функция упреждающего запуска робота, полностью исключающая обрывы Promise
function executeUprezhdaushiyRobot(userLogin) {
  const statusUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/repair-status.json?nocache=` + new Date().getTime();
  const signalUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/signal-repair.json`;

  // Сначала зряче проверяем, не запущен ли уже ремонт другим окном/преподавателем
  fetch(statusUrl, { headers: { "Authorization": "token " + accessToken } })
  .then(res => res.ok ? res.json() : null)
  .then(data => {
    if (data) {
      const jsonText = decodeURIComponent(atob(data.content).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
      const payload = JSON.parse(jsonText);
      
      // Аппаратный замок: робот уже работает! Не плодим мусорные коммиты, просто уходим в опрос!
      if (payload.status === "on") {
        console.log("[ЗАМОК] Робот уже выполняет проверку базы. Подключаемся к сессии.");
        startRepairStatusPolling();
        return null;
      }
    }
    
    // Если сервер свободен, запускаем штатную процедуру взвода светофора
    const statusPayload = { status: "on", mode: "", timestamp: new Date().toISOString() };
    const statusBody = {
      message: "chore: упреждающий запуск светофора при загрузке журнала [skip ci]",
      content: btoa(unescape(encodeURIComponent(JSON.stringify(statusPayload, null, 2))))
    };
    if (data && data.sha) statusBody.sha = data.sha;
    
    return fetch(`https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/repair-status.json`, {
      method: "PUT",
      headers: { "Authorization": "token " + accessToken, "Content-Type": "application/json" },
      body: JSON.stringify(statusBody)
    });
  })
  .then(res => {
    if (res === null) return; // Выход по замку
    if (!res.ok) throw new Error("Не удалось взвести статус");
    
    const signalPayload = { teacher_login: userLogin };
    const signalBody = {
      message: "chore: запрос проверки расписания для " + userLogin,
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
    if (res === undefined) return;
    if (!res.ok) throw new Error("Ошибка отправки сигнала");
    startRepairStatusPolling();
  })
  .catch(err => {
    console.error("Сбой авторемонта:", err);
    isRobotChecked = true;
    loadStudentsFromYaml();
  });
}
