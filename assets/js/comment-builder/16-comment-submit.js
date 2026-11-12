/**
 * @module  16-comment-submit.js
 * @about   Модуль обработки отправки комментария и сохранения черновика.
 * @purpose Проверка формы, координация сохранения Markdown и загрузки медиафайлов, обработка публикации или удаления черновика и завершение операции.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: handleCommentSubmit
// НАЗНАЧЕНИЕ: Проверяет форму, загружает медиафайлы и сохраняет комментарий или черновик.
async function handleCommentSubmit() {
  if (window.commentFormLocked) return;

  let markdownSaved = false;
  let mediaUploadCompleted = false;
  let uploadedMediaCount = 0;
  let mediaUploadErrorCount = 0;
  let keepFormLocked = false;

  try {
    if (!accessToken) {
      throw new Error("Нет активного токена!");
    }

    // Для нового комментария и выбранного черновика проверяем дату из поля формы.
    const dateToValidate = document.getElementById("target-date")?.value;

    if (!isValidCommentDate(dateToValidate)) {
      throw new Error("Неверный формат Даты");
    }

    const session = getCommentUploadSession();

    if (!session.discussion || !/^\d+$/.test(session.discussion)) {
      throw new Error("Укажите номер обсуждения");
    }

    if (!session.teacher) {
      throw new Error("Преподаватель не определён");
    }

    const validationError = validateCommentForm();
    if (validationError) {
      throw new Error(validationError);
    }

    setCommentOperationLock(true);
    setFormLock(true, "Подготовка комментария...");

    // При каждом сохранении обновляем только timestamp Front Matter.
    // Идентификатор сессии для имён файлов остаётся постоянным.
    const previousTimestamp = Number(
      currentCommentDraft?.timestamp || session.frontMatterTimestamp || 0
    );
    session.frontMatterTimestamp = String(
      Math.max(Math.floor(Date.now() / 1000), previousTimestamp + 1)
    );

    // Сначала назначаем имена новым файлам и сохраняем ссылки на них в Markdown.
    prepareLocalMediaFileNames(session);
    const markdown = buildCommentMarkdown(session);

    showNotify("Сохранение Markdown...", "success");
    const saved = await saveCommentMarkdown(session, markdown);
    markdownSaved = true;
    if (typeof commitDraftDeleteState === "function") commitDraftDeleteState();

    if (currentCommentDraft) {
      currentCommentDraft.date = session.date;
      currentCommentDraft.timestamp = session.frontMatterTimestamp;
    }

    // После сохранения манифеста загружаем физические файлы.
    showNotify("Загрузка новых медиафайлов...", "success");
    const uploadResult = await uploadLocalMediaFiles(session);
    uploadedMediaCount = uploadResult.uploaded;
    mediaUploadErrorCount = uploadResult.errors.length;
    mediaUploadCompleted = true;

    // После загрузки файлов обновляем Front Matter ещё раз:
    // это запускает workflow повторно, когда комплект уже собран.
    if (uploadResult.uploaded > 0) {
      const uploadedTimestamp = Number(session.frontMatterTimestamp || 0);
      session.frontMatterTimestamp = String(
        Math.max(Math.floor(Date.now() / 1000), uploadedTimestamp + 1)
      );

      if (currentCommentDraft) {
        currentCommentDraft.timestamp = session.frontMatterTimestamp;
      }

      const completedMarkdown = buildCommentMarkdown(session);
      const latestSha = saved.result?.content?.sha || null;
      await saveCommentMarkdown(session, completedMarkdown, latestSha);
    }

    const unresolvedMediaCount = [
      document.getElementById("photos-meta-container"),
      document.getElementById("videos-meta-container")
    ].filter(Boolean).reduce((total, container) => {
      const blocks = Array.from(container.querySelectorAll(".media-sub-block"));
      return total + blocks.reduce((count, block) => {
        const files = Array.isArray(block.mediaFiles) ? block.mediaFiles : [];
        return count + files.filter(file => file.kind === "missing").length;
      }, 0);
    }, 0);

    const deleteRequested = document.getElementById("delete-draft-flag")?.checked === true;
    const published = !deleteRequested && document.getElementById("publish-now-flag")?.checked === true;
    const saveMessage = deleteRequested
      ? "Черновик удалён!"
      : published
        ? "Комментарий сохранён!"
        : "Черновик сохранён!";

    // Убираем опубликованный комментарий из списка только после полной комплектации.
    if (published && unresolvedMediaCount === 0 && currentCommentDraft && Array.isArray(mockDrafts)) {
      mockDrafts = mockDrafts.filter(draft => draft.id !== saved.fileName);
      if (typeof refreshDraftSelect === "function") refreshDraftSelect();
    }

    if (uploadResult.errors.length || unresolvedMediaCount > 0) {
      showNotify(
        `Markdown сохранён | Медиа: загружены ${uploadResult.uploaded}, ошибок ${uploadResult.errors.length}`,
        "error"
      );
      if (uploadResult.errors.length) {
        console.warn("[COMMENT SAVE] Не загружены медиафайлы:", uploadResult.errors);
      }
    } else {
      showNotify(saveMessage, "success");

      console.log("[COMMENT SAVE] Файл сохранён:", saved.fileName);
      console.log("[COMMENT SAVE] Загружено новых медиафайлов:", uploadResult.uploaded);

      keepFormLocked = true;
      finishCommentFormOperation(true);
    }

  } catch (error) {
    console.error("[COMMENT SAVE] Ошибка:", error);
    let message = error.message || "Ошибка сохранения комментария.";
    if (message === "Failed to fetch") message = "Загрузка не удалась!";

    if (markdownSaved && !mediaUploadCompleted) {
      mediaUploadErrorCount = Math.max(mediaUploadErrorCount, 1);
      message = `Markdown сохранён | Медиа: загружены ${uploadedMediaCount}, ошибок ${mediaUploadErrorCount}`;
    } else if (markdownSaved && mediaUploadCompleted) {
      message = `Markdown не обновлён | Медиа: загружены ${uploadedMediaCount}, ошибок ${mediaUploadErrorCount}`;
    }

    showNotify(message, "error");

  } finally {
    if (!keepFormLocked) setFormLock(false);
    setCommentOperationLock(false);
  }
}
