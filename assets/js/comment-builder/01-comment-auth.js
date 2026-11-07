/**
 * @module  01-comment-auth.js
 * @about   Модуль авторизации и контроля доступа.
 * @purpose Автоматический вход по токену, проверка прав через API GitHub и запуск контура идентификации преподавателя.
 * @author  TechLab
 * @version 1.0.0
 */

// Настройки репозитория и проверка пароля преподавателя
const repo_owner = "eaststandart";
const repo_name = "techlab-comment-builder";
const allowedTeachers = ["eaststandart", "eastemitting"];

let accessToken = localStorage.getItem("github_comment_token");
let studentsData = {}; // Оставляем пустой объект для совместимости структур данных
let isRobotChecked = false; // Возвращаем в оперативную память для корректного сброса при Ctrl+F5

// Автоматический вход, если ключ уже сохранен в браузере
document.addEventListener("DOMContentLoaded", () => {
  if (accessToken) {
    showJournal();
  }
});

// Функция проверки введенного пароля
function submitToken() {
  const tokenValue = document.getElementById("token-input").value.trim();
  if (!tokenValue) {
    alert("Пожалуйста, введите ключ доступа!");
    return;
  }

  document.getElementById("btn-login").disabled = true;
  document.getElementById("btn-login").innerText = "Проверка пароля...";

  fetch("https://api.github.com/user", {
    headers: { "Authorization": `token ${tokenValue}` }
  })
  .then(response => {
    if (response.ok) {
      // Забираем логин пользователя прямо из ответа Гитхаба и проверяем белый список
      response.json().then(userData => {
        const userLogin = userData.login;
        
        if (!allowedTeachers.includes(userLogin)) {
          alert(`Доступ запрещен!\nПользователь "${userLogin}" не имеет прав доступа к Конструктору.`);
          document.getElementById("btn-login").disabled = false;
          document.getElementById("btn-login").innerText = "🔓 Подключить конструктор";
          return;
        }

        localStorage.setItem("github_comment_token", tokenValue);
        localStorage.setItem("github_comment_logged_user", userLogin);
        accessToken = tokenValue;
        showJournal();
      });
    } else {
      alert("Неверный ключ доступа! Проверьте символы.");
      document.getElementById("btn-login").disabled = false;
      document.getElementById("btn-login").innerText = "🔓 Подключить конструктор";
    }
  })
  .catch(err => {
    console.error(err);
    alert("Ошибка сети. Проверьте интернет-соединение.");
    document.getElementById("btn-login").disabled = false;
    document.getElementById("btn-login").innerText = "🔓 Подключить конструктор";
  });
}

function showJournal() {
  document.getElementById("auth-section").classList.add("hidden");
  document.getElementById("journal-section").classList.remove("hidden");

  // СКРЫВАЕМ ИНСТРУКЦИЮ ПОСЛЕ УСПЕШНОГО ВХОДА
  const instr = document.getElementById("instructions-section");
  if (instr) instr.classList.add("hidden");

  // При входе сначала запускаем жесткий однократный контур физической идентификации токена
  checkTeacherAuthorization();
}

function logoutTeacher() {
  if (confirm("Вы уверены, что хотите выйти из конструктора и сменить ключ доступа?")) {
    localStorage.removeItem("github_comment_token");
    localStorage.removeItem("github_comment_robot_ok"); // Полная зачистка кэша
    localStorage.removeItem("github_comment_logged_user");
    accessToken = null;

    // ПОКАЗЫВАЕМ ИНСТРУКЦИЮ ПРИ ВЫХОДЕ
    const instr = document.getElementById("instructions-section");
    if (instr) instr.classList.remove("hidden");

    window.location.reload();
  }
}

// ФУНКЦИЯ №1: Физическая идентификация токена преподавателя (Срабатывает СТРОГО 1 раз на старте)
function checkTeacherAuthorization() {
  showNotify("Идентификация пользователя...", "success");

  // Параллельный замок: таймер не менее 2 секунд и реальный сетевой fetch-запрос к GitHub
  const timerPromise = new Promise(resolve => setTimeout(resolve, 2000));
  const networkPromise = fetch("https://api.github.com/user", {
    headers: { "Authorization": `token ${accessToken}` }
  }).then(r => {
    if (!r.ok) throw new Error("AUTH_FAILED");
    return r.json();
  });

  Promise.all([timerPromise, networkPromise])
  .then(([_, userData]) => {
    const userLogin = userData.login;
    
    // Вторичная проверка белого списка при автоматическом входе из localStorage
    if (!allowedTeachers.includes(userLogin)) {
      showNotify("Критическая ошибка: доступ заблокирован правообладателем.", "error");
      localStorage.removeItem("github_comment_token");
      return;
    }

    localStorage.setItem("github_comment_logged_user", userLogin);
    
    // Идентификация успешно завершена! Передаем управление следующему контуру (будет в модуле 02)
    if (typeof loadCommentDraftsFromApi === "function") {
      loadCommentDraftsFromApi();
    } else {
      showNotify("Конструктор успешно загружен!", "success");
      setTimeout(() => { showNotify("👨‍🏫 Преподаватель: " + userLogin, "info"); }, 2000);
    }
  })
  .catch(err => {
    console.error(err);
    showNotify("Ошибка идентификации токена. Проверьте соединение или ключ на GitHub.", "error");
  });
}
