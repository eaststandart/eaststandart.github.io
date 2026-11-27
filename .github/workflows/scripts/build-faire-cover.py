# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка редакционной фотокомпозиции Hackaday.io из материалов Faire.
# @purpose Показывает рабочую среду, осциллограф, электронный эксперимент и робототехнику.
# @author  TechLab
# @version 1.4.1
# ==============================================================================

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter
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

def fit(photo, size, centering=(0.5, 0.5)):
    photo = ImageOps.fit(photo, size, method=Image.Resampling.LANCZOS, centering=centering)
    photo = ImageEnhance.Contrast(photo).enhance(1.06)
    return ImageEnhance.Color(photo).enhance(0.96)

def polygon_paste(canvas, photo, rect, polygon, centering=(0.5, 0.5)):
    x, y, width, height = rect
    frame = fit(photo, (width, height), centering)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).polygon([(px - x, py - y) for px, py in polygon], fill=255)
    canvas.paste(frame, (x, y), mask)

def add_inset(canvas, photo, rect):
    x, y, width, height = rect
    frame = fit(photo, (width, height))
    shadow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (x + 7, y + 9, x + width + 7, y + height + 9),
        radius=10, fill=(0, 0, 0, 170)
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(12)))
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=8, fill=255)
    canvas.paste(frame, (x, y), mask)
    ImageDraw.Draw(canvas).rounded_rectangle(
        (x, y, x + width - 1, y + height - 1),
        radius=8, outline=(232, 242, 245, 220), width=2
    )

def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        action_frame = extract_video_frame(
            "faire/detektor-pereliva/detektor-pereliva-01.webm",
            1.4,
            Path(temp_dir) / "detector-action.jpg",
        )

        # Широкая основа — реальный рабочий стол и собранный электронный узел.
        background = fit(
            load_photo("faire/podstavka-dlya-oscillografa/podstavka-dlya-oscillografa-04.webp"),
            SIZE, (0.52, 0.48)
        )
        canvas = background.convert("RGBA")

        # Крупные сцены перекрывают фон диагональными переходами, без ряда карточек.
        polygon_paste(
            canvas,
            load_photo("faire/robot-strannik/robot-strannik-01.webp"),
            (0, 0, 600, 400),
            [(0, 0), (555, 0), (485, 400), (0, 400)],
            (0.50, 0.50),
        )
        polygon_paste(
            canvas,
            load_photo("faire/podstavka-dlya-oscillografa/podstavka-dlya-oscillografa-06.webp"),
            (500, 0, 1430, 400),
            [(555, 0), (1465, 0), (1395, 400), (485, 400)],
            (0.50, 0.50),
        )

        # Небольшой видеокадр — фрагмент демонстрации электронного эксперимента.
        add_inset(canvas, action_frame, (1390, 36, 465, 260))

    # Локальное затемнение только под подписью, остальная фотография остаётся открытой.
    shade = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(286, 400):
        alpha = int(125 * ((y - 286) / 114) ** 1.2)
        sd.line((0, y, 540, y), fill=(5, 12, 18, alpha))
    canvas = Image.alpha_composite(canvas, shade)

    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 29)
    sub_font = ImageFont.truetype(font_path, 11)
    draw.text((48, 326), "TECHLAB", font=title_font,
              fill=(250, 252, 253, 250), stroke_width=1,
              stroke_fill=(8, 14, 20, 190))
    draw.text((51, 360), "ENGINEERING IN ACTION", font=sub_font,
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
