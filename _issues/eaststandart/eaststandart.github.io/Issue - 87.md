---
title: "[Сайт] Интеграция с Telegram Bot API для уведомлений родителей"
number: 87
state: "open"
type: "issue"
created: "30.09.2026, 11:42:46"
updated: "27.11.2026, 19:37:22"
url: "https://github.com/eaststandart/eaststandart.github.io/issues/87"
opened_by: "eaststandart"
assignees: []
labels: ["site"]
updateMode: "none"
allowDelete: true
---

# [Сайт] Интеграция с Telegram Bot API для уведомлений родителей
### 🎯 Цель задачи
Реализовать автоматическую отправку уведомлений о присутствии/отсутствии детей на занятиях в родительский чат Telegram сразу после отправки формы преподавателем.

### ⚙️ Техническая схема работы (API Workflow)
text
Преподаватель отправляет форму ➔ Формируется коммит в репозиторий ➔ Скрипт GitHub Actions перехватывает пуш ➔ Шлет POST-запрос на Telegram API ➔ Родители получают мгновенное push-уведомление.


### 📋 Чек-лист разработки
- [ ] Создать Telegram-бота через @BotFather и получить токен.
- [ ] Добавить токен бота в секреты репозитория (GitHub Secrets ➔ TELEGRAM_BOT_TOKEN).
- [ ] Разработать скрипт автоматизации .github/workflows/telegram-notify.yml.
- [ ] Настроить парсинг входящих данных из JSON/Markdown файлов журнала.
- [ ] Протестировать отправку тестового push-уведомления при коммите.

### 🔗 Полезные ресурсы
* Документация: https://telegram.org
* Базовый URL для запросов: https://telegram.org secrets.TELEGRAM_BOT_TOKEN /sendMessage


