/**
 * @module  05-attendance-commands.js
 * @about   Посещаемость и команды /d, /r, /m.
 * @purpose Сохранение посещаемости и обработка команд.
 * @author  TechLab
 * @version 1.0.0
 */

function saveGroupAttendance(day, time) {
  const dateStr = document.getElementById("global-journal-date").value.trim(); 
  const timeId = time.replace(':', '-');
  const newbiesInput = document.getElementById(`newbies-${time}`).value.trim();
  const probationInput = document.getElementById(`probation-${time}`).value.trim();

  // =========================================================================
  // 👑 ЕДИНЫЙ МОНОЛИТНЫЙ БЛОК ОБРАБОТКИ СИСТЕМНЫХ КОМАНД JOURNAL TECHLAB
  // =========================================================================
  const cmdWords = newbiesInput.split(' ').map(w => w.trim()).filter(Boolean);
  const allowedCmdKeys = ["/d", "/r", "/m"];
  
  const hasJournal = cmdWords.length > 0 && cmdWords[0].toLowerCase() === "journal";
  const hasCmdKey = cmdWords.length > 0 && allowedCmdKeys.includes(cmdWords[cmdWords.length - 1].toLowerCase());

  // ЕСЛИ СТРОКА НАЧИНАЕТСЯ НА JOURNAL И СОДЕРЖИТ РАЗРЕШЕННЫЙ КЛЮЧ:
  if (hasJournal && hasCmdKey) {
    const currentTeacher = localStorage.getItem("github_journal_logged_user") || repo_owner;
    const lastWordKey = cmdWords[cmdWords.length - 1].toLowerCase();
    
    let universalPayload = {
      teacher_login: currentTeacher,
      day: day,
      time: time.replace(/"/g, '').replace(/'/g, '').trim()
    };

    let bannerTitle = "";
    let bannerText = "";

    // Внутри этого единого блока зряче отделяем одни ключи от других:
    if (lastWordKey === "/d") {
      const studentName = cmdWords.slice(1, -1).join(' ').trim();
      if (!studentName) {
        alert('⚠️ СБОЙ КОМАНДЫ:\nУкажите имя ученика по стандарту: "journal Фамилия Имя /d"');
        return;
      }
      universalPayload.command = "delete";
      universalPayload.delete = [studentName];
      bannerTitle = "⚠️ ЗАПУЩЕНА ПРОЦЕДУРА ИЗМЕНЕНИЯ РАСПИСАНИЯ!";
      bannerText = `Запрос на удаление отправлен на сервер GitHub.<br>Цель: <code>${studentName}</code>.`;
    } 
    else if (lastWordKey === "/r") {
      if (cmdWords.length !== 2) {
        alert('⚠️ СБОЙ КОМАНДЫ:\nКоманда ремонта вводится строго по стандарту: "journal /r"');
        return;
      }
      universalPayload.command = "repair";
      universalPayload.repair = "";
      bannerTitle = "🛠️ ЗАПУЩЕНА ПРИНУДИТЕЛЬНАЯ ПРОВЕРКА БАЗЫ РАСПИСАНИЯ!";
      bannerText = "Команда полного ремонта успешно принята конвейером.";
    } 
    else if (lastWordKey === "/m") {
      if (cmdWords.length !== 4) {
        alert('⚠️ СБОЙ КОМАНДЫ:\nКоманда изменения времени вводится строго по стандарту: "journal [старое_время] [новое_время] /m"');
        return;
      }
      const oldDigits = cmdWords[1].replace(/\D/g, "");
      const newDigits = cmdWords[2].replace(/\D/g, "");
      if (oldDigits.length !== 4 || newDigits.length !== 4) {
        alert('⚠️ СБОЙ КОМАНДЫ:\nУкажите строго 4 цифры старого и нового времени суток (например: journal 1300 1200 /m)!');
        return;
      }
      universalPayload.command = "modify";
      universalPayload.time = oldDigits.substring(0, 2) + ":" + oldDigits.substring(2, 4);
      universalPayload.modify_time = newDigits.substring(0, 2) + ":" + newDigits.substring(2, 4);
      bannerTitle = "🛠️ ЗАПУЩЕНА ПРИНУДИТЕЛЬНАЯ МОДИФИКАЦИЯ РАСПИСАНИЯ!";
      bannerText = `Команда изменения структуры времени <code>${universalPayload.time} -> ${universalPayload.modify_time}</code> успешно принята.`;
    }

    // Блокируем экран Красным баннером перестройки расписания
    document.getElementById("groups-container").innerHTML = 
      "<div class='emergency-banner'>" + bannerTitle + "<br>" +
        "<span class='emergency-banner-sub'>" + bannerText + "<br><br>" +
          "<b>Генерация отчетов заблокирована до окончания перестройки файлов!</b>" +
        "</span>" +
      "</div>";

    // Скрываем весь родительский ряд глобального инпута даты занятий
    const cmdDateInput = document.getElementById("global-journal-date");
    if (cmdDateInput) {
      const cmdParentRow = cmdDateInput.closest('div');
      if (cmdParentRow) cmdParentRow.style.display = "none";
    }
    
    document.querySelectorAll('[id^="btn-day-"]').forEach(btn => { btn.disabled = true; btn.classList.remove("active"); });
    showNotify("❌ Обнаружено изменение базы данных журнала!", "error");

    sendUniversalRepairSignal(universalPayload);
    return; // Жестко прерываем выполнение, не пуская команду в Поток Б!
  }
  
  // ЗРЯЧИЙ ПРЕДОХРАНИТЕЛЬ ОПЕЧАТОК ПРЕПОДАВАТЕЛЯ
  if (hasJournal || hasCmdKey) {
    alert('⚠️ ОШИБКА ВВОДА:\nНарушен синтаксис системных команд!\nСлово "journal" и ключи /d, /r, /m обязаны использоваться строго вместе в одной строке.');
    return;
  }

  // =========================================================================
  // 🧱 ИНАЧЕ - ВСЁ ОСТАЛЬНОЕ: ШТАТНЫЙ КОНВЕЙЕР СБОРА ПОСЕЩАЕМОСТИ УЧЕНИКОВ
  // =========================================================================
  let presentKids = [];
  const checkboxes = document.querySelectorAll(`[id^="kid-${time.replace(':', '-')}-"]`);
  checkboxes.forEach(chk => {
    if (chk.checked) presentKids.push(chk.value);
  });

  // Функция-обработчик: выполняет сквозной перевод комбинаций ключей по белому списку по Регламенту
  const convertAndValidateInputs = (inputStr, fieldLabel) => {
    if (!inputStr) return [];

    // ЭТАП №1: ГЛОБАЛЬНЫЙ БРОНЕЩИТ ВСЕГО ПОЛЯ ВВОДА — ОТСЕКАЕМ ЛЮБОЙ БРАК НА СТАРТЕ
    const globalInputWhitelist = /^[a-zA-Zа-яА-ЯёЁ0-9\s,/#@-]+$/;
    if (!globalInputWhitelist.test(inputStr)) {
      alert(`⚠️ СБОЙ СИНТАКСИСА TECHLAB:\nВ поле "${fieldLabel}" обнаружены запрещённые или ломающие структуру спецсимволы!\nРазрешены строго только буквы, цифры, пробелы, запятые и знаки: / , # , @ , -`);
      return null;
    }
    
    let isErrorFound = false;
    let errorMessage = "";

    // Режем всю строку ввода по запятым на отдельные записи учащихся
    const cleanList = inputStr.split(',').map(item => {
      let rawKid = item.trim();
      if (!rawKid) return null;

      // 1. ЭТАП №1: Разбиваем сырую запись пробелами на отдельные чистые слова
      const words = rawKid.split(' ').map(w => w.trim()).filter(Boolean);
      if (words.length === 0) return null;

      // =========================================================================
      // 👑 ДВУХЗАМКОВЫЙ СУПЕР-ШЛЮЗ СИСТЕМНЫХ КОМАНД МОДЕРАЦИИ TECHLAB
      // =========================================================================
      const firstWord = words[0].toLowerCase();
      const lastWord = words[words.length - 1].toLowerCase();
      const allowedCmdKeys = ["/d", "/r", "/m"];

      if (firstWord === "journal" && allowedCmdKeys.includes(lastWord)) {
        if (lastWord === "/d") {
          const studentName = words.slice(1, -1).join(' ').trim();
          if (!studentName) {
            isErrorFound = true;
            errorMessage = 'Ошибка команды удаления! Укажите имя ученика по стандарту: "journal Фамилия Имя /d"';
            return null;
          }
          return { name: studentName, delete: true };
        }
        else if (lastWord === "/r") {
          if (words.length !== 2) {
            isErrorFound = true;
            errorMessage = 'Ошибка команды ремонта! Полный ремонт вводится строго как: "journal /r"';
            return null;
          }
          return { name: "journal", repair: true };
        }
        else if (lastWord === "/m") {
          if (words.length !== 4) {
            isErrorFound = true;
            errorMessage = 'Ошибка команды модификации! Изменение времени вводится строго как: "journal [старое_время] [новое_время] /m"';
            return null;
          }
          const oldDigits = words[1].replace(/\D/g, "");
          const newDigits = words[2].replace(/\D/g, "");
          if (oldDigits.length !== 4 || newDigits.length !== 4) {
            isErrorFound = true;
            errorMessage = 'Ошибка формата времени в команде /m! Укажите строго 4 цифры старого и нового времени (например: journal 1300 1400 /m)';
            return null;
          }
          return { name: "journal " + oldDigits + " " + newDigits, modify: true };
        }
      }

      let keysArray = [];
      let tagsArray = [];
      let nameWordsArray = [];

      // 2. ЭТАП №2: Распределяем слова по трем независимым карманам
      for (let w of words) {
        // Проверяем карман КЛЮЧЕЙ (всё, что начинается на слэш /)
        if (w.startsWith('/')) {
          if (w === '/э' || w === '/e' || w === '/с' || w === '/c' || w === '/d' || w === '/r' || w === '/m') {
            keysArray.push(w);
          } else {
            isErrorFound = true;
            errorMessage = `В записи "${rawKid}" обнаружен недопустимый ключ направления "${w}"!`;
            return null;
          }
        }
        // Проверяем карман ТЕГОВ (всё, что является одиночным #, начинается на @ или на #techlab-)
        else if (w === '#' || w.startsWith('@') || w.startsWith('#techlab-')) {
          tagsArray.push(w);
        }
        // Ошибочные левые хэштеги, не соответствующие платформе
        else if (w.startsWith('#')) {
          isErrorFound = true;
          errorMessage = `В записи "${rawKid}" обнаружен недопустимый тег "${w}"! Допускаются строго: одиночный "#" или системный "#techlab-"`;
          return null;
        }
        // Все остальные слова отправляются в карман ИМЕНИ
        else {
          nameWordsArray.push(w);
        }
      }

      // КОНТРОЛЬ МОНОПОЛИИ КЛЮЧА УДАЛЕНИЯ /d (БЕЗ ТЕГОВ И ДРУГИХ КЛЮЧЕЙ)
      if (keysArray.includes('/d')) {
        if (keysArray.length > 1 || tagsArray.length > 0) {
          isErrorFound = true;
          errorMessage = `В записи "${rawKid}" обнаружена ошибка! Ключ удаления /d должен вводиться строго отдельно от других ключей направлений и тегов.`;
          return null;
        }
      }

      // 3. ЭТАП №3: Склеиваем Фамилию Имя из кармана и проверяем её Whitelist
      const cleanName = nameWordsArray.join(' ').trim();

      // КОНТРОЛЬ МОНОПОЛИИ КЛЮЧА РЕМОНТА /r (БЕЗ ТЕГОВ И СТРОГО ДЛЯ СЛОВА JOURNAL)
      if (keysArray.includes('/r')) {
        if (keysArray.length > 1 || tagsArray.length > 0 || cleanName.toLowerCase() !== 'journal') {
          isErrorFound = true;
          errorMessage = `В записи "${rawKid}" обнаружена ошибка! Ключ ремонта /r должен вводиться строго отдельно от других ключей направлений и тегов.`;
          return null;
        }
      }

      // КОНТРОЛЬ МОНОПОЛИИ КЛЮЧА УДАЛЕНИЯ /d (БЕЗ ТЕГОВ И ДРУГИХ КЛЮЧЕЙ)
      if (keysArray.includes('/d')) {
        if (keysArray.length > 1 || tagsArray.length > 0) {
          isErrorFound = true;
          errorMessage = `В записи "${rawKid}" обнаружена ошибка! Ключ удаления /d должен вводиться строго отдельно от других ключей направлений и тегов.`;
          return null;
        }
      }

      // Контроль количества: максимум 1 ключ на запись учащегося
      if (keysArray.length > 1) {
        isErrorFound = true;
        errorMessage = `В записи "${rawKid}" обнаружено более одного ключа направления! Разрешен строго один ключ.`;
        return null;
      }

      // Жёсткий контроль количества: максимум 1 тег на запись учащегося
      if (tagsArray.length > 1) {
        isErrorFound = true;
        errorMessage = `В записи "${rawKid}" обнаружено более одного тега! Разрешен строго один тег: либо "#", либо "#techlab-", либо "@логин".`;
        return null;
      }

      // Проверка обязательного наличия Фамилии и Имени учащегося в строке
      if (!cleanName) {
        isErrorFound = true;
        errorMessage = `В поле "${fieldLabel}" обнаружена запись без Фамилии и Имени учащегося! Ввод голых ключей и тегов строго запрещён.`;
        return null;
      }

      // Изолированный Белый список символов для ИМЕНИ: только русские/английские буквы, пробел и дефис. Без цифр!
      const nameWhitelistRegex = /^[a-zA-Zа-яА-ЯёЁ\s-]+$/;
      if (!nameWhitelistRegex.test(cleanName)) {
        isErrorFound = true;
        errorMessage = `В поле "${fieldLabel}" у имени "${cleanName}" обнаружены недопустимые символы или цифры! Разрешены только буквы, пробелы и дефис.`;
        return null;
      }

      // Финальная конвертация Ключа из кармана в полное текстовое название
      let direction = "";
      if (keysArray.length === 1) {
        const k = keysArray[0].toLowerCase();
        if (k === '/э' || k === '/e') direction = "электронное конструирование";
        if (k === '/с' || k === '/c') direction = "столярное дело";
      }

      let finalTag = tagsArray.length === 1 ? tagsArray[0] : "";
      // Сборка идеального плоского объекта JSON строго по своим полям
      let studentObj = { name: cleanName };
      if (keysArray.includes('/d')) {
        studentObj.delete = true;
      } else if (keysArray.includes('/r')) {
        studentObj.repair = true;
      } else {
        studentObj.direction = direction;
        if (finalTag) studentObj.tag = finalTag;
      }
      return studentObj;

    }).filter(n => n !== null);

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

  // ЕДИНЫЙ МАСШТАБИРУЕМЫЙ КОНВЕЙЕР ПЕРЕХВАТА СИСТЕМНЫХ КОМАНД МОДЕРАЦИИ БАЗЫ TECHLAB
  const currentTeacher = localStorage.getItem("github_journal_logged_user") || repo_owner;
  const isDelete = newbiesList.some(item => item.delete === true);
  const isRepair = newbiesList.some(item => item.repair === true);
  const isModify = newbiesList.some(item => item.repair === false && newbiesInput.includes('/m'));

  if (isDelete || isRepair || isModify) {
    let universalPayload = {
      teacher_login: currentTeacher,
      day: day,
      time: time.replace(/"/g, '').replace(/'/g, '').trim()
    };

    let bannerTitle = "";
    let bannerText = "";

    if (isDelete) {
      const deleteNames = newbiesList.filter(item => item.delete === true).map(item => item.name);
      const currentGroupStudents = studentsData[day][time] || [];
      for (let nameToDelete of deleteNames) {
        if (!currentGroupStudents.includes(nameToDelete)) {
          alert(`⚠️ СБОЙ УДАЛЕНИЯ:\nУченика "${nameToDelete}" нет в базе этой группы!\nПроверьте буквы. Запрос отклонён.`);
          return;
        }
      }
      universalPayload.command = "delete";
      universalPayload.delete = deleteNames;
      bannerTitle = "⚠️ ЗАПУЩЕНА ПРОЦЕДУРА ИЗМЕНЕНИЯ БАЗЫ РАСПИСАНИЯ!";
      bannerText = "Запрос на удаление отправлен на сервер GitHub.<br>Список: <code>" + deleteNames.join(', ') + "</code>.";
    } 
    else if (isRepair) {
      universalPayload.command = "repair";
      universalPayload.repair = "";
      bannerTitle = "🛠️ ЗАПУЩЕНА ПРИНУДИТЕЛЬНАЯ ПРОВЕРКА БАЗЫ РАСПИСАНИЯ!";
      bannerText = "Команда полного ремонта <code>journal /r</code> успешно принята валидатором.";
    } 
    else if (isModify) {
      const cmdWords = newbiesInput.split(' ').map(w => w.trim()).filter(Boolean);
      const oldDigits = (cmdWords[1] || "").replace(/\D/g, "");
      const newDigits = (cmdWords[2] || "").replace(/\D/g, "");
      
      universalPayload.command = "modify";
      universalPayload.time = oldDigits.substring(0, 2) + ":" + oldDigits.substring(2, 4);
      universalPayload.modify_time = newDigits.substring(0, 2) + ":" + newDigits.substring(2, 4);
      bannerTitle = "🛠️ ЗАПУЩЕНА ПРИНУДИТЕЛЬНАЯ МОДИФИКАЦИЯ РАСПИСАНИЯ!";
      bannerText = "Команда изменения структуры времени успешно принята валидатором.";
    }

    document.getElementById("groups-container").innerHTML = 
      "<div class='emergency-banner'>" + bannerTitle + "<br>" +
        "<span class='emergency-banner-sub'>" + bannerText + "<br><br>" +
          "<b>Генерация отчетов заблокирована до окончания перестройки файлов!</b>" +
        "</span>" +
      "</div>";
    
    document.querySelectorAll('[id^="btn-day-"]').forEach(btn => { btn.disabled = true; btn.classList.remove("active"); });
    showNotify("❌ Обнаружено изменение базы данных журнала!", "error");

    sendUniversalRepairSignal(universalPayload);
    return;
  }

  showNotify(`Подготовка отчета для группы ${time}...`, "success");

  // Шаг 1: Узнаем логин преподавателя
  fetch("https://api.github.com/user", {
    headers: { "Authorization": `token ${accessToken}` }
  })
  .then(r => r.json())
  .then(userData => {
    const teacherUsername = userData.name || userData.login || "Преподаватель";
    const teacherLogin = userData.login; // Используем оригинальную переменную логина

    // Собираем пакет данных смены
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

// Функция управления постоянным статус-баром без прыжков интерфейса
