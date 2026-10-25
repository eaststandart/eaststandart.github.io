---
author: "TechLab"
layout: page
description: 
title: Журнал посещений
permalink: /discussions/
emoji: ""
---

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Конструктор Отчетов TechLab</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 20px auto; padding: 10px; background: #f9f9f9; color: #333; }
        .block { background: #fff; border: 1px solid #ccc; padding: 15px; margin-bottom: 15px; border-radius: 4px; }
        h3 { margin-top: 0; color: #555; border-bottom: 1px solid #eee; padding-bottom: 5px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; }
        input[type="text"], textarea, select { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }
        .row { display: flex; gap: 15px; align-items: center; margin-bottom: 10px; }
        .checkbox-container { display: flex; align-items: center; gap: 8px; font-weight: bold; cursor: pointer; }
        .drop-zone { border: 2px dashed #bbb; padding: 20px; text-align: center; color: #777; background: #fafafa; border-radius: 4px; margin-top: 5px; }
        .btn { background: #0076ff; color: #fff; border: none; padding: 10px 20px; font-size: 16px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; }
        .btn:hover { background: #0060d6; }
    </style>
</head>
<body>

    <h2>Унифицированная форма ввода TechLab</h2>

    <!-- БЛОК 1: ДАТА И ЧЕРНОВИКИ -->
    <div class="block">
        <h3>1. Дата публикации и Режим</h3>
        <div class="row">
            <div style="flex: 1;" id="date-field-container">
                <!-- Сюда JS будет подставлять либо ввод даты, либо выпадающий список черновиков -->
            </div>
            <div>
                <label class="checkbox-container">
                    <input type="checkbox" id="is-draft-mode" onchange="toggleDraftMode()"> 📂 Черновик
                </label>
            </div>
        </div>
    </div>

    <!-- БЛОК 2: ДИСКУССИЯ (НОМЕР ОБСУЖДЕНИЯ НА САЙТЕ) -->
    <div class="block">
        <label for="discussion-number">2. Целевая дискуссия (Номер обсуждения на сайте)</label>
        <input type="text" id="discussion-number" placeholder="Например: 83" value="83">
    </div>

    <!-- БЛОК 3: ЗАГОЛОВОК КОММЕНТАРИЯ -->
    <div class="block">
        <label for="post-title">3. Заголовок комментария</label>
        <input type="text" id="post-title" placeholder="Введите заголовок (необязательно)">
    </div>

    <!-- БЛОК 4: СОДЕРЖАТЕЛЬНАЯ ЧАСТЬ -->
    <div class="block">
        <label for="post-text">4. Описание (Основной текст отчета)</label>
        <textarea id="post-text" rows="6" placeholder="Что было сделано на занятии..."></textarea>
    </div>

    <!-- БЛОК 5: ФОТОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>5. 📸 Фотоматериалы</h3>
        <div class="drop-zone">Нажмите или перетащите сюда фотографии (.jpg, .png)</div>
    </div>

    <!-- БЛОК 6: ВИДЕОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>6. 🎥 Видеоматериалы</h3>
        <div class="drop-zone">Нажмите или перетащите сюда видеоролики (.mp4, .mov)</div>
    </div>

    <!-- БЛОК КОНТРОЛЯ: ОПУБЛИКОВАТЬ / СОХРАНИТЬ КАК ЧЕРНОВИК -->
    <div class="block" style="background: #f0f7ff; border-color: #b3d7ff;">
        <div class="row" style="justify-content: space-between; margin-bottom: 15px;">
            <label class="checkbox-container" style="color: #0056b3;">
                <input type="checkbox" id="publish-now-flag" checked> 🔥 Опубликовать сейчас (published: true)
            </label>
        </div>
        <button class="btn" onclick="generateMarkdownOutput()">Сформировать .md манифест</button>
    </div>

    <script>
        // Имитация базы данных черновиков, полученных с Гитхаба из папки _input
        const mockDrafts = [
            { id: "draft1", date: "2026-10-20", title: "Сборка каркаса корабля", text: "Сегодня собирали палубу и шпангоуты. Использовали клей и зажимы.", discussion: "83" },
            { id: "draft2", date: "2026-10-22", title: "Тест сервоприводов робота", text: "Программировали контроллер, проверили углы поворота манипулятора.", discussion: "45" }
        ];

        // Функция инициализации: при загрузке ставит текущую дату
        function initForm() {
            const container = document.getElementById("date-field-container");
            // Устанавливаем текущую дату по умолчанию в формате YYYY-MM-DD
            const today = new Date().toISOString().split('T')[0];
            container.innerHTML = `<input type="text" id="target-date" value="${today}" placeholder="YYYY-MM-DD">`;
        }

        // БЛОК 1 В ДЕЙСТВИИ: Переключение режима работы поля Даты при клике на галочку "Черновик"
        function toggleDraftMode() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const container = document.getElementById("date-field-container");
            const publishFlag = document.getElementById("publish-now-flag");

            if (isDraftMode) {
                // РЕЖИМ ЧЕРНОВИКА: Поле даты превращается в список существующих черновиков
                let selectHtml = `<select id="target-date" onchange="loadDraftData(this.value)">`;
                selectHtml += `<option value="">-- Выберите черновик для редактирования --</option>`;
                mockDrafts.forEach(draft => {
                    selectHtml += `<option value="${draft.id}">Черновик от ${draft.date} [${draft.title}]</option>`;
                });
                selectHtml += `</select>`;
                container.innerHTML = selectHtml;
                
                // Снимаем галочку публикации, так как мы открыли черновик
                publishFlag.checked = false;
            } else {
                // ОБЫЧНЫЙ РЕЖИМ: Поле превращается обратно в текстовый ввод даты
                const today = new Date().toISOString().split('T')[0];
                container.innerHTML = `<input type="text" id="target-date" value="${today}" placeholder="YYYY-MM-DD">`;
                publishFlag.checked = true;
                
                // Очищаем форму под новый чистый отчет
                document.getElementById("post-title").value = "";
                document.getElementById("post-text").value = "";
                document.getElementById("discussion-number").value = "83";
            }
        }

        // БЛОК 2 И 4 В ДЕЙСТВИИ: Загрузка СТАРЫХ данных выбранного черновика для редактирования
        function loadDraftData(draftId) {
            if (!draftId) return;
            const selectedDraft = mockDrafts.find(d => d.id === draftId);
            if (selectedDraft) {
                // Переносим старое содержание в поля формы без каких-либо принудительных дописок
                document.getElementById("post-title").value = selectedDraft.title;
                document.getElementById("post-text").value = selectedDraft.text;
                document.getElementById("discussion-number").value = selectedDraft.discussion;
            }
        }

        // Системная сборка итогового .md файла для проверки
        function generateMarkdownOutput() {
            const dateField = document.getElementById("target-date");
            let finalDate = dateField.value;
            
            // Если выбран черновик, вытаскиваем его реальную дату
            if (document.getElementById("is-draft-mode").checked) {
                const selectedDraft = mockDrafts.find(d => d.id === dateField.value);
                finalDate = selectedDraft ? selectedDraft.date : "2026-10-25";
            }

            const discussion = document.getElementById("discussion-number").value;
            const title = document.getElementById("post-title").value;
            const text = document.getElementById("post-text").value;
            const publishNow = document.getElementById("publish-now-flag").checked;

            // Конструируем итоговый вид текстового файла манифеста
            let md = `---\n`;
            md += `discussion_number: ${discussion}\n`;
            md += `date: ${finalDate}\n`;
            md += `published: ${publishNow}\n`;
            md += `---\n\n`;
            if (title) md += `## ${title}\n\n`;
            md += `${text}\n\n`;
            md += `### 📸 Фотоматериалы\n![[photo_01.jpg]]\n\n`;
            md += `### 🎥 Видеоматериалы\n`;

            alert("Сформирован следующий Markdown-текст для отправки в репозиторий:\n\n" + md);
        }

        // Запуск при старте страницы
        initForm();
    </script>
</body>
</html>
