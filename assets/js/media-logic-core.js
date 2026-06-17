/* ==========================================================================
   ЕДИНОЕ ЯДРО ПАРСИНГА МЕДИАФАЙЛОВ ОБСИДИАНА (media-logic-core.js)
   ========================================================================== */

function parseObsidianMedia() {
    // Выбираем все текстовые абзацы внутри контента статьи
    const paragraphs = document.querySelectorAll('.main-content p');

    paragraphs.forEach(p => {
        let html = p.innerHTML;

        // Если внутри абзаца есть хотя бы одна скобка Obsidian
        if (html.includes('![[')) {
            
            // Регулярное выражение находит все вхождения ![[ ... ]] внутри абзаца
            const regex = /!\[\[([^\]\n\r<]+)\]\]/g;
            
            // Заменяем каждую ссылку Obsidian на чистый HTML-тег <img> без инлайновых стилей
            html = html.replace(regex, function(match, rawPath) {
                // 1. Вырезаем технический корень GitHub по твоему требованию
                let cleanPath = rawPath.replace('github/eaststandart.github.io', '').trim();
                
                if (!cleanPath.startsWith('/')) {
                    cleanPath = '/' + cleanPath;
                }

                // 2. Возвращаем чистый оригинальный тег img, какой и был на сайте изначально
                return '<img src="' + cleanPath + '" alt="" />';
            });

            // Обновляем HTML внутри абзаца — теперь там лежат чистые теги <img>
            p.innerHTML = html;
        }
    });
}
