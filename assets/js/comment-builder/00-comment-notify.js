/**
 * @module  00-comment-notify.js
 * @about   Модуль отображения уведомлений и статусов.
 * @purpose Отображение сообщений пользователю, обновление статусных элементов и вывод диагностической информации.
 * @author  TechLab
 * @version 1.0.0
 */

// ФУНКЦИЯ: showNotify

// НАЗНАЧЕНИЕ: Показывает пользователю уведомление заданного типа.

function showNotify(text, type) {
  const el = document.getElementById("notification");
  if (!el) return;

  const logoutDisabled = window.commentFormLocked ? "disabled" : "";

  el.classList.remove("notify-success", "notify-error", "notify-blue");

  // Строка SVG-кода иконки Bootstrap Icons box-arrow-right
  const svgIcon = "<svg xmlns='http://w3.org' width='21' height='21' fill='currentColor' class='bi bi-box-arrow-right' viewBox='0 0 16 16'>" +
                    "<path fill-rule='evenodd' d='M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z'/>" +
                    "<path fill-rule='evenodd' d='M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z'/>" +
                  "</svg>";

  if (type === "success") {
    el.classList.add("notify-success");
    el.innerHTML = "<div class='notify-flex-content'>" +
                     "<span>" + text + "</span>" +
                     "<button " + logoutDisabled + " onclick='logoutTeacher()' class='btn-logout-svg' title='Выйти из конструктора'>" + svgIcon + "</button>" +
                   "</div>";
  }
  else if (type === "error") {
    el.classList.add("notify-error");
    el.innerHTML = "<div class='notify-flex-content'>" +
                     "<span>" + text + "</span>" +
                     "<button " + logoutDisabled + " onclick='logoutTeacher()' class='btn-logout-svg' title='Выйти из конструктора'>" + svgIcon + "</button>" +
                   "</div>";
  }
  else if (type === "info") {
    el.classList.add("notify-blue");
    el.innerHTML = "<div class='notify-flex-content'>" +
                     "<span>" + text + "</span>" +
                     "<button " + logoutDisabled + " onclick='logoutTeacher()' class='btn-logout-svg' title='Выйти из конструктора'>" + svgIcon + "</button>" +
                   "</div>";
  }
}