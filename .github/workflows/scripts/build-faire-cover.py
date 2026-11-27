# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка обложки Hackaday.io из фотографий проектов Faire.
# @purpose Создаёт отдельный артефакт 1920x400 px без изменения исходных файлов.
# @author  TechLab
# @version 1.0.0
# ==============================================================================

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import math

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output" / "faire-cover-1920x400.jpg"
SIZE = (1920, 400)

# Используются только существующие оригинальные фотографии из Faire.
PHOTOS = [
    "faire/robot-strannik/robot-strannik-01.webp",
    "faire/robot-krolik-iz-kartona/robot-krolik-iz-kartona-01.webp",
    "faire/blaster-elektroakusticheskij/blaster-elektroakusticheskij-01.webp",
    "faire/muzykalnyj-karandash/muzykalnyj-karandash-01.webp",
    "faire/podstavka-dlya-oscillografa/podstavka-dlya-oscillografa-01.webp",
    "faire/plavnoe-zazhiganie-svetodioda/plavnoe-zazhiganie-svetodioda-01.webp",
]

def load_photo(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Не найдена фотография: {relative_path}")
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGB")

def rounded_photo(canvas, photo, rect, radius=18, inset=3):
    x, y, w, h = rect
    image = ImageOps.fit(photo, (w, h), method=Image.Resampling.LANCZOS,
                         centering=(0.5, 0.5))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1),
                                           radius=radius, fill=255)
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((x + 4, y + 7, x + w + 4, y + h + 7),
                                  radius=radius, fill=(0, 0, 0, 125))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(9)))
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tile.paste(image, (0, 0), mask)
    canvas.alpha_composite(tile, (x, y))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((x, y, x + w - 1, y + h - 1),
                           radius=radius, outline=(160, 185, 198, 100), width=2)

def main():
    photos = [load_photo(p) for p in PHOTOS]
    canvas = Image.new("RGBA", SIZE, (17, 24, 31, 255))

    # Ненавязчивая инженерная сетка на фоне.
    grid = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, SIZE[0], 48):
        gd.line((x, 0, x, SIZE[1]), fill=(105, 145, 165, 18), width=1)
    for y in range(0, SIZE[1], 48):
        gd.line((0, y, SIZE[0], y), fill=(105, 145, 165, 18), width=1)
    canvas.alpha_composite(grid)

    # Шесть реальных кадров: робототехника, механика и электронные эксперименты.
    layout = [
        (24, 42, 286, 316),
        (326, 18, 306, 364),
        (648, 42, 286, 316),
        (950, 18, 306, 364),
        (1272, 42, 286, 316),
        (1574, 18, 322, 364),
    ]
    for photo, rect in zip(photos, layout):
        rounded_photo(canvas, photo, rect)

    # Тонкие сигнальные линии объединяют фотопанели в единую композицию.
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.line((24, 386, 1896, 386), fill=(69, 190, 198, 95), width=2)
    d.line((24, 14, 1896, 14), fill=(69, 190, 198, 55), width=1)
    for x in (310, 632, 954, 1266, 1568):
        d.ellipse((x - 3, 380, x + 3, 392), fill=(91, 211, 211, 180))
    canvas.alpha_composite(overlay)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "JPEG", quality=94, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-faire-cover] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")

if __name__ == "__main__":
    main()
