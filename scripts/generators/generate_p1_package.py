import io
import random
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Dependencies:
#   python3 -m pip install --user reportlab pillow
from PIL import Image, ImageEnhance, ImageFilter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

SEED = 43
random.seed(SEED)

ROOT = Path.cwd()
P1_INPUTS = ROOT / "P1" / "Inputs"
P1_OUTPUTS = ROOT / "P1" / "Outputs"

# Reuse the same asset source location used by Phase 0 generation.
ASSETS_DIR = Path(
    "/Users/rc/.cursor/projects/var-folders-m-fdkkzfb13z7c6gbcgc19n4sw0000gn-T-60687e3d-f30b-4bd0-9b54-6006fa63ce48/assets"
)

NAMEPLATE_SRC = [
    ASSETS_DIR / "P0_MDP_Nameplate_01.png",
    ASSETS_DIR / "P0_MDP_Nameplate_02.png",
    ASSETS_DIR / "P0_MDP_Nameplate_03.png",
    ASSETS_DIR / "P0_MDP_Nameplate_04.png",
]

SITE_SRC = [
    ASSETS_DIR / "P0_Site_Context_01.png",
    ASSETS_DIR / "P0_Site_Context_02.png",
    ASSETS_DIR / "P0_Site_Context_03.png",
    ASSETS_DIR / "P0_Site_Context_04.png",
    ASSETS_DIR / "P0_Site_Context_05.png",
    ASSETS_DIR / "P0_Site_Context_06.png",
    ASSETS_DIR / "P0_Site_Context_07.png",
    ASSETS_DIR / "P0_Site_Context_08.png",
]


def ensure_dirs() -> None:
    P1_INPUTS.mkdir(parents=True, exist_ok=True)
    P1_OUTPUTS.mkdir(parents=True, exist_ok=True)


def watermark_pdf(c: canvas.Canvas, text: str = "MOCK / EXAMPLE ONLY") -> None:
    c.saveState()
    c.setFillColor(colors.lightgrey)
    c.setFont("Helvetica-Bold", 48)
    c.translate(letter[0] / 2, letter[1] / 2)
    c.rotate(30)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def pdf_header_footer(
    c: canvas.Canvas,
    title: str,
    file_name: str,
    page_num: int,
    subtitle: Optional[str] = None,
    banner: str = "EV Charging Site Project — Phase 1 (MOCK)",
) -> None:
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.75 * inch, 10.55 * inch, title)
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    if subtitle:
        c.drawString(0.75 * inch, 10.33 * inch, subtitle)
    c.drawString(0.75 * inch, 10.15 * inch, banner)
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(
        0.75 * inch,
        0.5 * inch,
        f"File: {file_name}  |  Generated: {datetime.now().date()}  |  Page {page_num}",
    )
    c.setFillColor(colors.black)


def draw_wrapped(c: canvas.Canvas, x: float, y: float, text: str, max_width: float, font_size: int = 10) -> float:
    c.setFont("Helvetica", font_size)
    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, "Helvetica", font_size) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= 0.18 * inch
            line = w
    if line:
        c.drawString(x, y, line)
        y -= 0.18 * inch
    return y


def make_phone_filename(base_dt: datetime, idx: int, ext: str = "jpg") -> str:
    ts = (base_dt + timedelta(seconds=idx * 37)).strftime("%Y%m%d_%H%M%S")
    return f"IMG_{ts}_{idx:02d}.{ext}"


def _ahash(img: Image.Image, hash_size: int = 8) -> int:
    g = img.convert("L").resize((hash_size, hash_size), resample=Image.BICUBIC)
    px = list(g.getdata())
    avg = sum(px) / len(px)
    bits = 0
    for i, v in enumerate(px):
        if v >= avg:
            bits |= 1 << i
    return bits


def _transform_photo(img: Image.Image, stronger: bool = False) -> Image.Image:
    out = img.copy()
    w, h = out.size

    # Crop jitter
    max_crop = 0.07 if not stronger else 0.14
    dx = int(w * random.uniform(0.0, max_crop))
    dy = int(h * random.uniform(0.0, max_crop))
    if dx > 0 or dy > 0:
        out = out.crop((dx, dy, w - dx, h - dy)).resize((w, h), resample=Image.BICUBIC)

    # Mild tilt
    angle = random.uniform(-2.2, 2.2) if not stronger else random.uniform(-3.2, 3.2)
    out = out.rotate(angle, expand=False, resample=Image.BICUBIC)

    # Exposure + contrast + color drift
    out = ImageEnhance.Brightness(out).enhance(random.uniform(0.86, 1.18))
    out = ImageEnhance.Contrast(out).enhance(random.uniform(0.86, 1.24))
    out = ImageEnhance.Color(out).enhance(random.uniform(0.88, 1.16))

    # Blur
    if random.random() < (0.2 if not stronger else 0.33):
        out = out.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.4, 1.25)))

    # “Phone ISP” artifacts
    if random.random() < 0.85:
        scale = random.uniform(0.93, 0.985) if not stronger else random.uniform(0.90, 0.975)
        out = out.resize((int(w * scale), int(h * scale)), resample=Image.BICUBIC).resize((w, h), resample=Image.BICUBIC)

    return out


def build_photo_zip(zip_path: Path, sources: list[Path], total_images: int, start_dt: datetime) -> list[tuple[str, str]]:
    captions: list[str] = [p.stem.replace("_", " ") for p in sources]
    src_imgs = [Image.open(str(p)).convert("RGB") for p in sources]

    used_hashes: set[int] = set()
    manifest: list[tuple[str, str]] = []

    base_indices = list(range(len(src_imgs)))
    random.shuffle(base_indices)

    def pick_base(i: int) -> int:
        if i < len(base_indices):
            return base_indices[i]
        return random.randrange(0, len(src_imgs))

    max_attempts_per_img = 60

    with zipfile.ZipFile(str(zip_path), "w", compression=zipfile.ZIP_DEFLATED) as z:
        for idx in range(total_images):
            base_i = pick_base(idx)
            base_img = src_imgs[base_i]
            cap = captions[base_i]

            chosen = None
            for attempt in range(max_attempts_per_img):
                stronger = attempt > (max_attempts_per_img // 2)
                candidate = _transform_photo(base_img, stronger=stronger)
                hsh = _ahash(candidate, hash_size=8)
                if hsh not in used_hashes:
                    used_hashes.add(hsh)
                    chosen = candidate
                    break

            if chosen is None:
                chosen = _transform_photo(base_img, stronger=True)

            fname = make_phone_filename(start_dt, idx, ext="jpg")
            buf = io.BytesIO()
            chosen.save(buf, format="JPEG", quality=86)
            z.writestr(fname, buf.getvalue())
            manifest.append((fname, cap))

    return manifest


def write_photo_index_pdf(path: Path, zip_name: str, manifest: list[tuple[str, str]], title: str, subtitle: str) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    pdf_header_footer(c, title, path.name, 1, subtitle=subtitle)

    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        f"This index summarizes photos packaged in: {zip_name}. Captions describe electrical-only evidence intent. Replace with real field photos and markups.",
        7.0 * inch,
    )
    y -= 0.15 * inch

    # Make the index feel like a real evidence tool: include counts + separated sections.
    nameplate = [(f, cpt) for f, cpt in manifest if "MDP Nameplate" in cpt]
    site = [(f, cpt) for f, cpt in manifest if "Site Context" in cpt]
    other = [(f, cpt) for f, cpt in manifest if (f, cpt) not in nameplate and (f, cpt) not in site]

    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Photo set summary (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    c.drawString(1.0 * inch, y, f"- Total photos in ZIP: {len(manifest)}")
    y -= 0.22 * inch
    c.drawString(1.0 * inch, y, f"- Nameplates/labels: {len(nameplate)}")
    y -= 0.22 * inch
    c.drawString(1.0 * inch, y, f"- Site context: {len(site)}")
    y -= 0.22 * inch
    if other:
        c.drawString(1.0 * inch, y, f"- Other: {len(other)}")
        y -= 0.22 * inch
    y -= 0.15 * inch

    def draw_table(section_title: str, rows: list[tuple[str, str]], y0: float, max_rows: int) -> float:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.75 * inch, y0, section_title)
        y1 = y0 - 0.22 * inch
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75 * inch, y1, "Photo filename (inside ZIP)")
        c.drawString(3.15 * inch, y1, "What it evidences (electrical-only)")
        y1 -= 0.12 * inch
        c.setStrokeColor(colors.grey)
        c.line(0.75 * inch, y1, 7.75 * inch, y1)
        y1 -= 0.18 * inch
        c.setFont("Helvetica", 9)
        shown = 0
        for fname, cap in rows:
            c.drawString(0.75 * inch, y1, fname)
            c.drawString(3.15 * inch, y1, cap[:85])
            y1 -= 0.18 * inch
            shown += 1
            if shown >= max_rows or y1 < 1.2 * inch:
                break
        return y1

    y = draw_table("Section A — Nameplates / Label Evidence (excerpt)", nameplate or manifest, y, max_rows=12)
    if y < 4.2 * inch:
        c.showPage()
        watermark_pdf(c)
        pdf_header_footer(c, title, path.name, 2, subtitle=subtitle)
        y = 9.65 * inch
    y -= 0.25 * inch
    y = draw_table("Section B — Site Context / Gear Context (excerpt)", site or manifest, y, max_rows=12)

    c.showPage()

    # Add a checklist page so this reads like a usable evidence artifact.
    watermark_pdf(c)
    pdf_header_footer(c, "Photo Evidence — Acceptance + Verification Checklist (Mock)", path.name, 3, subtitle=subtitle)
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This checklist documents what makes the photo evidence usable for engineering and plan review. Replace with real checkmarks/initials in a live project.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Acceptance criteria (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Nameplate photos readable at 100% zoom (ratings, voltage/phase, manufacturer/model).",
        "Breaker labeling photos include both context and close-ups.",
        "Photos map cleanly to schedule/header fields (no ambiguity).",
        "Filenames preserved (no post-capture renaming); timestamps plausible.",
        "Sensitive info handled appropriately (redacted copies; originals archived).",
    ]:
        c.drawString(1.0 * inch, y, f"- [ ] {line}")
        y -= 0.22 * inch
    c.showPage()

    # Add a couple annotated thumbnail pages (for realism).
    thumbs = NAMEPLATE_SRC[:2] + SITE_SRC[:2]
    for page_num, img_path in enumerate(thumbs, start=4):
        watermark_pdf(c)
        pdf_header_footer(c, "Annotated Photo Sheet (Mock)", path.name, page_num, subtitle=f"Source: {img_path.name}")
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        c.drawString(0.75 * inch, 9.65 * inch, "Annotations are illustrative; replace with real field markups.")
        c.setFillColor(colors.black)

        pil = Image.open(str(img_path)).convert("RGB")
        max_w, max_h = 7.0 * inch, 6.7 * inch
        w, h = pil.size
        scale = min(max_w / w, max_h / h)
        tw, th = int(w * scale), int(h * scale)
        pil = pil.resize((tw, th), resample=Image.BICUBIC)
        tmp = io.BytesIO()
        pil.save(tmp, format="PNG")
        tmp.seek(0)
        c.drawImage(ImageReader(tmp), 0.75 * inch, 2.2 * inch, width=tw, height=th)

        # Simple callouts
        c.setStrokeColor(colors.red)
        c.setLineWidth(2)
        c.rect(0.95 * inch, 2.45 * inch, 2.6 * inch, 1.3 * inch)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.red)
        c.drawString(0.95 * inch, 1.95 * inch, "MOCK CALLOUT: verify rating / labeling / clearance")
        c.setFillColor(colors.black)

        c.showPage()

    c.save()


def write_site_plans_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)

    def north_arrow(x: float, y: float) -> None:
        c.saveState()
        c.setStrokeColor(colors.black)
        c.setFillColor(colors.black)
        c.setLineWidth(1)
        c.line(x, y, x, y + 0.8 * inch)
        c.line(x, y + 0.8 * inch, x - 0.08 * inch, y + 0.65 * inch)
        c.line(x, y + 0.8 * inch, x + 0.08 * inch, y + 0.65 * inch)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x, y + 0.92 * inch, "N")
        c.restoreState()

    def scale_bar(x: float, y: float, feet: int = 40) -> None:
        # Simple scale bar: not to scale, but looks like a plan artifact.
        c.saveState()
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.rect(x, y, 2.8 * inch, 0.18 * inch, stroke=1, fill=0)
        # alternating blocks
        block_w = (2.8 * inch) / 8
        for i in range(8):
            if i % 2 == 0:
                c.setFillColor(colors.black)
                c.rect(x + i * block_w, y, block_w, 0.18 * inch, stroke=0, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 8)
        c.drawString(x, y + 0.24 * inch, f"SCALE (mock): 1\" = {feet} ft")
        c.restoreState()

    def title_block(sheet: str, title: str, rev: str, date: str) -> None:
        c.saveState()
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        x0, y0, w, h = 0.75 * inch, 0.75 * inch, 7.0 * inch, 1.0 * inch
        c.rect(x0, y0, w, h, stroke=1, fill=0)
        c.line(x0 + 4.6 * inch, y0, x0 + 4.6 * inch, y0 + h)
        c.line(x0 + 6.0 * inch, y0, x0 + 6.0 * inch, y0 + h)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x0 + 0.12 * inch, y0 + 0.72 * inch, "PROJECT (mock):")
        c.setFont("Helvetica", 9)
        c.drawString(x0 + 1.35 * inch, y0 + 0.72 * inch, "EV Charging Site Project")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x0 + 0.12 * inch, y0 + 0.48 * inch, "SHEET TITLE:")
        c.setFont("Helvetica", 9)
        c.drawString(x0 + 1.35 * inch, y0 + 0.48 * inch, title)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x0 + 0.12 * inch, y0 + 0.24 * inch, "ADDRESS:")
        c.setFont("Helvetica", 9)
        c.drawString(x0 + 1.35 * inch, y0 + 0.24 * inch, "Place (Palo Alto, CA) (mock)")

        c.setFont("Helvetica-Bold", 9)
        c.drawString(x0 + 4.72 * inch, y0 + 0.72 * inch, "SHEET:")
        c.setFont("Helvetica", 9)
        c.drawString(x0 + 5.3 * inch, y0 + 0.72 * inch, sheet)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x0 + 4.72 * inch, y0 + 0.48 * inch, "REV:")
        c.setFont("Helvetica", 9)
        c.drawString(x0 + 5.3 * inch, y0 + 0.48 * inch, rev)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x0 + 4.72 * inch, y0 + 0.24 * inch, "DATE:")
        c.setFont("Helvetica", 9)
        c.drawString(x0 + 5.3 * inch, y0 + 0.24 * inch, date)

        c.setFont("Helvetica-Bold", 9)
        c.drawString(x0 + 6.12 * inch, y0 + 0.72 * inch, "ISSUED FOR:")
        c.setFont("Helvetica", 9)
        c.drawString(x0 + 6.12 * inch, y0 + 0.48 * inch, "REFERENCE")
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(x0 + 6.12 * inch, y0 + 0.24 * inch, "(electrical-only)")
        c.restoreState()

    # Page 1: cover / sheet index
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "Architectural Plan Set — Garage + Electrical Room Context (Mock)",
        path.name,
        1,
        subtitle="Project: EV Charging Site Project  |  Revision: Rev 2  |  Date: 2026-01-15",
        banner="EV Charging Site Project — Phase 1 Inputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.6 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This plan set is a mock artifact representing owner/architect-provided drawings. It is intended for electrical context only (service room location and reference geometry). It does not define constructability routing or civil scope.",
        7.0 * inch,
    )
    y -= 0.2 * inch

    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75 * inch, y, "Included sheets (mock):")
    c.setFont("Helvetica", 10)
    y -= 0.28 * inch
    for s in [
        "A0.01 Cover / Sheet Index",
        "A1.10 Garage Level 1 Plan (electrical context excerpt)",
        "A1.11 Electrical Room Plan (context excerpt)",
    ]:
        c.drawString(1.0 * inch, y, f"- {s}")
        y -= 0.22 * inch

    # Simple title block
    c.setStrokeColor(colors.black)
    c.rect(0.75 * inch, 0.9 * inch, 7.0 * inch, 1.2 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, 1.85 * inch, "TITLE BLOCK (mock)")
    c.setFont("Helvetica", 9)
    c.drawString(0.9 * inch, 1.6 * inch, "Project: EV Charging Site Project")
    c.drawString(0.9 * inch, 1.4 * inch, "Address: Place (Palo Alto, CA) (mock)")
    c.drawString(0.9 * inch, 1.2 * inch, "Sheet: A0.01   Rev: 2   Date: 2026-01-15")
    c.drawRightString(7.7 * inch, 1.2 * inch, "Issued For: Reference (electrical-only)")

    c.showPage()

    # Page 2: garage plan excerpt
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "A1.10 — Garage Level 1 Plan (Electrical Context Excerpt) (Mock)",
        path.name,
        2,
        subtitle="Revision: Rev 2  |  Date: 2026-01-15",
        banner="EV Charging Site Project — Phase 1 Inputs (MOCK)",
    )

    # Draw a more realistic “plan” (still schematic, but not empty).
    plan_x, plan_y, plan_w, plan_h = 0.9 * inch, 2.05 * inch, 6.9 * inch, 7.4 * inch
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.rect(plan_x, plan_y, plan_w, plan_h, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(plan_x, plan_y + plan_h + 0.15 * inch, "GARAGE LEVEL 1 — PLAN (context excerpt, mock)")

    # Grid lines / columns
    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(0.6)
    for i in range(1, 8):
        gx = plan_x + i * (plan_w / 8)
        c.line(gx, plan_y, gx, plan_y + plan_h)
    for j in range(1, 10):
        gy = plan_y + j * (plan_h / 10)
        c.line(plan_x, gy, plan_x + plan_w, gy)

    # Column markers
    c.setFillColor(colors.darkgrey)
    for i in range(1, 8, 2):
        for j in range(1, 10, 3):
            cx = plan_x + i * (plan_w / 8)
            cy = plan_y + j * (plan_h / 10)
            c.rect(cx - 0.07 * inch, cy - 0.07 * inch, 0.14 * inch, 0.14 * inch, stroke=0, fill=1)
    c.setFillColor(colors.black)

    # Drive aisle
    c.setStrokeColor(colors.grey)
    c.setLineWidth(2)
    aisle_y = plan_y + 3.7 * inch
    c.line(plan_x + 0.2 * inch, aisle_y, plan_x + plan_w - 0.2 * inch, aisle_y)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(plan_x + 0.25 * inch, aisle_y + 0.1 * inch, "DRIVE AISLE (ref)")
    c.setFillColor(colors.black)

    # Parking stalls (two banks)
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    stall_w = 0.55 * inch
    stall_h = 1.15 * inch
    start_x = plan_x + 0.35 * inch
    for row_idx, base_y in enumerate([plan_y + 0.35 * inch, plan_y + plan_h - (stall_h + 0.55 * inch)]):
        for i in range(11):
            x = start_x + i * (stall_w + 0.06 * inch)
            c.rect(x, base_y, stall_w, stall_h, stroke=1, fill=0)
            c.setFont("Helvetica", 6)
            c.setFillColor(colors.grey)
            stall_num = (1 + i) if row_idx == 0 else (20 + i)
            c.drawString(x + 0.03 * inch, base_y + 0.05 * inch, f"P{stall_num:02d}")
            c.setFillColor(colors.black)

    # Electrical room location callout (blue)
    c.setStrokeColor(colors.blue)
    c.setLineWidth(2.2)
    er_x, er_y, er_w, er_h = plan_x + 0.25 * inch, plan_y + plan_h - 1.25 * inch, 2.25 * inch, 0.95 * inch
    c.rect(er_x, er_y, er_w, er_h, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.blue)
    c.drawString(er_x + 0.08 * inch, er_y + 0.58 * inch, "ELECTRICAL ROOM")
    c.setFont("Helvetica", 8)
    c.drawString(er_x + 0.08 * inch, er_y + 0.33 * inch, "(see A1.11)")
    c.setFillColor(colors.black)

    # Notes / legend area
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(plan_x + plan_w - 2.35 * inch, plan_y + 0.35 * inch, 2.1 * inch, 1.35 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(plan_x + plan_w - 2.25 * inch, plan_y + 1.55 * inch, "LEGEND (mock)")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(plan_x + plan_w - 2.25 * inch, plan_y + 1.30 * inch, "Blue box: Electrical room")
    c.drawString(plan_x + plan_w - 2.25 * inch, plan_y + 1.10 * inch, "Gray squares: Columns")
    c.drawString(plan_x + plan_w - 2.25 * inch, plan_y + 0.90 * inch, "Parking stalls: reference only")
    c.setFillColor(colors.black)

    # North arrow and scale bar
    north_arrow(plan_x + plan_w - 0.45 * inch, plan_y + plan_h - 1.05 * inch)
    scale_bar(plan_x + plan_w - 3.2 * inch, plan_y + plan_h - 0.65 * inch)

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(
        0.9 * inch,
        1.9 * inch,
        "NOTE: schematic excerpt for electrical context only (no routing/trenching/constructability).",
    )
    c.setFillColor(colors.black)
    title_block(sheet="A1.10", title="Garage Level 1 Plan (Electrical Context Excerpt)", rev="2", date="2026-01-15")

    c.showPage()

    # Page 3: electrical room plan excerpt
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "A1.11 — Electrical Room Plan (Context Excerpt) (Mock)",
        path.name,
        3,
        subtitle="Revision: Rev 2  |  Date: 2026-01-15",
        banner="EV Charging Site Project — Phase 1 Inputs (MOCK)",
    )
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, 9.55 * inch, "ELECTRICAL ROOM — PLAN (context excerpt, mock)")

    rm_x, rm_y, rm_w, rm_h = 1.1 * inch, 2.15 * inch, 6.4 * inch, 7.2 * inch
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.rect(rm_x, rm_y, rm_w, rm_h, stroke=1, fill=0)

    # Door opening (simple break + swing arc)
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    door_x = rm_x + rm_w
    door_y0 = rm_y + 0.9 * inch
    door_y1 = door_y0 + 0.9 * inch
    c.setStrokeColor(colors.white)
    c.setLineWidth(6)
    c.line(door_x, door_y0, door_x, door_y1)  # erase wall segment
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(door_x, door_y0, door_x - 0.75 * inch, door_y0)  # door leaf
    c.setStrokeColor(colors.grey)
    c.arc(door_x - 0.75 * inch, door_y0 - 0.75 * inch, door_x + 0.75 * inch, door_y0 + 0.75 * inch, 90, 180)

    # Equipment footprints
    def gear_box(x: float, y: float, w: float, h: float, label: str) -> None:
        c.setStrokeColor(colors.darkgrey)
        c.setLineWidth(1.4)
        c.rect(x, y, w, h, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.darkgrey)
        c.drawCentredString(x + w / 2, y + h / 2 - 4, label)
        c.setFillColor(colors.black)

    mdp = (rm_x + 0.55 * inch, rm_y + rm_h - 1.05 * inch, 2.2 * inch, 0.75 * inch)
    meter = (rm_x + 3.05 * inch, rm_y + rm_h - 1.05 * inch, 2.0 * inch, 0.75 * inch)
    subp = (rm_x + 0.55 * inch, rm_y + rm_h - 2.05 * inch, 1.8 * inch, 0.65 * inch)
    comms = (rm_x + 3.05 * inch, rm_y + rm_h - 2.05 * inch, 1.8 * inch, 0.65 * inch)
    gear_box(*mdp, label="MDP")
    gear_box(*meter, label="METER")
    gear_box(*subp, label="SUBP-1")
    gear_box(*comms, label="TEL/COMMS")

    # Working clearance zones (dashed, red)
    c.setDash(6, 4)
    c.setStrokeColor(colors.red)
    c.setLineWidth(1.5)
    clr_depth = 3.0 * inch
    c.rect(mdp[0], mdp[1] - clr_depth, mdp[2], clr_depth, stroke=1, fill=0)
    c.rect(subp[0], subp[1] - clr_depth, subp[2], clr_depth, stroke=1, fill=0)
    c.setDash()
    c.setStrokeColor(colors.black)

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.red)
    c.drawString(mdp[0], mdp[1] - clr_depth - 0.2 * inch, "WORKING CLEARANCE (mock)")
    c.setFillColor(colors.black)

    # Keynotes box
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(rm_x + rm_w - 2.25 * inch, rm_y + 0.35 * inch, 2.0 * inch, 1.55 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(rm_x + rm_w - 2.15 * inch, rm_y + 1.70 * inch, "KEYNOTES (mock)")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(rm_x + rm_w - 2.15 * inch, rm_y + 1.42 * inch, "1. Verify MDP nameplate.")
    c.drawString(rm_x + rm_w - 2.15 * inch, rm_y + 1.22 * inch, "2. Confirm spare spaces.")
    c.drawString(rm_x + rm_w - 2.15 * inch, rm_y + 1.02 * inch, "3. Maintain clearances.")
    c.setFillColor(colors.black)

    north_arrow(rm_x + rm_w - 0.35 * inch, rm_y + rm_h - 1.0 * inch)
    scale_bar(rm_x + rm_w - 3.0 * inch, rm_y + rm_h - 0.6 * inch)

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.9 * inch, 1.9 * inch, "NOTE: field verification required; excerpt supports Phase 1 data collection only.")
    c.setFillColor(colors.black)
    title_block(sheet="A1.11", title="Electrical Room Plan (Context Excerpt)", rev="2", date="2026-01-15")

    c.save()


@dataclass(frozen=True)
class CircuitRow:
    slot: str
    poles: str
    breaker: str
    load: str
    notes: str


def build_mock_panel_data() -> tuple[list[str], list[CircuitRow], list[str], list[CircuitRow]]:
    """
    Returns (MDP header lines, MDP rows, SUBP header lines, SUBP rows).
    Used as the single source for both raw inputs (P1-I02) and normalized outputs (P1.2).
    """
    mdp_header = [
        "Panel: MDP (Main Distribution Panel)",
        "Location: Electrical Room (ref)   Label: MDP (mock)",
        "Main device: 800A (mock)   Bus: 800A (mock)",
        "System: 208Y/120V, 3Ø, 4W (mock)",
        "Available spaces: 4 (3-pole) (mock)",
        "Note: header values to be field-verified against nameplate photos (P1-I03).",
    ]
    mdp_rows = [
        CircuitRow("1", "3", "100A", "Elevator feeder", "Existing"),
        CircuitRow("5", "3", "225A", "House panel HP-1", "Existing"),
        CircuitRow("9", "3", "150A", "Mechanical", "Existing"),
        CircuitRow("13", "3", "125A", "Fire pump (if any)", "Existing (mock)"),
        CircuitRow("17", "3", "200A", "SUBP-1 (common areas)", "Existing"),
        CircuitRow("21", "3", "225A", "Garage ventilation equipment", "Existing"),
        CircuitRow("25", "3", "150A", "Lighting panel LP-1", "Existing (mock)"),
        CircuitRow("29", "3", "150A", "Office/amenities", "Existing (mock)"),
        CircuitRow("33", "3", "100A", "Life safety (ref)", "Existing (mock)"),
        CircuitRow("37", "3", "125A", "Common receptacles", "Existing (mock)"),
        CircuitRow("41", "3", "150A", "HVAC equipment", "Existing"),
        CircuitRow("45", "3", "100A", "Domestic water pump", "Existing (mock)"),
        CircuitRow("49", "3", "100A", "Spare", "Spare (mock)"),
        CircuitRow("53", "3", "100A", "Spare", "Spare (mock)"),
        CircuitRow("57", "3", "200A", "Spare/Space", "Available 3-pole"),
        CircuitRow("61", "3", "200A", "Spare/Space", "Available 3-pole"),
        CircuitRow("65", "3", "200A", "Spare/Space", "Available 3-pole"),
        CircuitRow("69", "3", "200A", "Spare/Space", "Available 3-pole"),
    ]

    subp_header = [
        "Panel: SUBP-1 (Common Area Subpanel) (mock)",
        "Location: Electrical Room (ref)   Fed from: MDP (mock)",
        "Main: 225A (mock)   Bus: 225A (mock)",
        "System: 208Y/120V, 3Ø, 4W (mock)",
        "Note: schedule excerpt intended for Phase 2 inputs; verify labeling in field.",
    ]
    subp_rows = [
        CircuitRow("1", "1", "20A", "Lighting — Garage Row A", "Existing"),
        CircuitRow("3", "1", "20A", "Lighting — Garage Row B", "Existing"),
        CircuitRow("5", "1", "20A", "Lighting — Egress", "Existing (mock)"),
        CircuitRow("7", "1", "20A", "Receptacles — Common", "Existing"),
        CircuitRow("9", "1", "20A", "Receptacles — Janitor", "Existing (mock)"),
        CircuitRow("11", "2", "30A", "Garage exhaust fan #1", "Existing"),
        CircuitRow("13", "2", "30A", "Garage exhaust fan #2", "Existing (mock)"),
        CircuitRow("15", "2", "20A", "Door operator", "Existing (mock)"),
        CircuitRow("17", "2", "20A", "Fire alarm panel", "Existing (mock)"),
        CircuitRow("19", "1", "20A", "Spare", "Available"),
        CircuitRow("21", "1", "20A", "Spare", "Available"),
        CircuitRow("23", "2", "30A", "Spare", "Available"),
    ]
    return mdp_header, mdp_rows, subp_header, subp_rows


def write_panel_schedules_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)

    def schedule_page(
        page_num: int,
        panel_name: str,
        header_lines: list[str],
        rows: list[CircuitRow],
    ) -> None:
        watermark_pdf(c)
        pdf_header_footer(
            c,
            f"Panel Schedule — {panel_name} (Mock)",
            path.name,
            page_num,
            subtitle="Source: Electrical Contractor (mock)  |  Date: 2026-01-16",
            banner="EV Charging Site Project — Phase 1 Inputs (MOCK)",
        )
        c.setFont("Helvetica", 10)
        y = 9.65 * inch
        for line in header_lines:
            c.drawString(0.75 * inch, y, line)
            y -= 0.22 * inch
        y -= 0.1 * inch

        # Table header
        c.setFont("Helvetica-Bold", 9)
        cols = [
            ("Slot", 0.75 * inch),
            ("Poles", 1.35 * inch),
            ("Breaker", 2.05 * inch),
            ("Load", 3.2 * inch),
            ("Notes", 5.15 * inch),
        ]
        for label, x in cols:
            c.drawString(x, y, label)
        y -= 0.12 * inch
        c.setStrokeColor(colors.grey)
        c.line(0.75 * inch, y, 7.75 * inch, y)
        y -= 0.18 * inch

        c.setFont("Helvetica", 9)
        for r in rows:
            c.drawString(cols[0][1], y, r.slot)
            c.drawString(cols[1][1], y, r.poles)
            c.drawString(cols[2][1], y, r.breaker)
            c.drawString(cols[3][1], y, r.load[:26])
            c.drawString(cols[4][1], y, r.notes[:32])
            y -= 0.18 * inch
            if y < 1.2 * inch:
                break

        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(
            0.75 * inch,
            1.0 * inch,
            "DISCLAIMER: Generated mock panel schedules for documentation realism only. Replace with field-verified schedules.",
        )
        c.setFillColor(colors.black)
        c.showPage()

    mdp_header, mdp_rows, subp_header, subp_rows = build_mock_panel_data()

    schedule_page(
        1,
        "MDP",
        header_lines=mdp_header,
        rows=mdp_rows,
    )

    schedule_page(
        2,
        "SUBP-1",
        header_lines=subp_header,
        rows=subp_rows,
    )

    # Page 3: collection/verification notes to avoid “checkbox-only” feel.
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "Panel Schedules — Collection Notes + Acceptance Criteria (Mock)",
        path.name,
        3,
        subtitle="Electrical-only evidence notes (supports P1.1)",
        banner="EV Charging Site Project — Phase 1 Inputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This page documents what was checked when accepting the schedule package as a Phase 1 input. Replace with real project notes and initials in production use.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Acceptance criteria (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Header legibility: main rating, bus rating, voltage/phase, panel designation.",
        "Circuit rows legible for EV-relevant feeders; spares/spaces identified.",
        "Cross-check planned: compare header ratings vs photo evidence (P1-I03).",
        "Latest revision/date visible; superseded versions retained separately if applicable.",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Downstream use (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Phase 2: NEC/CEC load calculation basis (P2.1).",
        "Phase 3: updated schedules and one-line development (P3.4 / P3.1).",
        "Phase 4: supporting attachments for permit application package (P4.2).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    c.showPage()
    c.save()


def write_evse_cutsheet(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)

    def page(title: str, page_num: int, subtitle: str) -> None:
        watermark_pdf(c)
        pdf_header_footer(c, title, path.name, page_num, subtitle=subtitle, banner="EV Charging Site Project — Phase 1 Inputs (MOCK)")

    # Page 1: Overview
    page("EVSE Cut Sheet (Mock) — ElectriCharge L2-7.6-G (revA)", 1, subtitle="Installer/Vendor PDF (mock format)  |  Rev: A")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, 9.55 * inch, "Key Electrical Ratings (mock)")
    c.setFont("Helvetica", 10)
    ratings = [
        ("Supply system", "208Y/120V, 3-phase (line-to-line load) (mock)"),
        ("Nominal output power", "7.6 kW (nominal)"),
        ("Continuous current", "32A"),
        ("Recommended OCPD", "40A"),
        ("Enclosure", "NEMA 3R (mock)"),
        ("Communications", "OCPP 1.6J (mock)"),
        ("Listing", "UL 2594 / UL 2231 (mock)"),
    ]
    y = 9.25 * inch
    for k, v in ratings:
        c.drawString(0.85 * inch, y, f"{k}:")
        c.drawString(2.55 * inch, y, v)
        y -= 0.22 * inch

    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, y - 0.05 * inch, "Installation Notes (mock)")
    y -= 0.35 * inch
    y = draw_wrapped(
        c,
        0.85 * inch,
        y,
        "Branch circuit sizing shall comply with applicable NEC/CEC requirements for continuous loads. A 40A breaker is typical for 32A continuous output. Final breaker and conductor sizing per Engineer-of-Record.",
        6.9 * inch,
    )
    c.showPage()

    # Page 2: Wiring and dimensions
    page("EVSE Cut Sheet (Mock) — Wiring/Dimensions (revA)", 2, subtitle="ElectriCharge — Product Data Sheet (mock)")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, 9.55 * inch, "Wiring (mock excerpt)")
    c.setFont("Helvetica", 10)
    c.drawString(0.85 * inch, 9.3 * inch, "Input: L1, L2, L3, G (no neutral required). Optional control wiring per network kit (mock).")
    c.setStrokeColor(colors.black)
    c.rect(0.85 * inch, 6.7 * inch, 6.9 * inch, 2.4 * inch, stroke=1, fill=0)
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawString(1.05 * inch, 8.9 * inch, "(Mock wiring diagram placeholder)")
    c.setFillColor(colors.black)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, 6.3 * inch, "Dimensions (mock)")
    c.setFont("Helvetica", 10)
    dims = [
        "Height: 18.5 in",
        "Width: 12.0 in",
        "Depth: 6.0 in",
        "Mounting: wall or pedestal (mock accessory)",
    ]
    y = 6.05 * inch
    for d in dims:
        c.drawString(0.85 * inch, y, f"- {d}")
        y -= 0.22 * inch

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: Generated mock cut sheet for documentation format realism only.")
    c.setFillColor(colors.black)
    c.showPage()

    # Page 3: Labeling / installation checklist (adds “meaning” beyond a stub)
    page("EVSE Cut Sheet (Mock) — Labeling / Installation Checklist (revA)", 3, subtitle="Field-install notes (mock)")
    c.setFont("Helvetica", 10)
    y = 9.55 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This page summarizes common electrical-only installation considerations typically included in manufacturer documentation or installer checklists. Final requirements must follow the AHJ-adopted code basis and the EOR permit set.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Labeling / placarding (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Circuit identification label at EVSE and at panel schedule.",
        "If an EMS/load management system is used, label the controlled system and setpoint.",
        "Mark EVSE as continuous load; confirm breaker sizing basis (125%).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch
    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Electrical notes (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "No neutral required for line-to-line EVSE supply (if configured as such).",
        "Provide equipment grounding conductor with branch circuit conductors.",
        "Verify maximum OCPD per manufacturer listing.",
        "Final conductor sizing per terminal temperature ratings and derating factors.",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: This checklist is illustrative for mock documentation realism.")
    c.setFillColor(colors.black)
    c.showPage()
    c.save()


def write_ahj_code_basis_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "AHJ Electrical Permitting + Code Basis Evidence Capture (Mock)",
        path.name,
        1,
        subtitle="Capture date: 2026-01-17  |  Source: AHJ website (mock capture)",
        banner="EV Charging Site Project — Phase 1 Inputs (MOCK)",
    )

    c.setFont("Helvetica", 10)
    y = 9.6 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This PDF represents a mock evidence capture of the Authority Having Jurisdiction (AHJ) electrical permitting page and adopted code basis. Replace with an actual screenshot/capture and preserve metadata.",
        7.0 * inch,
    )
    y -= 0.2 * inch

    # “Browser capture” box
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(0.75 * inch, 2.1 * inch, 7.0 * inch, 7.0 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.95 * inch, 8.75 * inch, "City of Palo Alto — Building Division (Electrical Permits) (mock)")
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.blue)
    c.drawString(0.95 * inch, 8.5 * inch, "https://www.cityofpaloalto.example/building/electrical-permits (mock)")
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 10)
    y2 = 8.15 * inch
    fields = [
        ("AHJ (electrical permitting)", "City of Palo Alto — Building Division (Electrical Permits)"),
        ("Adopted electrical code", "2022 California Electrical Code (CEC) (mock)"),
        ("Amendments noted", "Local amendments may apply (mock note)"),
        ("Permit submittal method", "Online portal upload (mock)"),
        ("Plan check contact", "electricalpermits@paloalto.example (mock)"),
    ]
    for k, v in fields:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.95 * inch, y2, f"{k}:")
        c.setFont("Helvetica", 10)
        c.drawString(3.0 * inch, y2, v)
        y2 -= 0.26 * inch

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(
        0.95 * inch,
        2.35 * inch,
        "Metadata: captured_by=Jordan Lee (mock) | method=PDF print | timezone=PT | browser=Chrome (mock)",
    )
    c.setFillColor(colors.black)

    c.showPage()

    # Page 2: submittal requirements capture excerpt (adds usable context)
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "AHJ Electrical Permitting — Submittal Requirements Excerpt (Mock)",
        path.name,
        2,
        subtitle="Source: AHJ checklist page (mock capture)",
        banner="EV Charging Site Project — Phase 1 Inputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This page captures a mock summary of common AHJ electrical submittal requirements, preserved as evidence for Phase 1 intake and Phase 4 application packaging.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Requirements checklist (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Stamped electrical plans (PDF) with title blocks and sheet index.",
        "Load calculation summary (where applicable).",
        "Equipment cut sheets (EVSE + EMS if used).",
        "Site/address and applicant/contractor information.",
        "Single-line / one-line diagram included in plan set.",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch
    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Code adoption excerpt (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    y = draw_wrapped(
        c,
        1.0 * inch,
        y,
        "The City has adopted the 2022 California Electrical Code (CEC). Project documents shall reference the adopted code edition and any local amendments as applicable. (Mock excerpt.)",
        6.75 * inch,
    )
    c.showPage()
    c.save()


def write_normalized_siteplans_excerpts(path: Path, source_name: str) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "P1.2 Site Plans — Electrical Context Excerpts (Normalized) (Mock)",
        path.name,
        1,
        subtitle=f"Derived from: {source_name}",
        banner="EV Charging Site Project — Phase 1 Normalized Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.6 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This normalized excerpt package contains only the minimum plan information needed for electrical engineering: electrical room identification, service room context, and reference geometry. No routing/trenching/constructability assumptions are included.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Normalization actions (mock):")
    c.setFont("Helvetica", 10)
    y -= 0.26 * inch
    for line in [
        "OCR applied; searchable text verified",
        "Bookmarks added per sheet",
        "Electrical-context-only sheets extracted; superseded pages omitted",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch
    c.showPage()

    # Add 2 excerpt pages (schematic but not empty)
    for page_num, label in [(2, "Garage Plan Excerpt"), (3, "Electrical Room Excerpt")]:
        watermark_pdf(c)
        pdf_header_footer(
            c,
            f"{label} (Normalized, Mock)",
            path.name,
            page_num,
            subtitle=f"Derived from: {source_name}",
            banner="EV Charging Site Project — Phase 1 Normalized Outputs (MOCK)",
        )
        box_x, box_y, box_w, box_h = 0.9 * inch, 2.05 * inch, 6.9 * inch, 7.4 * inch
        c.setStrokeColor(colors.black)
        c.setLineWidth(1.2)
        c.rect(box_x, box_y, box_w, box_h, stroke=1, fill=0)

        if "Garage" in label:
            # Drive aisle
            c.setStrokeColor(colors.grey)
            c.setLineWidth(2)
            aisle_y = box_y + 3.7 * inch
            c.line(box_x + 0.2 * inch, aisle_y, box_x + box_w - 0.2 * inch, aisle_y)

            # stalls
            c.setStrokeColor(colors.grey)
            c.setLineWidth(1)
            stall_w, stall_h = 0.55 * inch, 1.15 * inch
            start_x = box_x + 0.35 * inch
            for base_y in [box_y + 0.35 * inch, box_y + box_h - (stall_h + 0.55 * inch)]:
                for i in range(11):
                    x = start_x + i * (stall_w + 0.06 * inch)
                    c.rect(x, base_y, stall_w, stall_h, stroke=1, fill=0)

            # electrical room highlight
            c.setStrokeColor(colors.blue)
            c.setLineWidth(2.2)
            c.rect(box_x + 0.25 * inch, box_y + box_h - 1.25 * inch, 2.25 * inch, 0.95 * inch, stroke=1, fill=0)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.blue)
            c.drawString(box_x + 0.35 * inch, box_y + box_h - 0.85 * inch, "ELECTRICAL ROOM (ref)")
            c.setFillColor(colors.black)
        else:
            # equipment footprints
            c.setStrokeColor(colors.darkgrey)
            c.setLineWidth(1.4)
            c.rect(box_x + 0.55 * inch, box_y + box_h - 1.15 * inch, 2.2 * inch, 0.75 * inch, stroke=1, fill=0)
            c.rect(box_x + 3.05 * inch, box_y + box_h - 1.15 * inch, 2.0 * inch, 0.75 * inch, stroke=1, fill=0)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.darkgrey)
            c.drawCentredString(box_x + 0.55 * inch + 1.1 * inch, box_y + box_h - 0.77 * inch, "MDP")
            c.drawCentredString(box_x + 3.05 * inch + 1.0 * inch, box_y + box_h - 0.77 * inch, "METER")
            c.setFillColor(colors.black)

            # dashed clearance
            c.setDash(6, 4)
            c.setStrokeColor(colors.red)
            c.setLineWidth(1.5)
            c.rect(box_x + 0.55 * inch, box_y + box_h - 1.15 * inch - 3.0 * inch, 2.2 * inch, 3.0 * inch, stroke=1, fill=0)
            c.setDash()
            c.setStrokeColor(colors.black)

        c.showPage()

    c.save()


def write_normalized_panel_schedules(path: Path, source_name: str) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "P1.2 Panel Schedules — Normalized Package (Mock)",
        path.name,
        1,
        subtitle=f"Derived from: {source_name}",
        banner="EV Charging Site Project — Phase 1 Normalized Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.6 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This normalized schedule package standardizes scan quality, table ordering, and header callouts required for Phase 2 load calculations and Phase 3 schedule updates.",
        7.0 * inch,
    )
    y -= 0.2 * inch

    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Header callouts (mock excerpt):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "MDP: 800A main, 800A bus, 208Y/120V, 3Ø",
        "Spare spaces: 4 (3-pole) identified",
        "Panel nomenclature standardized (MDP, SUBP-1)",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Normalization actions (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "OCR applied; searchable text verified.",
        "Header fields extracted to standardized table.",
        "Row ordering standardized; illegible rows flagged for field verification.",
        "Superseded pages omitted from the engineering package (retained separately in raw archive).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    c.showPage()

    mdp_header, mdp_rows, subp_header, subp_rows = build_mock_panel_data()

    def normalized_table(page_num: int, panel: str, header_lines: list[str], rows: list[CircuitRow]) -> None:
        watermark_pdf(c)
        pdf_header_footer(
            c,
            f"Normalized Schedule — {panel} (Mock)",
            path.name,
            page_num,
            subtitle=f"Derived from: {source_name}",
            banner="EV Charging Site Project — Phase 1 Normalized Outputs (MOCK)",
        )
        c.setFont("Helvetica", 10)
        y0 = 9.65 * inch
        for line in header_lines:
            c.drawString(0.75 * inch, y0, line)
            y0 -= 0.22 * inch
        y0 -= 0.08 * inch

        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75 * inch, y0, "Slot")
        c.drawString(1.35 * inch, y0, "Poles")
        c.drawString(2.05 * inch, y0, "Breaker")
        c.drawString(3.2 * inch, y0, "Load (standardized)")
        c.drawString(5.55 * inch, y0, "Disposition")
        y0 -= 0.12 * inch
        c.setStrokeColor(colors.grey)
        c.line(0.75 * inch, y0, 7.75 * inch, y0)
        y0 -= 0.18 * inch

        c.setFont("Helvetica", 9)
        for r in rows:
            c.drawString(0.75 * inch, y0, r.slot)
            c.drawString(1.35 * inch, y0, r.poles)
            c.drawString(2.05 * inch, y0, r.breaker)
            c.drawString(3.2 * inch, y0, r.load[:26])
            disp = "SPARE" if ("Spare" in r.load or "Spare" in r.notes) else "OK"
            c.drawString(5.55 * inch, y0, disp)
            y0 -= 0.18 * inch
            if y0 < 1.2 * inch:
                break

        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(0.75 * inch, 1.0 * inch, "NOTE: Normalized excerpt for engineering package use (mock).")
        c.setFillColor(colors.black)
        c.showPage()

    normalized_table(
        2,
        "MDP",
        mdp_header[:4] + ["Engineering extraction: spare 3-pole spaces noted; verify against field labels."],
        mdp_rows,
    )
    normalized_table(
        3,
        "SUBP-1",
        subp_header[:4] + ["Engineering extraction: common-area loads present; verify labeling in field."],
        subp_rows,
    )
    c.save()


def write_normalized_photos_index(path: Path, source_name: str, zip_name: str, manifest: list[tuple[str, str]]) -> None:
    write_photo_index_pdf(
        path=path,
        zip_name=zip_name,
        manifest=manifest,
        title="P1.2 Photos — Annotated Index (Normalized) (Mock)",
        subtitle=f"Derived from: {source_name}",
    )


def write_normalized_evse_cutsheet(path: Path, source_name: str) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "P1.2 EVSE Cut Sheet — Frozen for Design Basis (Mock)",
        path.name,
        1,
        subtitle=f"Derived from: {source_name}  |  Status: Frozen for Phase 2/3",
        banner="EV Charging Site Project — Phase 1 Normalized Outputs (MOCK)",
    )
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.darkred)
    c.drawCentredString(letter[0] / 2, 7.6 * inch, "FROZEN FOR DESIGN BASIS")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    y = draw_wrapped(
        c,
        0.75 * inch,
        6.9 * inch,
        "This normalized cut sheet is the design-basis EVSE document for Phase 2 and Phase 3. If the EVSE model/revision changes, Phase 2 (load calc) and downstream drawings must be revalidated.",
        7.0 * inch,
    )
    y -= 0.15 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Extracted design-basis values (mock):")
    y -= 0.26 * inch
    for k, v in [
        ("Model", "ElectriCharge L2-7.6-G"),
        ("Supply", "208Y/120V, 3Φ (line-to-line)"),
        ("Continuous current", "32A"),
        ("Typical OCPD", "40A"),
        ("Downstream use", "P2.1 load calc; P3.1 one-line; P3.4 schedules"),
    ]:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.9 * inch, y, f"{k}:")
        c.setFont("Helvetica", 10)
        c.drawString(2.6 * inch, y, v)
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Change control (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    draw_wrapped(
        c,
        0.9 * inch,
        y,
        "If EVSE revision changes from revA, archive the new revision as a new evidence item and re-run Phase 2 validation. Do not silently replace design-basis evidence without updating the register.",
        6.85 * inch,
    )
    c.showPage()
    c.save()


def write_normalized_ahj_code_basis(path: Path, source_name: str) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "P1.2 AHJ + Code Basis Evidence (Normalized) (Mock)",
        path.name,
        1,
        subtitle=f"Derived from: {source_name}",
        banner="EV Charging Site Project — Phase 1 Normalized Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.6 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This normalized evidence preserves the AHJ identity and adopted electrical code basis used for code sheets and permit application packaging. Replace with actual capture and archive portal/download metadata.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Normalized fields (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "AHJ: City of Palo Alto — Building Division (Electrical Permits)",
        "Code basis: 2022 California Electrical Code (CEC)",
        "Capture timestamp and capture method recorded",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch
    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Downstream usage (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "P3.5 electrical notes/code sheet references",
        "P4.2 permit application package (forms + metadata)",
        "P5 plan-check responses anchored to adopted code edition",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch
    c.showPage()
    c.save()


def main() -> None:
    ensure_dirs()

    # --- Phase 1 Inputs (stable filenames per Addendum A) ---
    p1_i01 = P1_INPUTS / "P1-I01_SitePlans_Arch_Set_rev2_2026-01-15.pdf"
    p1_i02 = P1_INPUTS / "P1-I02_PanelSchedules_MDP_and_Subpanels_2026-01-16.pdf"
    p1_i03_zip = P1_INPUTS / "P1-I03_PhotoSet_ServiceGear_Nameplates_2026-01-16.zip"
    p1_i03_index = P1_INPUTS / "P1-I03_PhotoIndex_Annotated_2026-01-16.pdf"
    p1_i04 = P1_INPUTS / "P1-I04_EVSE_CutSheet_ElectriCharge_L2-7.6-G_revA.pdf"
    p1_i05 = P1_INPUTS / "P1-I05_AHJ_Electrical_Permitting_CodeBasis_2026-01-17.pdf"

    write_site_plans_pdf(p1_i01)
    write_panel_schedules_pdf(p1_i02)
    manifest = build_photo_zip(
        p1_i03_zip,
        sources=(NAMEPLATE_SRC + SITE_SRC),
        total_images=24,
        start_dt=datetime(2026, 1, 16, 10, 5, 0),
    )
    write_photo_index_pdf(
        path=p1_i03_index,
        zip_name=p1_i03_zip.name,
        manifest=manifest,
        title="Photo Index — Annotated (Mock) (Phase 1 Input)",
        subtitle="Index for P1-I03 photo set (mock)",
    )
    write_evse_cutsheet(p1_i04)
    write_ahj_code_basis_pdf(p1_i05)

    # --- Phase 1 Normalized Outputs (P1.2) ---
    p1_2_siteplans = P1_OUTPUTS / "P1.2_SitePlans_ElectricalContext_Excerpts_2026-01-18.pdf"
    p1_2_schedules = P1_OUTPUTS / "P1.2_PanelSchedules_Normalized_MDP_Subpanels_2026-01-18.pdf"
    p1_2_photos = P1_OUTPUTS / "P1.2_Photos_Annotated_Index_2026-01-18.pdf"
    p1_2_evse = P1_OUTPUTS / "P1.2_EVSE_CutSheet_FrozenForDesign_revA_2026-01-18.pdf"
    p1_2_ahj = P1_OUTPUTS / "P1.2_AHJ_CodeBasis_Normalized_2026-01-18.pdf"

    write_normalized_siteplans_excerpts(p1_2_siteplans, source_name=p1_i01.name)
    write_normalized_panel_schedules(p1_2_schedules, source_name=p1_i02.name)
    write_normalized_photos_index(p1_2_photos, source_name=p1_i03_index.name, zip_name=p1_i03_zip.name, manifest=manifest)
    write_normalized_evse_cutsheet(p1_2_evse, source_name=p1_i04.name)
    write_normalized_ahj_code_basis(p1_2_ahj, source_name=p1_i05.name)

    print("Generated Phase 1 package:")
    for f in [p1_i01, p1_i02, p1_i03_zip, p1_i03_index, p1_i04, p1_i05, p1_2_siteplans, p1_2_schedules, p1_2_photos, p1_2_evse, p1_2_ahj]:
        print(" -", f.relative_to(ROOT))


if __name__ == "__main__":
    main()

