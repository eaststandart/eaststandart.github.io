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
    <title>Конструктор Отчетов TechLab v8</title>
    <style>
        body { font-family: sans-serif; max-width: 480px; margin: 10px auto; padding: 10px; background: #f4f4f4; color: #333; }
        .block { background: #fff; border: 1px solid #ccc; padding: 12px; margin-bottom: 12px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        h3 { margin-top: 0; margin-bottom: 10px; color: #444; border-bottom: 1px solid #eee; padding-bottom: 5px; font-size: 16px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px; color: #555; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; background: #fff; margin-bottom: 10px; }
        input[type="text"]:last-child, textarea:last-child { margin-bottom: 0; }
        
        .header-line { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
        .header-line:last-child { margin-bottom: 0; }
        .inline-label { font-weight: bold; font-size: 14px; color: #444; white-space: nowrap; }
        
        .input-date { width: 120px !important; text-align: center; font-family: monospace; }
        .input-disc { width: 55px !important; text-align: center; font-family: monospace; }
        .input-commit { width: 95px !important; text-align: center; font-family: monospace; }
        
        .draft-trigger { display: flex; align-items: center; gap: 4px; font-size: 18px; cursor: pointer; user-select: none; margin-left: auto; }
        .draft-trigger input { width: 20px; height: 20px; cursor: pointer; margin: 0; }
        
        /* СТИЛИ ДИНАМИЧЕСКИХ МЕДИА-БЛОКОВ */
        .media-sub-block { border-left: 3px solid #0076ff; padding-left: 10px; margin-bottom: 15px; }
        .media-sub-block:last-child { margin-bottom: 0; }
        .video-block-border { border-left-color: #ff9500; } /* Видео выделим оранжевым */
        .drop-zone { border: 2px dashed #bbb; padding: 15px; text-align: center; color: #777; background: #fafafa; border-radius: 4px; font-size: 14px; margin-top: 5px; }
        
        /* КНОПКИ ДОБАВЛЕНИЯ БЛОКОВ */
        .btn-add { background: #fff; color: #0076ff; border: 1px dashed #0076ff; padding: 8px; font-size: 14px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 5px; margin-bottom: 5px; }
        .btn-add-video { color: #ff9500; border-color: #ff9500; }
        .btn { background: #0076ff; color: #fff; border: none; padding: 12px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 5px; }
    </style>
</head>
<body>

    <h3 style="text-align: center; color: #0076ff; font-size: 18px; margin-bottom: 15px;">Унифицированная форма TechLab v8</h3>

    <!-- БЛОК 1: ТРЁХЛИНЕЙНАЯ УПРАВЛЯЮЩАЯ ШАПКА CMS -->
    <div class="block">
        <h3>1. Параметры публикации</h3>
        <div class="header-line">
            <span class="inline-label">Дата:</span>
            <input type="text" id="target-date" class="input-date" maxlength="10" value="2026-10-25" placeholder="YYYY-MM-DD" onchange="currentNormalDate=this.value">
            
            <label class="draft-trigger">
                <span class="inline-label">Черновик:</span><input type="checkbox" id="is-draft-mode" onchange="toggleDraftBehavior()">
            </label>
        </div>
        <div class="header-line">
            <span class="inline-label">Дискуссия:</span>
            <input type="text" id="discussion-number" class="input-disc" maxlength="3" value="" placeholder="№">       
            <span class="inline-label" style="margin-left: auto;">#:</span>
            <input type="text" id="commit-id" class="input-commit" maxlength="8" value="" placeholder="коммит">
        </div>
        <div class="header-line" style="margin-top: 12px;">
            <div id="dynamic-field-container" style="width: 100%;"></div>
        </div>
    </div>

    <!-- БЛОК 2: КОНТЕКСТ ОТЧЕТА -->
    <div class="block">
        <h3>2. Контекст отчета</h3>
        <input type="text" id="post-title" placeholder="Заголовок комментария (если есть)">
        <textarea id="post-text" rows="5" placeholder="Описание: Основной текст отчета (Что было сделано на занятии...)"></textarea>
        <textarea id="post-footer" rows="3" placeholder="Подвал комментария: дополнительные сведения, метки, информация о подмене..."></textarea>
    </div>

    <!-- БЛОК 3: ДИНАМИЧЕСКИЕ ФОТОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>3. 📸 Фотоматериалы</h3>
        <div id="photos-meta-container">
            <!-- Сюда JS будет дописывать новые блоки фото под своими заголовками H3 -->
        </div>
        <button class="btn-add" onclick="addPhotoBlock()">+ Добавить блок фото</button>
    </div>

    <!-- БЛОК 4: ДИНАМИЧЕСКИЕ ВИДЕОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>4. 🎥 Видеоматериалы</h3>
        <div id="videos-meta-container">
            <!-- Сюда JS будет дописывать новые блоки видео под своими заголовками H3 -->
        </div>
        <button class="btn-add btn-add-video" onclick="addVideoBlock()">+ Добавить блок видео</button>
    </div>

    <!-- БЛОК КОНТРОЛЯ -->
    <div class="block" style="background: #f0f7ff; border-color: #b3d7ff;">
        <div style="display: flex; align-items: center; gap: 6px; font-weight: bold; font-size: 15px; color: #0056b3; margin-bottom: 12px; cursor: pointer; user-select: none;">
            <input type="checkbox" id="publish-now-flag" checked onchange="updatePublishLabel()" style="width: 18px; height: 18px; margin: 0;"> 
            <span id="publish-label-text">🔥 Опубликовать сейчас (published: true)</span>
        </div>
        <button class="btn" onclick="generateMarkdownOutput()">Создать комментарий</button>
    </div>
    <script>
        // Имитация базы данных черновиков
        const mockDrafts = [
            { id: "draft1", date: "2026-10-20", title: "Сборка каркаса корабля", text: "Сегодня собирали палубу и шпангоуты.", discussion: "83", commit: "1867726", footer: "Преподаватель: Иванов И.И." }
        ];

        let currentNormalDate = "2026-10-25";
        
        // Счётчики для генерации уникальных ID динамических блоков
        let photoBlockIdx = 0;
        let videoBlockIdx = 0;

        function initForm() {
            const container = document.getElementById("dynamic-field-container");
            container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
            
            // Генерируем по одному дефолтному блоку при старте, чтобы форма не была пустой
            addPhotoBlock();
            addVideoBlock();
        }

        // ДИНАМИЧЕСКОЕ ДОБАВЛЕНИЕ БЛОКОВ ФОТО (Пункт 1 вашего вопроса)
        function addPhotoBlock() {
            photoBlockIdx++;
            const container = document.getElementById("photos-meta-container");
            
            const subBlock = document.createElement("div");
            subBlock.className = "media-sub-block";
            subBlock.id = `photo-sub-block-${photoBlockIdx}`;
            
            // Внутрь блока закладываем поле заголовка H3 и собственную Drag&Drop зону
            subBlock.innerHTML = `
                <input type="text" class="photo-h3-title" placeholder="Заголовок(например: Фотоматериалы фундамент)">
                <div class="drop-zone">Нажмите для выбора или перетащите фото в этот блок</div>
            `;
            container.appendChild(subBlock);
        }

        // ДИНАМИЧЕСКОЕ ДОБАВЛЕНИЕ БЛОКОВ ВИДЕО (Пункт 2 вашего вопроса)
        function addVideoBlock() {
            videoBlockIdx++;
            const container = document.getElementById("videos-meta-container");
            
            const subBlock = document.createElement("div");
            subBlock.className = "media-sub-block video-block-border";
            subBlock.id = `video-sub-block-${videoBlockIdx}`;
            
            subBlock.innerHTML = `
                <input type="text" class="video-h3-title" placeholder="Заголовок (например: Видеоматериалы стены)">
                <div class="drop-zone">Нажмите для выбора или перетащите видео в этот блок</div>
            `;
            container.appendChild(subBlock);
        }

        function updatePublishLabel() {
            const isChecked = document.getElementById("publish-now-flag").checked;
            const labelText = document.getElementById("publish-label-text");
            labelText.innerText = isChecked ? "🔥 Опубликовать сейчас (published: true)" : "📁 Сохранить как черновик (published: false)";
        }

        function toggleDraftBehavior() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const container = document.getElementById("dynamic-field-container");
            const publishFlag = document.getElementById("publish-now-flag");

            if (isDraftMode) {
                let selectHtml = `<select id="draft-select" onchange="loadDraftData(this.value)">`;
                selectHtml += `<option value="">-- Выберите сохраненный черновик --</option>`;
                mockDrafts.forEach(draft => {
                    selectHtml += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
                });
                selectHtml += `</select>`;
                container.innerHTML = selectHtml;
                publishFlag.checked = false;
                updatePublishLabel();
            } else {
                container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
                publishFlag.checked = true;
                updatePublishLabel();
                
                document.getElementById("target-date").value = "2026-10-25";
                currentNormalDate = "2026-10-25";
                document.getElementById("post-title").value = "";
                document.getElementById("post-text").value = "";
                document.getElementById("post-footer").value = "";
                document.getElementById("discussion-number").value = "83";
                document.getElementById("commit-id").value = "";
            }
        }

        function loadDraftData(draftId) {
            if (!draftId) return;
            const selectedDraft = mockDrafts.find(d => d.id === draftId);
            if (selectedDraft) {
                document.getElementById("target-date").value = selectedDraft.date;
                currentNormalDate = selectedDraft.date;
                document.getElementById("discussion-number").value = selectedDraft.discussion;
                document.getElementById("commit-id").value = selectedDraft.commit || "";
                document.getElementById("post-title").value = selectedDraft.title;
                document.getElementById("post-text").value = selectedDraft.text;
                document.getElementById("post-footer").value = selectedDraft.footer || "";
            }
        }

        // УМНАЯ СБОРКА ПОТОКА СВЕРХУ ВНИЗ
        function generateMarkdownOutput() {
            const date = document.getElementById("target-date").value;
            const discussion = document.getElementById("discussion-number").value;
            const commitId = document.getElementById("commit-id").value;
            const title = document.getElementById("post-title").value;
            const text = document.getElementById("post-text").value;
            const footer = document.getElementById("post-footer").value;
            const publishNow = document.getElementById("publish-now-flag").checked;

            let md = `---\n`;
            md += `discussion_number: ${discussion}\n`;
            if (commitId) md += `comment_id: ${commitId}\n`;
            md += `date: ${date}\n`;
            md += `published: ${publishNow}\n`;
            md += `---\n\n`;
            
            if (title) md += `## ${title}\n\n`;
            if (text) md += `${text}\n\n`;
            
            // 🔄 Сканируем и собираем все созданные блоки ФОТО
            const photoInputs = document.querySelectorAll(".photo-h3-title");
            photoInputs.forEach((input, index) => {
                // Если преподаватель не написал свой заголовок, ставим стандартный по ТЗ
                const h3Text = input.value.trim() || `📸 Фотоматериалы`;
                md += `### ${h3Text}\n`;
                // Имитируем прикрепленные файлы конкретно этого подблока
                md += `![[photo_block_${index + 1}_01.jpg]]\n`;
                md += `![[photo_block_${index + 1}_02.jpg]]\n\n`;
            });

            // 🔄 Сканируем и собираем все созданные блоки ВИДЕО
            const videoInputs = document.querySelectorAll(".video-h3-title");
            videoInputs.forEach((input, index) => {
                const h3Text = input.value.trim() || `🎥 Видеоматериалы`;
                md += `### ${h3Text}\n`;
                md += `![[video_block_${index + 1}_01.mp4]]\n\n`;
            });
            
            if (footer) {
                md += `---\n${footer}\n`;
            }

            alert("Сформирован структурированный Markdown-текст:\n\n" + md);
        }

        initForm();
    </script>
</body>
</html>
