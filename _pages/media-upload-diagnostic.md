---
layout: page
title: Диагностика загрузки медиа
permalink: /media-upload-diagnostic/
---

<div style="max-width: 600px; margin: 30px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px;">
  <h3>Тест загрузки файла</h3>

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

  <pre
    id="upload-result"
    style="white-space: pre-wrap; overflow-wrap: anywhere; margin-top: 20px;"
  ></pre>
</div>

<script>
(() => {
  const button = document.getElementById("upload-button");
  const input = document.getElementById("test-file");
  const output = document.getElementById("upload-result");

  const owner = "eaststandart";
  const repo = "techlab-comment-builder";

  function log(data) {
    output.textContent = JSON.stringify(data, null, 2);
  }

  async function fileToBase64(file) {
    const buffer = await file.arrayBuffer();
    const bytes = new Uint8Array(buffer);
    let binary = "";

    const chunkSize = 0x8000;

    for (let i = 0; i < bytes.length; i += chunkSize) {
      binary += String.fromCharCode(
        ...bytes.subarray(i, i + chunkSize)
      );
    }

    return btoa(binary);
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

    button.disabled = true;
    output.textContent = "Подготовка файла...";

    try {
      const content = await fileToBase64(file);
      const extension = file.name.includes(".")
        ? file.name.split(".").pop().toLowerCase()
        : "bin";

      const fileName = `diagnostic-upload-${Date.now()}.${extension}`;
      const path = `_input/${fileName}`;

      output.textContent = "Отправка запроса в GitHub...";

      const response = await fetch(
        `https://api.github.com/repos/${owner}/${repo}/contents/${path}`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            Accept: "application/vnd.github+json",
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            message: `Diagnostic upload: ${fileName}`,
            content
          })
        }
      );

      const result = await response.json().catch(() => ({}));

      log({
        status: response.status,
        message: result.message,
        requestId: response.headers.get("x-github-request-id"),
        fileName,
        fileSize: file.size,
        base64Length: content.length,
        path: result.content?.path,
        sha: result.content?.sha
      });

    } catch (error) {
      log({
        error: error.message
      });
    } finally {
      button.disabled = false;
    }
  });
})();
</script>
