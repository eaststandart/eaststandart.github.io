---
layout: page
title: Тестирование модуля базовых изображений (img_base.py)
permalink: /test/img-base/
---

## Часть 1: Одиночные базовые картинки (Сборка одиночных кадров в теге p)

1-1. Запись: ![](url)
   
![](test/folder/test.webp)

1-2. Запись: ![Текст подписи](url)
   
![Человеческий текст подписи одиночной базовой картинки](test/folder/test.webp)

![|Человеческий текст подписи одиночной базовой картинки](test/folder/test.webp)

![{alt text}](test/folder/test.webp)

![{alt text}|Человеческий текст подписи одиночной базовой картинки](test/folder/test.webp)

1-3. Запись: ![{v}](url)
   
![{v}](test/folder/test.webp)

1-4. Запись: ![{v}|Текст подписи](url)
   
![{v} | Вертикальная базовая картинка с человеческой подписью](test/folder/test.webp)

1-5. Запись: ![{503x152}|Текст подписи] (Кастомный широкий ландшафт)
   
![{503x152} | Базовый широкий кадр с вычислением соотношения сторон](test/folder/test.webp)

1-6. Запись: ![{152x503}|Текст подписи] (Кастомный узкий портрет)
   
![{152x503} | Базовый узкий кадр с вычислением соотношения сторон](test/folder/test.webp)

1-7. Запись: ![{503х152}|Текст подписи] (Защита от опечатки - русская х)
   
![{503х152} | Проверка корректности перехвата русской раскладки](test/folder/test.webp)

1-8. Запись: ![Текст подписи|400](url) (Очистка хвоста ширины Obsidian)
   
![Чистый текст описания с обсидиановым хвостом ширины|400](test/folder/test.webp)


## Часть 2: Групповые базовые картинки (Автоматическая сборка галерей)

2-1. Запись: ![](url) / ![](url) (Два ландшафта подряд)
   
![](test/folder/test.webp)
![](test/folder/test.webp)

2-2. Запись: ![{v}](url) / ![{v}](url) (Два портрета подряд)
   
![{v} | Левый кадр базовой галереи](test/folder/test.webp)
![{v} | Правый кадр базовой галереи](test/folder/test.webp)

2-3. Запись: ![](url) / ![{v}](url) (Ландшафт + Портрет)
   
![](test/folder/test.webp)
![{v} | Правый вертикальный кадр в базовом ряду](test/folder/test.webp)

2-4. Запись: ![{v}](url) / ![](url) (Портрет + Ландшафт)
   
![{v} | Левый вертикальный кадр в базовом ряду](test/folder/test.webp)
![](test/folder/test.webp)

2-5. Запись: ![](url) / ![](url) / ![](url) (Три ландшафта подряд)
   
![](test/folder/test.webp)
![](test/folder/test.webp)
![](test/folder/test.webp)

2-6. Запись: ![{v}](url) / ![{v}](url) / ![{v}](url) (Три портрета подряд)
   
![{v}](test/folder/test.webp)
![{v}](test/folder/test.webp)
![{v}](test/folder/test.webp)

2-7. Запись: ![](url) / ![{v}](url) / ![{v}](url) (Ландшафт + Два портрета)
   
![](test/folder/test.webp)
![{v}](test/folder/test.webp)
![{v}](test/folder/test.webp)

2-8. Запись: ![{v}](url) / ![{v}](url) / ![](url) (Два портрета + Ландшафт)
   
![{v}](test/folder/test.webp)
![{v}](test/folder/test.webp)
![](test/folder/test.webp)

2-9. Запись: ![{v}](url) / ![](url) / ![{v}](url) (Портрет + Ландшафт + Портрет)
   
![{v}](test/folder/test.webp)
![](test/folder/test.webp)
![{v}](test/folder/test.webp)

2-10. Запись: ![](url) / ![{v}](url) / ![](url) (Ландшафт + Портрет + Ландшафт)
   
![](test/folder/test.webp)
![{v}](test/folder/test.webp)
![](test/folder/test.webp)