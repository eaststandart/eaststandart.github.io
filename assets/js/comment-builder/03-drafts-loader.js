/**
 * @module  03-drafts-loader.js
 * @about   Загрузка списка черновиков из GitHub API.
 * @purpose 
 * @author  TechLab
 * @version 1.0.0
 */

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

    const parsedDrafts = await Promise.all(fetchPromises);

    mockDrafts = parsedDrafts.filter(d =>
      d !== null &&
      String(d.published).toLowerCase() === "false"
    );

    if (typeof refreshDraftSelect === "function") {
      refreshDraftSelect();
    }

    if (mockDrafts.length === 0) {
      showNotify("Черновики не обнаружены.", "success");
      return;
    }

    showNotify(
      `Загружено черновиков: ${mockDrafts.length}.`,
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

