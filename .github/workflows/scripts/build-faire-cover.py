# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка обложки Hackaday.io из оригинальных фотографий TechLab.
# @purpose Сохраняет реальные изображения без генерации, наложения и деформации.
# @author  TechLab
# @version 3.0.0
# ==============================================================================

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output" / "faire-cover-1920x400.jpg"
SIZE = (1920, 400)
GUTTER = 5
BACKGROUND = (13, 22, 31)
PANELS = [
    ("Спутник-1", "faire/sputnik-1/sputnik-1-01.webp", 350, (0.52, 0.50)),
    ("Электронный орган", "faire/elektronnyj-organ/elektronnyj-organ-02.webp", 430, (0.50, 0.50)),
    ("Условные обозначения", "faire/pano-uslovnye-oboznacheniya/pano-uslovnye-oboznacheniya.webp", 300, (0.50, 0.50)),
    ("Метроном сигнальный", "faire/metronom-signalnyj/metronom-signalnyj-24.webp", 430, (0.50, 0.50)),
    ("Детектор перелива", "faire/detektor-pereliva/detektor-pereliva-09.webp", 390, (0.50, 0.50)),
]


def load_image(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Не найдено изображение: {relative_path}")
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGBA")


def panel_image(source, size, centering):
    width, height = size
    if source.getchannel("A").getextrema()[0] < 255:
        # Прозрачные предметные фото размещаем целиком, не обрезая объект.
        background = Image.new("RGB", size, BACKGROUND)
        item = source.copy()
        item.thumbnail((width - 24, height - 24), Image.Resampling.LANCZOS)
        x = (width - item.width) // 2
        y = (height - item.height) // 2
        background.paste(item, (x, y), item.getchannel("A"))
        return background
    return ImageOps.fit(
        source.convert("RGB"), size,
        method=Image.Resampling.LANCZOS,
        centering=centering,
    )


def main():
    total_width = sum(item[2] for item in PANELS) + GUTTER * (len(PANELS) - 1)
    if total_width != SIZE[0]:
        raise RuntimeError(f"Сумма ширин панелей {total_width}, ожидалось {SIZE[0]}")

    canvas = Image.new("RGB", SIZE, BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    label_font = ImageFont.truetype(font_path, 16)
    x = 0

    for label, relative_path, width, centering in PANELS:
        source = load_image(relative_path)
        frame = panel_image(source, (width, SIZE[1]), centering)
        canvas.paste(frame, (x, 0))

        # Небольшая подпись на затемнённой полосе; фото остаётся нетронутым.
        overlay = Image.new("RGBA", (width, 42), (5, 12, 19, 190))
        canvas.paste(overlay, (x, SIZE[1] - 42), overlay)
        draw.text((x + 15, SIZE[1] - 29), label, font=label_font,
                  fill=(245, 248, 250))
        x += width + GUTTER

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, "JPEG", quality=96, subsampling=0, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-faire-cover] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")


if __name__ == "__main__":
    main()
