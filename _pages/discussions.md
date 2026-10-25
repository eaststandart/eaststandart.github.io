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
    <title>Конструктор Отчетов TechLab v6</title>
    <style>
        body { font-family: sans-serif; max-width: 480px; margin: 10px auto; padding: 10px; background: #f4f4f4; color: #333; }
        .block { background: #fff; border: 1px solid #ccc; padding: 12px; margin-bottom: 12px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        h3 { margin-top: 0; margin-bottom: 10px; color: #444; border-bottom: 1px solid #eee; padding-bottom: 5px; font-size: 16px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px; color: #555; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; background: #fff; }
        
        /* ТРЁХЛИНЕЙНАЯ СТРУКТУРА ШАПКИ ДЛЯ МОБИЛЬНЫХ ЭКРАНОВ */
        .header-line { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
        .header-line:last-child { margin-bottom: 0; }
        .inline-label { font-weight: bold; font-size: 14px; color: #444; white-space: nowrap; }
        
        /* Строгие фиксированные размеры полей по лимитам CMS */
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

    <h3 style="text-align: center; color: #0076ff; font-size: 18px; margin-bottom: 15px;">Унифицированная форма TechLab v6</h3>

    <!-- БЛОК 1: ТРЁХЛИНЕЙНАЯ УПРАВЛЯЮЩАЯ ШАПКА CMS -->
    <div class="block">
        <h3>1. Параметры публикации</h3>
        
        <!-- ЛИНИЯ 1: Дата + Черновик с бестекстовой галочкой -->
        <div class="header-line">
            <span class="inline-label">Дата:</span>
            <input type="text" id="target-date" class="input-date" maxlength="10" value="2026-10-25" placeholder="YYYY-MM-DD" onchange="currentNormalDate=this.value">
            
            
            <label class="draft-trigger"><span class="inline-label">Черновик:</span><input type="checkbox" id="is-draft-mode" onchange="toggleDraftBehavior()"></label>
        </div>

        <!-- ЛИНИЯ 2: Дискуссия № (3 цифры) + Коммит (8 цифр) -->
        <div class="header-line">
            <span class="inline-label">Дискуссия:</span>
            <input type="text" id="discussion-number" class="input-disc" maxlength="3" value="" placeholder="№">
            
            <span class="inline-label" style="margin-left: auto;">#:</span>
            <input type="text" id="commit-id" class="input-commit" maxlength="8" value="" placeholder="коммит">
        </div>

        <!-- ЛИНИЯ 3: Поле черновиков на всю ширину экрана -->
        <div class="header-line" style="margin-top: 12px;">
            <div id="dynamic-field-container" style="width: 100%;">
                <!-- Изначально заблокировано скриптом: "черновиков нет" -->
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

        // ЛИНИЯ 1 В ДЕЙСТВИИ: Логика управления Линией 3 по клику на бестекстовую галочку
        function toggleDraftBehavior() {
            const isDraftMode = document.getElementById("is-draft-mode").checked;
            const container = document.getElementById("dynamic-field-container");
            const publishFlag = document.getElementById("publish-now-flag");

            if (isDraftMode) {
                // АКТИВНЫЙ РЕЖИМ: Линия 3 разворачивает список черновиков на всю ширину экрана
                let selectHtml = `<select id="draft-select" onchange="loadDraftData(this.value)">`;
                selectHtml += `<option value="">-- Выберите сохраненный черновик --</option>`;
                mockDrafts.forEach(draft => {
                    selectHtml += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
                });
                selectHtml += `</select>`;
                container.innerHTML = selectHtml;
                
                // Перевод флага контроля в режим черновика
                publishFlag.checked = false;
            } else {
                // ДЕФОЛТНЫЙ РЕЖИМ: Линия 3 переходит в состояние заблокировано строго по ТЗ
                container.innerHTML = `<select id="draft-select" disabled><option value="">черновиков нет</option></select>`;
                publishFlag.checked = true;
                
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

        // ЛИНИИ 1 И 2 В ДЕЙСТВИИ: Наполнение шапки оригинальными данными выбранного черновика
        function loadDraftData(draftId) {
            if (!draftId) return;
            const selectedDraft = mockDrafts.find(d => d.id === draftId);
            if (selectedDraft) {
                // Синхронизируем Линию 1 и Линию 2 без принудительных дописок текста
                document.getElementById("target-date").value = selectedDraft.date;
                currentNormalDate = selectedDraft.date;
                document.getElementById("discussion-number").value = selectedDraft.discussion;
                document.getElementById("commit-id").value = selectedDraft.commit;
                
                // Обновляем описание, заголовок и подвал отчета один в один
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

            // БЛОК 1: Сборка оригинального Front Matter
            let md = `---\n`;
            md += `discussion_number: ${discussion}\n`;
            if (commitId) md += `comment_id: ${commitId}\n`;
            md += `date: ${date}\n`;
            md += `published: ${publishNow}\n`;
            md += `---\n\n`;
            
            // БЛОК 2 И 3: Заголовок и Текст описания
            if (title) md += `## ${title}\n\n`;
            if (text) md += `${text}\n\n`;
            
            // БЛОК 4 И 5: Жестко заданные Markdown-заголовки медиаматериалов
            md += `### 📸 Фотоматериалы\n![[photo_01.jpg]]\n\n`;
            md += `### 🎥 Видеоматериалы\n\n`;
            
            // БЛОК 6: Обычный текст подвала, приписываемый через черту
            if (footer) {
                md += `---\n${footer}\n`;
            }

            alert("Сформирован следующий Markdown-текст:\n\n" + md);
        }

        // Запуск инициализации при загрузке страницы
        initForm();
    </script>
</body>
</html>
