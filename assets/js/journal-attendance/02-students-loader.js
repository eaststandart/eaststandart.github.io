/**
 * @module  02-students-loader.js
 * @about   Загрузка расписания.
 * @purpose Загрузка расписания.
 * @author  TechLab
 * @version 1.0.0
 */

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
