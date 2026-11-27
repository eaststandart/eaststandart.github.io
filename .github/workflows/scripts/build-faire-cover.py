# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка инженерной фотопанорамы Hackaday.io из материалов Faire.
# @purpose Акцент на изготовлении печатных плат, пайке, измерениях и рабочем месте.
# @author  TechLab
# @version 1.5.0
# ==============================================================================

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output" / "faire-cover-1920x400.jpg"
SIZE = (1920, 400)

def load_photo(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Не найдено фото: {relative_path}")
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGB")

def fit(photo, size, centering=(0.5, 0.5)):
    photo = ImageOps.fit(photo, size, method=Image.Resampling.LANCZOS, centering=centering)
    photo = ImageEnhance.Contrast(photo).enhance(1.07)
    return ImageEnhance.Color(photo).enhance(0.94)

def scene(canvas, photo, rect, polygon, centering=(0.5, 0.5)):
    x, y, width, height = rect
    frame = fit(photo, (width, height), centering)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).polygon([(px - x, py - y) for px, py in polygon], fill=255)
    canvas.paste(frame, (x, y), mask)

def inset(canvas, photo, rect, centering=(0.5, 0.5)):
    x, y, width, height = rect
    frame = fit(photo, (width, height), centering)
    shadow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (x + 5, y + 8, x + width + 5, y + height + 8),
        radius=7, fill=(0, 0, 0, 175)
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(11)))
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=6, fill=255)
    canvas.paste(frame, (x, y), mask)
    ImageDraw.Draw(canvas).rounded_rectangle(
        (x, y, x + width - 1, y + height - 1),
        radius=6, outline=(225, 239, 241, 220), width=2
    )

def main():
    # Основа — не готовое изделие, а реальный стол с инструментом и оснасткой.
    canvas = fit(
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-29.webp"),
        SIZE, (0.52, 0.50)
    ).convert("RGBA")

    # Слева — изготовленные печатные платы и заготовки.
    scene(
        canvas,
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-17.webp"),
        (0, 0, 620, 400),
        [(0, 0), (590, 0), (510, 400), (0, 400)],
        (0.50, 0.50),
    )

    # В центре — пайка/электромонтаж: паяльник, кусачки и собираемое устройство.
    scene(
        canvas,
        load_photo("faire/metronom-signalnyj/metronom-signalnyj-05.webp"),
        (500, 0, 1320, 400),
        [(590, 0), (1350, 0), (1270, 400), (510, 400)],
        (0.48, 0.50),
    )

    # Правая часть — измерительный прибор на фоне настоящей мастерской.
    scene(
        canvas,
        load_photo("faire/podstavka-dlya-oscillografa/podstavka-dlya-oscillografa-06.webp"),
        (1270, 0, 1920, 400),
        [(1350, 0), (1920, 0), (1920, 400), (1270, 400)],
        (0.50, 0.50),
    )

    # Дополнительная крупная деталь платы, снятой в руках.
    inset(
        canvas,
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-26.webp"),
        (900, 24, 430, 245),
        (0.50, 0.50),
    )

    # Небольшая подпись поверх затемнённого нижнего левого края.
    shade = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(300, 400):
        alpha = int(125 * ((y - 300) / 100) ** 1.2)
        sd.line((0, y, 520, y), fill=(5, 12, 18, alpha))
    canvas = Image.alpha_composite(canvas, shade)

    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 29)
    sub_font = ImageFont.truetype(font_path, 11)
    draw.text((46, 326), "TECHLAB", font=title_font,
              fill=(250, 252, 253, 250), stroke_width=1,
              stroke_fill=(8, 14, 20, 190))
    draw.text((49, 360), "ENGINEERING IN ACTION", font=sub_font,
              fill=(116, 225, 225, 250))
    draw.line((0, 397, 1920, 397), fill=(77, 198, 204, 130), width=2)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "JPEG", quality=94, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-faire-cover] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")

if __name__ == "__main__":
    main()
