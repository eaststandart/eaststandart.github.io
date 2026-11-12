/**
 * @module  15-comment-github-save.js
 * @about   Модуль сохранения Markdown-файлов через GitHub API.
 * @purpose Создание и обновление файлов комментариев и черновиков через GitHub Contents API, проверка актуальной версии файла и повторные попытки при временных ошибках.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: waitBeforeRetry
// НАЗНАЧЕНИЕ: Ожидает перед повторной попыткой сохранения после временной ошибки.
function waitBeforeRetry(seconds, attempt) {
  return new Promise(resolve => {
    let remaining = seconds;

    showNotify(
      `Ошибка сети. Повтор ${attempt}/3 через ${remaining} сек.`,
      "error"
    );

    const timer = setInterval(() => {
      remaining--;

      if (remaining <= 0) {
        clearInterval(timer);
        resolve();
        return;
      }

      showNotify(
        `Ошибка сети. Повтор ${attempt}/3 через ${remaining} сек.`,
        "error"
      );
    }, 1000);
  });
}

// ФУНКЦИЯ: saveCommentMarkdownOnce
// НАЗНАЧЕНИЕ: Выполняет одну попытку создания или обновления Markdown-файла в GitHub.
async function saveCommentMarkdownOnce(url, headers, fileName, markdown, knownSha = null) {
  // ФУНКЦИЯ: getCurrentFile
  // НАЗНАЧЕНИЕ: Получает актуальную версию Markdown-файла и его SHA.
  async function getCurrentFile() {
    const response = await fetch(`${url}?ref=main&_=${Date.now()}`, {
      method: "GET",
      headers,
      cache: "no-store"
    });

    if (response.status === 404) return null;

    if (!response.ok) {
      const error = new Error(`Ошибка проверки файла: HTTP ${response.status}`);
      error.status = response.status;
      throw error;
    }

    return await response.json();
  }

  // ФУНКЦИЯ: putFile

  // НАЗНАЧЕНИЕ: Создаёт или обновляет Markdown-файл через GitHub Contents API.
  async function putFile(sha) {
    const payload = {
      message: `${sha ? "Update" : "Create"} comment: ${fileName}`,
      content: commentToBase64(markdown),
      branch: "main"
    };

    if (sha) payload.sha = sha;

    return await fetch(url, {
      method: "PUT",
      headers,
      body: JSON.stringify(payload)
    });
  }

  const existingFile = knownSha ? { sha: knownSha } : await getCurrentFile();
  let sha = existingFile?.sha || null;

  if (
    existingFile?.content &&
    decodeGithubContent(existingFile.content) === markdown
  ) {
    return {
      fileName,
      result: existingFile,
      alreadySaved: true
    };
  }

  let response = await putFile(sha);

  if (response.status === 409) {
    const latestFile = await getCurrentFile();

    if (!latestFile) {
      response = await putFile(null);
    } else {
      if (latestFile.content &&
          decodeGithubContent(latestFile.content) === markdown) {
        return {
          fileName,
          result: latestFile,
          alreadySaved: true
        };
      }

      response = await putFile(latestFile.sha);
    }
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const error = new Error(
      errorData.message || `Комментарий не сохранён: HTTP ${response.status}`
    );
    error.status = response.status;
    throw error;
  }

  return {
    fileName,
    result: await response.json()
  };
}

// ФУНКЦИЯ: saveCommentMarkdown
// НАЗНАЧЕНИЕ: Сохраняет Markdown-файл с повторными попытками при временных ошибках.
async function saveCommentMarkdown(session, markdown, knownSha = null) {
  const fileName = currentCommentDraft
    ? currentCommentDraft.id
    : `${session.date}-${session.timestamp}_discussion_${session.discussion}_${session.teacher}.md`;

  const url =
    `https://api.github.com/repos/${repo_owner}/${repo_name}/contents/_input/${encodeURIComponent(fileName)}`;

  const headers = {
    Authorization: `Bearer ${accessToken}`,
    Accept: "application/vnd.github+json",
    "Content-Type": "application/json"
  };

  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return await saveCommentMarkdownOnce(
        url, headers, fileName, markdown,
        attempt === 1 ? knownSha : null
      );

    } catch (error) {
      const isNetworkError =
        error instanceof TypeError ||
        (error.status >= 500 && error.status <= 599);

      if (!isNetworkError || attempt === 3) {
        throw error;
      }

      await waitBeforeRetry(60, attempt + 1);
    }
  }
}
