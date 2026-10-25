---
author: "TechLab"
layout: page
description: 
title: Журнал посещений
permalink: /discussions/
emoji: ""
---

<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Конструктор Отчетов TechLab v5</title>
    <style>
        body { font-family: sans-serif; max-width: 480px; margin: 10px auto; padding: 10px; background: #f4f4f4; color: #333; }
        .block { background: #fff; border: 1px solid #ccc; padding: 12px; margin-bottom: 12px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        h3 { margin-top: 0; margin-bottom: 10px; color: #444; border-bottom: 1px solid #eee; padding-bottom: 5px; font-size: 16px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px; color: #555; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; background: #fff; }
        
        /* СВЕРХКОМПАКТНАЯ СТРОКА УПРАВЛЕНИЯ */
        .control-row { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
        .input-date { width: 115px !important; text-align: center; font-family: monospace; letter-spacing: 0.5px; padding: 10px 5px !important; }
        .label-num { font-weight: bold; font-size: 16px; color: #444; }
        .input-num { width: 55px !important; text-align: center; font-family: monospace; padding: 10px 5px !important; }
        .draft-trigger { display: flex; align-items: center; gap: 4px; font-size: 18px; cursor: pointer; user-select: none; margin-left: auto; }
        .draft-trigger input { width: 20px; height: 20px; cursor: pointer; margin: 0; }
        
        .drop-zone { border: 2px dashed #bbb; padding: 15px; text-align: center; color: #777; background: #fafafa; border-radius: 4px; font-size: 14px; }
        .btn { background: #0076ff; color: #fff; border: none; padding: 12px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 5px; }
    </style>
</head>
<body>

    <h3 style="text-align: center; color: #0076ff; font-size: 18px; margin-bottom: 15px;">Унифицированная форма TechLab v5</h3>

    <!-- БЛОК 1: СВЕРХКОМПАКТНАЯ ОДНОСТРОЧНАЯ ШАПКА + ПОЛЕ ЧЕРНОВИКОВ СНИЗУ -->
    <div class="block">
        <div class="control-row">
            <!-- Поле даты (ровно 10 символов YYYY-MM-DD) -->
            <input type="text" id="target-date" class="input-date" maxlength="10" value="2026-10-25" placeholder="YYYY-MM-DD" onchange="currentNormalDate=this.value">
            
            <span class="label-num">№:</span>
            
            <!-- Поле дискуссии (макс 3 символа) -->
            <input type="text" id="discussion-number" class="input-num" maxlength="3" value="83" placeholder="№">
            
            <!-- Эмодзи черновика и сама бестекстовая галочка -->
            <label class="draft-trigger">
                📂 <input type="checkbox" id="is-draft-mode" onchange="toggleDraftBehavior()">
            </label>
        </div>

        <!-- ПОЛЕ ЧЕРНОВИКОВ НА ВСЮ ШИРИНУ ПОД НИМИ -->
        <div>
            <div id="dynamic-field-container">
                <!-- Сюда JS подставит либо заблокированный селект "черновиков нет", либо активный список -->
            </div>
        </div>
    </div>

    <!-- БЛОК 2: ЗАГОЛОВОК КОММЕНТАРИЯ -->
    <div class="block">
        <label for="post-title">2. Заголовок комментария</label>
        <input type="text" id="post-title" placeholder="Введите заголовок (если есть)">
    </div>

    <!-- БЛОК 3: СОДЕРЖАТЕЛЬНАЯ ЧАСТЬ -->
    <div class="block">
        <label for="post-text">3. Описание (Основной текст отчета)</label>
        <textarea id="post-text" rows="5" placeholder="Что было сделано на занятии..."></textarea>
    </div>

    <!-- БЛОК 4: 📸 ФОТОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>4. 📸 Фотоматериалы</h3>
        <div class="drop-zone">Нажмите для выбора или перетащите фото</div>
    </div>

    <!-- БЛОК 5: 🎥 ВИДЕОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>5. 🎥 Видеоматериалы</h3>
        <div class="drop-zone">Нажмите для выбора или перетащите видео</div>
    </div>

    <!-- БЛОК 6: НАСТРАИВАЕМЫЙ ПОДВАЛ -->
    <div class="block">
        <label for="post-footer">6. Подвал комментария (Обычный текст)</label>
        <textarea id="post-footer" rows="3" placeholder="Дополнительные сведения, метки, информация о подмене..."></textarea>
    </div>

    <!-- БЛОК КОНТРОЛЯ: ОПУБЛИКОВАТЬ / СОХРАНИТЬ КАК ЧЕРНОВИК -->
    <div class="block" style="background: #f0f7ff; border-color: #b3d7ff;">
        <div style="display: flex; align-items: center; gap: 6px; font-weight: bold; font-size: 15px; color: #0056b3; margin-bottom: 12px; cursor: pointer; user-select: none;">
            <input type="checkbox" id="publish-now-flag" checked style="width: 18px; height: 18px; margin: 0;"> 🔥 Опубликовать сейчас (published: true)
        </div>
        <button class="btn" onclick="generateMarkdownOutput()">Сформировать .md манифест</button>
    </div>

    <script>
        // Имитация базы данных черновиков с Гитхаба
        const mockDrafts = [
            { id: "draft1", date: "2026-10-20", title: "Сборка каркаса корабля", text: "Сегодня собирали палубу и шпангоуты.", discussion: "83", footer: "Преподаватель: Иванов И.И.\nВ кадре: Младшая группа" },
            { id: "draft2", date: "2026-10-22", title: "Тест сервоприводов робота", text: "Программировали контроллер, проверили углы поворота манипулятора.", discussion: "45", footer: "В кадре: Робототехники" }
        ];

        let currentNormalDate = "2026-10-25";

        // По умолчанию выводим заблокированное поле "черновиков нет"
        function initForm() {
            const container = document.getElementById("dynamic-field-container");
            container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
        }

        // БЛОК 1 В ДЕЙСТВИИ: Логика управления полем черновиков по клику на бестекстовую галочку
        function toggleDraftBehavior() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const container = document.getElementById("dynamic-field-container");
            const publishFlag = document.getElementById("publish-now-flag");

            if (isDraftMode) {
                // АКТИВНЫЙ РЕЖИМ: Разворачиваем выпадающий список со всеми черновиками на всю ширину
                let selectHtml = `<select id="draft-select" onchange="loadDraftData(this.value)">`;
                selectHtml += `<option value="">-- Выберите сохраненный черновик --</option>`;
                mockDrafts.forEach(draft => {
                    selectHtml += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
                });
                selectHtml += `</select>`;
                container.innerHTML = selectHtml;
                
                publishFlag.checked = false;
            } else {
                // ДЕФОЛТНЫЙ РЕЖИМ: Возвращаем заблокированное "черновиков нет" строго по условию
                container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
                publishFlag.checked = true;
                
                // Сброс формы в исходное чистое состояние
                document.getElementById("target-date").value = "2026-10-25";
                currentNormalDate = "2026-10-25";
                document.getElementById("post-title").value = "";
                document.getElementById("post-text").value = "";
                document.getElementById("post-footer").value = "";
                document.getElementById("discussion-number").value = "83";
            }
        }

        // Загрузка СТАРЫХ данных черновика для чистого редактирования
        function loadDraftData(draftId) {
            if (!draftId) return;
            const selectedDraft = mockDrafts.find(d => d.id === draftId);
            if (selectedDraft) {
                // Автоматически обновляем данные в компактной строке шапки
                document.getElementById("target-date").value = selectedDraft.date;
                currentNormalDate = selectedDraft.date;
                document.getElementById("discussion-number").value = selectedDraft.discussion;
                
                // Обновляем описание, заголовок и подвал отчета один в один
                document.getElementById("post-title").value = selectedDraft.title;
                document.getElementById("post-text").value = selectedDraft.text;
                document.getElementById("post-footer").value = selectedDraft.footer;
            }
        }

        function generateMarkdownOutput() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const date = document.getElementById("target-date").value;
            const discussion = document.getElementById("discussion-number").value;
            const title = document.getElementById("post-title").value;
            const text = document.getElementById("post-text").value;
            const footer = document.getElementById("post-footer").value;
            const publishNow = document.getElementById("publish-now-flag").checked;

            // Сборка манифеста по нашей жесткой 5-блочной схеме
            let md = `---\n`;
            md += `discussion_number: ${discussion}\n`;
            md += `date: ${date}\n`;
            md += `published: ${publishNow}\n`;
            md += `---\n\n`;
            
            if (title) md += `## ${title}\n\n`;
            if (text) md += `${text}\n\n`;
            
            md += `### 📸 Фотоматериалы\n![[photo_01.jpg]]\n\n`;
            md += `### 🎥 Видеоматериалы\n\n`;
            
            if (footer) {
                md += `---\n${footer}\n`;
            }

            alert("Сформирован следующий Markdown-текст:\n\n" + md);
        }


        // Инициализация при старте
        initForm();
    </script>
</body>
</html>
