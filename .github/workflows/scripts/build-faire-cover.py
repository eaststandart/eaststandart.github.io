# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка фотопанорамы Hackaday.io из реальных кадров Faire.
# @purpose Показывает робототехнику, электронный эксперимент, осциллограф и рабочее место.
# @author  TechLab
# @version 1.3.0
# ==============================================================================

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output" / "faire-cover-1920x400.jpg"
SIZE = (1920, 400)

def load_photo(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Не найдено фото: {relative_path}")
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGB")

def extract_video_frame(relative_path, seconds, destination):
    source = ROOT / relative_path
    if not source.is_file():
        raise FileNotFoundError(f"Не найдено видео: {relative_path}")
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", str(seconds), "-i", str(source),
        "-frames:v", "1", "-q:v", "2", str(destination),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0 or not destination.is_file():
        raise RuntimeError(f"Не удалось извлечь кадр {relative_path}: {result.stderr.strip()}")
    with Image.open(destination) as image:
        return ImageOps.exif_transpose(image).convert("RGB")

def prepare(photo, size, centering=(0.5, 0.5)):
    photo = ImageOps.fit(photo, size, method=Image.Resampling.LANCZOS, centering=centering)
    photo = ImageEnhance.Contrast(photo).enhance(1.05)
    return ImageEnhance.Color(photo).enhance(0.96)

def paste_scene(canvas, photo, rect, polygon, centering):
    x, y, width, height = rect
    frame = prepare(photo, (width, height), centering)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).polygon([(px - x, py - y) for px, py in polygon], fill=255)
    canvas.paste(frame, (x, y), mask)

def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        video_frame = extract_video_frame(
            "faire/detektor-pereliva/detektor-pereliva-01.webm",
            1.4,
            Path(temp_dir) / "detector-action.jpg",
        )
        scenes = [
            (load_photo("faire/robot-strannik/robot-strannik-01.webp"),
             (0, 0, 540, 400), (0.50, 0.50)),
            (video_frame, (455, 0, 1120, 400), (0.50, 0.50)),
            (load_photo("faire/podstavka-dlya-oscillografa/podstavka-dlya-oscillografa-03.webp"),
             (1030, 0, 1580, 400), (0.50, 0.50)),
            (load_photo("faire/podstavka-dlya-oscillografa/podstavka-dlya-oscillografa-04.webp"),
             (1480, 0, 1920, 400), (0.50, 0.50)),
        ]

        polygons = [
            [(0, 0), (500, 0), (445, 400), (0, 400)],
            [(500, 0), (1120, 0), (1065, 400), (445, 400)],
            [(1120, 0), (1575, 0), (1515, 400), (1065, 400)],
            [(1575, 0), (1920, 0), (1920, 400), (1515, 400)],
        ]
        canvas = Image.new("RGB", SIZE, (12, 19, 26))
        for scene, polygon in zip(scenes, polygons):
            paste_scene(canvas, scene[0], scene[1], polygon, scene[2])

    # Единый тональный слой и тонкая сигнальная линия вместо рамок-карточек.
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(280, 400):
        alpha = int(95 * ((y - 280) / 120) ** 1.3)
        draw.line((0, y, SIZE[0], y), fill=(5, 12, 18, alpha))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 28)
    sub_font = ImageFont.truetype(font_path, 11)
    draw.text((48, 326), "TECHLAB", font=title_font, fill=(250, 252, 253, 245),
              stroke_width=1, stroke_fill=(8, 14, 20, 180))
    draw.text((51, 360), "ENGINEERING IN ACTION", font=sub_font,
              fill=(116, 225, 225, 245))
    draw.line((0, 397, 1920, 397), fill=(77, 198, 204, 125), width=2)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "JPEG", quality=94, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-faire-cover] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")

if __name__ == "__main__":
    main()
