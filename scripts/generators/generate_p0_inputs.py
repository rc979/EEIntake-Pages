import csv
import io
import math
import os
import random
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Dependencies:
#   python3 -m pip install --user reportlab pillow
from PIL import Image, ImageEnhance
from PIL import ImageFilter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


SEED = 42
random.seed(SEED)

ROOT = Path.cwd()
P0_INPUTS = ROOT / "P0" / "Inputs"

# These source images were generated earlier and live in Cursor's assets folder.
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
    P0_INPUTS.mkdir(parents=True, exist_ok=True)


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
) -> None:
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.75 * inch, 10.55 * inch, title)
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    if subtitle:
        c.drawString(0.75 * inch, 10.33 * inch, subtitle)
    c.drawString(0.75 * inch, 10.15 * inch, "EV Charging Site Project — Phase 0 Inputs (MOCK)")
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(
        0.75 * inch,
        0.5 * inch,
        f"File: {file_name}  |  Generated: {datetime.now().date()}  |  Page {page_num}",
    )
    c.setFillColor(colors.black)


def draw_paragraph(c: canvas.Canvas, x: float, y: float, text: str, max_width: float) -> float:
    """Draw simple wrapped paragraph and return new y."""
    c.setFont("Helvetica", 10)
    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, "Helvetica", 10) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= 0.18 * inch
            line = w
    if line:
        c.drawString(x, y, line)
        y -= 0.18 * inch
    return y


def gen_interval_series_2025() -> list[tuple[datetime, float]]:
    """15-min interval demand (kW) for 2025. Realistic daily/weekly/seasonal pattern."""
    start = datetime(2025, 1, 1, 0, 0)
    end = datetime(2026, 1, 1, 0, 0)
    step = timedelta(minutes=15)

    series: list[tuple[datetime, float]] = []
    t = start
    while t < end:
        hour = t.hour + t.minute / 60
        day = t.timetuple().tm_yday
        dow = t.weekday()  # 0=Mon

        # Base building load (multifamily garage + common area).
        base = 18.0
        # Daily shape: midday higher, overnight lower.
        daily = 10.0 + 14.0 * math.sin((hour - 7.0) / 24.0 * 2.0 * math.pi)
        # Weekday/weekend adjustment: weekends slightly lower.
        weekend_adj = -2.5 if dow >= 5 else 0.0
        # Seasonal: summer higher (ventilation + cooling).
        seasonal = 4.5 * math.sin((day - 170.0) / 365.0 * 2.0 * math.pi)
        # Random noise.
        noise = random.uniform(-2.2, 2.2)

        kw = max(8.0, base + daily + weekend_adj + seasonal + noise)

        # Introduce occasional spikes (elevator/garage fans).
        if random.random() < 0.002:
            kw *= random.uniform(1.15, 1.35)

        # Missingness: 0.3% flagged by writing blank value later; keep kw but track separately.
        series.append((t, kw))
        t += step

    return series


@dataclass(frozen=True)
class MonthlyStats:
    year: int
    month: int
    kwh: float
    peak_kw: float


def monthly_stats_from_series(series: list[tuple[datetime, float]]) -> list[MonthlyStats]:
    # kWh per 15-min interval = kW * 0.25
    monthly: dict[tuple[int, int], dict[str, float]] = {}
    for ts, kw in series:
        key = (ts.year, ts.month)
        if key not in monthly:
            monthly[key] = {"kwh": 0.0, "peak_kw": 0.0}
        monthly[key]["kwh"] += kw * 0.25
        monthly[key]["peak_kw"] = max(monthly[key]["peak_kw"], kw)

    out: list[MonthlyStats] = []
    for (y, m) in sorted(monthly.keys()):
        out.append(
            MonthlyStats(
                year=y,
                month=m,
                kwh=monthly[(y, m)]["kwh"],
                peak_kw=monthly[(y, m)]["peak_kw"],
            )
        )
    return out


def write_green_button_csv(path: Path, series: list[tuple[datetime, float]]) -> None:
    # Green Button exports vary; this is a representative, normalized CSV.
    # Keep it clearly MOCK.
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "timestamp_local",
                "timezone",
                "interval_minutes",
                "demand_kw",
                "quality",
                "note",
            ]
        )
        for ts, kw in series:
            quality = "ACTUAL"
            if random.random() < 0.003:
                quality = "ESTIMATED"
            if random.random() < 0.003:
                quality = "MISSING"
                w.writerow([ts.strftime("%Y-%m-%d %H:%M:%S"), "Local", 15, "", quality, "MOCK"])
            else:
                w.writerow([ts.strftime("%Y-%m-%d %H:%M:%S"), "Local", 15, f"{kw:.2f}", quality, "MOCK"])


def write_utility_bills_pdf(path: Path, stats: list[MonthlyStats]) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    pages = 1 + 12  # summary + one page per month

    # Summary page
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "Utility Bills — Consolidated Summary",
        path.name,
        1,
        subtitle="Account: XXX-123-456 (masked)  |  Service: 120/208V, 3Ø, 4W  |  Rate: GS-2 (mock)",
    )

    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_paragraph(
        c,
        0.75 * inch,
        y,
        "This consolidated PDF is a representative mock of 12 monthly electric bills used for Phase 0 screening-level feasibility only. Values are derived from the accompanying Green Button interval dataset (P0-I01).",
        max_width=7.0 * inch,
    )
    y -= 0.1 * inch

    # Table header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Billing Period (2025)")
    c.drawString(3.0 * inch, y, "Usage (kWh)")
    c.drawString(4.35 * inch, y, "Peak Demand (kW)")
    c.drawString(6.1 * inch, y, "Amount Due ($)")
    y -= 0.18 * inch
    c.setStrokeColor(colors.grey)
    c.line(0.75 * inch, y, 7.75 * inch, y)
    y -= 0.22 * inch

    c.setFont("Helvetica", 10)
    total_kwh = 0.0
    for s in stats:
        total_kwh += s.kwh
        # Simple mock bill amount: base charge + energy + demand
        amount = 65 + (s.kwh * 0.14) + (s.peak_kw * 9.5)
        c.drawString(0.75 * inch, y, f"{s.year}-{s.month:02d}-01 to {s.year}-{s.month:02d}-{28 if s.month==2 else 30 if s.month in (4,6,9,11) else 31}")
        c.drawRightString(4.1 * inch, y, f"{s.kwh:,.0f}")
        c.drawRightString(5.85 * inch, y, f"{s.peak_kw:,.1f}")
        c.drawRightString(7.75 * inch, y, f"{amount:,.2f}")
        y -= 0.2 * inch
        if y < 1.3 * inch:
            break

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Annual total (kWh):")
    c.drawRightString(4.1 * inch, y, f"{total_kwh:,.0f}")

    c.showPage()

    # Monthly pages
    for idx, s in enumerate(stats, start=2):
        watermark_pdf(c)
        month_name = datetime(s.year, s.month, 1).strftime("%B %Y")
        pdf_header_footer(
            c,
            f"Electric Bill (Mock) — {month_name}",
            path.name,
            idx,
            subtitle="UtilityCo Electric — Statement (mock format)",
        )

        # Left column details
        c.setFont("Helvetica", 10)
        y = 9.65 * inch
        lines = [
            "Service Address: 123 Demo St, Example City, ST (mock)",
            "Meter: MTR-XXXXXX (masked)",
            "Customer: Example Owner LLC (mock)",
            "Billing Type: Non-residential common-area meter (mock)",
            "",
            f"Usage (kWh): {s.kwh:,.0f}",
            f"Peak Demand (kW): {s.peak_kw:,.1f}",
            "Power Factor: 0.96 (mock)",
            "",
        ]
        for line in lines:
            c.drawString(0.75 * inch, y, line)
            y -= 0.22 * inch

        # Charges box
        c.setStrokeColor(colors.black)
        c.rect(0.75 * inch, 5.4 * inch, 7.0 * inch, 2.7 * inch, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.95 * inch, 7.85 * inch, "Charges (mock)")
        c.setFont("Helvetica", 10)

        base = 65.00
        energy = s.kwh * 0.14
        demand = s.peak_kw * 9.5
        taxes = (base + energy + demand) * 0.06
        total = base + energy + demand + taxes

        charge_lines = [
            ("Customer charge", base),
            ("Energy charge", energy),
            ("Demand charge", demand),
            ("Taxes/fees", taxes),
        ]
        y2 = 7.55 * inch
        for label, amt in charge_lines:
            c.drawString(0.95 * inch, y2, label)
            c.drawRightString(7.55 * inch, y2, f"${amt:,.2f}")
            y2 -= 0.28 * inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.95 * inch, y2 - 0.05 * inch, "Amount due")
        c.drawRightString(7.55 * inch, y2 - 0.05 * inch, f"${total:,.2f}")

        # Disclaimer
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(
            0.75 * inch,
            1.05 * inch,
            "DISCLAIMER: This page is a generated mock artifact for documentation format realism only.",
        )
        c.setFillColor(colors.black)

        c.showPage()

    c.save()


def write_utility_service_info_letter(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "Utility Service Information Letter (Mock)",
        path.name,
        1,
        subtitle="UtilityCo Electric — Service Planning (mock letterhead)",
    )
    c.setFont("Helvetica", 10)
    y = 9.6 * inch
    body = [
        "Date: 2025-12-18 (mock)",
        "To: Project Team (Owner + Electrical Engineer)",
        "Subject: Service information — EV charging screening inquiry (mock reference: UTIL-REQ-2025-1193)",
        "",
        "Service summary (best-effort, non-binding):",
        "- Existing service: 120/208V, 3Ø, 4W",
        "- Meter class: self-contained (mock)",
        "- Recorded maximum demand (12-mo): ~68 kW (mock)",
        "- Service equipment rating: 400A main (field-verified via nameplate photos)",
        "",
        "Requirements for progressing to formal review:",
        "1) Submit a load letter including existing + new connected load and any load management.",
        "2) Provide a single-line diagram for EV equipment and interconnection point.",
        "3) If using an EMS, include product listing and setpoint strategy.",
        "",
        "DISCLAIMERS:",
        "- This information is provided for screening only and does not reserve capacity.",
        "- Final acceptance is subject to utility engineering review and field verification.",
        "",
        "Utility contact (technical): Taylor Nguyen (mock)  |  t.nguyen@utilityco.example  |  (555) 010-2040",
    ]
    for line in body:
        if line == "":
            y -= 0.12 * inch
        else:
            c.drawString(0.75 * inch, y, line)
            y -= 0.22 * inch

    c.save()


def write_evse_cutsheet(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)

    def page(title: str, page_num: int) -> None:
        watermark_pdf(c)
        pdf_header_footer(c, title, path.name, page_num, subtitle="ElectriCharge — Product Data Sheet (mock)")

    # Page 1: Overview
    page("EVSE Cut Sheet — Model L2-7.6-G (Mock)", 1)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, 9.55 * inch, "Key Ratings (mock)")
    c.setFont("Helvetica", 10)
    ratings = [
        ("Input voltage", "208/240 VAC, single-phase (configurable)"),
        ("Max output power", "7.6 kW @ 240V (32A)"),
        ("Continuous current", "32A"),
        ("Enclosure", "NEMA 3R"),
        ("Cable", "18 ft (mock)"),
        ("Communications", "OCPP 1.6J (mock)"),
        ("Listing", "UL 2594 / UL 2231 (mock)"),
    ]
    y = 9.25 * inch
    for k, v in ratings:
        c.drawString(0.85 * inch, y, f"{k}:")
        c.drawString(2.35 * inch, y, v)
        y -= 0.22 * inch

    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, y - 0.05 * inch, "Installation Notes (mock)")
    y -= 0.35 * inch
    c.setFont("Helvetica", 10)
    y = draw_paragraph(
        c,
        0.85 * inch,
        y,
        "Branch circuit sizing shall comply with applicable NEC/CEC requirements for continuous loads. A 40A breaker is typical for 32A continuous output. Final breaker and conductor sizing per engineer of record.",
        6.9 * inch,
    )
    c.showPage()

    # Page 2: Wiring and dimensions
    page("EVSE Cut Sheet — Wiring/Dimensions (Mock)", 2)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, 9.55 * inch, "Wiring (mock diagram excerpt)")
    c.setFont("Helvetica", 10)
    c.drawString(0.85 * inch, 9.3 * inch, "Input: L1, L2, G (no neutral required). Optional control wiring per network kit (mock).")
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
    c.drawString(
        0.75 * inch,
        1.05 * inch,
        "NOTE: This is a generated mock cut sheet for documentation format realism only.",
    )
    c.setFillColor(colors.black)
    c.showPage()

    c.save()


def make_phone_filename(base_dt: datetime, idx: int, ext: str = "jpg") -> str:
    ts = (base_dt + timedelta(seconds=idx * 37)).strftime("%Y%m%d_%H%M%S")
    return f"IMG_{ts}_{idx:02d}.{ext}"


def _ahash(img: Image.Image, hash_size: int = 8) -> int:
    """
    Average hash (aHash) for perceptual dedupe.
    Returns an integer bitmask of length hash_size^2.
    """
    g = img.convert("L").resize((hash_size, hash_size), resample=Image.BICUBIC)
    px = list(g.getdata())
    avg = sum(px) / len(px)
    bits = 0
    for i, v in enumerate(px):
        if v >= avg:
            bits |= 1 << i
    return bits


def _transform_photo(img: Image.Image, stronger: bool = False) -> Image.Image:
    """
    Apply phone-like imperfections to create distinct-looking photos.
    Stronger transforms kick in if uniqueness is hard to reach.
    """
    out = img.copy()
    w, h = out.size

    # Crop jitter (more aggressive than before)
    max_crop = 0.06 if not stronger else 0.12
    dx = int(w * random.uniform(0.0, max_crop))
    dy = int(h * random.uniform(0.0, max_crop))
    if dx > 0 or dy > 0:
        out = out.crop((dx, dy, w - dx, h - dy)).resize((w, h), resample=Image.BICUBIC)

    # Slight rotation / hand tilt
    angle = random.uniform(-1.8, 1.8) if not stronger else random.uniform(-3.0, 3.0)
    out = out.rotate(angle, expand=False, resample=Image.BICUBIC)

    # Exposure + color drift
    out = ImageEnhance.Brightness(out).enhance(random.uniform(0.85, 1.18))
    out = ImageEnhance.Contrast(out).enhance(random.uniform(0.85, 1.22))
    out = ImageEnhance.Color(out).enhance(random.uniform(0.88, 1.18))

    # Occasional mild blur (motion / focus)
    if random.random() < (0.18 if not stronger else 0.28):
        out = out.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.4, 1.2 if stronger else 0.9)))

    # Add a tiny amount of noise/grain (JPEG + low light)
    if random.random() < 0.85:
        # Simple grain: resize down/up slightly (phone ISP artifacts)
        scale = random.uniform(0.94, 0.985) if not stronger else random.uniform(0.90, 0.975)
        out = out.resize((int(w * scale), int(h * scale)), resample=Image.BICUBIC).resize((w, h), resample=Image.BICUBIC)

    return out


def build_photo_zip(zip_path: Path, sources: list[Path], total_images: int, start_dt: datetime) -> list[tuple[str, str]]:
    """
    Create a zip of JPG images with phone-like filenames.
    Returns list of (filename_in_zip, caption) for index.
    """
    captions: list[str] = []
    for p in sources:
        captions.append(p.stem.replace("_", " "))

    # Load images
    src_imgs = [Image.open(str(p)).convert("RGB") for p in sources]

    # Generate unique-looking images on the fly using perceptual hashing.
    # This avoids "same photo with tiny tweaks" repeating across the ZIP.
    used_hashes: set[int] = set()
    manifest: list[tuple[str, str]] = []

    # Ensure at least one variant per source before filling the rest.
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
            # Try to find a perceptually unique transform.
            for attempt in range(max_attempts_per_img):
                stronger = attempt > (max_attempts_per_img // 2)
                candidate = _transform_photo(base_img, stronger=stronger)
                hsh = _ahash(candidate, hash_size=8)
                if hsh not in used_hashes:
                    used_hashes.add(hsh)
                    chosen = candidate
                    break

            if chosen is None:
                # Fallback: accept whatever we have, but still vary filename.
                chosen = _transform_photo(base_img, stronger=True)

            fname = make_phone_filename(start_dt, idx, ext="jpg")
            buf = io.BytesIO()
            chosen.save(buf, format="JPEG", quality=86)
            z.writestr(fname, buf.getvalue())
            manifest.append((fname, cap))

    return manifest


def write_photo_index_pdf(path: Path, nameplate_manifest: list[tuple[str, str]], site_manifest: list[tuple[str, str]]) -> None:
    """
    Produce an annotated PDF index referencing images inside the two zips.
    (We don't embed the images from inside the zip; instead we include key thumbnails from source set.)
    """
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    pdf_header_footer(
        c,
        "Photo Index — Annotated (Mock)",
        path.name,
        1,
        subtitle="Index for P0-I02 and P0-I04 photo sets (mock)",
    )

    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    intro = (
        "This index summarizes representative field photos collected during a screening-level walkdown. "
        "Photo sets are packaged as ZIP files. Captions indicate what the photo is intended to evidence for electrical design."
    )
    y = draw_paragraph(c, 0.75 * inch, y, intro, 7.0 * inch)
    y -= 0.15 * inch

    def draw_table(title: str, rows: list[tuple[str, str]], y0: float) -> float:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.75 * inch, y0, title)
        y = y0 - 0.22 * inch
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75 * inch, y, "Photo filename (in ZIP)")
        c.drawString(3.25 * inch, y, "What it shows (electrical-only)")
        y -= 0.12 * inch
        c.setStrokeColor(colors.grey)
        c.line(0.75 * inch, y, 7.75 * inch, y)
        y -= 0.18 * inch
        c.setFont("Helvetica", 9)
        for fname, cap in rows[:18]:
            c.drawString(0.75 * inch, y, fname)
            c.drawString(3.25 * inch, y, cap[:80])
            y -= 0.18 * inch
            if y < 1.2 * inch:
                break
        return y

    y = draw_table("P0-I02 — MDP Nameplate Photos (ZIP)", nameplate_manifest, y)
    if y < 4.2 * inch:
        c.showPage()
        watermark_pdf(c)
        pdf_header_footer(c, "Photo Index — Annotated (Mock)", path.name, 2)
        y = 9.65 * inch
    y -= 0.25 * inch
    y = draw_table("P0-I04 — Existing Gear + Garage Area Photos (ZIP)", site_manifest, y)

    c.showPage()

    # Add a few “annotated thumbnail” pages using source images (for realism).
    thumbs = NAMEPLATE_SRC[:2] + SITE_SRC[:4]
    for page_num, img_path in enumerate(thumbs, start=3):
        watermark_pdf(c)
        pdf_header_footer(c, "Annotated Photo Sheet (Mock)", path.name, page_num)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.75 * inch, 9.65 * inch, f"Source: {img_path.name}")
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        c.drawString(0.75 * inch, 9.45 * inch, "Annotations are illustrative; replace with real field markups.")
        c.setFillColor(colors.black)

        pil = Image.open(str(img_path)).convert("RGB")
        # Resize to fit
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
        c.rect(0.95 * inch, 2.45 * inch, 2.4 * inch, 1.2 * inch)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.red)
        c.drawString(0.95 * inch, 1.95 * inch, "MOCK CALLOUT: verify rating / clearance")
        c.setFillColor(colors.black)

        c.showPage()

    c.save()


def main() -> None:
    ensure_dirs()

    # 1) Generate Green Button CSV
    series = gen_interval_series_2025()
    csv_path = P0_INPUTS / "P0-I01_GreenButton_IntervalData_2025.csv"
    write_green_button_csv(csv_path, series)

    # 2) Derive stats and generate bills PDF
    stats = monthly_stats_from_series(series)
    bills_pdf = P0_INPUTS / "P0-I01_Utility_Bills_2025-01_to_2025-12.pdf"
    write_utility_bills_pdf(bills_pdf, stats)

    # 3) Utility service info letter
    util_letter = P0_INPUTS / "P0-I02_Utility_Service_Info_Letter.pdf"
    write_utility_service_info_letter(util_letter)

    # 4) EVSE cut sheet
    evse_pdf = P0_INPUTS / "P0-I03_ElectriCharge_L2-7.6-G_CutSheet_revA.pdf"
    write_evse_cutsheet(evse_pdf)

    # 5) Build photo zips
    nameplate_zip = P0_INPUTS / "P0-I02_MDP_Nameplate_Photos.zip"
    site_zip = P0_INPUTS / "P0-I04_PhotoSet_ExistingGear_and_GarageArea.zip"

    nameplate_manifest = build_photo_zip(
        nameplate_zip, NAMEPLATE_SRC, total_images=16, start_dt=datetime(2025, 12, 12, 10, 15, 0)
    )
    site_manifest = build_photo_zip(
        site_zip, SITE_SRC, total_images=32, start_dt=datetime(2025, 12, 12, 10, 45, 0)
    )

    # 6) Photo index PDF referencing ZIP contents
    index_pdf = P0_INPUTS / "P0-I04_PhotoIndex_Annotated.pdf"
    write_photo_index_pdf(index_pdf, nameplate_manifest, site_manifest)

    print("Generated Phase 0 inputs in:", str(P0_INPUTS))
    for f in [
        bills_pdf,
        csv_path,
        nameplate_zip,
        util_letter,
        evse_pdf,
        site_zip,
        index_pdf,
    ]:
        print(" -", f.name)


if __name__ == "__main__":
    main()

