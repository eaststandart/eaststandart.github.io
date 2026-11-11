/**
 * @module  08-comment-lock.js
 * @about   Модуль блокировки интерфейса конструктора.
 * @purpose Блокировка и разблокировка рабочей области на время выполнения операций.
 * @author  TechLab
 * @version 1.0.0
 */

// Единое состояние блокировки для всех модулей
window.commentFormLocked = false;

// ФУНКЦИЯ: setFormLock
// НАЗНАЧЕНИЕ: Блокировка и разблокировка рабочей области
function setFormLock(isLocked, message = "") {
  const section = document.getElementById("journal-section");

  if (!section) return;

  window.commentFormLocked = Boolean(isLocked);

  section.classList.toggle(
    "is-locked",
    window.commentFormLocked
  );

  const controls = section.querySelectorAll(
    "input, select, textarea, button"
  );

  controls.forEach(control => {
    if (control.closest("#notification")) return;

    if (window.commentFormLocked) {
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
    showNotify(message, "success");
  }
}

// ФУНКЦИЯ: finishCommentFormOperation
// НАЗНАЧЕНИЕ: Завершает успешную операцию, показывает статус преподавателя и только затем разблокирует форму.
async function finishCommentFormOperation(resetForm = false) {
  const wait = milliseconds =>
    new Promise(resolve => setTimeout(resolve, milliseconds));

  await wait(2000);

  if (resetForm && typeof resetCommentForm === "function") {
    resetCommentForm();
    await wait(2000);
  }

  const teacher = localStorage.getItem("github_comment_logged_user");
  if (teacher) {
    showNotify("👨‍🎓 Преподаватель: " + teacher, "info");
  }

  setFormLock(false);
}