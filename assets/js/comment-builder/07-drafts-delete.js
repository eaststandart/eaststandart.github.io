/**
 * @module  11-drafts-delete.js
 * @about   Управление отметкой удаления черновика.
 * @purpose Отображение, переключение и сохранение состояния published: delete.
 * @author  TechLab
 * @version 1.0.0
 */

let draftDeleteBaselinePublished = false;

// ФУНКЦИЯ: ensureDraftDeleteControl
// НАЗНАЧЕНИЕ: Создаёт третий чекбокс с иконкой корзины рядом с существующими флагами.
function ensureDraftDeleteControl() {
  const checkbox = document.getElementById("delete-draft-flag");
  if (!checkbox) return null;

  if (checkbox.dataset.deleteHandlerAttached !== "1") {
    checkbox.addEventListener("change", handleDraftDeleteChange);
    checkbox.dataset.deleteHandlerAttached = "1";
  }

  return document.getElementById("delete-draft-option");
}

// ФУНКЦИЯ: setDraftDeleteState
// НАЗНАЧЕНИЕ: Устанавливает состояние отметки для выбранного черновика.
function setDraftDeleteState(draft) {
  const checkbox = document.getElementById("delete-draft-flag");
  if (!checkbox) return;

  const status = String(draft?.published ?? "false").toLowerCase();
  draftDeleteBaselinePublished = status === "true";
  checkbox.checked = status === "delete";
  checkbox.disabled = !draft;
  if (checkbox.hasAttribute("data-lock-disabled")) {
    checkbox.dataset.lockDisabled = draft ? "0" : "1";
  }
}

// ФУНКЦИЯ: handleDraftDeleteChange
// НАЗНАЧЕНИЕ: При снятии отметки возвращает исходный статус до сохранения.
function handleDraftDeleteChange() {
  const checkbox = document.getElementById("delete-draft-flag");
  if (!checkbox || !currentCommentDraft) {
    if (checkbox) checkbox.checked = false;
    return;
  }

  const publishFlag = document.getElementById("publish-now-flag");

  if (checkbox.checked) {
    if (publishFlag) publishFlag.checked = false;
  } else if (publishFlag) {
    publishFlag.checked = draftDeleteBaselinePublished;
  }

  if (typeof updatePublishLabel === "function") updatePublishLabel();
}

// ФУНКЦИЯ: commitDraftDeleteState
// НАЗНАЧЕНИЕ: Фиксирует новое исходное состояние после успешного сохранения Markdown.
function commitDraftDeleteState() {
  if (!currentCommentDraft) return;

  const deleteRequested =
    document.getElementById("delete-draft-flag")?.checked === true;
  const published =
    document.getElementById("publish-now-flag")?.checked === true;

  currentCommentDraft.published = deleteRequested
    ? "delete"
    : String(published);

  draftDeleteBaselinePublished = deleteRequested ? false : published;

  const option = Array.from(
    document.getElementById("draft-select")?.options || []
  ).find(item => item.value === currentCommentDraft.id);

  if (option) {
    option.classList.toggle("is-delete-requested", deleteRequested);
    if (deleteRequested) {
      option.classList.remove("is-published-complete");
    }
  }
}

// Отметка публикации и отметка удаления взаимоисключающие.
document.getElementById("publish-now-flag")?.addEventListener("change", () => {
  const deleteCheckbox = document.getElementById("delete-draft-flag");
  if (deleteCheckbox?.checked) {
    deleteCheckbox.checked = false;
    if (typeof updatePublishLabel === "function") updatePublishLabel();
  }
});

ensureDraftDeleteControl();
console.log("[DRAFT DELETE] Модуль 11 загружен");
