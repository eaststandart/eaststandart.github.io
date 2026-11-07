/**
 * @module  03-comment-drafts.js
 * @about   Модуль сетевой загрузки базы черновиков.
 * @purpose Запрос списка манифестов из папки _input медиа-репозитория, чтение их Front Matter без кэширования, разбор Markdown-тела и восстановление структуры блоков формы.
 * @author  TechLab
 * @version 1.0.0
 */

// Глобальный массив для хранения распарсенных черновиков в оперативной памяти страницы
let mockDrafts = []; 

/**
 * ФУНКЦИЯ №3: Контур многократной загрузки черновиков и работы с API сервера
 */
function loadCommentDraftsFromApi() {
  const userLogin = localStorage.getItem("github_comment_logged_user") || repo_owner;

  showNotify("Загрузка списка черновиков...", "success");
  
  // Запрашиваем содержимое папки _input медиа-репозитория напрямую из GitHub API
  const inputFolderUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_input?nocache=${new Date().getTime()}`;
  
  fetch(inputFolderUrl, { headers: { "Authorization": `token ${accessToken}` } })
  .then(response => {
    if (!response.ok) throw new Error("Папка _input не найдена или пуста");
    return response.json();
  })
  .then(files => {
    // 1. Отбираем строго .md файлы, в имени которых содержится логин текущего преподавателя
    const myDraftFiles = files.filter(file => 
      file.name.endsWith(".md") && file.name.includes(`_${userLogin}`)
    );

    if (myDraftFiles.length === 0) {
      mockDrafts = [];
      refreshDraftSelect();
      showNotify("Черновики не обнаружены.", "success");
      setTimeout(() => { showNotify("👨‍🏫 Преподаватель: " + userLogin, "info"); }, 2000);
      return;
    }

    // 2. Для каждого файла запускаем параллельную загрузку его контента для разбора Front Matter и Markdown-тела
    const fetchPromises = myDraftFiles.map(file => {
      const fileUrl = `${file.url}&nocache=${new Date().getTime()}`;
      return fetch(fileUrl, { headers: { "Authorization": `token ${accessToken}` } })
        .then(res => res.ok ? res.json() : null)
        .then(fileData => {
          if (!fileData) return null;
          
          // Декодируем текстовый поток строго по эталону Журнала (1 в 1)
          const mdText = decodeURIComponent(atob(fileData.content).split('').map(function(c) {
              return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
          }).join(''));

          return parseManifestContent(file.name, mdText, fileData.sha);
        });
    });

    return Promise.all(fetchPromises);
  })
  .then(parsedDrafts => {
    if (!parsedDrafts) return;
    
    // Фильтруем успешные разборы и сохраняем в оперативную память
    mockDrafts = parsedDrafts.filter(d => d !== null);
    
    // Обновляем выпадающий список
    refreshDraftSelect();

    showNotify("Черновики успешно загружены!", "success");
    setTimeout(() => { showNotify("👨‍🏫 Преподаватель: " + userLogin, "info"); }, 2000);
  })
  .catch(err => {
    console.error(err);
    showNotify("Ошибка загрузки файлов из папки черновиков.", "error");
  });
}

/**
 * Вспомогательный разбор контента .md черновика для извлечения Front Matter и остатка тела
 */
function parseManifestContent(fileName, text, sha) {
  try {
    const yamlMatch = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
    if (!yamlMatch) return null;

    const yamlBlock = yamlMatch[1];
    const rawBodyText = text.substring(yamlMatch[0].length);
    
    let meta = { id: fileName, sha: sha };
    
    // Построчно вытаскиваем ключевые YAML параметры
    yamlBlock.split('\n').forEach(line => {
      if (line.includes(':')) {
        const parts = line.split(':');
        const key = parts[0].trim().toLowerCase();
        const value = parts.slice(1).join(':').trim().replace(/^["']|["']$/g, '');
        meta[key] = value;
      }
    });

    return {
      id: fileName,
      sha: sha,
      date: meta.date || "",
      discussion: meta.discussion_number || "",
      commit: meta.discussion_comment || meta.comment_id || "",
      title: meta.title || "Без заголовка",
      text: rawBodyText, // Сохраняем полное markdown-тело для последующего парсинга блоков
      timestamp: meta.timestamp || "",
      published: meta.published || "false",
      teacher: meta.teacher || ""
    };
  } catch (e) {
    console.error("Ошибка парсинга Front Matter черновика: ", e);
    return null;
  }
}

/**
 * Функция обновления и перерисовки выпадающего списка на Линии 2
 */
function refreshDraftSelect() {
  const select = document.getElementById("draft-select");
  const isDraftMode = document.getElementById("is-draft-mode")?.checked;
  
  if (!select) return;

  if (isDraftMode) {
    let html = `<option value="">-- Сохраненный черновик --</option>`;
    mockDrafts.forEach(draft => {
      html += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
    });
    select.innerHTML = html;
    select.disabled = false;
  } else {
    select.innerHTML = `<option value="">Выберите черновик --></option>`;
    select.disabled = true;
  }
}

/**
 * ЛИНИЯ 2 В ДЕЙСТВИИ: Включение и отключение селекта Линии 2 (Поведение из монолитного скрипта)
 */
function toggleDraftBehavior() {
  const isDraftMode = document.getElementById("is-draft-mode").checked;
  const select = document.getElementById("draft-select");
  const publishFlag = document.getElementById("publish-now-flag");

  if (isDraftMode) {
    // Включаем режим черновика: блокируем прямую отправку и запрашиваем API шлюза
    if (publishFlag) publishFlag.checked = false;
    if (typeof updatePublishLabel === "function") updatePublishLabel();
    loadCommentDraftsFromApi();
  } else {
    // Отключаем режим черновика: чистим и сбрасываем форму в дефолтное состояние Потока Б
    if (select) {
      select.innerHTML = `<option value="">Выберите черновик --></option>`;
      select.disabled = true;
    }
    if (publishFlag) publishFlag.checked = true;
    if (typeof updatePublishLabel === "function") updatePublishLabel();
    
    // Возвращаем текущую дату занятий
    const localToday = new Date();
    const offset = localToday.getTimezoneOffset();
    const correctedDate = new Date(localToday.getTime() - (offset * 60 * 1000));
    const defaultDateStr = correctedDate.toISOString().split('T')[0];

    const dateInput = document.getElementById("target-date");
    if (dateInput) dateInput.value = defaultDateStr;
    
    // Зачищаем все текстовые поля Блока 2
    const postTitle = document.getElementById("post-title");
    const postText = document.getElementById("post-text");
    const postFooter = document.getElementById("post-footer");
    
    if (postTitle) postTitle.value = "";
    if (postText) postText.value = "";
    if (postFooter) postFooter.value = "";
    
    document.getElementById("discussion-combo").value = "";
    document.getElementById("commit-id").value = "";

    // Наглухо сбрасываем интерфейс медиа-блоков в стартовое состояние (по 1 пустому блоку)
    if (typeof initCommentInterface === "function") {
      initCommentInterface();
    }
  }
}

/**
 * ЖЕСТКАЯ СИНХРОНИЗАЦИЯ И РАЗВЕРТЫВАНИЕ СТРУКТУРЫ: Наполнение всех полей и блоков 2, 3 и 4 при выборе из списка
 */
function loadDraftData(draftId) {
  if (!draftId) return;
  const selectedDraft = mockDrafts.find(d => d.id === draftId);
  if (!selectedDraft) return;

  // 1. Наполнение Линии 1 шапки
  const dateInput = document.getElementById("target-date");
  if (dateInput) dateInput.value = selectedDraft.date;
  
  document.getElementById("discussion-combo").value = selectedDraft.discussion;
  document.getElementById("commit-id").value = selectedDraft.commit || "";
  
  // 2. Очищаем старые контейнеры медиа-блоков на экране перед восстановлением структуры
  const containerPhotos = document.getElementById("photos-meta-container");
  const containerVideos = document.getElementById("videos-meta-container");
  if (containerPhotos) containerPhotos.innerHTML = "";
  if (containerVideos) containerVideos.innerHTML = "";
  
  // Сбрасываем глобальные индексы блочного генератора
  photoBlockIdx = 0;
  videoBlockIdx = 0;

  // 3. Сканируем и извлекаем текст Описания и Подвала из тела Markdown
  let bodyText = selectedDraft.text;
  let postTitleText = selectedDraft.title !== "Без заголовка" ? selectedDraft.title : "";
  let postMainText = "";
  let postFooterText = "";

  // Вырезаем подвал, если он отделен через черту ---
  if (bodyText.includes("---")) {
    const parts = bodyText.split("---");
    postMainText = parts[0].trim();
    postFooterText = parts.slice(1).join("---").trim();
  } else {
    postMainText = bodyText.trim();
  }

  // 4. ПАРСИНГ И ИНТЕЛЛЕКТУАЛЬНОЕ ВОССТАНОВЛЕНИЕ ДИНАМИЧЕСКИХ МЕДИА-БЛОКОВ
  // Делим текст на секции по разделителям блоков "### "
  const sections = postMainText.split(/(?=### )/);
  let cleanDescriptionText = "";

  sections.forEach(section => {
    if (!section.trim()) return;

    // Проверяем, является ли секция блоком ФОТО
    if (section.includes("![[photo_") || section.includes("![photo_")) {
      const titleMatch = section.match(/###\s*(.*?)\n/);
      const title = titleMatch ? titleMatch[1].trim() : "📸 Фотоматериалы";
      
      // Краткое описание — это текст между заголовком h3 и ссылкой на файл ![[...]]
      let desc = section.replace(/###.*?\n/, "").replace(/!\[\[.*?\]\]/, "").replace(/!\[.*?\]\(.*?\)/, "").trim();
      
      if (typeof addPhotoBlock === "function") {
        addPhotoBlock(title, desc);
      }
    }
    // Проверяем, является ли секция блоком ВИДЕО
    else if (section.includes("![[video_") || section.includes("![video_")) {
      const titleMatch = section.match(/###\s*(.*?)\n/);
      const title = titleMatch ? titleMatch[1].trim() : "🎥 Видеоматериалы";
      
      let desc = section.replace(/###.*?\n/, "").replace(/!\[\[.*?\]\]/, "").replace(/!\[.*?\]\(.*?\)/, "").trim();
      
      if (typeof addVideoBlock === "function") {
        addVideoBlock(title, desc);
      }
    }
    // Если это не медиа-блок, значит это основной текст описания комментария из Блока 2
    else {
      cleanDescriptionText += section + "\n";
    }
  });

  // Наполняем контекст полей Блока 2
  const titleInput = document.getElementById("post-title");
  const textInput = document.getElementById("post-text");
  const footerInput = document.getElementById("post-footer");

  if (titleInput) titleInput.value = postTitleText;
  if (textInput) textInput.value = cleanDescriptionText.replace(/##.*?\n/, "").trim(); // Очищаем от дублирования h2
  if (footerInput) footerInput.value = postFooterText;

  // Если вдруг в черновике не было медиа-блоков, принудительно возвращаем по 1 дефолтному
  if (document.querySelectorAll("#photos-meta-container .media-sub-block").length === 0) {
    if (typeof addPhotoBlock === "function") addPhotoBlock();
  }
  if (document.querySelectorAll("#videos-meta-container .media-sub-block").length === 0) {
    if (typeof addVideoBlock === "function") addVideoBlock();
  }

  showNotify(`Черновик от ${selectedDraft.date} успешно развернут!`, "success");
}
