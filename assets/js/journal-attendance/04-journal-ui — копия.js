/**
 * @module  04-journal-ui.js
 * @about   Отображение дней и групп.
 * @purpose Отображение дней и групп.
 * @author  TechLab
 * @version 1.0.0
 */

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

  const dateContainer = document.getElementById("global-date-container");
  if (dateContainer) {
    // Аппаратно активируем рамки и тени карточки строго в момент отрисовки дня
    dateContainer.className = "global-date-box";
    dateContainer.innerHTML = 
      "<span>📅 Дата занятий:</span>" +
      "<input type='text' id='global-journal-date' value='" + defaultDateStr + "' class='global-date-input'>";
  }

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
    groupHtml += 
      "<div class='inputs-inline-row'>" +
        "<div class='input-container-half'>" +
          "<input type='text' id='newbies-" + time + "' class='input-text' placeholder='➕ Новые постоянные ученики...'>" +
        "</div>" +
        "<div class='input-container-half'>" +
          "<input type='text' id='probation-" + time + "' class='input-text input-probation' placeholder='⏳ Временные ученики (только сегодня)...'>" +
        "</div>" +
      "</div>" +
      "<button class='btn-big btn-save' id='btn-save-" + time.replace(':', '-') + "' onclick='saveGroupAttendance(\"" + day + "\", \"" + time + "\")'>💾 Отправить группу " + cleanBtnTextTime + "</button>" +
    "</div>";
  
    container.innerHTML += groupHtml;
  });
}
