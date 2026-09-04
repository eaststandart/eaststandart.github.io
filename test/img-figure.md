---
layout: page
title: Тестирование модуля групповых журнальных блоков (img_figure.py)
permalink: /test/img-figure/
---

## Часть 1: Одиночные журнальные картинки (Сборка одиночных кадров в блоки figure)

1-1. Запись: ![{fig}](url)
   
![{fig}](/test/folder/test.webp)

1-2. Запись: ![{fig}|Текст подписи](url) (Закон дублирования подписи в alt)
   
![{fig} | Человеческий текст подписи одиночного журнального ландшафта](/test/folder/test.webp)

1-3. Запись: ![{fig|v}](url)
   
![{fig|v}](/test/folder/test.webp)

1-4. Запись: ![{fig|v}|Текст подписи](url) (Вертикальный журнальный кадр)
   
![{fig|v} | Человеческий текст подписи одиночного журнального портрета](/test/folder/test.webp)

1-5. Запись: ![{fig|alt text}](url) (Только скрытый SEO Alt, без подписи для людей)
   
![{fig|скрытый seo alt одиночного кадра}](/test/folder/test.webp)

1-6. Запись: ![{fig|alt text}|Текст подписи](url) (Полное независимое разделение текстов)
   
![{fig|скрытый seo alt ландшафта} | Человеческий текст подписи журнального блока](/test/folder/test.webp)

1-7. Запись: ![{fig|v|alt text}|Текст подписи](url) (Полное разделение для вертикального кадра)
   
![{fig|v|скрытый seo alt портрета} | Человеческий текст подписи вертикального журнального блока](/test/folder/test.webp)

1-8. Запись: ![{fig|503x152}|Текст подписи] (Кастомный широкий журнальный ландшафт)
   
![{fig|503x152} | Кастомный широкий журнальный блок с вычислением соотношения сторон](/test/folder/test.webp)

1-9. Запись: ![{fig|152x503}|Текст подписи] (Кастомный узкий журнальный портрет)
   
![{fig|152x503} | Кастомный узкий журнальный блок с вычислением соотношения сторон](/test/folder/test.webp)

1-10. Запись: ![{fig|503х152}|Текст подписи] (Защита от опечатки - русская х в журнальном блоке)
   
![{fig|503х152} | Проверка корректности перехвата русской раскладки в журнальном блоке](/test/folder/test.webp)

1-11. Запись: ![{fig}|Текст подписи|400](url) (Очистка хвоста ширины Obsidian в журнальном блоке)
   
![{fig} | Чистый текст журнального описания с обсидиановым хвостом ширины|400](/test/folder/test.webp)


## Часть 2: Групповые журнальные картинки (Сборка групповых кадров в блоки figure)

### Группа 1: Двойные ряды без текста (Различные формы кадров)

1-1. Запись: ![{fig}](url) / ![{fig}](url)
   
![{fig}](/test/folder/test.webp)
![{fig}](/test/folder/test.webp)

1-2. Запись: ![{fig|v}](url) / ![{fig|v}](url)
   
![{fig|v}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)

1-3. Запись: ![{fig}](url) / ![{fig|v}](url)
   
![{fig}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)

1-4. Запись: ![{fig|v}](url) / ![{fig}](url)
   
![{fig|v}](/test/folder/test.webp)
![{fig}](/test/folder/test.webp)


### Группа 2: Двойные ряды с текстом (SEO Alt, Живые подписи и Дублирование)

2-1. Запись: ![{fig|alt text}](url) / ![{fig}|Текст подписи](url)
   
![{fig|alt text}](/test/folder/test.webp)
![{fig}|Текст подписи](/test/folder/test.webp)

2-2. Запись: ![{fig|v|alt text}|ПОДПИСЬ](url) / ![{fig|v}|ПОДПИСЬ](url)
   
![{fig|v|левый alt}|Левая живая подпись](/test/folder/test.webp)
![{fig|v}|Правая живая подпись](/test/folder/test.webp)

2-3. Запись: ![{fig}|Подпись 1](url) / ![{fig}|Подпись 2](url)
   
![{fig}|Первая живая подпись](/test/folder/test.webp)
![{fig}|Вторая живая подпись](/test/folder/test.webp)

2-4. Запись: ![{fig|alt text 1}](url) / ![{fig|alt text 2}](url)
   
![{fig|alt text 1}](/test/folder/test.webp)
![{fig|alt text 2}](/test/folder/test.webp)


### Группа 3: Тройные ряды во всех возможных комбинациях форм (Максимум 3 кадра)

3-1. Запись: ![{fig}](url) / ![{fig}](url) / ![{fig}](url)
   
![{fig}](/test/folder/test.webp)
![{fig}](/test/folder/test.webp)
![{fig}](/test/folder/test.webp)

3-2. Запись: ![{fig|v}](url) / ![{fig|v}](url) / ![{fig|v}](url)
   
![{fig|v}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)

3-3. Запись: ![{fig}](url) / ![{fig|v}](url) / ![{fig|v}](url)
   
![{fig}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)

3-4. Запись: ![{fig|v}](url) / ![{fig|v}](url) / ![{fig}](url)
   
![{fig|v}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)
![{fig}](/test/folder/test.webp)

3-5. Запись: ![{fig|v}](url) / ![{fig}](url) / ![{fig|v}](url)
   
![{fig|v}](/test/folder/test.webp)
![{fig}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)

3-6. Запись: ![{fig}](url) / ![{fig|v}](url) / ![{fig}](url)
   
![{fig}](/test/folder/test.webp)
![{fig|v}](/test/folder/test.webp)
![{fig}](/test/folder/test.webp)


### Группа 4: Тройные ряды со сложным смешанным текстом

4-1. Запись: ![{fig}|Текст 1](url) / ![{fig|alt 2}](url) / ![{fig|v|alt 3}|Текст 3](url)
   
![{fig}|Левая живая подпись](/test/folder/test.webp)
![{fig|центральный alt}](/test/folder/test.webp)
![{fig|v|правый alt}|Правая живая подпись](/test/folder/test.webp)

4-2. Запись: ![{fig|v}](url) / ![{fig}|Текст 2](url) / ![{fig}](url)
   
![{fig|v}](/test/folder/test.webp)
![{fig}|Центральная подпись](/test/folder/test.webp)
![{fig}](/test/folder/test.webp)


### Группа 5: Проверка кастомных размеров и опечаток раскладки внутри рядов

5-1. Запись: ![{fig|503x152}](url) / ![{fig|152x503}](url)
   
![{fig|503x152|ландшафт}](/test/folder/test.webp)
![{fig|152x503|портрет}](/test/folder/test.webp)

5-2. Запись: ![{fig|503х152}](url) / ![{fig|503x152}](url)
   
![{fig|503х152|русская х}](/test/folder/test.webp)
![{fig|503x152|английская x}](/test/folder/test.webp)
