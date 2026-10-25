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
    <title>Конструктор Отчетов TechLab v7</title>
    <style>
        body { font-family: sans-serif; max-width: 480px; margin: 10px auto; padding: 10px; background: #f4f4f4; color: #333; }
        .block { background: #fff; border: 1px solid #ccc; padding: 12px; margin-bottom: 12px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        h3 { margin-top: 0; margin-bottom: 10px; color: #444; border-bottom: 1px solid #eee; padding-bottom: 5px; font-size: 16px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px; color: #555; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; background: #fff; margin-bottom: 10px; }
        input[type="text"]:last-child, textarea:last-child { margin-bottom: 0; }
        
        /* СТРУКТУРА ШАПКИ УПРАВЛЕНИЯ CMS */
        .header-line { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
        .header-line:last-child { margin-bottom: 0; }
        .inline-label { font-weight: bold; font-size: 14px; color: #444; white-space: nowrap; }
        
        /* Калибровка размеров полей ввода под лимиты данных */
        .input-date { width: 120px !important; text-align: center; font-family: monospace; }
        .input-disc { width: 55px !important; text-align: center; font-family: monospace; }
        .input-commit { width: 95px !important; text-align: center; font-family: monospace; }
        
        .draft-trigger { display: flex; align-items: center; gap: 4px; font-size: 18px; cursor: pointer; user-select: none; margin-left: auto; }
        .draft-trigger input { width: 20px; height: 20px; cursor: pointer; margin: 0; }
        
        .drop-zone { border: 2px dashed #bbb; padding: 15px; text-align: center; color: #777; background: #fafafa; border-radius: 4px; font-size: 14px; }
        .btn { background: #0076ff; color: #fff; border: none; padding: 12px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 5px; }
    </style>
</head>
<body>

    <h3 style="text-align: center; color: #0076ff; font-size: 18px; margin-bottom: 15px;">Унифицированная форма TechLab v7</h3>

    <!-- БЛОК 1: ТРЁХЛИНЕЙНАЯ УПРАВЛЯЮЩАЯ ШАПКА CMS -->
    <div class="block">
        <h3>1. Параметры публикации</h3>
        
        <!-- ЛИНИЯ 1: Дата + Чекбокс переключения в режим черновика -->
        <div class="header-line">
            <span class="inline-label">Дата:</span>
            <input type="text" id="target-date" class="input-date" maxlength="10" value="2026-10-25" placeholder="YYYY-MM-DD" onchange="currentNormalDate=this.value">
            
            <label class="draft-trigger">
                <span class="inline-label">Черновик:</span><input type="checkbox" id="is-draft-mode" onchange="toggleDraftBehavior()">
            </label>
        </div>

        <!-- ЛИНИЯ 2: Дискуссия № (3 цифры) + Коммит (8 цифр) -->
        <div class="header-line">
            <span class="inline-label">Дискуссия:</span>
            <input type="text" id="discussion-number" class="input-disc" maxlength="3" value="" placeholder="№">
            
            <span class="inline-label" style="margin-left: auto;">#:</span>
            <input type="text" id="commit-id" class="input-commit" maxlength="8" value="" placeholder="коммит">
        </div>

        <!-- ЛИНИЯ 3: Поле черновиков на всю ширину мобильного экрана -->
        <div class="header-line" style="margin-top: 12px;">
            <div id="dynamic-field-container" style="width: 100%;">
                <!-- Контейнер для списка набросков -->
            </div>
        </div>
    </div>

    <!-- ОБЪЕДИНЕННЫЙ БЛОК 2: КОНТЕКСТ ОТЧЕТА (ВСЕ ТЕКСТОВЫЕ ПОЛЯ БЕЗ ВНЕШНИХ ПОДПИСЕЙ) -->
    <div class="block">
        <h3>2. Контекст комментария</h3>
        
        <!-- Заголовок комментария -->
        <input type="text" id="post-title" placeholder="Заголовок комментария (если есть)">
        
        <!-- Описание занятия -->
        <textarea id="post-text" rows="5" placeholder="Описание: Основной текст отчета (Что было сделано на занятии...)"></textarea>
        
        <!-- Подвал комментария -->
        <textarea id="post-footer" rows="4" placeholder="Подвал комментария: дополнительные сведения, метки ..."></textarea>
    </div>

    <!-- БЛОК 3: 📸 ФОТОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>3. 📸 Фотоматериалы</h3>
        <div class="drop-zone">Нажмите для выбора или перетащите фото</div>
    </div>

    <!-- БЛОК 4: 🎥 ВИДЕОМАТЕРИАЛЫ -->
    <div class="block">
        <h3>4. 🎥 Видеоматериалы</h3>
        <div class="drop-zone">Нажмите для выбора или перетащите видео</div>
    </div>

    <!-- БЛОК КОНТРОЛЯ С ДИНАМИЧЕСКИМ ТЕКСТОМ ГАЛОЧКИ -->
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
            { id: "draft1", date: "2026-10-20", title: "Сборка каркаса корабля", text: "Сегодня собирали палубу и шпангоуты.", discussion: "83", commit: "1867726", footer: "Преподаватель: Иванов И.И.\nВ кадре: Младшая группа" },
            { id: "draft2", date: "2026-10-22", title: "Тест сервоприводов робота", text: "Программировали контроллер, проверили углы поворота манипулятора.", discussion: "45", commit: "", footer: "В кадре: Робототехники" }
        ];

        let currentNormalDate = "2026-10-25";

        // Функция инициализации: по умолчанию третья линия заблокирована
        function initForm() {
            const container = document.getElementById("dynamic-field-container");
            container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
        }

        // ДИНАМИЧЕСКАЯ СМЕНА ТЕКСТА ГАЛОЧКИ КОНТРОЛЯ СТРОГО ПО ТЗ
        function updatePublishLabel() {
            const isChecked = document.getElementById("publish-now-flag").checked;
            const labelText = document.getElementById("publish-label-text");
            
            if (isChecked) {
                labelText.innerText = "🔥 Опубликовать сейчас (published: true)";
            } else {
                labelText.innerText = "📁 Сохранить как черновик (published: false)";
            }
        }

        // ЛИНИЯ 1 В ДЕЙСТВИИ: Переключение режима работы Линии 3 по клику на бестекстовую галочку
        function toggleDraftBehavior() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const container = document.getElementById("dynamic-field-container");
            
            if (isDraftMode) {
                // АКТИВНЫЙ РЕЖИМ: Линия 3 открывает список черновиков на всю ширину
                let selectHtml = `<select id="draft-select" onchange="loadDraftData(this.value)">`;
                selectHtml += `<option value="">-- Выберите сохраненный черновик --</option>`;
                mockDrafts.forEach(draft => {
                    selectHtml += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
                });
                selectHtml += `</select>`;
                container.innerHTML = selectHtml;
                
                // Переключаем нижний флаг в положение черновика и обновляем текст надписи
                document.getElementById("publish-now-flag").checked = false;
                updatePublishLabel();
            } else {
                // ДЕФОЛТНЫЙ РЕЖИМ: Линия 3 переходит в состояние заблокировано
                container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
                document.getElementById("publish-now-flag").checked = true;
                updatePublishLabel();
                
                // Полный сброс всей формы под новый чистый отчет
                document.getElementById("target-date").value = "2026-10-25";
                currentNormalDate = "2026-10-25";
                document.getElementById("post-title").value = "";
                document.getElementById("post-text").value = "";
                document.getElementById("post-footer").value = "";
                document.getElementById("discussion-number").value = "83";
                document.getElementById("commit-id").value = "";
            }
        }

        // ОБЪЕДИНЕННЫЙ БЛОК 2 В ДЕЙСТВИИ: Загрузка старых данных черновика без лишних подписей
        function loadDraftData(draftId) {
            if (!draftId) return;
            const selectedDraft = mockDrafts.find(d => d.id === draftId);
            if (selectedDraft) {
                // Синхронизируем Линию 1 и Линию 2 шапки
                document.getElementById("target-date").value = selectedDraft.date;
                currentNormalDate = selectedDraft.date;
                document.getElementById("discussion-number").value = selectedDraft.discussion;
                document.getElementById("commit-id").value = selectedDraft.commit;
                
                // Наполняем три текстовых поля объединенного Блока 2 один в один
                document.getElementById("post-title").value = selectedDraft.title;
                document.getElementById("post-text").value = selectedDraft.text;
                document.getElementById("post-footer").value = selectedDraft.footer;
            }
        }

        // Генерация итогового структурированного .md файла манифеста
        function generateMarkdownOutput() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const date = document.getElementById("target-date").value;
            const discussion = document.getElementById("discussion-number").value;
            const commitId = document.getElementById("commit-id").value;
            const title = document.getElementById("post-title").value;
            const text = document.getElementById("post-text").value;
            const footer = document.getElementById("post-footer").value;
            const publishNow = document.getElementById("publish-now-flag").checked;

            // Сборка Front Matter
            let md = `---\n`;
            md += `discussion_number: ${discussion}\n`;
            if (commitId) md += `comment_id: ${commitId}\n`;
            md += `date: ${date}\n`;
            md += `published: ${publishNow}\n`;
            md += `---\n\n`;
            
            // Наполнение контентом
            if (title) md += `## ${title}\n\n`;
            if (text) md += `${text}\n\n`;
            
            md += `### 📸 Фотоматериалы\n![[photo_01.jpg]]\n\n`;
            md += `### 🎥 Видеоматериалы\n\n`;
            
            // Если подвал заполнен, приписываем его чистый текст вниз через черту
            if (footer) {
                md += `---\n${footer}\n`;
            }

            alert("Сформирован следующий Markdown-текст:\n\n" + md);
        }

        // Стартовая инициализация при загрузке страницы
        initForm();
    </script>
</body>
</html>
