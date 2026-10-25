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
    <title>Конструктор Отчетов TechLab v10</title>
    <style>
        body { font-family: sans-serif; max-width: 480px; margin: 10px auto; padding: 10px; background: #f4f4f4; color: #333; }
        .block { background: #fff; border: 1px solid #ccc; padding: 12px; margin-bottom: 12px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        h3 { margin-top: 0; margin-bottom: 10px; color: #444; border-bottom: 1px solid #eee; padding-bottom: 5px; font-size: 16px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px; color: #555; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; background: #fff; margin-bottom: 10px; }
        input[type="text"]:last-child, textarea:last-child { margin-bottom: 0; }
        
        /* СТРОГАЯ ТРЁХЛИНЕЙНАЯ ШАПКА CMS ПО ВАШЕМУ ЗАДАНИЮ */
        .header-line { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
        .header-line:last-child { margin-bottom: 0; }
        .inline-label { font-weight: bold; font-size: 14px; color: #444; white-space: nowrap; }
        
        .input-date { width: 120px !important; text-align: center; font-family: monospace; }
        /* ВЫРАВНИВАНИЕ ПО ЛЕВОМУ КРАЮ И ШИРИНА ДЛЯ ДИСКУССИИ */
        .input-combo { width: 160px !important; text-align: left; font-family: monospace; }
        
        .draft-trigger { display: flex; align-items: center; gap: 4px; font-size: 15px; font-weight: bold; cursor: pointer; user-select: none; margin-left: auto; }
        .draft-trigger input { width: 20px; height: 20px; cursor: pointer; margin: 0; }
        
        /* СТИЛИ ДИНАМИЧЕСКИХ МЕДИА-БЛОКОВ С КНОПКОЙ УДАЛЕНИЯ */
        .media-sub-block { position: relative; border-left: 3px solid #0076ff; padding-left: 10px; margin-bottom: 15px; background: #fbfbfb; padding-top: 5px; padding-bottom: 28px; border-radius: 0 4px 4px 0; }
        .media-sub-block:last-child { margin-bottom: 0; }
        .video-block-border { border-left-color: #ff9500; }
        .drop-zone { border: 2px dashed #bbb; padding: 15px; text-align: center; color: #777; background: #fafafa; border-radius: 4px; font-size: 14px; margin-top: 5px; }
        
        /* КНОПКА УДАЛЕНИЯ БЛОКА В ПРАВОМ НИЖНЕМ УГЛУ КАРТОЧКИ */
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
        
        <!-- ЛИНИЯ 1: Дата: Поле даты (И больше ничего!) -->
        <div class="header-line">
            <span class="inline-label">Дата публикации:</span>
            <input type="text" id="target-date" class="input-date" maxlength="10" value="2026-10-25" placeholder="YYYY-MM-DD" onchange="currentNormalDate=this.value">           
        </div>

        <!-- ЛИНИЯ 2: Дискуссия: [№-коммит] + Черновик: [Галочка] -->
        <div class="header-line">
            <span class="inline-label">Дискуссия:</span>
            <input type="text" id="discussion-combo" class="input-combo" value="" placeholder="№-коммит">
            <label class="draft-trigger">
                <span class="inline-label">📂:</span><input type="checkbox" id="is-draft-mode" onchange="toggleDraftBehavior()">
            </label>
        </div>

        <!-- ЛИНИЯ 3: Поле черновиков на всю ширину -->
        <div class="header-line" style="margin-top: 12px;">
            <div id="dynamic-field-container" style="width: 100%;"></div>
        </div>
    </div>

    <!-- БЛОК 2: КОНТЕКСТ ОТЧЕТА СО ВСЕМИ ТОЧНЫМИ ПОДПИСЯМИ -->
    <div class="block">
        <h3>2. Контекст комментария</h3>
        <input type="text" id="post-title" placeholder="Заголовок комментария (если есть)">
        <textarea id="post-text" rows="5" placeholder="Описание комментария: основной текст, например, что было сделано или создано на занятии..."></textarea>
        <textarea id="post-footer" rows="3" placeholder="Подвал комментария: дополнительные сведения, автор, метки, ссылки..."></textarea>
    </div>

    <!-- БЛОК 3: ФОТОМАТЕРИАЛЫ С КНОПКАМИ УДАЛЕНИЯ -->
    <div class="block">
        <h3>3. 📸 Фотоматериалы</h3>
        <div id="photos-meta-container">
            <!-- Динамический контейнер -->
        </div>
        <button class="btn-add" onclick="addPhotoBlock()">+ Добавить блок фото</button>
    </div>

    <!-- БЛОК 4: ВИДЕОМАТЕРИАЛЫ С КНОПКАМИ УДАЛЕНИЯ -->
    <div class="block">
        <h3>4. 🎥 Видеоматериалы</h3>
        <div id="videos-meta-container">
            <!-- Динамический контейнер -->
        </div>
        <button class="btn-add btn-add-video" onclick="addVideoBlock()">+ Добавить блок видео</button>
    </div>

    <!-- БЛОК КОНТРОЛЯ И КНОПКА "Создать комментарий" -->
    <div class="block" style="background: #f0f7ff; border-color: #b3d7ff;">
        <div style="display: flex; align-items: center; gap: 6px; font-weight: bold; font-size: 15px; color: #0056b3; margin-bottom: 12px; cursor: pointer; user-select: none;">
            <input type="checkbox" id="publish-now-flag" checked onchange="updatePublishLabel()" style="width: 18px; height: 18px; margin: 0;"> 
            <span id="publish-label-text">🔥 Опубликовать сейчас (published: true)</span>
        </div>
        <button class="btn" onclick="generateMarkdownOutput()">Создать комментарий</button>
    </div>
    <script>
        // Имитация базы данных черновиков, полученных из папки _input медиа-репозитория
        const mockDrafts = [
            { id: "draft1", date: "2026-10-20", title: "Сборка каркаса корабля", text: "Сегодня собирали палубу и шпангоуты.", discussion: "83", commit: "1867726", footer: "Преподаватель: Иванов И.И." }
        ];

        let currentNormalDate = "2026-10-25";
        
        // Индексы для генерации уникальных ID динамических блоков
        let photoBlockIdx = 0;
        let videoBlockIdx = 0;

        // Стартовая инициализация: по умолчанию третья линия заблокирована
        function initForm() {
            const container = document.getElementById("dynamic-field-container");
            container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
            
            // Автоматически создаем по одному начальному блоку по умолчанию
            addPhotoBlock();
            addVideoBlock();
        }

        // АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ФОТО
        function updatePhotoDeleteButtons() {
            const blocks = document.querySelectorAll("#photos-meta-container .media-sub-block");
            blocks.forEach((block) => {
                const deleteContainer = block.querySelector(".btn-delete-container");
                // Если блок один — кнопка удаления скрыта. Если больше одного — показывается на всех.
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
        function updatePublishLabel() {
            const isChecked = document.getElementById("publish-now-flag").checked;
            const labelText = document.getElementById("publish-label-text");
            labelText.innerText = isChecked ? "🔥 Опубликовать сейчас (published: true)" : "📁 Сохранить как черновик (published: false)";
        }

        // ЛИНИЯ 2 В ДЕЙСТВИИ: Переключение режима работы Линии 3 по клику на галочку "Черновик"
        function toggleDraftBehavior() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const container = document.getElementById("dynamic-field-container");
            const publishFlag = document.getElementById("publish-now-flag");

            if (isDraftMode) {
                // АКТИВНЫЙ РЕЖИМ: Линия 3 открывает список черновиков на всю ширину экрана
                let selectHtml = `<select id="draft-select" onchange="loadDraftData(this.value)">`;
                selectHtml += `<option value="">-- Выберите сохраненный черновик --</option>`;
                mockDrafts.forEach(draft => {
                    selectHtml += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
                });
                selectHtml += `</select>`;
                container.innerHTML = selectHtml;
                
                // Перевод флага контроля в режим черновика
                publishFlag.checked = false;
                updatePublishLabel();
            } else {
                // ДЕФОЛТНЫЙ РЕЖИМ: Линия 3 возвращается в состояние заблокировано строго по вашему ТЗ
                container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
                publishFlag.checked = true;
                updatePublishLabel();
                
                // Полный сброс всей формы под новый чистый отчет
                document.getElementById("target-date").value = "2026-10-25";
                currentNormalDate = "2026-10-25";
                document.getElementById("post-title").value = "";
                document.getElementById("post-text").value = "";
                document.getElementById("post-footer").value = "";
                document.getElementById("discussion-combo").value = "83";
            }
        }

        // ЛИНИИ 1 И 2 В ДЕЙСТВИИ: Загрузка старых данных черновика без лишних подписей
        function loadDraftData(draftId) {
            if (!draftId) return;
            const selectedDraft = mockDrafts.find(d => d.id === draftId);
            if (selectedDraft) {
                // Синхронизируем Линию 1 и Линию 2 шапки
                document.getElementById("target-date").value = selectedDraft.date;
                currentNormalDate = selectedDraft.date;
                
                // Собираем обратно комбо-строку формата [№-коммит] для Линии 2
                if (selectedDraft.commit) {
                    document.getElementById("discussion-combo").value = `${selectedDraft.discussion}-${selectedDraft.commit}`;
                } else {
                    document.getElementById("discussion-combo").value = selectedDraft.discussion;
                }
                
                // Наполняем три текстовых поля объединенного Блока 2 один в один
                document.getElementById("post-title").value = selectedDraft.title;
                document.getElementById("post-text").value = selectedDraft.text;
                document.getElementById("post-footer").value = selectedDraft.footer || "";
            }
        }

        // УМНЫЙ СБОР ПАКЕТА С РАЗБИЕНИЕМ СТРОКИ [№-коммит] НА ДВЕ ПЕРЕМЕННЫЕ FRONT MATTER
        function generateMarkdownOutput() {
            const date = document.getElementById("target-date").value;
            const comboValue = document.getElementById("discussion-combo").value.trim();
            const title = document.getElementById("post-title").value;
            const text = document.getElementById("post-text").value;
            const footer = document.getElementById("post-footer").value;
            const publishNow = document.getElementById("publish-now-flag").checked;

            // Математический парсинг строки Линии 2: разделяем по знаку дефиса
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
            md += `---\n\n`;
            
            if (title) md += `## ${title}\n\n`;
            if (text) md += `${text}\n\n`;
            
            // 🔄 Сборка динамических блоков ФОТО
            const photoBlocks = document.querySelectorAll("#photos-meta-container .media-sub-block");
            photoBlocks.forEach((block, index) => {
                const h3Input = block.querySelector(".photo-h3-title");
                const descInput = block.querySelector(".photo-block-desc");
                
                const h3Text = h3Input.value.trim() || `📸 Фотоматериалы`;
                const descText = descInput.value.trim();
                
                md += `### ${h3Text}\n`;
                if (descText) md += `${descText}\n\n`;
                
                md += `![[photo_block_${index + 1}_01.jpg]]\n`;
                md += `![[photo_block_${index + 1}_02.jpg]]\n\n`;
            });

            // 🔄 Сборка динамических блоков ВИДЕО
            const videoBlocks = document.querySelectorAll("#videos-meta-container .media-sub-block");
            videoBlocks.forEach((block, index) => {
                const h3Input = block.querySelector(".video-h3-title");
                const descInput = block.querySelector(".video-block-desc");
                
                const h3Text = h3Input.value.trim() || `🎥 Видеоматериалы`;
                const descText = descInput.value.trim();
                
                md += `### ${h3Text}\n`;
                if (descText) md += `${descText}\n\n`;
                
                md += `![[video_block_${index + 1}_01.mp4]]\n\n`;
            });
            
            if (footer) {
                md += `---\n${footer}\n`;
            }

            alert("Сформирован структурированный Markdown-текст:\n\n" + md);
        }

        // Запуск стартовой инициализации формы
        initForm();
    </script>
</body>
</html>

