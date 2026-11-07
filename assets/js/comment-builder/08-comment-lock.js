/**
 * @module  08-comment-lock.js
 * @about   Управление блокировкой интерфейса конструктора.
 * @purpose Полная блокировка рабочей области на время выполнения операций.
 * @author  TechLab
 * @version 1.0.0
 */

let isCommentFormLocked = false;

/**
 * Блокировка и разблокировка рабочей области
 */
function setFormLock(isLocked, message = "") {
  const section = document.getElementById("journal-section");

  if (!section) return;

  isCommentFormLocked = Boolean(isLocked);

  section.classList.toggle("is-locked", isCommentFormLocked);

  const controls = section.querySelectorAll(
    "input, select, textarea, button"
  );

  controls.forEach(control => {
    if (control.closest("#notification")) return;

    if (isCommentFormLocked) {
      if (!control.hasAttribute("data-lock-disabled")) {
        control.dataset.lockDisabled = control.disabled ? "1" : "0";
      }

      control.disabled = true;
    } else if (control.hasAttribute("data-lock-disabled")) {
      control.disabled = control.dataset.lockDisabled === "1";
      delete control.dataset.lockDisabled;
    }
  });

  if (message) {
    showNotify(message, "info");
  }
}