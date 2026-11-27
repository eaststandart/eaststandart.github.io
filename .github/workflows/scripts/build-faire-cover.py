# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка фотопанорамы Hackaday.io по реальным этапам проектов TechLab.
# @purpose Показывает конструирование, изготовление плат, монтаж, пайку и измерения.
# @author  TechLab
# @version 1.6.0
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
    photo = ImageEnhance.Contrast(photo).enhance(1.06)
    return ImageEnhance.Color(photo).enhance(0.97)

def panel(canvas, photo, rect, polygon, centering=(0.5, 0.5)):
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
        radius=7, fill=(0, 0, 0, 180)
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=6, fill=255)
    canvas.paste(frame, (x, y), mask)
    ImageDraw.Draw(canvas).rounded_rectangle(
        (x, y, x + width - 1, y + height - 1),
        radius=6, outline=(230, 240, 244, 225), width=2
    )

def main():
    # Фотопанорама собрана из конкретных кадров публикаций пользователя.
    # Слева направо: Sputnik-1 в мастерской, плата в руках,
    # пайка/монтаж на держателе, работающий узел на столе.
    canvas = Image.new("RGBA", SIZE, (10, 17, 24, 255))

    panel(
        canvas,
        load_photo("faire/sputnik-1/sputnik-1-03.webp"),
        (0, 0, 560, 400),
        [(0, 0), (525, 0), (455, 400), (0, 400)],
        (0.50, 0.48),
    )
    panel(
        canvas,
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-25.webp"),
        (455, 0, 1060, 400),
        [(525, 0), (1080, 0), (1010, 400), (455, 400)],
        (0.52, 0.50),
    )
    panel(
        canvas,
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-36.webp"),
        (1010, 0, 1515, 400),
        [(1080, 0), (1540, 0), (1470, 400), (1010, 400)],
        (0.50, 0.50),
    )
    panel(
        canvas,
        load_photo("faire/metronom-signalnyj/metronom-signalnyj-18.webp"),
        (1470, 0, 1920, 400),
        [(1540, 0), (1920, 0), (1920, 400), (1470, 400)],
        (0.52, 0.50),
    )

    # Детали процесса: готовая плата в монтажном держателе и осциллограмма.
    inset(
        canvas,
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-34.webp"),
        (700, 22, 390, 220),
        (0.50, 0.50),
    )
    inset(
        canvas,
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-41.webp"),
        (1430, 22, 420, 220),
        (0.50, 0.50),
    )

    # Подпись на затемнённом участке, не перекрывающем ключевые детали.
    shade = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(300, 400):
        alpha = int(130 * ((y - 300) / 100) ** 1.15)
        sd.line((0, y, 590, y), fill=(4, 10, 16, alpha))
    canvas = Image.alpha_composite(canvas, shade)

    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 29)
    sub_font = ImageFont.truetype(font_path, 11)
    draw.text((42, 326), "TECHLAB", font=title_font,
              fill=(250, 252, 253, 250), stroke_width=1,
              stroke_fill=(8, 14, 20, 190))
    draw.text((45, 360), "ENGINEERING IN ACTION", font=sub_font,
              fill=(116, 225, 225, 250))
    draw.line((0, 397, 1920, 397), fill=(77, 198, 204, 140), width=2)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "JPEG", quality=95, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-faire-cover] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")

if __name__ == "__main__":
    main()
