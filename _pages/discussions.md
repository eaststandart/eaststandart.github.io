---
author: "TechLab"
layout: page
description: 
title: Форма для публикации комментариев в обсуждениях
permalink: /discussions/
emoji: ""
custom_css: "/assets/css/discussions.css"
---

{% include discussions.liquid %}

{%- comment -%}

<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Конструктор Отчетов TechLab v10</title>
    <style>
        body { font-family: sans-serif; max-width: 480px; margin: 10px auto; padding: 10px; background: #f4f4f4; color: #333; }
        .block { background: #fff; border: 1px solid #ccc; padding: 12px; margin-bottom: 12px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        h3 { margin-top: 0; margin-bottom: 10px; color: #444; border-bottom: 1px solid #eee; padding-bottom: 5px; font-size: 16px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px; color: #555; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; background: #fff; margin-bottom: 10px; }
        input[type="text"]:last-child, textarea:last-child { margin-bottom: 0; }
        
        /* СТРОГАЯ ТРЁХЛИНЕЙНАЯ ШАПКА CMS */
        .header-line { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
        .header-line:last-child { margin-bottom: 0; }
        .inline-label { font-weight: bold; font-size: 14px; color: #444; white-space: nowrap; }
        
        .input-date { width: 120px !important; text-align: center; font-family: monospace; }
        .input-combo { width: 105px !important; max-width: 105px !important; text-align: left; font-family: monospace; }
        
        .draft-trigger { display: flex; align-items: center; gap: 4px; font-size: 15px; font-weight: bold; cursor: pointer; user-select: none; margin-left: auto; }
        .draft-trigger input { width: 20px; height: 20px; cursor: pointer; margin: 0; }
        
        /* СТИЛИ ДИНАМИЧЕСКИХ МЕДИА-БЛОКОВ С КНОПКОЙ УДАЛЕНИЯ */
        .media-sub-block { position: relative; border-left: 3px solid #0076ff; padding-left: 10px; margin-bottom: 15px; background: #fbfbfb; padding-top: 5px; padding-bottom: 28px; border-radius: 0 4px 4px 0; }
        .media-sub-block:last-child { margin-bottom: 0; }
        .video-block-border { border-left-color: #ff9500; }
        .drop-zone { border: 2px dashed #bbb; padding: 15px; text-align: center; color: #777; background: #fafafa; border-radius: 4px; font-size: 14px; margin-top: 5px; }
        
        .btn-delete-container { position: absolute; bottom: 5px; right: 5px; text-align: right; width: 100%; }
        .btn-delete-block { background: none; color: #ff3b30; border: none; font-size: 13px; font-weight: bold; cursor: pointer; padding: 2px 5px; }
        .btn-delete-block:hover { text-decoration: underline; }
        
        .btn-add { background: #fff; color: #0076ff; border: 1px dashed #0076ff; padding: 8px; font-size: 14px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 5px; margin-bottom: 5px; }
        .btn-add-video { color: #ff9500; border-color: #ff9500; }
        .btn { background: #0076ff; color: #fff; border: none; padding: 12px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 5px; }
    </style>
</head>
<body>

    <h3 style="text-align: center; color: #0076ff; font-size: 18px; margin-bottom: 15px;">Унифицированная форма TechLab v10</h3>

    <!-- БЛОК 1: ТРЁХЛИНЕЙНАЯ УПРАВЛЯЮЩАЯ ШАПКА CMS -->
    <div class="block">
        <h3>1. Параметры публикации</h3>
        
        <!-- ЛИНИЯ 1: Дата: Поле даты -->
        <div class="header-line">
            <span class="inline-label">Дата:</span>
            <input type="text" id="target-date" class="input-date" maxlength="10" value="2026-10-25" placeholder="YYYY-MM-DD" onchange="currentNormalDate=this.value">           
        </div>

        <!-- ЛИНИЯ 2: Дискуссия: [№-коммит] + Черновик: [Галочка] -->
        <div class="header-line">
            <span class="inline-label">Дискуссия:</span>
            <input type="text" id="discussion-combo" class="input-combo" maxlength="11" value="" placeholder="№-коммит">       
            
            <label class="draft-trigger">
                <span class="inline-label">Черновик:</span><input type="checkbox" id="is-draft-mode" onchange="toggleDraftBehavior()">
            </label>
        </div>

        <!-- ЛИНИЯ 3: Поле черновиков на всю ширину экрана -->
        <div class="header-line" style="margin-top: 12px;">
            <div id="dynamic-field-container" style="width: 100%;">
                <select id="draft-select" onchange="loadDraftData(this.value)">
                    <!-- Наполняется через JS -->
                </select>
            </div>
        </div>
    </div>

    <!-- БЛОК 2: КОНТЕКСТ ОТЧЕТА (ОБЪЕДИНЕННЫЙ) -->
    <div class="block">
        <h3>2. Контекст отчета</h3>
        <input type="text" id="post-title" placeholder="Заголовок комментария (если есть)">
        <textarea id="post-text" rows="5" placeholder="Описание комментария: основной текст, например, что было сделано или создано на занятии..."></textarea>
        <textarea id="post-footer" rows="3" placeholder="Подвал комментария: дополнительные сведения, автор, метки, ссылки..."></textarea>
    </div>

    <!-- БЛОК 3: ФОТОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>3. 📸 Фотоматериалы</h3>
        <div id="photos-meta-container"></div>
        <button class="btn-add" onclick="addPhotoBlock()">+ Добавить блок фото</button>
    </div>

    <!-- БЛОК 4: ВИДЕОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>4. 🎥 Видеоматериалы</h3>
        <div id="videos-meta-container"></div>
        <button class="btn-add btn-add-video" onclick="addVideoBlock()">+ Добавить блок видео</button>
    </div>

    <!-- БЛОК КОНТРОЛЯ -->
    <div class="block" style="background: #f0f7ff; border-color: #b3d7ff;">
        <div style="display: flex; align-items: center; gap: 6px; font-weight: bold; font-size: 15px; color: #0056b3; margin-bottom: 12px; cursor: pointer; user-select: none;">
            <input type="checkbox" id="publish-now-flag" checked onchange="updatePublishLabel()" style="width: 18px; height: 18px; margin: 0;"> 
            <span id="publish-label-text">🔥 Опубликовать сейчас (published: true)</span>
        </div>
        <button class="btn" id="submit-btn" onclick="generateMarkdownOutput()">Создать комментарий</button>
    </div>
    <script>
        // Имитация базы данных черновиков с Гитхаба (Имена полей строго выверены)
        const mockDrafts = [
            { 
                id: "draft1", 
                date: "2026-10-20", 
                discussion: "83", 
                commit: "1867726", 
                title: "Сборка каркаса корабля", 
                text: "Сегодня собирали палубу и шпангоуты.", 
                footer: "Преподаватель: Иванов И.И.\nВ кадре: Младшая группа" 
            },
            { 
                id: "draft2", 
                date: "2026-10-22", 
                discussion: "45", 
                commit: "", 
                title: "Тест сервоприводов робота", 
                text: "Программировали контроллер, проверили углы поворота манипулятора.", 
                footer: "В кадре: Робототехники" 
            }
        ];

        let currentNormalDate = "2026-10-25";
        let photoBlockIdx = 0;
        let videoBlockIdx = 0;

        // Стартовая инициализация: жестко набиваем селект дефолтным текстом и блокируем
        function initForm() {
            const select = document.getElementById("draft-select");
            select.innerHTML = `<option value="">черновиков нет</option>`;
            select.disabled = true;
            addPhotoBlock();
            addVideoBlock();
        }

        // АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ФОТО
        function updatePhotoDeleteButtons() {
            const blocks = document.querySelectorAll("#photos-meta-container .media-sub-block");
            blocks.forEach((block) => {
                const deleteContainer = block.querySelector(".btn-delete-container");
                if (blocks.length > 1) {
                    deleteContainer.style.display = "block";
                } else {
                    deleteContainer.style.display = "none";
                }
            });
        }

        // АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ВИДЕО
        function updateVideoDeleteButtons() {
            const blocks = document.querySelectorAll("#videos-meta-container .media-sub-block");
            blocks.forEach((block) => {
                const deleteContainer = block.querySelector(".btn-delete-container");
                if (blocks.length > 1) {
                    deleteContainer.style.display = "block";
                } else {
                    deleteContainer.style.display = "none";
                }
            });
        }

        // ДОБАВЛЕНИЕ БЛОКА ФОТО С ВАШИМИ ПОДПИСЯМИ И КНОПКОЙ УДАЛЕНИЯ
        function addPhotoBlock() {
            photoBlockIdx++;
            const container = document.getElementById("photos-meta-container");
            const subBlock = document.createElement("div");
            subBlock.className = "media-sub-block";
            subBlock.id = `photo-sub-block-${photoBlockIdx}`;
            subBlock.innerHTML = `
                <input type="text" class="photo-h3-title" placeholder="Заголовок для фотоматериалов">
                <textarea class="photo-block-desc" rows="2" placeholder="Краткое описание блока..."></textarea>
                <div class="drop-zone">Нажмите для выбора или перетащите фото в этот блок</div>
                <div class="btn-delete-container" style="display: none;">
                    <button class="btn-delete-block" type="button" onclick="deletePhotoBlock('${subBlock.id}')">[Удалить блок]</button>
                </div>
            `;
            container.appendChild(subBlock);
            updatePhotoDeleteButtons();
        }

        function deletePhotoBlock(blockId) {
            const block = document.getElementById(blockId);
            if (block) {
                block.remove();
                updatePhotoDeleteButtons();
            }
        }

        // ДОБАВЛЕНИЕ БЛОКА ВИДЕО С ВАШИМИ ПОДПИСЯМИ И КНОПКОЙ УДАЛЕНИЯ
        function addVideoBlock() {
            videoBlockIdx++;
            const container = document.getElementById("videos-meta-container");
            const subBlock = document.createElement("div");
            subBlock.className = "media-sub-block video-block-border";
            subBlock.id = `video-sub-block-${videoBlockIdx}`;
            subBlock.innerHTML = `
                <input type="text" class="video-h3-title" placeholder="Заголовок для видеоматериалов">
                <textarea class="video-block-desc" rows="2" placeholder="Краткое описание блока..."></textarea>
                <div class="drop-zone">Нажмите для выбора или перетащите видео в этот блок</div>
                <div class="btn-delete-container" style="display: none;">
                    <button class="btn-delete-block" type="button" onclick="deleteVideoBlock('${subBlock.id}')">[Удалить блок]</button>
                </div>
            `;
            container.appendChild(subBlock);
            updateVideoDeleteButtons();
        }

        function deleteVideoBlock(blockId) {
            const block = document.getElementById(blockId);
            if (block) {
                block.remove();
                updateVideoDeleteButtons();
            }
        }
        // ФУНКЦИЯ БЛОКИРОВКИ ИНТЕРФЕЙСА ПРИ СТАТУСЕ ON
        function setFormLock(isLocked, message = "") {
            const submitBtn = document.getElementById("submit-btn");
            const inputs = document.querySelectorAll("input, textarea, select");
            inputs.forEach(input => {
                if (input.id !== "is-draft-mode") {
                    input.disabled = isLocked;
                }
            });
            if (isLocked) {
                submitBtn.innerText = message || "⏳ Обработка на сервере...";
                submitBtn.style.background = "#85b7ff";
            } else {
                updatePublishLabel();
                submitBtn.style.background = "#0076ff";
            }
        }

        // ДИНАМИЧЕСКИЙ ПЕРЕКЛЮЧАТЕЛЬ ТЕКСТА КНОПКИ СТРОГО ПО ТЗ
        function updatePublishLabel() {
            const isChecked = document.getElementById("publish-now-flag").checked;
            const labelText = document.getElementById("publish-label-text");
            const submitBtn = document.getElementById("submit-btn");
            if (isChecked) {
                labelText.innerText = "🔥 Опубликовать сейчас (published: true)";
                submitBtn.innerText = "Создать комментарий";
            } else {
                labelText.innerText = "🔥 Опубликовать сейчас (published: false)";
                submitBtn.innerText = "Сохранить черновик";
            }
        }

        // ЛИНИЯ 2 В ДЕЙСТВИИ: Включение и отключение селекта Линии 3
        function toggleDraftBehavior() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const select = document.getElementById("draft-select");
            const publishFlag = document.getElementById("publish-now-flag");

            if (isDraftMode) {
                let html = `<option value="">-- Выберите сохраненный черновик --</option>`;
                mockDrafts.forEach(draft => {
                    html += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
                });
                select.innerHTML = html;
                select.disabled = false;
                publishFlag.checked = false;
                updatePublishLabel();
            } else {
                select.innerHTML = `<option value="">черновиков нет</option>`;
                select.disabled = true;
                publishFlag.checked = true;
                updatePublishLabel();
                
                document.getElementById("target-date").value = "2026-10-25";
                currentNormalDate = "2026-10-25";
                document.getElementById("post-title").value = "";
                document.getElementById("post-text").value = "";
                document.getElementById("post-footer").value = "";
                document.getElementById("discussion-combo").value = "";
            }
        }

        // ЖЕСТКАЯ СИНХРОНИЗАЦИЯ ДАННЫХ С МАССИВОМ
        function loadDraftData(draftId) {
            if (!draftId) return;
            const selectedDraft = mockDrafts.find(d => d.id === draftId);
            if (selectedDraft) {
                // 1. Мгновенно переписываем дату на Линии 1 на оригинальную дату черновика
                document.getElementById("target-date").value = selectedDraft.date;
                currentNormalDate = selectedDraft.date;
                
                // 2. Восстанавливаем комбо-строку формата [№-коммит] на Линии 2
                if (selectedDraft.commit) {
                    document.getElementById("discussion-combo").value = `${selectedDraft.discussion}-${selectedDraft.commit}`;
                } else {
                    document.getElementById("discussion-combo").value = selectedDraft.discussion;
                }
                
                // 3. Моментально наполняем оригинальным текстом все три поля Блока 2 один в один
                document.getElementById("post-title").value = selectedDraft.title;
                document.getElementById("post-text").value = selectedDraft.text;
                document.getElementById("post-footer").value = selectedDraft.footer;
            }
        }

        // СКВОЗНАЯ ПЕРЕНУМЕРАЦИЯ, ВШИВАНИЕ СЕМАФОРА И СБОРКА МАНИФЕСТА
        function generateMarkdownOutput() {
            const date = document.getElementById("target-date").value;
            const comboValue = document.getElementById("discussion-combo").value.trim();
            const title = document.getElementById("post-title").value;
            const text = document.getElementById("post-text").value;
            const footer = document.getElementById("post-footer").value;
            const publishNow = document.getElementById("publish-now-flag").checked;

            let discussion = comboValue;
            let commitId = "";
            if (comboValue.includes("-")) {
                const parts = comboValue.split("-");
                discussion = parts[0].trim();
                commitId = parts[1].trim();
            }

            let md = `---\n`;
            md += `discussion_number: ${discussion}\n`;
            if (commitId) md += `comment_id: ${commitId}\n`;
            md += `date: ${date}\n`;
            md += `published: ${publishNow}\n`;
            md += `status: on\n`;
            md += `---\n\n`;
            
            if (title) md += `## ${title}\n\n`;
            if (text) md += `${text}\n\n`;
            
            const photoBlocks = document.querySelectorAll("#photos-meta-container .media-sub-block");
            photoBlocks.forEach((block, index) => {
                const h3Input = block.querySelector(".photo-h3-title");
                const descInput = block.querySelector(".photo-block-desc");
                const h3Text = h3Input.value.trim() || `📸 Фотоматериалы`;
                const descText = descInput.value.trim();
                const finalIdx = String(index + 1).padStart(2, '0');
                
                md += `### ${h3Text}\n`;
                if (descText) md += `${descText}\n\n`;
                md += `![[photo_${finalIdx}.jpg]]\n\n`;
            });

            const videoBlocks = document.querySelectorAll("#videos-meta-container .media-sub-block");
            videoBlocks.forEach((block, index) => {
                const h3Input = block.querySelector(".video-h3-title");
                const descInput = block.querySelector(".video-block-desc");
                const h3Text = h3Input.value.trim() || `🎥 Видеоматериалы`;
                const descText = descInput.value.trim();
                const finalIdx = String(index + 1).padStart(2, '0');
                
                md += `### ${h3Text}\n`;
                if (descText) md += `${descText}\n\n`;
                md += `![[video_${finalIdx}.mp4]]\n\n`;
            });
            
            if (footer) {
                md += `---\n${footer}\n`;
            }

            alert("Сформирован структурированный Markdown-текст:\n\n" + md);
            setFormLock(true, "⏳ Синхронизация медиа-файлов на сервере...");
        }

        initForm();
    </script>
</body>
</html>

{%- endcomment -%}