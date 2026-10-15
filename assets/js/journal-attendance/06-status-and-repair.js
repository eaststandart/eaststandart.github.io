/**
 * @module  06-status-and-repair.js
 * @about   Статусы и ремонт.
 * @purpose Уведомления, опрос статуса и сигналы ремонта.
 * @author  TechLab
 * @version 1.0.0
 */

function showNotify(text, type) {
  const el = document.getElementById("notification");
  if (!el) return;
  
  el.classList.remove("notify-success", "notify-error", "notify-blue");
  
  // Строка SVG-кода иконки Bootstrap Icons box-arrow-right
  const svgIcon = "<svg xmlns='http://w3.org' width='21' height='21' fill='currentColor' class='bi bi-box-arrow-right' viewBox='0 0 16 16'>" +
                    "<path fill-rule='evenodd' d='M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z'/>" +
                    "<path fill-rule='evenodd' d='M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z'/>" +
                  "</svg>";

  if (type === "success") {
    el.classList.add("notify-success");
    el.innerHTML = "<div class='notify-flex-content'>" +
                     "<span>" + text + "</span>" +
                     "<button onclick='logoutTeacher()' class='btn-logout-svg' title='Выйти из журнала'>" + svgIcon + "</button>" +
                   "</div>";
  } 
  else if (type === "error") {
    el.classList.add("notify-error");
    el.innerHTML = "<div class='notify-flex-content'>" +
                     "<span>" + text + "</span>" +
                     "<button onclick='logoutTeacher()' class='btn-logout-svg' title='Выйти из журнала'>" + svgIcon + "</button>" +
                   "</div>";
  } 
  else if (type === "info") {
    el.classList.add("notify-blue");
    el.innerHTML = "<div class='notify-flex-content'>" +
                     "<span>" + text + "</span>" +
                     "<button onclick='logoutTeacher()' class='btn-logout-svg' title='Выйти из журнала'>" + svgIcon + "</button>" +
                   "</div>";
  }
}


// Функция зрячего 5-секундного опроса файла статуса
function startRepairStatusPolling() {
  const btn = document.getElementById("btn-force-repair");
  const currentTeacher = localStorage.getItem("github_journal_logged_user") || repo_owner;
  const statusUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/repair-status-${currentTeacher}.json`;

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
        showNotify("🟢 База данных успешно проверена сервером!", "success");
        
        document.getElementById("groups-container").innerHTML = "";
        // Возвращаем глобальное поле выбора даты занятий в штатный режим отображения
        const dateCont = document.getElementById("global-journal-date");
        if (dateCont) dateCont.style.display = "block";
        
        localStorage.setItem("github_journal_robot_ok", "true");
        isRobotChecked = true; 
        
        loadStudentsFromYaml(); // Запускаем загрузку чистого файла расписания
      }
      
      if (payload.status === "error") {
        clearInterval(intervalId);
        const serverDetails = payload.errorDetails || "Критический сбой интерпретатора или рассинхронизация веток репозитория";
        
        // Передаем в чистый баннер Ветки В статус отказа воркфлоу и живой лог из Питона
        triggerEmergencyBlock("GitHub Actions", "Отказ выполнения воркфлоу сессии ремонта", serverDetails, "manual", currentTeacher);
        showNotify("❌ Критическая ошибка структуры расписания на сервере!", "error");
        
        if (btn) {
          btn.disabled = false;
          btn.innerText = "❌ Сбой структуры. Исправьте вручную";
        }
      }
    })
    .catch(err => { console.warn("Опрос статуса:", err.message); });
  }, 5000);
}

// Единая функция для вывода баннера аварийной блокировки и кнопки ремонта сервера
function triggerEmergencyBlock(lineNum, cleanText, errorDetails, errorType = "", forcedDay = "") {
  let bannerHtml = "";

  // ВЕТКА А: Точечная модификация цифр времени суток при идеальных отступах
  if (errorType === "modify_time") {
    const onlyDigits = cleanText.replace(/\D/g, "");
    const badH = onlyDigits.substring(0, 2) || "00";
    const badM = onlyDigits.substring(2, 4) || "00";
    const cleanOldTime = badH + ":" + badM;

    bannerHtml = 
      "<div class='emergency-banner'>" +
        "⚠️ АВАРИЙНАЯ БЛОКИРОВКА: КРИТИЧЕСКИЙ СБОЙ ВРЕМЕНИ ГРУППЫ!<br>" +
        "<span class='emergency-banner-sub'>" +
          "В строке №" + lineNum + " обнаружено " + errorDetails + "<br>" +
          "Исправьте время прямо в полях ниже:<br>" +
          "<div class='emergency-inputs-row'>" +
            "<input type='text' id='repair-hour' class='global-date-input emergency-time-input' maxlength='2' value='" + badH + "'>" +
            "<span class='emergency-separator'>:</span>" +
            "<input type='text' id='repair-minute' class='global-date-input emergency-time-input' maxlength='2' value='" + badM + "'>" +
          "</div>" +
          "<b>Генерация отчетов полностью заблокирована!</b><br>" +
          "<button id='btn-force-repair' class='btn-big btn-save btn-emergency-repair' onclick=\"(function(){ " +
            "const rawH = document.getElementById('repair-hour').value.trim(); " +
            "const rawM = document.getElementById('repair-minute').value.trim(); " +
            "const h = parseInt(rawH, 10); " +
            "const m = parseInt(rawM, 10); " +
            "if (isNaN(h) || isNaN(m) || h < 0 || h > 23 || m < 0 || m > 59 || rawH.length === 0 || rawM.length === 0) { " +
              "alert('⚠️ ОШИБКА ВВОДА:\\nНекорректное время суток!\\nЧасы должны быть от 00 до 23, минуты от 00 до 59.\\nЗапрос отклонён.'); " +
              "return; " +
            "} " +
            "const newTimeStr = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0'); " +
            "const currentTeacher = localStorage.getItem('github_journal_logged_user') || repo_owner; " +
            "sendUniversalRepairSignal({ " +
              "teacher_login: currentTeacher, " +
              "day: '" + forcedDay + "', " +
              "time: '" + cleanOldTime + "', " +
              "command: 'modify', " +
              "modify_time: newTimeStr " +
            "}); " +
          "})()\">🛠️ Починить время на сервере</button>" +
        "</span>" +
      "</div>";
  } 
  // ВЕТКА Б: Полная принудительная перестройка геометрии отступов (Команда "repair")
  else if (errorType === "repair") {
    const currentTeacher = localStorage.getItem("github_journal_logged_user") || repo_owner;
    const classicPayload = {
      teacher_login: currentTeacher,
      day: forcedDay,
      time: "00:00",
      command: "repair",
      repair: ""
    };
    const payloadJsonStr = btoa(unescape(encodeURIComponent(JSON.stringify(classicPayload))));

    bannerHtml = 
      "<div class='emergency-banner'>" +
        "⚠️ АВАРИЙНАЯ БЛОКИРОВКА: НАРУШЕНА ГЕОМЕТРИЯ РАСПИСАНИЯ!<br>" +
        "<span class='emergency-banner-sub'>" +
          "В строке №" + lineNum + " обнаружена ошибка отступов: " + errorDetails + "<br>" +
          "Проблемный текст базы: <code>" + cleanText + "</code>.<br><br>" +
          "<b>Генерация отчетов полностью заблокирована!</b> Требуется принудительное выравнивание пробелов базы на сервере GitHub.<br><br>" +
          "<button id='btn-force-repair' class='btn-big btn-save btn-emergency-repair' onclick=\"sendUniversalRepairSignal(JSON.parse(decodeURIComponent(escape(atob('" + payloadJsonStr + "')))))\">🛠️ Исправить базу данных на сервере</button>" +
        "</span>" +
      "</div>";
  }
  // ВЕТКА В: Аварийный сбой или отказ выполнения на стороне сервера GitHub Actions (Команда "manual")
  else {
    bannerHtml = 
      "<div class='emergency-banner'>" +
        "⚠️ АВАРИЙНАЯ БЛОКИРОВКА: ОТКАЗ СЕРВЕРА GITHUB ACTIONS!<br>" +
        "<span class='emergency-banner-sub'>" +
          "Статус воркфлоу: <b>" + cleanText + "</b>.<br>" +
          "Логгер сервера: <code>" + errorDetails + "</code>.<br><br>" +
          "<b>Автоматическое исправление в Журнале полностью заблокировано!</b><br>" +
          "Робот не смог обработать файл расписания. Пожалуйста, откройте репозиторий и <b>исправьте базу руками.</b>" +
        "</span>" +
      "</div>";
  }

  document.getElementById("groups-container").innerHTML = bannerHtml;
  
  // Жестко скрываем глобальное поле даты занятий, исключая наложение интерфейса
  const dateCont = document.getElementById("global-journal-date");
  if (dateCont) dateCont.style.display = "none";
  
  const allDayButtons = document.querySelectorAll('[id^="btn-day-"]');
  allDayButtons.forEach(function(btn) { btn.disabled = true; btn.classList.remove("active"); });
  
  showNotify("❌ Обнаружена критическая ошибка синтаксиса в файле!", "error");
}

// Единая универсальная функция отправки любых сигналов модерации базы данных TechLab
function sendUniversalRepairSignal(payload) {
  // Твои фирменные логи инспекции TechLab перед отправкой пакета на сайт
  console.log("Проверка ремонта:", {
    forcedDay: payload.day,
    currentDayName: payload.day,
    oldTimeDigits: payload.time ? payload.time.replace(/\D/g, "") : "0000",
    cleanOldTime: payload.time
  });
  console.log("JSON перед отправкой:", JSON.stringify(payload));

  const currentTeacher = payload.teacher_login;
  const statusUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/repair-status-${currentTeacher}.json`;
  const signalUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/signal-repair-${currentTeacher}.json`;

  const statusPayload = { status: "on", mode: "repair", timestamp: new Date().toISOString() };
  const statusBody = {
    message: "chore: взвод светофора для сессии " + payload.command + " [skip ci]",
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
    if (!res.ok) throw new Error("Не удалось взвести файл статуса");
    
    const signalBody = {
      message: "chore: универсальный сигнал команды " + payload.command + " для " + currentTeacher,
      content: btoa(unescape(encodeURIComponent(JSON.stringify(payload, null, 2))))
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
    if (!res.ok) throw new Error("Ошибка отправки файла сигнала");
    showNotify("🟢 Команда " + payload.command + " успешно отправлена на сервер!", "success");
    startRepairStatusPolling();
  })
  .catch(err => {
    console.error(err);
    showNotify("❌ Не удалось связаться с сервером при отправке сигнала.", "error");
  });
}
