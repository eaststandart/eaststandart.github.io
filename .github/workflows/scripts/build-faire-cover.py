# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка фотопанорамы Hackaday.io из фотографий проектов и мастерской.
# @purpose Показывает реальные этапы конструирования, пайки, монтажа и сборки.
# @author  TechLab
# @version 1.7.0
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
    return ImageEnhance.Color(photo).enhance(0.96)

def paste_scene(canvas, photo, rect, polygon, centering=(0.5, 0.5)):
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
        (x + 6, y + 8, x + width + 6, y + height + 8),
        radius=8, fill=(0, 0, 0, 185)
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(12)))
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=7, fill=255)
    canvas.paste(frame, (x, y), mask)
    ImageDraw.Draw(canvas).rounded_rectangle(
        (x, y, x + width - 1, y + height - 1),
        radius=7, outline=(226, 240, 243, 225), width=2
    )

def main():
    # Фон — рабочее место мастерской из проекта «Условные обозначения».
    canvas = fit(
        load_photo("faire/pano-uslovnye-oboznacheniya/pano-uslovnye-oboznacheniya-02.webp"),
        SIZE, (0.50, 0.55)
    ).convert("RGBA")

    # Три крупных перекрывающихся сюжета, объединённые диагональными переходами.
    # Sputnik-1: проволочная конструкция и макетирование на столе.
    paste_scene(
        canvas,
        load_photo("faire/sputnik-1/sputnik-1-03.webp"),
        (0, 0, 690, 400),
        [(0, 0), (650, 0), (565, 400), (0, 400)],
        (0.52, 0.48),
    )

    # Электронный орган: обратная сторона платы с реальными паяными соединениями.
    paste_scene(
        canvas,
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-36.webp"),
        (565, 0, 1370, 400),
        [(650, 0), (1390, 0), (1305, 400), (565, 400)],
        (0.50, 0.50),
    )

    # Метроном: навесной монтаж компонентов на медных шинах крупным планом.
    paste_scene(
        canvas,
        load_photo("faire/metronom-signalnyj/metronom-signalnyj-24.webp"),
        (1305, 0, 1920, 400),
        [(1390, 0), (1920, 0), (1920, 400), (1305, 400)],
        (0.50, 0.50),
    )

    # Отдельный кадр платы в руках связывает пайку с изготовлением платы.
    inset(
        canvas,
        load_photo("faire/elektronnyj-organ/elektronnyj-organ-25.webp"),
        (740, 22, 410, 220),
        (0.50, 0.50),
    )

    # Тонкая нижняя подпись, без карточных рамок и декоративных пиктограмм.
    shade = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(305, 400):
        alpha = int(125 * ((y - 305) / 95) ** 1.2)
        sd.line((0, y, 620, y), fill=(4, 10, 16, alpha))
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
