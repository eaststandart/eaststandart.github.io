/**
 * @module  03-drafts-loader.js
 * @about   Модуль сетевого сканирования буферного шлюза.
 * @purpose Запрос списка файлов из папки _input медиа-репозитория и фильтрация манифестов по логину автора.
 * @author  TechLab
 * @version 1.0.0
 */

/**
 * ФУНКЦИЯ №3: Контур многократной загрузки списка черновиков из API
 */
function loadCommentDraftsFromApi() {
  const userLogin = localStorage.getItem("github_comment_logged_user") || repo_owner;

  showNotify("Загрузка списка черновиков...", "success");
  
  // Запрашиваем структуру директории _input напрямую через GitHub API без кэширования
  const inputFolderUrl = `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_input?nocache=${new Date().getTime()}`;
  
  fetch(inputFolderUrl, { headers: { "Authorization": `token ${accessToken}` } })
  .then(response => {
    if (!response.ok) throw new Error("Папка _input не найдена или пуста");
    return response.json();
  })
  .then(files => {
    // Отбираем строго .md манифесты, содержащие в имени маркер сессии текущего преподавателя
    const myDraftFiles = files.filter(file => 
      file.name.endsWith(".md") && file.name.includes(`_${userLogin}`)
    );

    if (myDraftFiles.length === 0) {
      mockDrafts = [];
      if (typeof refreshDraftSelect === "function") refreshDraftSelect();
      showNotify("Черновики не обнаружены.", "success");
      setTimeout(() => { showNotify("👨‍🏫 Преподаватель: " + userLogin, "info"); }, 2000);
      return;
    }

    // 2. Для каждого найденного файла запускаем параллельный пулл его контента
    const fetchPromises = myDraftFiles.map(file => {
      const fileUrl = `${file.url}&nocache=${new Date().getTime()}`;
      // 🔥 ИСПРАВЛЕНО: Добавлен return, который связывает сетевой fetch с массивом Promises
      return fetch(fileUrl, { headers: { "Authorization": `token ${accessToken}` } })
        .then(res => res.ok ? res.json() : null)
        .then(fileData => {
          if (!fileData) return null;
          
          // Декодируем текстовый поток 1 в 1 по эталону Журнала
          const mdText = decodeURIComponent(atob(fileData.content).split('').map(function(c) {
              return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
          }).join(''));

          // Передаем сырое имя файла и чистый текст следующему модулю-парсеру 04
          if (typeof parseManifestContent === "function") {
            return parseManifestContent(file.name, mdText, fileData.sha);
          }
          return null;
        });
    });

    return Promise.all(fetchPromises);
  })
  .then(parsedDrafts => {
    if (!parsedDrafts) return;
    
    // Фильтруем успешные разборы и сохраняем в оперативную память страницы
    mockDrafts = parsedDrafts.filter(d => d !== null);
    
    // Вызываем обновление выпадающего списка (функция будет в модуле 05)
    if (typeof refreshDraftSelect === "function") {
      refreshDraftSelect();
    }

    showNotify("Черновики успешно загружены!", "success");
    setTimeout(() => { showNotify("👨‍🏫 Преподаватель: " + userLogin, "info"); }, 2000);
  })
  .catch(err => {
    console.error(err);
    showNotify("Ошибка загрузки файлов из папки черновиков.", "error");
  });
}
