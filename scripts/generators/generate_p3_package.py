import io
import math
import random
from datetime import datetime
from pathlib import Path

# Dependencies:
#   python3 -m pip install --user reportlab pillow PyPDF2
from PIL import Image
from PyPDF2 import PdfMerger
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

SEED = 44
random.seed(SEED)

ROOT = Path.cwd()
P3_INPUTS = ROOT / "P3" / "Inputs"
P3_OUTPUTS = ROOT / "P3" / "Outputs"

# Reuse the same asset source location used by Phase 0/1 generation.
ASSETS_DIR = Path(
    "/Users/rc/.cursor/projects/var-folders-m-fdkkzfb13z7c6gbcgc19n4sw0000gn-T-60687e3d-f30b-4bd0-9b54-6006fa63ce48/assets"
)

SITE_SRC = [
    ASSETS_DIR / "P0_Site_Context_01.png",
    ASSETS_DIR / "P0_Site_Context_02.png",
    ASSETS_DIR / "P0_Site_Context_03.png",
]


def ensure_dirs() -> None:
    P3_INPUTS.mkdir(parents=True, exist_ok=True)
    P3_OUTPUTS.mkdir(parents=True, exist_ok=True)


def watermark_pdf(c: canvas.Canvas, text: str = "MOCK / EXAMPLE ONLY") -> None:
    c.saveState()
    c.setFillColor(colors.lightgrey)
    c.setFont("Helvetica-Bold", 48)
    c.translate(letter[0] / 2, letter[1] / 2)
    c.rotate(30)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def header_footer(
    c: canvas.Canvas,
    title: str,
    file_name: str,
    page_num: int,
    subtitle: str = "",
    banner: str = "EV Charging Site Project — Phase 3 (MOCK)",
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


def title_block(c: canvas.Canvas, sheet: str, sheet_title: str, rev: str, date: str, issued_for: str = "UNSTAMPED") -> None:
    c.saveState()
    x0, y0, w, h = 0.75 * inch, 0.75 * inch, 7.0 * inch, 1.0 * inch
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
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
    c.drawString(x0 + 1.35 * inch, y0 + 0.48 * inch, sheet_title[:40])
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
    c.drawString(x0 + 6.12 * inch, y0 + 0.48 * inch, issued_for)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(x0 + 6.12 * inch, y0 + 0.24 * inch, "(electrical-only)")
    c.restoreState()


def north_arrow(c: canvas.Canvas, x: float, y: float) -> None:
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


def scale_bar(c: canvas.Canvas, x: float, y: float, feet: int = 40) -> None:
    c.saveState()
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(x, y, 2.8 * inch, 0.18 * inch, stroke=1, fill=0)
    block_w = (2.8 * inch) / 8
    for i in range(8):
        if i % 2 == 0:
            c.setFillColor(colors.black)
            c.rect(x + i * block_w, y, block_w, 0.18 * inch, stroke=0, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    c.drawString(x, y + 0.24 * inch, f"SCALE (mock): 1\" = {feet} ft")
    c.restoreState()


def write_parking_layout_input(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "Parking Layout — Owner Provided (Mock)",
        path.name,
        1,
        subtitle="Input to P3.2 site plan sheet (electrical-impacting locations only)  |  Date: 2026-01-20",
        banner="EV Charging Site Project — Phase 3 Inputs (MOCK)",
    )

    plan_x, plan_y, plan_w, plan_h = 0.9 * inch, 2.0 * inch, 6.9 * inch, 7.5 * inch
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.rect(plan_x, plan_y, plan_w, plan_h, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(plan_x, plan_y + plan_h + 0.15 * inch, "GARAGE PARKING LAYOUT (mock)")

    # Stalls
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    stall_w, stall_h = 0.55 * inch, 1.15 * inch
    start_x = plan_x + 0.35 * inch
    banks = [plan_y + 0.35 * inch, plan_y + plan_h - (stall_h + 0.55 * inch)]
    for row_idx, base_y in enumerate(banks):
        for i in range(11):
            x = start_x + i * (stall_w + 0.06 * inch)
            c.rect(x, base_y, stall_w, stall_h, stroke=1, fill=0)
            c.setFont("Helvetica", 6)
            c.setFillColor(colors.grey)
            stall_num = (1 + i) if row_idx == 0 else (20 + i)
            c.drawString(x + 0.03 * inch, base_y + 0.05 * inch, f"P{stall_num:02d}")
            c.setFillColor(colors.black)

    # Proposed EVSE stalls (mock): highlight 8 locations
    ev_stalls = ["P04", "P05", "P06", "P07", "P22", "P23", "P24", "P25"]
    c.setStrokeColor(colors.green)
    c.setLineWidth(2.2)
    for stall in ev_stalls:
        # map stall label to rectangle
        num = int(stall[1:])
        row_idx = 0 if num < 20 else 1
        i = (num - 1) if row_idx == 0 else (num - 20)
        x = start_x + i * (stall_w + 0.06 * inch)
        y = banks[row_idx]
        c.rect(x, y, stall_w, stall_h, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.green)
        c.drawCentredString(x + stall_w / 2, y + stall_h + 0.06 * inch, "EV")
        c.setFillColor(colors.black)

    # Notes box
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(plan_x + plan_w - 2.4 * inch, plan_y + 0.35 * inch, 2.2 * inch, 1.55 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(plan_x + plan_w - 2.3 * inch, plan_y + 1.70 * inch, "NOTES (mock)")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(plan_x + plan_w - 2.3 * inch, plan_y + 1.42 * inch, "Green outline = proposed EV stalls")
    c.drawString(plan_x + plan_w - 2.3 * inch, plan_y + 1.22 * inch, "Exact EVSE offsets by installer")
    c.drawString(plan_x + plan_w - 2.3 * inch, plan_y + 1.02 * inch, "No routing/constructability")
    c.setFillColor(colors.black)

    north_arrow(c, plan_x + plan_w - 0.45 * inch, plan_y + plan_h - 1.05 * inch)
    scale_bar(c, plan_x + plan_w - 3.2 * inch, plan_y + plan_h - 0.65 * inch)
    title_block(c, sheet="P3-PARK", sheet_title="Parking Layout (Owner Provided)", rev="0", date="2026-01-20", issued_for="REFERENCE")

    c.showPage()
    c.save()


def write_routing_assumptions_input(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "Routing Assumptions Memo — Installer Provided (Mock)",
        path.name,
        1,
        subtitle="Input to P3.3 details sheet (electrical-impacting assumptions only)  |  Date: 2026-01-20",
        banner="EV Charging Site Project — Phase 3 Inputs (MOCK)",
    )

    c.setFont("Helvetica", 10)
    y = 9.6 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This memo records routing and site-condition assumptions that affect electrical design outputs (e.g., voltage drop basis, assumed feeder length, transition points). It does not specify construction means-and-methods.",
        7.0 * inch,
    )
    y -= 0.2 * inch

    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Assumptions (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Assumed electrical path length MDP → EVSP-1: 165 ft (basis for voltage drop and impedance).",
        "Wiring method basis: raceway system, indoors/garage environment (CEC/NEC compliant).",
        "Assume no core drilling through rated walls without separate approvals (constraint only).",
        "Assume existing spare 3-pole spaces in MDP are available for EV feeder breaker (verify).",
        "Assume EVSE pedestals/wall mounts located per owner parking layout (P3-PARK) with field offsets.",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Design impacts (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Voltage drop check uses 165 ft basis; final field measurement may adjust conductor sizing.",
        "Feeder routing transition points labeled for clarity on drawings (no trenching/civil scope).",
        "Separation requirements noted for power vs communications cabling (if any).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    # Attach a couple site photos as “supporting context”
    watermark_pdf(c)
    header_footer(
        c,
        "Routing Assumptions Memo — Photo Context (Mock)",
        path.name,
        2,
        subtitle="Representative site context images (mock) used to inform constraints",
        banner="EV Charging Site Project — Phase 3 Inputs (MOCK)",
    )
    y0 = 9.4 * inch
    for idx, img_path in enumerate(SITE_SRC[:2]):
        pil = Image.open(str(img_path)).convert("RGB")
        max_w, max_h = 3.25 * inch, 4.6 * inch
        w, h = pil.size
        scale = min(max_w / w, max_h / h)
        tw, th = int(w * scale), int(h * scale)
        pil = pil.resize((tw, th))
        buf = io.BytesIO()
        pil.save(buf, format="PNG")
        buf.seek(0)
        x = 0.75 * inch + idx * (3.55 * inch)
        c.drawImage(ImageReader(buf), x, 4.2 * inch, width=tw, height=th)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, 4.05 * inch, f"Photo context {idx+1} (mock)")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: Photos are illustrative mock assets; replace with project field photos.")
    c.setFillColor(colors.black)
    c.showPage()

    c.save()


def write_p3_1_one_line(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(c, "E-001 — One-Line Diagram (Preliminary, Unstamped) (Mock)", path.name, 1, subtitle="P3.1", banner="EV Charging Site Project — Phase 3 Outputs (MOCK)")

    # Simple one-line layout
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, 9.85 * inch, "ONE-LINE DIAGRAM (mock)")

    # Nodes positions
    x0 = 1.3 * inch
    y0 = 8.6 * inch
    gap = 1.7 * inch

    def node(x: float, y: float, label: str, sub: str) -> None:
        c.setStrokeColor(colors.black)
        c.setLineWidth(1.5)
        c.rect(x, y, 1.6 * inch, 0.75 * inch, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 0.8 * inch, y + 0.46 * inch, label)
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawCentredString(x + 0.8 * inch, y + 0.22 * inch, sub)
        c.setFillColor(colors.black)

    # Source, MDP, feeder, EVSP-1, EVSE branch
    node(x0, y0, "UTILITY XFMR", "120/208V (mock)")
    node(x0 + gap, y0, "MDP", "800A, 208Y/120V (mock)")
    node(x0 + 2 * gap, y0, "EV FEEDER OCPD", "350A, 3P (mock)")
    node(x0 + 3 * gap, y0, "EVSP-1", "400A bus (mock)")

    # Connections
    c.setLineWidth(2)
    c.line(x0 + 1.6 * inch, y0 + 0.37 * inch, x0 + gap, y0 + 0.37 * inch)
    c.line(x0 + gap + 1.6 * inch, y0 + 0.37 * inch, x0 + 2 * gap, y0 + 0.37 * inch)
    c.line(x0 + 2 * gap + 1.6 * inch, y0 + 0.37 * inch, x0 + 3 * gap, y0 + 0.37 * inch)

    # Branch circuits block
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.5)
    c.rect(x0 + 3 * gap, 6.9 * inch, 1.6 * inch, 0.75 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x0 + 3 * gap + 0.8 * inch, 7.36 * inch, "EVSE BRANCHES")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(x0 + 3 * gap + 0.8 * inch, 7.12 * inch, "8x (40A) (mock)")
    c.setFillColor(colors.black)
    c.setLineWidth(2)
    c.line(x0 + 3 * gap + 0.8 * inch, y0, x0 + 3 * gap + 0.8 * inch, 7.65 * inch)

    # EMS bubble
    c.setStrokeColor(colors.darkgreen)
    c.setLineWidth(2)
    c.circle(6.5 * inch, 6.9 * inch, 0.55 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.darkgreen)
    c.drawCentredString(6.5 * inch, 6.95 * inch, "EMS")
    c.setFont("Helvetica", 8)
    c.drawCentredString(6.5 * inch, 6.75 * inch, "cap 250A")
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.darkgreen)
    c.setLineWidth(1.5)
    c.line(6.0 * inch, 7.1 * inch, x0 + 3 * gap + 1.6 * inch, 7.1 * inch)

    # Notes
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, 5.9 * inch, "NOTES (mock):")
    c.setFont("Helvetica", 9)
    notes = [
        "1. Existing service basis: 800A, 208Y/120V, 3Ø (verify in Phase 1 evidence).",
        "2. EVSE loads treated as continuous; branch OCPD basis 40A per 32A continuous (mock).",
        "3. EMS/load management shown to cap aggregate EV demand to ≤250A (mock basis).",
        "4. Final conductor sizing, AIC, and coordination to be confirmed in stamped set.",
    ]
    y = 5.65 * inch
    for n in notes:
        c.drawString(0.9 * inch, y, n)
        y -= 0.22 * inch

    title_block(c, sheet="E-001", sheet_title="One-Line Diagram (Preliminary)", rev="0", date="2026-01-26", issued_for="UNSTAMPED")
    c.showPage()
    c.save()


def write_p3_2_site_plan(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(c, "E-002 — Site Plan with EVSE Locations (Preliminary) (Mock)", path.name, 1, subtitle="P3.2", banner="EV Charging Site Project — Phase 3 Outputs (MOCK)")

    plan_x, plan_y, plan_w, plan_h = 0.9 * inch, 2.0 * inch, 6.9 * inch, 7.5 * inch
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.rect(plan_x, plan_y, plan_w, plan_h, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(plan_x, plan_y + plan_h + 0.15 * inch, "GARAGE PLAN — EVSE LOCATION OVERLAY (mock)")

    # Basic aisle + stall grid
    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(0.6)
    for i in range(1, 8):
        gx = plan_x + i * (plan_w / 8)
        c.line(gx, plan_y, gx, plan_y + plan_h)
    for j in range(1, 10):
        gy = plan_y + j * (plan_h / 10)
        c.line(plan_x, gy, plan_x + plan_w, gy)

    # EVSE markers (8)
    ev_labels = [f"EVSE-{i:02d}" for i in range(1, 9)]
    c.setFillColor(colors.darkblue)
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(1.5)
    pts = [
        (plan_x + 1.3 * inch, plan_y + 0.9 * inch),
        (plan_x + 2.0 * inch, plan_y + 0.9 * inch),
        (plan_x + 2.7 * inch, plan_y + 0.9 * inch),
        (plan_x + 3.4 * inch, plan_y + 0.9 * inch),
        (plan_x + 4.2 * inch, plan_y + 6.2 * inch),
        (plan_x + 4.9 * inch, plan_y + 6.2 * inch),
        (plan_x + 5.6 * inch, plan_y + 6.2 * inch),
        (plan_x + 6.3 * inch, plan_y + 6.2 * inch),
    ]
    c.setFont("Helvetica-Bold", 8)
    for (x, y), lab in zip(pts, ev_labels):
        c.circle(x, y, 0.12 * inch, stroke=1, fill=0)
        c.drawString(x + 0.16 * inch, y - 0.04 * inch, lab)
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)

    # Equipment locations: MDP room + EVSP-1
    c.setStrokeColor(colors.blue)
    c.setLineWidth(2.2)
    c.rect(plan_x + 0.25 * inch, plan_y + plan_h - 1.25 * inch, 2.25 * inch, 0.95 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.blue)
    c.drawString(plan_x + 0.35 * inch, plan_y + plan_h - 0.85 * inch, "ELECTRICAL ROOM (ref)")
    c.setFillColor(colors.black)

    c.setStrokeColor(colors.darkred)
    c.setLineWidth(2)
    c.rect(plan_x + 0.55 * inch, plan_y + plan_h - 2.55 * inch, 1.4 * inch, 0.55 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.darkred)
    c.drawString(plan_x + 0.62 * inch, plan_y + plan_h - 2.28 * inch, "EVSP-1 (ref)")
    c.setFillColor(colors.black)

    # Notes box
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(plan_x + plan_w - 2.55 * inch, plan_y + 0.35 * inch, 2.35 * inch, 1.8 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(plan_x + plan_w - 2.45 * inch, plan_y + 2.0 * inch, "NOTES (mock)")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    for i, line in enumerate(
        [
            "EVSE locations per P3-PARK (owner)",
            "EVSP-1 location ref only",
            "No civil routing specified",
            "Use for plan-check clarity",
        ]
    ):
        c.drawString(plan_x + plan_w - 2.45 * inch, plan_y + 1.72 * inch - i * 0.2 * inch, f"- {line}")
    c.setFillColor(colors.black)

    north_arrow(c, plan_x + plan_w - 0.45 * inch, plan_y + plan_h - 1.05 * inch)
    scale_bar(c, plan_x + plan_w - 3.2 * inch, plan_y + plan_h - 0.65 * inch)
    title_block(c, sheet="E-002", sheet_title="Site Plan — EVSE Locations", rev="0", date="2026-01-26", issued_for="UNSTAMPED")
    c.showPage()
    c.save()


def write_p3_3_details(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(c, "E-003 — Conduit & Trenching Details (Electrical-Impacting) (Mock)", path.name, 1, subtitle="P3.3", banner="EV Charging Site Project — Phase 3 Outputs (MOCK)")

    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This sheet documents electrical-impacting routing assumptions, transition points, and typical details. It is not a civil/constructability plan.",
        7.0 * inch,
    )
    y -= 0.2 * inch

    # Detail blocks
    def detail_box(x: float, y: float, w: float, h: float, title: str) -> None:
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.rect(x, y, w, h, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 0.1 * inch, y + h - 0.25 * inch, title)

    detail_box(0.75 * inch, 6.2 * inch, 3.4 * inch, 3.0 * inch, "DETAIL 1 — Feeder Path (mock)")
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(2)
    c.line(1.0 * inch, 7.7 * inch, 3.9 * inch, 7.7 * inch)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(1.0 * inch, 7.45 * inch, "MDP → EVSP-1 assumed path length: 165 ft (basis)")
    c.setFillColor(colors.black)

    detail_box(4.35 * inch, 6.2 * inch, 3.4 * inch, 3.0 * inch, "DETAIL 2 — Typical Raceway Notes (mock)")
    c.setFont("Helvetica", 8)
    y2 = 8.8 * inch
    for line in [
        "Raceway sized per NEC/CEC Chapter 9 (mock).",
        "Parallel conductors permitted as designed (mock).",
        "Provide EGC with feeder conductors.",
        "Maintain separation from comms wiring (as applicable).",
    ]:
        c.drawString(4.45 * inch, y2, f"- {line}")
        y2 -= 0.2 * inch

    detail_box(0.75 * inch, 2.2 * inch, 3.4 * inch, 3.7 * inch, "DETAIL 3 — EVSE Branch Typical (mock)")
    c.setFont("Helvetica", 8)
    y3 = 5.6 * inch
    for line in [
        "Branch: 40A OCPD for 32A continuous (mock basis).",
        "Conductor sizing per terminal temp rating + derating.",
        "Provide disconnecting means as required by code/AHJ.",
        "Label EVSE circuit ID at equipment and panel.",
    ]:
        c.drawString(0.85 * inch, y3, f"- {line}")
        y3 -= 0.2 * inch

    detail_box(4.35 * inch, 2.2 * inch, 3.4 * inch, 3.7 * inch, "DETAIL 4 — Grounding/Bonding Intent (mock)")
    c.setFont("Helvetica", 8)
    y4 = 5.6 * inch
    for line in [
        "Bond raceways where required (mock).",
        "EGC sized per code basis (final by EOR).",
        "Panel ground bars bonded to GES (reference).",
        "Provide bonding jumpers at transitions.",
    ]:
        c.drawString(4.45 * inch, y4, f"- {line}")
        y4 -= 0.2 * inch

    title_block(c, sheet="E-003", sheet_title="Conduit & Trenching Details (Electrical-Impacting)", rev="0", date="2026-01-26", issued_for="UNSTAMPED")
    c.showPage()
    c.save()


def write_p3_4_schedules(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(c, "E-004 — Updated Panel Schedules (MDP + EVSP-1) (Mock)", path.name, 1, subtitle="P3.4", banner="EV Charging Site Project — Phase 3 Outputs (MOCK)")

    def table(x: float, y: float, title: str, rows: list[tuple[str, str, str, str]]) -> None:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, title)
        y -= 0.22 * inch
        c.setFont("Helvetica-Bold", 8)
        headers = [("Slot", x), ("Breaker", x + 0.7 * inch), ("Load", x + 2.0 * inch), ("Notes", x + 4.2 * inch)]
        for h, hx in headers:
            c.drawString(hx, y, h)
        y -= 0.12 * inch
        c.setStrokeColor(colors.grey)
        c.line(x, y, x + 7.0 * inch, y)
        y -= 0.18 * inch
        c.setFont("Helvetica", 8)
        for slot, brk, load, note in rows:
            c.drawString(x, y, slot)
            c.drawString(x + 0.7 * inch, y, brk)
            c.drawString(x + 2.0 * inch, y, load[:30])
            c.drawString(x + 4.2 * inch, y, note[:30])
            y -= 0.18 * inch

    mdp_rows = [
        ("40/42/44", "350A 3P", "EVSP-1 feeder", "Managed to 250A (mock)"),
        ("17", "200A 3P", "SUBP-1", "Existing"),
        ("57", "Spare", "Spare/Space", "Available 3-pole"),
    ]
    evsp_rows = [(f"{i}", "40A 3P", f"EVSE-{i:02d}", "32A cont (mock)") for i in range(1, 9)]

    table(0.75 * inch, 9.65 * inch, "MDP — Updated (excerpt) (mock)", mdp_rows)
    table(0.75 * inch, 6.85 * inch, "EVSP-1 — New (excerpt) (mock)", evsp_rows)

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.9 * inch, "NOTE: schedules are mock excerpts; full schedules included per P1 evidence in real project.")
    c.setFillColor(colors.black)

    title_block(c, sheet="E-004", sheet_title="Panel Schedules (MDP + EVSP-1)", rev="0", date="2026-01-26", issued_for="UNSTAMPED")
    c.showPage()
    c.save()


def write_p3_5_notes(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(c, "E-005 — Electrical Notes & Code Sheet (Mock)", path.name, 1, subtitle="P3.5", banner="EV Charging Site Project — Phase 3 Outputs (MOCK)")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75 * inch, 9.65 * inch, "GENERAL NOTES (electrical-only, mock)")
    c.setFont("Helvetica", 9)
    y = 9.35 * inch
    notes = [
        "1. Applicable code basis: 2022 California Electrical Code (CEC) (mock). Verify AHJ amendments.",
        "2. EVSE loads treated as continuous; size OCPD and conductors accordingly (125% basis).",
        "3. EMS/load management (if used) shall be listed and configured to enforce aggregate cap (mock: 250A).",
        "4. Provide identification labeling for EV equipment and circuits; coordinate with panel schedules.",
        "5. Provide grounding and bonding per code; bond raceways as required.",
        "6. Verify available fault current and minimum AIC ratings in final stamped set.",
    ]
    for n in notes:
        c.drawString(0.85 * inch, y, n)
        y -= 0.22 * inch

    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75 * inch, y - 0.1 * inch, "SYMBOLS / LEGEND (mock)")
    y -= 0.4 * inch
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.5)
    c.circle(0.95 * inch, y, 0.12 * inch, stroke=1, fill=0)
    c.setFont("Helvetica", 9)
    c.drawString(1.2 * inch, y - 0.05 * inch, "EVSE location marker")
    y -= 0.35 * inch
    c.setStrokeColor(colors.darkgreen)
    c.circle(0.95 * inch, y, 0.12 * inch, stroke=1, fill=0)
    c.setFillColor(colors.darkgreen)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1.2 * inch, y - 0.05 * inch, "EMS / Load management annotation")
    c.setFillColor(colors.black)

    title_block(c, sheet="E-005", sheet_title="Electrical Notes & Code Sheet", rev="0", date="2026-01-26", issued_for="UNSTAMPED")
    c.showPage()
    c.save()


def merge_pdfs(out_path: Path, inputs: list[Path]) -> None:
    merger = PdfMerger()
    for p in inputs:
        merger.append(str(p))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    merger.write(str(out_path))
    merger.close()


def write_p3_6_compiled_set(path: Path, component_paths: list[Path]) -> None:
    # Build a cover page, then merge cover + sheets.
    cover = P3_OUTPUTS / "_tmp_P3.6_cover.pdf"
    c = canvas.Canvas(str(cover), pagesize=letter)
    watermark_pdf(c)
    header_footer(c, "Permit Drawing Set — Unstamped (Compiled) (Mock)", cover.name, 1, subtitle="P3.6", banner="EV Charging Site Project — Phase 3 Outputs (MOCK)")
    c.setFont("Helvetica", 10)
    y = 9.6 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This file represents the compiled unstamped electrical permit drawing set assembled from P3.1–P3.5. In a real project this compilation is performed under document control with sheet indexing and QA logs.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Included sheets (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for p in component_paths:
        c.drawString(1.0 * inch, y, f"- {p.name}")
        y -= 0.22 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: This compilation is a mock artifact; replace with real CAD/PDF exports and stamps.")
    c.setFillColor(colors.black)
    c.showPage()
    c.save()

    merge_pdfs(path, [cover] + component_paths)
    try:
        cover.unlink()
    except OSError:
        pass


def main() -> None:
    ensure_dirs()

    # Inputs (per Addendum A)
    p3_park = P3_INPUTS / "P3-PARK_ParkingLayout_OwnerProvided_2026-01-20.pdf"
    p3_i03 = P3_INPUTS / "P3-I03_RoutingAssumptions_InstallerMemo_2026-01-20.pdf"
    write_parking_layout_input(p3_park)
    write_routing_assumptions_input(p3_i03)

    # Outputs (per Addendum A)
    p3_1 = P3_OUTPUTS / "P3.1_OneLine_Prelim_Unstamped_2026-01-26.pdf"
    p3_2 = P3_OUTPUTS / "P3.2_SitePlan_EVSE_Locations_Prelim_2026-01-26.pdf"
    p3_3 = P3_OUTPUTS / "P3.3_Conduit_Trenching_Details_ElectricalImpacting_2026-01-26.pdf"
    p3_4 = P3_OUTPUTS / "P3.4_PanelSchedules_Updated_MDP_and_EVSP_2026-01-26.pdf"
    p3_5 = P3_OUTPUTS / "P3.5_ElectricalNotes_CodeSheets_2026-01-26.pdf"
    p3_6 = P3_OUTPUTS / "P3.6_PermitSet_Unstamped_2026-01-26.pdf"

    write_p3_1_one_line(p3_1)
    write_p3_2_site_plan(p3_2)
    write_p3_3_details(p3_3)
    write_p3_4_schedules(p3_4)
    write_p3_5_notes(p3_5)
    write_p3_6_compiled_set(p3_6, [p3_1, p3_2, p3_3, p3_4, p3_5])

    print("Generated Phase 3 package:")
    for f in [p3_park, p3_i03, p3_1, p3_2, p3_3, p3_4, p3_5, p3_6]:
        print(" -", f.relative_to(ROOT))


if __name__ == "__main__":
    main()

