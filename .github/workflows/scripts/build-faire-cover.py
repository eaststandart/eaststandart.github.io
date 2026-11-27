# ==============================================================================
# @module  build-faire-cover.py
# @about   Сборка профессиональной фотопанорамы Hackaday.io из материалов TechLab.
# @purpose Показывает проекты в заданной последовательности и реальные процессы
#          изготовления, монтажа и проверки электронных устройств.
# @author  TechLab
# @version 2.0.0
# ==============================================================================

from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output" / "faire-cover-1920x400.jpg"
TEMP = ROOT / "output" / "video-frame.jpg"
SIZE = (1920, 400)


def load_image(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Не найдено изображение: {relative_path}")
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGBA")


def fit_photo(photo, size, centering=(0.5, 0.5)):
    photo = ImageOps.fit(
        photo.convert("RGB"), size,
        method=Image.Resampling.LANCZOS,
        centering=centering,
    )
    photo = ImageEnhance.Contrast(photo).enhance(1.10)
    return ImageEnhance.Color(photo).enhance(1.03)


def gradient_background(size, left=(8, 18, 29), right=(19, 37, 48)):
    width, height = size
    result = Image.new("RGB", size)
    draw = ImageDraw.Draw(result)
    for x in range(width):
        t = x / max(1, width - 1)
        color = tuple(round(left[i] * (1 - t) + right[i] * t) for i in range(3))
        draw.line((x, 0, x, height), fill=color)
    return result.convert("RGBA")


def paste_panel(canvas, photo, x0, x1, centering=(0.5, 0.5),
                left_slant=0, right_slant=0):
    width = x1 - x0
    frame = fit_photo(photo, (width, SIZE[1]), centering)
    mask = Image.new("L", (width, SIZE[1]), 0)
    points = [
        (left_slant, 0), (width - right_slant, 0),
        (width, SIZE[1]), (0, SIZE[1]),
    ]
    ImageDraw.Draw(mask).polygon(points, fill=255)
    canvas.paste(frame.convert("RGBA"), (x0, 0), mask)


def paste_cutout(canvas, relative_path, bounds, background=(12, 27, 39)):
    cutout = load_image(relative_path)
    x, y, width, height = bounds
    cutout.thumbnail((width, height), Image.Resampling.LANCZOS)
    glow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse(
        (x + width * 0.18, y + height * 0.20,
         x + width * 0.88, y + height * 0.90),
        fill=(44, 105, 127, 70),
    )
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(42)))
    canvas.alpha_composite(cutout, (x + (width - cutout.width) // 2,
                                    y + (height - cutout.height) // 2))


def add_inset(canvas, photo, rect, label, centering=(0.5, 0.5)):
    x, y, width, height = rect
    frame = fit_photo(photo, (width, height), centering).convert("RGBA")
    shadow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (x + 5, y + 7, x + width + 5, y + height + 7),
        radius=6, fill=(0, 0, 0, 190),
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, width - 1, height - 1), radius=5, fill=255
    )
    canvas.paste(frame, (x, y), mask)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (x, y, x + width - 1, y + height - 1),
        radius=5, outline=(174, 211, 219, 220), width=2,
    )
    label_font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10
    )
    label_y = y + height - 23
    draw.rectangle((x + 1, label_y, x + width - 1, y + height - 1),
                   fill=(5, 13, 21, 190))
    draw.text((x + 9, label_y + 6), label, font=label_font,
              fill=(238, 247, 249, 255))


def extract_video_frame():
    video = ROOT / "faire/metronom-signalnyj/metronom-signalnyj-01.webm"
    if not video.is_file():
        print("[build-faire-cover] Видео не найдено, используем фотокадр.")
        return None
    TEMP.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-y", "-ss", "1.5", "-i", str(video),
        "-frames:v", "1", "-q:v", "2", str(TEMP),
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        with Image.open(TEMP) as frame:
            frame.verify()
        print("[build-faire-cover] Получен кадр из видео метронома.")
        return TEMP
    except (subprocess.CalledProcessError, OSError):
        print("[build-faire-cover] Не удалось извлечь кадр видео.")
        return None


def main():
    canvas = gradient_background(SIZE)

    # Основная последовательность проектов: Спутник-1, орган, панно,
    # метроном и детектор перелива. Переходы сделаны диагональными.
    paste_panel(
        canvas, load_image("faire/sputnik-1/sputnik-1-01.webp"),
        0, 365, (0.53, 0.50), 0, 22,
    )
    paste_panel(
        canvas, load_image("faire/elektronnyj-organ/elektronnyj-organ-02.webp"),
        343, 790, (0.50, 0.50), 22, 20,
    )
    paste_panel(
        canvas, load_image("faire/pano-uslovnye-oboznacheniya/pano-uslovnye-oboznacheniya.webp"),
        770, 1105, (0.50, 0.50), 20, 18,
    )
    paste_panel(
        canvas, load_image("faire/metronom-signalnyj/metronom-signalnyj-24.webp"),
        1087, 1510, (0.50, 0.50), 18, 20,
    )
    paste_panel(
        canvas, load_image("faire/detektor-pereliva/detektor-pereliva-09.webp"),
        1490, 1920, (0.50, 0.50), 20, 0,
    )

    # Предметные изображения на прозрачном фоне усиливают первые и третьи
    # сюжеты: сам объект читается крупно, без случайного фона мастерской.
    paste_cutout(canvas, "faire/sputnik-1/sputnik-1.webp",
                 (18, 38, 330, 315))
    paste_cutout(canvas, "faire/pano-uslovnye-oboznacheniya/pano-uslovnye-oboznacheniya.webp",
                 (790, 66, 285, 265))

    # Дополнительные кадры показывают изготовление платы и проверку сигнала.
    add_inset(
        canvas, load_image("faire/elektronnyj-organ/elektronnyj-organ-36.webp"),
        (505, 18, 250, 142), "PCB / SOLDERING", (0.50, 0.50),
    )
    add_inset(
        canvas, load_image("faire/elektronnyj-organ/elektronnyj-organ-41.webp"),
        (1260, 18, 235, 132), "OSCILLOSCOPE TEST", (0.50, 0.50),
    )

    # Кадр из настоящего WebM добавляется, если FFmpeg успешно его извлёк.
    video_frame = extract_video_frame()
    if video_frame:
        with Image.open(video_frame) as source:
            add_inset(canvas, source.convert("RGBA"),
                      (1280, 245, 215, 125), "VIDEO FRAME", (0.50, 0.50))

    # Неброская нижняя маркировка, не перекрывающая инженерные объекты.
    shade = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    shade_draw = ImageDraw.Draw(shade)
    for y in range(342, 400):
        alpha = int(125 * ((y - 342) / 58) ** 1.25)
        shade_draw.line((0, y, SIZE[0], y), fill=(3, 10, 17, alpha))
    canvas = Image.alpha_composite(canvas, shade)

    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 27)
    sub_font = ImageFont.truetype(font_path, 10)
    draw.text((34, 350), "TECHLAB", font=title_font,
              fill=(250, 252, 253, 250), stroke_width=1,
              stroke_fill=(8, 14, 20, 190))
    draw.text((37, 381), "ENGINEERING IN ACTION", font=sub_font,
              fill=(139, 220, 225, 250))
    draw.line((0, 397, SIZE[0], 397), fill=(77, 198, 204, 145), width=2)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "JPEG", quality=95, optimize=True)
    with Image.open(OUTPUT) as result:
        if result.size != SIZE:
            raise RuntimeError(f"Неверный размер результата: {result.size}")
    print(f"[build-faire-cover] Готово: {OUTPUT} ({SIZE[0]}x{SIZE[1]})")


if __name__ == "__main__":
    main()
