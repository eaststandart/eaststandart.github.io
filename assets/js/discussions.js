/**
 * @module  discussions.js
 * @about   Ядро логики Конструктора Отчетов и взаимодействия с медиа-шлюзом.
 * @purpose Сквозная перенумерация блоков, раздельный парсинг полей, управление семафором защиты сессии.
 * @author  TechLab
 * @version 2.0.0
 */

// Имитация базы данных черновиков, полученных из папки _input медиа-репозитория
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

// Функция инициализации: жестко набиваем селект дефолтным текстом и блокируем
function initForm() {
    const select = document.getElementById("draft-select");
    if (select) {
        select.innerHTML = `<option value="">черновиков нет</option>`;
        select.disabled = true;
    }
    addPhotoBlock();
    addVideoBlock();
}

// Отслеживание ручного изменения поля даты
function updateNormalDateValue(val) {
    currentNormalDate = val;
}

// АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ФОТО
function updatePhotoDeleteButtons() {
    const blocks = document.querySelectorAll("#photos-meta-container .media-sub-block");
    blocks.forEach((block) => {
        const deleteContainer = block.querySelector(".btn-delete-container");
        if (deleteContainer) {
            deleteContainer.style.display = (blocks.length > 1) ? "block" : "none";
        }
    });
}

// АВТОМАТИЧЕСКИЙ КОНТРОЛЬ КНОПОК УДАЛЕНИЯ ДЛЯ ВИДЕО
function updateVideoDeleteButtons() {
    const blocks = document.querySelectorAll("#videos-meta-container .media-sub-block");
    blocks.forEach((block) => {
        const deleteContainer = block.querySelector(".btn-delete-container");
        if (deleteContainer) {
            deleteContainer.style.display = (blocks.length > 1) ? "block" : "none";
        }
    });
}

// ДОБАВЛЕНИЕ БЛОКА ФОТО С ВАШИМИ ПОДПИСЯМИ И КНОПКОЙ УДАЛЕНИЯ
function addPhotoBlock() {
    photoBlockIdx++;
    const container = document.getElementById("photos-meta-container");
    if (!container) return;
    
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
    if (!container) return;
    
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
        if (submitBtn) {
            submitBtn.innerText = message || "⏳ Обработка на сервере...";
            submitBtn.style.background = "#85b7ff";
        }
    } else {
        updatePublishLabel();
        if (submitBtn) submitBtn.style.background = "#0076ff";
    }
}

// ДИНАМИЧЕСКИЙ ПЕРЕКЛЮЧАТЕЛЬ ТЕКСТА КНОПКИ СТРОГО ПО ТЗ
function updatePublishLabel() {
    const isChecked = document.getElementById("publish-now-flag").checked;
    const labelText = document.getElementById("publish-label-text");
    const submitBtn = document.getElementById("submit-btn");
    
    if (isChecked) {
        if (labelText) labelText.innerText = "🔥 Опубликовать сейчас (published: true)";
        if (submitBtn) submitBtn.innerText = "Создать комментарий";
    } else {
        if (labelText) labelText.innerText = "🔥 Опубликовать сейчас (published: false)";
        if (submitBtn) submitBtn.innerText = "Сохранить черновик";
    }
}

// ЛИНИЯ 2 В ДЕЙСТВИИ: Включение и отключение селекта Линии 2
function toggleDraftBehavior() {
    const isDraftMode = document.getElementById("is-draft-mode").checked;
    const select = document.getElementById("draft-select");
    const publishFlag = document.getElementById("publish-now-flag");

    if (isDraftMode) {
        let html = `<option value="">-- Сохраненный черновик --</option>`;
        mockDrafts.forEach(draft => {
            html += `<option value="${draft.id}">[${draft.date}] ${draft.title}</option>`;
        });
        if (select) {
            select.innerHTML = html;
            select.disabled = false;
        }
        if (publishFlag) publishFlag.checked = false;
        updatePublishLabel();
    } else {
        if (select) {
            select.innerHTML = `<option value="">Выберите черновик --></option>`;
            select.disabled = true;
        }
        if (publishFlag) publishFlag.checked = true;
        updatePublishLabel();
        
        const dateInput = document.getElementById("target-date");
        if (dateInput) dateInput.value = "2026-10-25";
        currentNormalDate = "2026-10-25";
        
        document.getElementById("post-title").value = "";
        document.getElementById("post-text").value = "";
        document.getElementById("post-footer").value = "";
        document.getElementById("discussion-combo").value = "";
        document.getElementById("commit-id").value = "";
    }
}

// ЖЕСТКАЯ СИНХРОНИЗАЦИЯ: Моментальное наполнение раздельных полей Номера и Коммита на Линии 1
function loadDraftData(draftId) {
    if (!draftId) return;
    const selectedDraft = mockDrafts.find(d => d.id === draftId);
    if (selectedDraft) {
        // Обновляем Дату на Линии 1
        const dateInput = document.getElementById("target-date");
        if (dateInput) dateInput.value = selectedDraft.date;
        currentNormalDate = selectedDraft.date;
        
        // Точечно раскидываем значения по двум раздельным полям Линии 1
        const discInput = document.getElementById("discussion-combo");
        const commitInput = document.getElementById("commit-id");
        
        if (discInput) discInput.value = selectedDraft.discussion;
        if (commitInput) commitInput.value = selectedDraft.commit || "";
        
        // Наполняем контекст Блока 2
        document.getElementById("post-title").value = selectedDraft.title;
        document.getElementById("post-text").value = selectedDraft.text;
        document.getElementById("post-footer").value = selectedDraft.footer;
    }
}

// СКВОЗНАЯ ПЕРЕНУМЕРАЦИЯ И СБОРКА МАНИФЕСТА С РАЗДЕЛЬНЫХ ПОЛЕЙ ШАПКИ
function generateMarkdownOutput() {
    const date = document.getElementById("target-date").value;
    // Считываем значения напрямую из независимых полей без ручного парсинга дефиса
    const discussion = document.getElementById("discussion-combo").value.trim();
    const commitId = document.getElementById("commit-id").value.trim();
    
    const title = document.getElementById("post-title").value;
    const text = document.getElementById("post-text").value;
    const footer = document.getElementById("post-footer").value;
    const publishNow = document.getElementById("publish-now-flag").checked;

    let md = `---\n`;
    md += `discussion_number: ${discussion}\n`;
    if (commitId) md += `comment_id: ${commitId}\n`;
    md += `date: ${date}\n`;
    md += `published: ${publishNow}\n`;
    md += `status: on\n`;
    md += `---\n\n`;
    
    if (title) md += `## ${title}\n\n`;
    if (text) md += `${text}\n\n`;
    
    // Сборка динамических блоков ФОТО со сквозным двузначным пересчетом
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

    // Сборка динамических блоков ВИДЕО со сквозным двузначным пересчетом
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

// Запуск стартовой инициализации
initForm();
