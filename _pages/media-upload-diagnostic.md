---
layout: page
title: Диагностика загрузки медиа
permalink: /media-upload-diagnostic/
---

<div style="max-width: 680px; margin: 30px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px;">
  <h3>Тест загрузки файла</h3>

  <label for="upload-method" style="display:block; margin:16px 0 6px;">Способ загрузки</label>
  <select id="upload-method" style="display:block; width:100%; padding:9px; margin-bottom:18px;">
    <option value="contents">Contents API — текущий способ (PUT)</option>
    <option value="git-database">Git Database API — Blob → Tree → Commit → Ref</option>
  </select>

  <input
    type="file"
    id="test-file"
    style="display: block; width: 100%; margin: 20px 0;"
  >

  <button
    type="button"
    id="upload-button"
    style="padding: 10px 20px; cursor: pointer;"
  >
    Загрузить файл
  </button>

  <p style="font-size: 13px; color: #666; margin-top: 14px;">
    Оба способа передают файл в Base64. Второй способ проверяет другой набор GitHub API, но сам по себе не уменьшает объём передачи.
  </p>

  <pre
    id="upload-result"
    style="white-space: pre-wrap; overflow-wrap: anywhere; margin-top: 20px;"
  ></pre>
</div>

<script>
(() => {
  const button = document.getElementById("upload-button");
  const input = document.getElementById("test-file");
  const methodSelect = document.getElementById("upload-method");
  const output = document.getElementById("upload-result");

  const owner = "eaststandart";
  const repo = "techlab-comment-builder";
  const branch = "main";
  const api = `https://api.github.com/repos/${owner}/${repo}`;

  function log(data) {
    output.textContent = JSON.stringify(data, null, 2);
  }

  async function fileToBase64(file) {
    const buffer = await file.arrayBuffer();
    const bytes = new Uint8Array(buffer);
    let binary = "";
    const chunkSize = 0x8000;

    for (let i = 0; i < bytes.length; i += chunkSize) {
      binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
    }

    return btoa(binary);
  }

  async function githubRequest(stage, url, token, options = {}) {
    const started = performance.now();
    let response;

    try {
      response = await fetch(url, {
        ...options,
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json",
          ...options.headers
        }
      });
    } catch (error) {
      const details = {
        stage,
        error: error.message,
        durationMs: Math.round(performance.now() - started)
      };
      throw Object.assign(new Error(`Сбой сети на этапе ${stage}`), { details });
    }

    const text = await response.text();
    let data = {};
    try {
      data = text ? JSON.parse(text) : {};
    } catch {
      data = { rawResponse: text };
    }

    const details = {
      stage,
      status: response.status,
      durationMs: Math.round(performance.now() - started),
      requestId: response.headers.get("x-github-request-id"),
      message: data.message
    };

    if (!response.ok) {
      throw Object.assign(
        new Error(`${stage}: HTTP ${response.status} ${data.message || response.statusText}`),
        { details, response: data }
      );
    }

    return { data, details };
  }

  async function uploadWithContentsApi(fileName, content, token) {
    const path = `_input/${fileName}`;
    const result = await githubRequest(
      "Contents API PUT",
      `${api}/contents/${path}`,
      token,
      {
        method: "PUT",
        body: JSON.stringify({
          message: `Diagnostic upload: ${fileName}`,
          content
        })
      }
    );

    return {
      path: result.data.content?.path,
      sha: result.data.content?.sha,
      commitSha: result.data.commit?.sha,
      steps: [result.details]
    };
  }

  async function uploadWithGitDatabaseApi(fileName, content, token) {
    const steps = [];

    const refResult = await githubRequest(
      "Получение текущей ветки",
      `${api}/git/ref/heads/${branch}`,
      token
    );
    steps.push(refResult.details);
    const parentSha = refResult.data.object.sha;

    const parentCommitResult = await githubRequest(
      "Получение базового коммита и дерева",
      `${api}/git/commits/${parentSha}`,
      token
    );
    steps.push(parentCommitResult.details);
    const baseTreeSha = parentCommitResult.data.tree.sha;

    const blobResult = await githubRequest(
      "Создание Blob",
      `${api}/git/blobs`,
      token,
      {
        method: "POST",
        body: JSON.stringify({
          content,
          encoding: "base64"
        })
      }
    );
    steps.push(blobResult.details);
    const blobSha = blobResult.data.sha;

    const treeResult = await githubRequest(
      "Создание Tree",
      `${api}/git/trees`,
      token,
      {
        method: "POST",
        body: JSON.stringify({
          base_tree: baseTreeSha,
          tree: [{
            path: `_input/${fileName}`,
            mode: "100644",
            type: "blob",
            sha: blobSha
          }]
        })
      }
    );
    steps.push(treeResult.details);

    const commitResult = await githubRequest(
      "Создание Commit",
      `${api}/git/commits`,
      token,
      {
        method: "POST",
        body: JSON.stringify({
          message: `Diagnostic upload: ${fileName}`,
          tree: treeResult.data.sha,
          parents: [parentSha]
        })
      }
    );
    steps.push(commitResult.details);

    const updateRefResult = await githubRequest(
      "Обновление ветки main",
      `${api}/git/refs/heads/${branch}`,
      token,
      {
        method: "PATCH",
        body: JSON.stringify({
          sha: commitResult.data.sha,
          force: false
        })
      }
    );
    steps.push(updateRefResult.details);

    return {
      path: `_input/${fileName}`,
      blobSha,
      commitSha: commitResult.data.sha,
      steps
    };
  }

  button.addEventListener("click", async () => {
    const file = input.files[0];

    if (!file) {
      log({ error: "Сначала выбери файл." });
      return;
    }

    const token = localStorage.getItem("github_comment_token");
    if (!token) {
      log({ error: "Токен github_comment_token не найден." });
      return;
    }

    const method = methodSelect.value;
    const extension = file.name.includes(".")
      ? file.name.split(".").pop().toLowerCase()
      : "bin";
    const fileName = `diagnostic-${method}-${Date.now()}.${extension}`;

    button.disabled = true;
    methodSelect.disabled = true;
    input.disabled = true;
    output.textContent = "Подготовка файла...";

    const started = performance.now();

    try {
      const content = await fileToBase64(file);
      output.textContent = "Загрузка в GitHub...";

      const result = method === "git-database"
        ? await uploadWithGitDatabaseApi(fileName, content, token)
        : await uploadWithContentsApi(fileName, content, token);

      log({
        success: true,
        method: method === "git-database" ? "Git Database API" : "Contents API",
        fileName,
        fileSize: file.size,
        base64Length: content.length,
        jsonContentLength: JSON.stringify({ content }).length,
        totalDurationMs: Math.round(performance.now() - started),
        ...result
      });
    } catch (error) {
      log({
        success: false,
        method: method === "git-database" ? "Git Database API" : "Contents API",
        fileName,
        fileSize: file.size,
        totalDurationMs: Math.round(performance.now() - started),
        error: error.message,
        failedStep: error.details,
        response: error.response
      });
    } finally {
      button.disabled = false;
      methodSelect.disabled = false;
      input.disabled = false;
    }
  });
})();
</script>
