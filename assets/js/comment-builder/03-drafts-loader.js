/**
 * @module  03-drafts-loader.js
 * @about   Модуль загрузки черновиков из GitHub.
 * @purpose Получение файлов из буферного репозитория, проверка статуса публикации и подготовка списка черновиков.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: waitDraftRetry
// НАЗНАЧЕНИЕ: Ожидает заданное время перед повторной попыткой загрузки черновиков.
function waitDraftRetry(seconds, attempt) {
  return new Promise(resolve => {
    let remaining = seconds;

    showNotify(
      `Ошибка сети. Повтор загрузки ${attempt}/3 через ${remaining} сек.`,
      "info"
    );

    const timer = setInterval(() => {
      remaining--;

      if (remaining <= 0) {
        clearInterval(timer);
        resolve();
        return;
      }

      showNotify(
        `Ошибка сети. Повтор загрузки ${attempt}/3 через ${remaining} сек.`,
        "info"
      );
    }, 1000);
  });
}

// ФУНКЦИЯ: fetchDraftJson
// НАЗНАЧЕНИЕ: Получает JSON-данные из GitHub API с обработкой временных ошибок.
async function fetchDraftJson(url, headers) {
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const response = await fetch(url, { headers });

      if (!response.ok) {
        const error = new Error(
          `Ошибка GitHub API: HTTP ${response.status}`
        );
        error.status = response.status;
        throw error;
      }

      return await response.json();

    } catch (error) {
      const isNetworkError =
        error instanceof TypeError ||
        (error.status >= 500 && error.status <= 599);

      if (!isNetworkError || attempt === 3) {
        throw error;
      }

      await waitDraftRetry(60, attempt + 1);
    }
  }
}

// ФУНКЦИЯ: loadCommentDraftsFromApi
// НАЗНАЧЕНИЕ: Загружает из репозитория только черновики текущего преподавателя.
async function loadCommentDraftsFromApi() {
  const userLogin =
    localStorage.getItem("github_comment_logged_user") || repo_owner;

  const headers = {
    Authorization: `token ${accessToken}`,
    Accept: "application/vnd.github+json"
  };

  try {
    showNotify("Загрузка списка черновиков...", "info");

    const inputFolderUrl =
      `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_input?nocache=${Date.now()}`;

    const files = await fetchDraftJson(inputFolderUrl, headers);

    const myDraftFiles = files.filter(file =>
      file.name.endsWith(".md") &&
      file.name.includes(`_${userLogin}`)
    );

    if (myDraftFiles.length === 0) {
      mockDrafts = [];
      if (typeof refreshDraftSelect === "function") {
        refreshDraftSelect();
      }
      showNotify("Черновики не обнаружены.", "success");
      return;
    }

    const fetchPromises = myDraftFiles.map(async file => {
      const fileUrl = `${file.url}&nocache=${Date.now()}`;
      const fileData = await fetchDraftJson(fileUrl, headers);

      const mdText = decodeURIComponent(
        atob(fileData.content.replace(/\s/g, ""))
          .split("")
          .map(c =>
            "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2)
          )
          .join("")
      );

      if (typeof parseManifestContent === "function") {
        return parseManifestContent(file.name, mdText, fileData.sha);
      }

      return null;
    });

    const availableFiles = new Set(
      files.filter(file => file.type === "file").map(file => file.name)
    );

    const parsedDrafts = await Promise.all(fetchPromises);

    mockDrafts = parsedDrafts.filter(d => {
      if (!d) return false;

      const mediaNames = [
        ...(d.photos || []).flatMap(block => block.files || []),
        ...(d.videos || []).flatMap(block => block.files || [])
      ];

      d.missingFiles = mediaNames.filter(name => !availableFiles.has(name));

      return String(d.published).toLowerCase() === "false" ||
        (String(d.published).toLowerCase() === "true" && d.missingFiles.length > 0);
    });

    if (typeof refreshDraftSelect === "function") {
      refreshDraftSelect();
    }

    if (mockDrafts.length === 0) {
      showNotify("Черновики не обнаружены.", "success");
      return;
    }

    const incompleteCount = mockDrafts.filter(d => d.missingFiles?.length > 0).length;
    const draftCount = mockDrafts.length - incompleteCount;

    showNotify(
      `Загружено: черновиков ${draftCount}, не собрано ${incompleteCount}.`,
      "success"
    );

  } catch (error) {
    console.error("[DRAFTS LOADER] Ошибка:", error);
    showNotify(
      error.message || "Ошибка загрузки черновиков.",
      "error"
    );
  }
}

