from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def make_placeholder(path: Path, title: str, subtitle: str) -> None:
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), (245, 247, 250))
    d = ImageDraw.Draw(img)

    # Border
    d.rectangle([20, 20, w - 20, h - 20], outline=(180, 185, 195), width=6)

    # Try to use a default font; fall back gracefully.
    try:
        font_title = ImageFont.truetype("Arial.ttf", 64)
        font_sub = ImageFont.truetype("Arial.ttf", 32)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Centered title/subtitle
    def center_text(text: str, y: int, font) -> None:
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        d.text((x, y), text, fill=(40, 45, 55), font=font)

    center_text(title, 260, font_title)
    center_text(subtitle, 360, font_sub)
    center_text("MOCK / PLACEHOLDER IMAGE", 520, font_sub)

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)


def main() -> None:
    out = Path("doc_assets")
    items = {
        "image1": "EV charging overview photo",
        "image2": "Garage with EVSE installed",
        "image3": "Documents/blueprints montage",
        "image4": "Garage plan excerpt",
        "image5": "MDP + meter photo",
        "image6": "Garage area context photo",
        "image9": "Engineer reviewing drawings",
        "image10": "Electrical system close-up",
        "image11": "Blueprint-style EV layout",
        "image12": "EVSE location plan excerpt",
    }

    for key, desc in items.items():
        make_placeholder(out / f"{key}.png", title=key, subtitle=desc)

    print("Generated placeholders in:", out)


if __name__ == "__main__":
    main()

