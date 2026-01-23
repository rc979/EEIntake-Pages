import io
import zipfile
from datetime import datetime
from pathlib import Path

# Dependencies:
#   python3 -m pip install --user reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path.cwd()
P2_INPUTS = ROOT / "P2" / "Inputs"
P2_OUTPUTS = ROOT / "P2" / "Outputs"


def ensure_dirs() -> None:
    P2_INPUTS.mkdir(parents=True, exist_ok=True)
    P2_OUTPUTS.mkdir(parents=True, exist_ok=True)


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
    banner: str = "EV Charging Site Project — Phase 2 (MOCK)",
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


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def write_minimal_xlsx(path: Path) -> None:
    """
    Write a small, standards-compliant .xlsx without external deps.
    We keep it simple: 3 sheets, inline strings + numbers, no styling beyond defaults.
    """
    # Three sheets of data (rows are lists of values)
    inputs_rows = [
        ["Phase 2 Load Calc Workbook (MOCK)", "", "", ""],
        ["Project", "EV Charging Site Project", "", ""],
        ["Site", "Place (Palo Alto, CA) (mock)", "", ""],
        ["Code basis (mock)", "2022 CEC; NEC concepts referenced (mock)", "", ""],
        ["EVSE model (basis)", "ElectriCharge L2-7.6-G (revA)", "", ""],
        ["EVSE ports", 8, "", ""],
        ["EVSE continuous current per port (A)", 32, "", ""],
        ["Continuous load factor", 1.25, "", ""],
        ["Unmanaged EV feeder current (A)", 320, "", "8 * (32 * 1.25)"],
        ["Service headroom (A) (from screening)", 250, "", "From Phase 0 screening (mock)"],
        ["Decision constraint", "Avoid service upgrade unless unavoidable", "", ""],
    ]
    calc_rows = [
        ["Load Calc (mock excerpt)", "", "", ""],
        ["Item", "Value", "Units", "Notes"],
        ["Ports", 8, "ea", "Program intent basis"],
        ["I_cont per port", 32, "A", "From EVSE cut sheet (revA, mock)"],
        ["Continuous factor", 1.25, "-", "Per continuous-load treatment (mock)"],
        ["I_design per port", 40, "A", "32 * 1.25"],
        ["I_unmanaged total", 320, "A", "8 * 40"],
        ["Headroom available", 250, "A", "Service utilization basis (mock)"],
        ["Deficit (unmanaged)", -70, "A", "250 - 320"],
        ["Managed cap target", 250, "A", "EMS setpoint basis (mock)"],
        ["Feeder OCPD (selected)", 350, "A", "Mock selection"],
        ["EV subpanel bus (selected)", 400, "A", "Mock selection"],
    ]
    summary_rows = [
        ["Summary (mock)", "", ""],
        ["Outcome", "Unmanaged exceeds headroom; EMS required", ""],
        ["Key numbers", "", ""],
        ["Unmanaged EV current", "320 A", "8 ports @ 32A cont, 125%"],
        ["Headroom basis", "250 A", "screening (mock)"],
        ["Required measure", "Listed EMS to cap ≤250A", "architecture decision input"],
        ["Downstream use", "P3 one-line, notes, schedules; P6 utility letter", ""],
    ]

    def sheet_xml(rows: list[list[object]]) -> str:
        # Convert to basic Office Open XML worksheet with inline strings.
        # Column width defaults; each row uses r="1..n".
        lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
            "<sheetData>",
        ]
        for r_idx, row in enumerate(rows, start=1):
            lines.append(f'<row r="{r_idx}">')
            for c_idx, v in enumerate(row, start=1):
                col = ""
                n = c_idx
                while n:
                    n, rem = divmod(n - 1, 26)
                    col = chr(65 + rem) + col
                cell_ref = f"{col}{r_idx}"
                if v is None or v == "":
                    continue
                if isinstance(v, (int, float)):
                    lines.append(f'<c r="{cell_ref}"><v>{v}</v></c>')
                else:
                    s = _xml_escape(str(v))
                    lines.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{s}</t></is></c>')
            lines.append("</row>")
        lines.append("</sheetData></worksheet>")
        return "\n".join(lines)

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"""
    workbook = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Inputs" sheetId="1" r:id="rId1"/>
    <sheet name="LoadCalc" sheetId="2" r:id="rId2"/>
    <sheet name="Summary" sheetId="3" r:id="rId3"/>
  </sheets>
</workbook>
"""
    workbook_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
</Relationships>
"""

    with zipfile.ZipFile(str(path), "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml(inputs_rows))
        z.writestr("xl/worksheets/sheet2.xml", sheet_xml(calc_rows))
        z.writestr("xl/worksheets/sheet3.xml", sheet_xml(summary_rows))


def write_ems_brief(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "EMS Technical Brief (revB) — Load Management for EVSE (Mock)",
        path.name,
        1,
        subtitle="Vendor brief (mock)  |  Rev: B  |  Date: 2026-01-21",
        banner="EV Charging Site Project — Phase 2 Inputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This document is a mock technical brief for a listed Energy Management System (EMS) used to cap aggregate EV charging demand. Replace with actual vendor documentation and listing evidence.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Key capabilities (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Aggregate current cap setpoint (mock): 250A at EV feeder.",
        "Per-port load allocation across up to 16 ports (mock).",
        "Fail-safe behavior: on comms loss, enforce conservative cap (mock).",
        "Listed to applicable standards (mock listing placeholders).",
        "Provides configuration export for as-built documentation (Phase 7).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Integration points (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Measures feeder current via CTs at EVSP-1 feeder (monitoring point).",
        "Controls EVSE output via network interface (OCPP) or hardwired control (mock).",
        "Setpoint documented on one-line and notes sheet (Phase 3).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    c.showPage()

    watermark_pdf(c)
    header_footer(
        c,
        "EMS Technical Brief (revB) — Configuration + Compliance Notes (Mock)",
        path.name,
        2,
        subtitle="Appendix: configuration fields (mock)",
        banner="EV Charging Site Project — Phase 2 Inputs (MOCK)",
    )
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, 9.65 * inch, "Configuration fields (mock):")
    c.setFont("Helvetica", 9)
    y = 9.35 * inch
    for k, v in [
        ("Project ID", "EV-PA-001 (mock)"),
        ("Cap setpoint", "250A"),
        ("Monitoring point", "EV feeder at MDP/EVSP-1"),
        ("Fail-safe mode", "Cap enforced on fault"),
        ("Export format", "PDF + JSON (mock)"),
    ]:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.85 * inch, y, f"{k}:")
        c.setFont("Helvetica", 9)
        c.drawString(2.5 * inch, y, v)
        y -= 0.22 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: This is a generated mock EMS brief for documentation realism only.")
    c.setFillColor(colors.black)
    c.showPage()
    c.save()


def write_loadcalc_summary(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "P2.1 Load Calculation Summary (Mock)",
        path.name,
        1,
        subtitle="Prepared: 2026-01-22 (v1.0)  |  Basis: Phase 1 evidence pointers (mock)",
        banner="EV Charging Site Project — Phase 2 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This summary captures the key results of the Phase 2 load calculation. Replace with an Engineer-of-Record signed calculation and jurisdiction-specific methodology where required.",
        7.0 * inch,
    )
    y -= 0.15 * inch

    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Inputs (by evidence pointer, mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Panel schedules: phases/P1/Inputs/P1-I02_PanelSchedules_MDP_and_Subpanels_2026-01-16.pdf",
        "EVSE cut sheet: phases/P1/Inputs/P1-I04_EVSE_CutSheet_ElectriCharge_L2-7.6-G_revA.pdf",
        "AHJ/code basis: phases/P1/Inputs/P1-I05_AHJ_Electrical_Permitting_CodeBasis_2026-01-17.pdf",
        "EMS brief: phases/P2/Inputs/P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Key calculation results (mock):")
    y -= 0.26 * inch

    # Small table
    rows = [
        ("Ports", "8"),
        ("EVSE continuous current / port", "32A"),
        ("Continuous factor", "125%"),
        ("Design current / port", "40A"),
        ("Total unmanaged EV current", "320A"),
        ("Headroom basis (screening)", "250A"),
        ("Result", "Unmanaged exceeds headroom by 70A → EMS required"),
    ]
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.75 * inch, y, "Parameter")
    c.drawString(3.7 * inch, y, "Value")
    y -= 0.12 * inch
    c.setStrokeColor(colors.grey)
    c.line(0.75 * inch, y, 7.75 * inch, y)
    y -= 0.18 * inch
    c.setFont("Helvetica", 9)
    for k, v in rows:
        c.drawString(0.75 * inch, y, k)
        c.drawString(3.7 * inch, y, v)
        y -= 0.18 * inch

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: Mock summary only; final engineering must be stamped where required.")
    c.setFillColor(colors.black)
    c.showPage()
    c.save()


def write_loadcalc_check_memo(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "P2.1 Independent Load Calc Check Memo (Mock)",
        path.name,
        1,
        subtitle="Checker: Alex Kim, EE (mock)  |  Date: 2026-01-22",
        banner="EV Charging Site Project — Phase 2 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This memo documents an independent check of the Phase 2 load calculation workbook and summary. Replace with actual review sign-off and attachments.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Check scope (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Arithmetic check: unmanaged EV load and continuous factor application.",
        "Input traceability: evidence pointers match Phase 1 package.",
        "Logic check: architecture conclusion follows from headroom deficit.",
        "Red flags: confirm AHJ accepted method for managed EV loads (when applicable).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Outcome (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    y = draw_wrapped(
        c,
        1.0 * inch,
        y,
        "Calculation logic and arithmetic verified; inputs align to Phase 1 evidence pointers; conclusion supported: unmanaged EV current (320A) exceeds headroom basis (250A), therefore a listed EMS cap (≤250A) is required to avoid service upgrade.",
        6.75 * inch,
    )
    c.setFont("Helvetica", 9)
    c.drawString(0.75 * inch, 2.0 * inch, "Signature (mock): _______________________   Date: 2026-01-22")
    c.showPage()
    c.save()


def write_architecture_decision_record(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "P2.2 Architecture Decision Record (Mock)",
        path.name,
        1,
        subtitle="Prepared: 2026-01-22 (v1.0)  |  Decision: Managed-load architecture",
        banner="EV Charging Site Project — Phase 2 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This record documents the selected EV electrical architecture based on the Phase 2 load calculation and Phase 1 site constraints. Replace with an Engineer-of-Record signed decision where required.",
        7.0 * inch,
    )
    y -= 0.15 * inch

    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Decision drivers (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Project constraint: avoid service upgrade unless unavoidable.",
        "Unmanaged EV load (320A) exceeds headroom basis (250A).",
        "Maintain 8-port scope without reducing EVSE count.",
        "Adopt listed EMS/load management to cap aggregate EV demand.",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Selected architecture (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "New EV subpanel: EVSP-1, 400A bus (mock).",
        "Feeder OCPD: 350A, 3-pole (mock).",
        "Branch circuits: (8) 40A OCPD for EVSE-01..EVSE-08 (mock).",
        "EMS: cap aggregate EV demand to ≤250A (setpoint documented on drawings).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    y -= 0.05 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Downstream impacts (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "P3.1 one-line must depict EMS and cap logic; include fail-safe note placeholder.",
        "P3.4 schedules must reflect EVSP-1 and branch circuit IDs.",
        "P6 utility package should include EMS brief and cap statement.",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: Mock decision record; replace with signed EOR memo and attachments.")
    c.setFillColor(colors.black)
    c.showPage()
    c.save()


def main() -> None:
    ensure_dirs()

    # Inputs (per Addendum A)
    ems = P2_INPUTS / "P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf"
    write_ems_brief(ems)

    # Outputs (per Addendum A)
    wb = P2_OUTPUTS / "P2.1_LoadCalc_Workbook_2026-01-22.xlsx"
    summary = P2_OUTPUTS / "P2.1_LoadCalc_Summary_2026-01-22.pdf"
    check = P2_OUTPUTS / "P2.1_LoadCalc_CheckMemo_2026-01-22.pdf"
    adr = P2_OUTPUTS / "P2.2_Architecture_Decision_Record_2026-01-22.pdf"

    write_minimal_xlsx(wb)
    write_loadcalc_summary(summary)
    write_loadcalc_check_memo(check)
    write_architecture_decision_record(adr)

    print("Generated Phase 2 package:")
    for f in [ems, wb, summary, check, adr]:
        print(" -", f.relative_to(ROOT))


if __name__ == "__main__":
    main()

