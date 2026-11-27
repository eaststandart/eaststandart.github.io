# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка фотопанорамы Hackaday.io из реальных видео и фото Faire.
# @purpose Показывает инженерные эксперименты, работающие устройства и лабораторную оснастку.
# @author  TechLab
# @version 1.2.0
# ==============================================================================

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output" / "faire-cover-1920x400.jpg"
SIZE = (1920, 400)

# Видеокадры выбраны как моменты демонстрации работы устройств.
VIDEO_SCENES = [
    ("faire/robot-strannik/robot-strannik-01.webm", 1.2, (0, 0, 560, 400), (0.50, 0.50)),
    ("faire/detektor-pereliva/detektor-pereliva-01.webm", 1.4, (440, 0, 1120, 400), (0.50, 0.50)),
    ("faire/elektronnyj-organ/elektronnyj-organ-01.webm", 1.3, (1010, 0, 1510, 400), (0.50, 0.50)),
]
PHOTO_SCENE = (
    "faire/podstavka-dlya-oscillografa/podstavka-dlya-oscillografa-05.webp",
    (1400, 0, 1920, 400),
    (0.50, 0.50),
)

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
        raise RuntimeError(
            f"Не удалось извлечь кадр {relative_path}: {result.stderr.strip()}"
        )
    with Image.open(destination) as image:
        return ImageOps.exif_transpose(image).convert("RGB")

def load_photo(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Не найдено фото: {relative_path}")
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGB")

def prepare(photo, size, centering):
    photo = ImageOps.fit(
        photo, size, method=Image.Resampling.LANCZOS, centering=centering
    )
    photo = ImageEnhance.Contrast(photo).enhance(1.06)
    photo = ImageEnhance.Color(photo).enhance(0.94)
    return photo

def paste_scene(canvas, photo, rect, polygon, centering):
    x, y, width, height = rect
    frame = prepare(photo, (width, height), centering)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).polygon(
        [(px - x, py - y) for px, py in polygon], fill=255
    )
    canvas.paste(frame, (x, y), mask)

def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        scenes = []
        for index, (video, seconds, rect, centering) in enumerate(VIDEO_SCENES):
            frame_path = temp_dir / f"scene-{index}.jpg"
            frame = extract_video_frame(video, seconds, frame_path)
            scenes.append((frame, rect, centering))

        photo_path, photo_rect, photo_centering = PHOTO_SCENE
        scenes.append((load_photo(photo_path), photo_rect, photo_centering))

        canvas = Image.new("RGB", SIZE, (12, 19, 26))
        polygons = [
            [(0, 0), (520, 0), (455, 400), (0, 400)],
            [(520, 0), (1125, 0), (1060, 400), (455, 400)],
            [(1125, 0), (1530, 0), (1485, 400), (1060, 400)],
            [(1530, 0), (1920, 0), (1920, 400), (1485, 400)],
        ]
        for (photo, rect, centering), polygon in zip(scenes, polygons):
            paste_scene(canvas, photo, rect, polygon, centering)

    # Мягкое затемнение снизу связывает кадры и оставляет место для подписи.
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(245, 400):
        alpha = int(105 * ((y - 245) / 155) ** 1.25)
        draw.line((0, y, SIZE[0], y), fill=(5, 12, 18, alpha))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 30)
    sub_font = ImageFont.truetype(font_path, 12)
    draw.text((54, 318), "TECHLAB", font=title_font,
              fill=(250, 252, 253, 245), stroke_width=1,
              stroke_fill=(8, 14, 20, 180))
    draw.text((57, 356), "ENGINEERING IN ACTION", font=sub_font,
              fill=(116, 225, 225, 245))
    draw.line((56, 382, 275, 382), fill=(90, 207, 211, 210), width=2)
    draw.line((0, 397, 1920, 397), fill=(77, 198, 204, 125), width=2)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "JPEG", quality=94, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-faire-cover] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")

if __name__ == "__main__":
    main()
