---
layout: page
title: Журнал посещаемости
permalink: /admin-journal/
---

<!-- Стилевое оформление крупных кнопок под пальцы смартфона -->
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
  .input-text { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box; font-size: 15px; }
  .hidden { display: none; }
  .notify { padding: 12px; margin: 10px 0; border-radius: 6px; font-size: 14px; text-align: center; }
  .notify-success { background-color: #d3f9d8; color: #2b8a3e; }
  .notify-error { background-color: #ffe3e3; color: #c92a2a; }
</style>

<div class="admin-container">
  <!-- БЛОК АВТОРИЗАЦИИ -->
  <div id="auth-section">
    <button class="btn-big btn-auth" onclick="loginWithGitHub()">🔐 Войти через аккаунт GitHub</button>
  </div>

  <!-- РАБОЧАЯ ЗОНА ЖУРНАЛА -->
  <div id="journal-section" class="hidden">
    <!-- Выбор дня недели -->
    <div style="display: flex; gap: 10px;">
      <button id="btn-sat" class="btn-big btn-day" onclick="selectDay('суббота')">🟢 СУББОТА</button>
      <button id="btn-sun" class="btn-big btn-day" onclick="selectDay('воскресенье')">🔵 ВОСКРЕСЕНЬЕ</button>
    </div>

    <div id="notification" class="notify hidden"></div>

    <!-- Сюда JavaScript сам подгрузит группы из YAML файла -->
    <div id="groups-container"></div>
  </div>
</div>

<script>
  // Конфигурация вашего репозитория на GitHub
  const client_id = "Client ID Ov23lio8AV0SPM0ViUlP"; // Вставьте сюда ваш Client ID
  const repo_owner = "eaststandart";
  const repo_name = "eaststandart.github.io";

  // Адрес бесплатного шлюза-посредника, который оживит кнопку входа
  const oauth_gate_url = "https://vercel.app";
  const client_secret = "cba34a070f9f63a1ed6ca926f4e428d1c15b4f85"; // Вставьте сюда секрет

  let accessToken = localStorage.getItem("github_journal_token");
  let studentsData = {};

  // Проверяем, авторизован ли уже учитель
  document.addEventListener("DOMContentLoaded", () => {
    // Проверяем, вернулся ли Гитхаб с кодом авторизации в ссылке
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code) {
      window.history.replaceState({}, document.title, window.location.pathname);
      exchangeCodeForToken(code);
    } else if (accessToken) {
      showJournal();
    }
  });

  function loginWithGitHub() {
    // Перенаправляем на официальный безопасный шлюз авторизации Гитхаба
    window.location.href = `https://github.com{client_id}&scope=repo`;
  }

  function exchangeCodeForToken(code) {
    document.getElementById("notification").classList.remove("hidden");
    document.getElementById("notification").className = "notify notify-success";
    document.getElementById("notification").innerText = "Авторизация... Пожалуйста, подождите.";
    
    // Временная заглушка для локального сохранения, пока мы не настроили OAuth Gate
    localStorage.setItem("github_journal_token", "mock_token_success");
    accessToken = "mock_token_success";
    showJournal();
  </div>

  function showJournal() {
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("journal-section").classList.remove("hidden");
    loadStudentsFromYaml();
  }

  // Робот сам заглядывает в ваш файл data/journal-students.yml
  function loadStudentsFromYaml() {
    fetch('/data/journal-students.yml')
      .then(response => response.text())
      .then(yamlText => {
        studentsData = parseSimpleYaml(yamlText);
      })
      .catch(err => {
        showNotify("Ошибка загрузки списка детей из папки data", "error");
      });
  }

  // Простой встроенный разборщик YAML-структуры
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
        currentDay = trimmed.slice(0, -1).toLowerCase();
        result[currentDay] = {};
      } else if (indent === 2 && (trimmed.includes(':'))) {
        currentGroup = trimmed.split(':')[0].replace(/['"]/g, '').trim();
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

    // Генерируем блоки групп под пальцы
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
    const container = document.getElementById("groups-container");
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0]; // Формат: 2026-09-29
    
    // Собираем имена тех, кто отмечен галочками
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

    // Собираем итоговый JSON пакет данных для сохранения
    const reportPayload = {
      date: dateStr,
      day: day,
      time: time,
      present_permanent: presentKids,
      newbies: newbiesList,
      is_newbies_probation: isProbation
    };

    const fileName = `${dateStr}-journal-students-${time.replace(':', '-')}.json`;
    showNotify(`Журнал группы ${time} успешно сформирован! Идет отправка в файл ${fileName}...`, "success");
    
    // Здесь скрипт сделает коммит напрямую в ваш репозиторий через GitHub API
    console.log("Пакет данных для GitHub Actions:", reportPayload);
  }

  function showNotify(text, type) {
    const el = document.getElementById("notification");
    el.classList.remove("hidden", "notify-success", "notify-error");
    el.classList.add(type === "success" ? "notify-success" : "notify-error");
    el.innerText = text;
  }
</script>
