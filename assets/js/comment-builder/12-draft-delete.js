/**
 * @module  12-draft-delete.js
 * @about   Управление отметкой удаления черновика.
 * @purpose Отображение, переключение и сохранение состояния published: delete.
 * @author  TechLab
 * @version 1.0.0
 */

let draftDeleteBaselinePublished = false;

// ФУНКЦИЯ: ensureDraftDeleteControl
// НАЗНАЧЕНИЕ: Создаёт третий чекбокс с иконкой корзины рядом с существующими флагами.
function ensureDraftDeleteControl() {
  const publishOption = document.querySelector(".publish-option");
  if (!publishOption) return null;

  let label = document.getElementById("delete-draft-option");
  if (label) return label;

  label = document.createElement("label");
  label.id = "delete-draft-option";
  label.className = "publish-delete-option";
  label.title = "Пометить черновик на удаление";

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.id = "delete-draft-flag";
  checkbox.disabled = true;
  checkbox.addEventListener("change", handleDraftDeleteChange);

  const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  icon.setAttribute("viewBox", "0 0 24 24");
  icon.setAttribute("width", "18");
  icon.setAttribute("height", "18");
  icon.setAttribute("fill", "none");
  icon.setAttribute("stroke", "currentColor");
  icon.setAttribute("stroke-width", "1.8");
  icon.setAttribute("stroke-linecap", "round");
  icon.setAttribute("stroke-linejoin", "round");
  icon.setAttribute("aria-hidden", "true");

  const paths = [
    "M3 6h18",
    "M8 6V4h8v2",
    "M19 6l-1 14H6L5 6",
    "M10 11v5",
    "M14 11v5"
  ];

  paths.forEach(d => {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", d);
    icon.appendChild(path);
  });

  label.append(checkbox, icon);

  const botOption = document.querySelector(".publish-bot-option");
  if (botOption) {
    botOption.insertAdjacentElement("afterend", label);
  } else {
    publishOption.appendChild(label);
  }

  return label;
}

// ФУНКЦИЯ: setDraftDeleteState
// НАЗНАЧЕНИЕ: Восстанавливает отметку удаления и исходный статус выбранного черновика.
function setDraftDeleteState(draft) {
  const checkbox = document.getElementById("delete-draft-flag");
  if (!checkbox) return;

  const status = String(draft?.published ?? "false").toLowerCase();
  draftDeleteBaselinePublished = status === "true";

  checkbox.checked = status === "delete";
  checkbox.disabled = !draft;
}

// ФУНКЦИЯ: handleDraftDeleteChange
// НАЗНАЧЕНИЕ: При снятии отметки возвращает исходный статус до сохранения.
function handleDraftDeleteChange() {
  const checkbox = document.getElementById("delete-draft-flag");
  if (!checkbox || !currentCommentDraft) {
    if (checkbox) checkbox.checked = false;
    return;
  }

  if (!checkbox.checked) {
    const publishFlag = document.getElementById("publish-now-flag");
    if (publishFlag) {
      publishFlag.checked = draftDeleteBaselinePublished;
      if (typeof updatePublishLabel === "function") updatePublishLabel();
    }
  }
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

  const option = document.querySelector(
    `#draft-select option[value="${CSS.escape(currentCommentDraft.id)}"]`
  );

  if (option) {
    option.classList.toggle("is-delete-requested", deleteRequested);
  }
}

// Подключение управления к существующим функциям без изменения их основной логики.
const originalUpdatePublishLabelForDelete = updatePublishLabel;
updatePublishLabel = function(...args) {
  originalUpdatePublishLabelForDelete.apply(this, args);
  ensureDraftDeleteControl();
  const checkbox = document.getElementById("delete-draft-flag");
  if (checkbox) checkbox.disabled = !currentCommentDraft;
};

const originalLoadDraftDataForDelete = loadDraftData;
loadDraftData = function(draftId, ...args) {
  const result = originalLoadDraftDataForDelete.call(this, draftId, ...args);
  const draft = mockDrafts.find(item => item.id === draftId) || null;
  setDraftDeleteState(draft);
  return result;
};

const originalToggleDraftBehaviorForDelete = toggleDraftBehavior;
toggleDraftBehavior = async function(...args) {
  const result = await originalToggleDraftBehaviorForDelete.apply(this, args);
  if (!document.getElementById("is-draft-mode")?.checked) {
    setDraftDeleteState(null);
  } else if (!currentCommentDraft) {
    setDraftDeleteState(null);
  }
  return result;
};

const originalResetCommentFormForDelete = resetCommentForm;
resetCommentForm = function(...args) {
  const result = originalResetCommentForm.apply(this, args);
  setDraftDeleteState(null);
  return result;
};

const originalRefreshDraftSelectForDelete = refreshDraftSelect;
refreshDraftSelect = function(...args) {
  const result = originalRefreshDraftSelect.apply(this, args);

  mockDrafts.forEach(draft => {
    if (String(draft.published).toLowerCase() !== "delete") return;
    const option = Array.from(
      document.getElementById("draft-select")?.options || []
    ).find(item => item.value === draft.id);
    if (option) option.classList.add("is-delete-requested");
  });

  return result;
};

ensureDraftDeleteControl();
console.log("[DRAFT DELETE] Модуль 12 загружен");
