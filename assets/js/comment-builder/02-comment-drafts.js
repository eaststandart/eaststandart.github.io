/**
 * @module  02-comment-drafts.js
 * @about   Модуль сетевой загрузки базы черновиков.
 * @purpose Запрос списка манифестов из папки _input медиа-репозитория, чтение их Front Matter без кэширования и наполнение селекта.
 * @author  TechLab
 * @version 1.0.0
 */

// Глобальный массив для хранения распарсенных черновиков в оперативной памяти страницы
let mockDrafts = []; 

// ФУНКЦИЯ №2: Контур многократной загрузки черновиков и работы с API сервера
function loadCommentDraftsFromApi() {
  const userLogin = localStorage.getItem("github_comment_logged_user") || repo_owner;

  // --- ЭТАП №3: ОТРИСОВКА И ЗАГРУЗКА ДАННЫХ ЧЕРНОВИКОВ ПРЕПОДАВАТЕЛЯ НАПРЯМУЮ ---
  showNotify("Загрузка списка черновиков...", "success");
  
  // Запрашиваем содержимое папки _input медиа-репозитория
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

    // 2. Для каждого файла запускаем параллельную загрузку его контента для разбора Front Matter
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
    
    // Обновляем выпадающий список (если режим черновика уже активен)
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
 * Вспомогательный разбор контента .md черновика для извлечения Front Matter
 */
function parseManifestContent(fileName, text, sha) {
  try {
    const yamlMatch = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
    if (!yamlMatch) return null;

    const yamlBlock = yamlMatch[1];
    const bodyText = text.substring(yamlMatch[0].length);
    
    let meta = { id: fileName, sha: sha, text: bodyText };
    
    // Построчно вытаскиваем ключевые YAML параметры
    yamlBlock.split('\n').forEach(line => {
      if (line.includes(':')) {
        const parts = line.split(':');
        const key = parts[0].trim().toLowerCase();
        const value = parts.slice(1).join(':').trim().replace(/^["']|["']$/g, '');
        meta[key] = value;
      }
    });

    // Приведение к единой структуре полей Конструктора
    return {
      id: fileName,
      sha: sha,
      date: meta.date || "",
      discussion: meta.discussion_number || "",
      commit: meta.discussion_comment || "",
      title: meta.title || "Без заголовка",
      text: meta.text || "", // Сюда уйдет чистый остаток markdown тела
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
