# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка профессиональной обложки Hackaday.io из реальных кадров Faire.
# @purpose Создаёт цельную фотокомпозицию 1920x400 px без изменения исходников.
# @author  TechLab
# @version 1.1.0
# ==============================================================================

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import math

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output" / "faire-cover-1920x400.jpg"
SIZE = (1920, 400)

# Кадры из проектов Faire. Часть WebP-файлов — превью соответствующих видео.
SCENES = [
    ("faire/robot-strannik/robot-strannik-01.webp", (0, 0, 470, 400), "robot"),
    ("faire/detektor-pereliva/detektor-pereliva-02.webp", (390, 0, 1120, 400), "electronics"),
    ("faire/elektronnyj-organ/elektronnyj-organ-01.webp", (1010, 0, 1510, 400), "instrument"),
    ("faire/podstavka-dlya-oscillografa/podstavka-dlya-oscillografa-05.webp", (1430, 0, 1920, 400), "lab"),
]
DETAILS = [
    ("faire/vibrohod-iz-zubnoj-shchetki/vibrohod-iz-zubnoj-shchetki-01.webp", (90, 238, 390, 390)),
    ("faire/blaster-elektroakusticheskij/blaster-elektroakusticheskij-02.webp", (1510, 22, 1850, 190)),
]

def load_photo(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Не найден кадр: {relative_path}")
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGB")

def fit_photo(photo, size, centering=(0.5, 0.5)):
    return ImageOps.fit(photo, size, method=Image.Resampling.LANCZOS, centering=centering)

def scene_mask(size, polygon):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    return mask

def add_scene(canvas, photo, rect, polygon):
    x, y, w, h = rect
    frame = fit_photo(photo, (w, h))
    mask = scene_mask((w, h), [(px - x, py - y) for px, py in polygon])
    canvas.paste(frame, (x, y), mask)

def add_detail(canvas, photo, rect):
    x, y, w, h = rect
    frame = fit_photo(photo, (w, h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=9, fill=255)
    shadow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((x + 5, y + 7, x + w + 5, y + h + 7),
                                              radius=10, fill=(0, 0, 0, 150))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    canvas.paste(frame, (x, y), mask)
    ImageDraw.Draw(canvas).rounded_rectangle((x, y, x + w - 1, y + h - 1),
                                               radius=9, outline=(225, 239, 242, 170), width=2)

def main():
    photos = {path: load_photo(path) for path, _, _ in SCENES}
    photos.update({path: load_photo(path) for path, _ in DETAILS})
    canvas = Image.new("RGB", SIZE, (13, 20, 27))

    # Фотосцены собираются в одну панораму с диагональными переходами,
    # а не в ряд одинаковых карточек.
    polygons = [
        [(0, 0), (505, 0), (435, 400), (0, 400)],
        [(505, 0), (1190, 0), (1105, 400), (435, 400)],
        [(1190, 0), (1575, 0), (1510, 400), (1105, 400)],
        [(1575, 0), (1920, 0), (1920, 400), (1510, 400)],
    ]
    for (path, rect, _), polygon in zip(SCENES, polygons):
        add_scene(canvas, photos[path], rect, polygon)

    # Затемнение по краям и снизу помогает композиции выглядеть цельно
    # и сохраняет читаемость короткой подписи.
    shade = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(650):
        alpha = int(155 * (1 - x / 650) ** 1.7)
        sd.line((x, 0, x, 400), fill=(5, 12, 18, alpha))
    for y in range(250, 400):
        alpha = int(105 * ((y - 250) / 150))
        sd.line((0, y, 1920, y), fill=(5, 12, 18, alpha))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shade)

    # Два небольших кадра-детали добавляют ощущение репортажа с рабочего места.
    for path, rect in DETAILS:
        add_detail(canvas, photos[path], rect)

    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    small_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    title_font = ImageFont.truetype(font_path, 43)
    sub_font = ImageFont.truetype(small_path, 15)
    draw.text((58, 42), "TECHLAB", font=title_font, fill=(248, 251, 252, 255),
              stroke_width=1, stroke_fill=(8, 14, 20, 130))
    draw.text((62, 96), "ENGINEERING IN ACTION", font=sub_font,
              fill=(105, 225, 225, 255), spacing=4)

    # Тонкая техническая линия и маркеры — только графическая связка сцен.
    draw.line((62, 126, 286, 126), fill=(95, 210, 214, 210), width=2)
    draw.ellipse((282, 122, 290, 130), fill=(120, 235, 230, 255))
    draw.line((0, 397, 1920, 397), fill=(77, 198, 204, 130), width=2)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "JPEG", quality=94, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-faire-cover] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")

if __name__ == "__main__":
    main()
