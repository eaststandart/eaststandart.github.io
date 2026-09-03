---
layout: page
title: Tест с преобразованием ссылок фото и видео
permalink: /test/links/
---

### Тестирование модуля одиночных журнальных блоков (fig)

#### 🌅 Группа 1: Базовые горизонтальные одиночки (Landscape)

1-1. `![{fig}|400](url)`
![{fig}|400](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

1-2. `![{fig}|Текст подписи|400](url)`
![{fig}|Текст подписи|400](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

1-3. `![{fig|alt text}|Текст подписи|400](url)`
![{fig|alt text}|Текст подписи|400](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)


#### 🌌 Группа 2: Стандартные вертикальные одиночки (Portrait)

2-1. `![{fig|v}](url)`
![{fig|v}](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

2-2. `![{fig|v}|Текст подписи](url)`
![{fig|v}|Текст подписи](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

2-3. `![{fig|v|alt text}|Текст подписи](url)`
![{fig|v|alt text}|Текст подписи](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

2-4. `![{fig|alt text|v}|Текст подписи|300](url)`
![{fig|alt text|v}|Текст подписи|300](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)


#### 🛠️ Группа 3: Кастомные размеры (Сравнение сторон за 1 шаг)

3-1. `![{fig|152x503}|Текст подписи](url)`
![{fig|152x503}|Текст подписи](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

3-2. `![{fig|503x152}|Текст подписи](url)`
![{fig|503x152}|Текст подписи](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

3-3. `![{fig|503x152|alt text}|Текст подписи|400](url)`
![{fig|503x152|alt text}|Текст подписи|400](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

3-4. `![{fig|152x503|alt text}|Текст подписи](url)`
![{fig|152x503|alt text}|Текст подписи](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)

3-5. `![{fig|503х152}|Текст подписи](url)`
![{fig|503х152}|Текст подписи](github/eaststandart.github.io/faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)


#### 🔒 Группа 4: Неприкосновенные блоки (Проверка сейфа кода)

4-1. Строчный код
`![{fig|alt text}|Текст подписи|400](faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)`

4-2. Многострочный блок кода
```markdown
![{fig|503x152}|Текст подписи|400](faire/fonarik-svetodiodnyj-bumazhnyj/fonarik-svetodiodnyj-bumazhnyj-05.webp)
```


### Одиночные картинки

1-1 `!\[](url) и ![[путь]] `

![](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp)

![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp]]

![](../faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp)

1-2 `![{v}](url) и ![[путь|{v}]]`

![{v}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)

![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{v}]]

1-3  `![{alt text}](url) и ![[путь|{alt text}]]`

![{alt text}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp)

![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp|{alt text}]]

1-4  `![{v|alt text}](url) и ![[путь|{v|alt text}]]`

![{v|alt text}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)

![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{v|alt text}]]

1-5 `![{320x405}](url) и ![[путь|{320x405}]]`

![{320x405}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)

![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{320x405}]]

1-6  `![{320x405|alt text}](url) и ![[путь|{320x405|alt text}]]`

![{320x405|alt text}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)

![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{320x405|alt text}]]

1-7  `![{alt text}|400](url) и ![[путь|{alt text}|400]]`

![{alt text}|400](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)

![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{alt text|400}]]

#### Групповые картинки

2-1 `!\[](url) и ![[путь]] `

![](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp)
![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp]]
![](../faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp)

2-2 `![{v}](url) и ![[путь|{v}]]`

![{v}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)
![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{v}]]

2-3  `![{alt text}](url) и ![[путь|{alt text}]]`

![{alt text}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp)
![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-19.webp|{alt text}]]

2-4  `![{v|alt text}](url) и ![[путь|{v|alt text}]]`

![{v|alt text}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)
![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{v|alt text}]]

2-5 `![{320x405}](url) и ![[путь|{320x405}]]`

![{320x405}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)
![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{320x405}]]

2-6  `![{320x405|alt text}](url) и ![[путь|{320x405|alt text}]]`

![{320x405|alt text}](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)
![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{320x405|alt text}]]

2-7  `![{alt text}|400](url) и ![[путь|{alt text}|400]]`

![{alt text}|400](github/eaststandart.github.io/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)
![[../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp|{alt text|400}]]

#### Сокращенный вариант записи ссылки

3-7 `![](путь) ![](/путь) ![](../путь)`

1 `![](folder/test-v.webp)`

![](folder/test-v.webp)

2 `![](faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)`

![](faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)

3 `![](/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)`

![](/faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)

4 `![](../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)`

![](../faire/muzykalnyj-karandash/muzykalnyj-karandash-02.webp)


#### Ссылки в тексте

Посмотрим, из чего она состоит: *R1* – резистор с сопротивлением 1–6,8 кОм, *R2* – резистор с сопротивлением 2,7–3,6 кОм, *С1* – конденсатор емкостью 10 мкФ х 10 В, рассчитанный на рабочее напряжение не ниже 6–10 В, *VT1* – любой маломощный транзистор структуры *p-n-p* (МП39–МП42). *G1* – батарея питания напряжением 9 В типа «Крона». *SA1* – выключатель любой конструкции. *Т1* – любой выходной трансформатор транзисторного радиоприемника (ТВКП – трансформатор выходной карманного приемника), от радиоточки (абонентского громкоговорителя) или [[самодельный трансформатор|самодельный]]. *BA1* – любой динамик до 0,5 Вт сопротивлением 8 Ом, возможно от радиоточки.


