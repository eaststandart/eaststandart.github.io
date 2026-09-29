---
layout: page
title: Журнал посещаемости
permalink: /admin-journal/
---

<!-- Часть 1: Обновленные стили оформления и форма ввода ключа-пароля -->
<style>
  .admin-container { font-family: system-ui, sans-serif; max-width: 600px; margin: 0 auto; padding: 15px; }
  .btn-big { display: block; width: 100%; padding: 15px; margin: 10px 0; font-size: 16px; font-weight: bold; text-align: center; border: none; border-radius: 8px; cursor: pointer; }
  .btn-auth { background-color: #24292e; color: white; }
  .btn-day { background-color: #f1f3f5; color: #495057; border: 1px solid #ced4da; }
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
  .notify { padding: 12px; margin: 10px 0; border-radius: 6px; font-size: 14px; text-align: center; }
  .notify-success { background-color: #d3f9d8; color: #2b8a3e; }
  .notify-error { background-color: #ffe3e3; color: #c92a2a; }
  .auth-box { background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
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
    <div style="display: flex; gap: 10px;">
      <button id="btn-sat" class="btn-big btn-day" onclick="selectDay('суббота')">🟢 СУББОТА</button>
      <button id="btn-sun" class="btn-big btn-day" onclick="selectDay('воскресенье')">🔵 ВОСКРЕСЕНЬЕ</button>
    </div>

    <div id="notification" class="notify hidden"></div>

    <!-- Контейнер для динамических групп детей -->
    <div id="groups-container"></div>
  </div>
</div>
<script>
  // Часть 2: Настройки репозитория и логика проверки ключа-пароля
  const repo_owner = "eaststandart";
  const repo_name = "eaststandart.github.io";

  let accessToken = localStorage.getItem("github_journal_token");
  let studentsData = {};

  // Проверяем, заходил ли учитель ранее
  document.addEventListener("DOMContentLoaded", () => {
    if (accessToken) {
      showJournal();
    }
  });

  // Функция проверки и сохранения пароля-токена
  function submitToken() {
    const tokenValue = document.getElementById("token-input").value.trim();
    if (!tokenValue) {
      alert("Пожалуйста, введите ключ доступа!");
      return;
    }

    document.getElementById("btn-login").disabled = true;
    document.getElementById("btn-login").innerText = "Проверка пароля...";

    // Проверяем ключ, делая запрос к официальному API профиля
    fetch("https://api.github.com/user", {
      headers: { "Authorization": `token ${tokenValue}` }
    })
    .then(response => {
      if (response.ok) {
        // Если ключ подошел, запоминаем его в памяти браузера
        localStorage.setItem("github_journal_token", tokenValue);
        accessToken = tokenValue;
        showJournal();
      } else {
        alert("Неверный ключ доступа! Проверьте, правильно ли вы его скопировали.");
        document.getElementById("btn-login").disabled = false;
        document.getElementById("btn-login").innerText = "🔓 Подключить журнал";
      }
    })
    .catch(err => {
      console.error(err);
      alert("Ошибка сети при проверке пароля. Попробуйте еще раз.");
      document.getElementById("btn-login").disabled = false;
      document.getElementById("btn-login").innerText = "🔓 Подключить журнал";
    });
  }

  function showJournal() {
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("journal-section").classList.remove("hidden");
    loadStudentsFromYaml();
  }
  // Часть 3: Чтение базы детей, генерация интерфейса и отправка отчета
  function loadStudentsFromYaml() {
    showNotify("Загрузка списка учеников...", "success");
    
    // Адрес запроса: https://api .github .com/repos/owner/name/contents/_data/journal-students.yml
    fetch(`https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_data/journal-students.yml`, {
      headers: { "Authorization": `token ${accessToken}` }
    })
    .then(response => {
      if (!response.ok) throw new Error("Не удалось скачать файл из репозитория");
      return response.json();
    })
    .then(data => {
      // Декодируем Base64 с полной поддержкой кириллицы (UTF-8)
      const yamlText = decodeURIComponent(atob(data.content).split('').map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      
      studentsData = parseSimpleYaml(yamlText);
      showNotify("Список учеников успешно загружен!", "success");
      setTimeout(() => { document.getElementById("notification").classList.add("hidden"); }, 2000);
    })
    .catch(err => {
      console.error(err);
      showNotify("Ошибка загрузки списка детей из папки _data. Проверьте токен.", "error");
    });
  }

  // Разборщик YAML-структуры
  function parseSimpleYaml(text) {
    let result = {};
    let currentDay = "";
    let currentGroup = "";
    const lines = text.split('\n');

    lines.forEach(line => {
      const trimmed = line.trimEnd();
      if (!trimmed || trimmed.startsWith('#')) return;

      const indent = line.search(/\S/);
      if (indent === 0 && trimmed.endsWith(':')) {
        currentDay = trimmed.slice(0, -1).toLowerCase().trim();
        result[currentDay] = {};
      } else if (indent === 2 && (trimmed.includes(':'))) {
        currentGroup = trimmed.split(':').map(s => s.trim()).filter(s => s)[0].replace(/['"]/g, '');
        result[currentDay][currentGroup] = [];
      } else if (indent === 4 && trimmed.startsWith('-')) {
        const name = trimmed.substring(trimmed.indexOf('-') + 1).trim();
        if (currentDay && currentGroup) {
          result[currentDay][currentGroup].push(name);
        }
      }
    });
    return result;
  }

  function selectDay(day) {
    document.getElementById("btn-sat").className = "btn-big btn-day " + (day === "суббота" ? "active-sat" : "");
    document.getElementById("btn-sun").className = "btn-big btn-day " + (day === "воскресенье" ? "active-sun" : "");
    
    const container = document.getElementById("groups-container");
    container.innerHTML = "";

    if (!studentsData[day] || Object.keys(studentsData[day]).length === 0) {
      container.innerHTML = "<p style='text-align:center; color:#868e96;'>В этот день групп нет.</p>";
      return;
    }

    Object.keys(studentsData[day]).sort().forEach(time => {
      const kids = studentsData[day][time];
      let groupHtml = `<div class="group-block">
        <h3 class="group-title">⏰ Группа ${time}</h3>`;
      
      kids.forEach((kid, index) => {
        const id = `kid-${time}-${index}`;
        groupHtml += `
          <div class="kid-row">
            <input type="checkbox" id="${id}" class="chk-big" value="${kid}">
            <label for="${id}" class="lbl-big">${kid}</label>
          </div>`;
      });

      groupHtml += `
        <div style="margin-top: 15px;">
          <label class="lbl-big" style="font-weight: bold;">➕ Новые ученики на ${time}:</label>
          <input type="text" id="newbies-${time}" class="input-text" placeholder="Имена через запятую (например: Марк В., Лев К.)">
          <div class="kid-row" style="border:none; padding: 5px 0 0 0;">
            <input type="checkbox" id="probation-${time}" class="chk-big" style="width:20px; height:20px;">
            <label for="probation-${time}" class="lbl-big" style="font-size:14px; color:#6c757d;">⚠️ Только пробное занятие (не добавлять в базу насовсем)</label>
          </div>
        </div>
        <button class="btn-big btn-save" onclick="saveGroupAttendance('${day}', '${time}')">💾 Сохранить группу ${time}</button>
      </div>`;
      
      container.innerHTML += groupHtml;
    });
  }

  function saveGroupAttendance(day, time) {
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0]; 
    
    let presentKids = [];
    const checkboxes = document.querySelectorAll(`[id^="kid-${time}-"]`);
    checkboxes.forEach(chk => {
      if (chk.checked) presentKids.push(chk.value);
    });

    const newbiesInput = document.getElementById(`newbies-${time}`).value.trim();
    const isProbation = document.getElementById(`probation-${time}`).checked;

    let newbiesList = [];
    if (newbiesInput !== "") {
      newbiesList = newbiesInput.split(',').map(n => n.trim()).filter(n => n !== "");
    }

    const reportPayload = {
      date: dateStr,
      day: day,
      time: time,
      present_permanent: presentKids,
      newbies: newbiesList,
      is_newbies_probation: isProbation
    };

    const fileName = `${dateStr}-journal-students-${time.replace(':', '-')}.json`;
    const filePath = `_attendance/${fileName}`;
    
    showNotify("Отправка отчета на GitHub...", "success");

    // Адрес отправки: https://api .github .com/repos/owner/name/contents/_attendance/filename
    fetch(`https://api.github.com/repos/${repo_owner}/${repo_name}/contents/${filePath}`, {
      method: "PUT",
      headers: {
        "Authorization": `token ${accessToken}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: `Отчет по посещаемости: Группа ${time} (${day})`,
        content: btoa(unescape(encodeURIComponent(JSON.stringify(reportPayload, null, 2))))
      })
    })
    .then(response => {
      if (!response.ok) throw new Error("Ошибка при записи файла на GitHub");
      return response.json();
    })
    .then(data => {
      showNotify(`Успешно отправлено! Робот обновит Дискуссии в течение 1-2 минут.`, "success");
      document.getElementById(`newbies-${time}`).value = "";
      document.getElementById(`probation-${time}`).checked = false;
    })
    .catch(err => {
      console.error(err);
      showNotify("Не удалось отправить отчет. Убедитесь в правильности токена.", "error");
    });
  }

  function showNotify(text, type) {
    const el = document.getElementById("notification");
    el.classList.remove("hidden", "notify-success", "notify-error");
    el.classList.add(type === "success" ? "notify-success" : "notify-error");
    el.innerText = text;
  }
</script>
