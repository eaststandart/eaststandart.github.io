# ==============================================================================
# @module  build-hackaday-cover-test.py
# @about   Тестовая сборка обложки Hackaday.io с соотношением сторон 2.76:1.
# @purpose Создаёт отдельный вариант 1920x696 из тех же пяти оригинальных фото.
# @author  TechLab
# @version 1.0.0
# ==============================================================================

from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "faire" / "hackaday-cover-1920x696-test.jpg"
SIZE = (1920, 696)
GUTTER = 5
BACKGROUND = (13, 22, 31)
PANELS = [
    ("Спутник-1", "faire/sputnik-1/sputnik-1-01.webp", 350, (0.52, 0.50)),
    ("Электронный орган", "faire/elektronnyj-organ/elektronnyj-organ-02.webp", 430, (0.50, 0.50)),
    ("Условные обозначения", "faire/pano-uslovnye-oboznacheniya/pano-uslovnye-oboznacheniya-01.webp", 300, (0.50, 0.50)),
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
    x = 0

    for _, relative_path, width, centering in PANELS:
        source = load_image(relative_path)
        frame = panel_image(source, (width, SIZE[1]), centering)
        canvas.paste(frame, (x, 0))
        x += width + GUTTER

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, "JPEG", quality=96, subsampling=0, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-hackaday-cover-test] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")


if __name__ == "__main__":
    main()
