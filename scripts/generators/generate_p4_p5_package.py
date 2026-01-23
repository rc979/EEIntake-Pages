import zipfile
from datetime import datetime
from pathlib import Path

# Dependencies:
#   python3 -m pip install --user reportlab PyPDF2
from PyPDF2 import PdfMerger
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path.cwd()

P3_OUTPUTS = ROOT / "P3" / "Outputs"
P4_INPUTS = ROOT / "P4" / "Inputs"
P4_OUTPUTS = ROOT / "P4" / "Outputs"
P5_INPUTS = ROOT / "P5" / "Inputs"
P5_OUTPUTS = ROOT / "P5" / "Outputs"


def ensure_dirs() -> None:
    for p in [P4_INPUTS, P4_OUTPUTS, P5_INPUTS, P5_OUTPUTS]:
        p.mkdir(parents=True, exist_ok=True)


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
    banner: str = "EV Charging Site Project (MOCK)",
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


def merge_pdfs(out_path: Path, inputs: list[Path]) -> None:
    merger = PdfMerger()
    for p in inputs:
        merger.append(str(p))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    merger.write(str(out_path))
    merger.close()


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def write_minimal_xlsx(path: Path, sheets: list[tuple[str, list[list[object]]]]) -> None:
    """
    Write a small .xlsx without external deps.
    sheets: list of (sheet_name, rows).
    """
    def sheet_xml(rows: list[list[object]]) -> str:
        lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
            "<sheetData>",
        ]
        for r_idx, row in enumerate(rows, start=1):
            lines.append(f'<row r="{r_idx}">')
            for c_idx, v in enumerate(row, start=1):
                # convert c_idx -> column letters
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

    # content types
    ct = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '  <Default Extension="xml" ContentType="application/xml"/>',
        '  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
    ]
    for i in range(1, len(sheets) + 1):
        ct.append(
            f'  <Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    ct.append("</Types>\n")
    content_types = "\n".join(ct)

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"""

    # workbook + relationships
    wb_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
        "  <sheets>",
    ]
    wb_rels_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for i, (name, _) in enumerate(sheets, start=1):
        wb_lines.append(f'    <sheet name="{_xml_escape(name)}" sheetId="{i}" r:id="rId{i}"/>')
        wb_rels_lines.append(
            f'  <Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        )
    wb_lines.extend(["  </sheets>", "</workbook>\n"])
    wb_rels_lines.append("</Relationships>\n")

    with zipfile.ZipFile(str(path), "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", "\n".join(wb_lines))
        z.writestr("xl/_rels/workbook.xml.rels", "\n".join(wb_rels_lines))
        for i, (_, rows) in enumerate(sheets, start=1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(rows))


# -------------------------
# Phase 4 (P4)
# -------------------------


def write_p4_eor_review_notes(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "EOR Review Notes (Mock)",
        path.name,
        1,
        subtitle="Input to stamping issuance  |  Date: 2026-01-28",
        banner="EV Charging Site Project — Phase 4 Inputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This memo represents mock Engineer-of-Record (EOR) review notes prior to issuing the stamped permit set. Replace with actual EOR markups and sign-off.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Notes (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Confirm EMS cap note and fail-safe statement included on one-line.",
        "Verify nomenclature EVSP-1 consistent across sheets.",
        "Ensure code notes reference adopted code edition (CEC 2022) and EVSE continuous load treatment.",
        "Administrative: add stamp block on cover sheet; include project address.",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch
    c.setFont("Helvetica", 9)
    c.drawString(0.75 * inch, 2.0 * inch, "Signature (mock): _______________________   Date: 2026-01-28")
    c.showPage()
    c.save()


def write_p4_stamped_set(path: Path, base_unstamped: Path) -> None:
    # Create a stamp cover page then merge with P3.6.
    cover = P4_OUTPUTS / "_tmp_P4.1_stamp_cover.pdf"
    c = canvas.Canvas(str(cover), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "Stamped Permit Drawings (Mock)",
        cover.name,
        1,
        subtitle="P4.1  |  Stamp date: 2026-01-29  |  Engineer-of-Record: Priya Shah, PE (mock)",
        banner="EV Charging Site Project — Phase 4 Outputs (MOCK)",
    )
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, 9.65 * inch, "STAMP BLOCK (mock)")
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(0.75 * inch, 6.8 * inch, 3.2 * inch, 2.6 * inch, stroke=1, fill=0)
    c.setFont("Helvetica", 10)
    c.drawString(0.9 * inch, 9.05 * inch, "Priya Shah, PE (mock)")
    c.drawString(0.9 * inch, 8.85 * inch, "CA PE ###### (mock)")
    c.drawString(0.9 * inch, 8.65 * inch, "Date: 2026-01-29")
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawString(0.9 * inch, 6.95 * inch, "NOTE: This is not a real stamp. For mock documentation only.")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    draw_wrapped(
        c,
        4.15 * inch,
        9.25 * inch,
        "This cover page is added to represent an EOR stamped set. The remainder of the set is the compiled P3.6 unstamped permit set (mock).",
        3.6 * inch,
    )
    c.showPage()
    c.save()

    merge_pdfs(path, [cover, base_unstamped])
    try:
        cover.unlink()
    except OSError:
        pass


def write_p4_application_forms(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "AHJ Permit Application Forms (Mock)",
        path.name,
        1,
        subtitle="P4.2 forms export  |  Date: 2026-01-29",
        banner="EV Charging Site Project — Phase 4 Outputs (MOCK)",
    )
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75 * inch, 9.65 * inch, "Application info (mock)")
    c.setFont("Helvetica", 10)
    y = 9.35 * inch
    fields = [
        ("AHJ", "City of Palo Alto — Building Division (Electrical Permits)"),
        ("Permit application number", "EL-2026-01472 (mock)"),
        ("Site address", "Place (Palo Alto, CA) (mock)"),
        ("Project description", "Install (8) Level-2 EVSE with load management (mock)"),
        ("Applicant", "Jordan Lee (PM) (mock)"),
        ("Contractor", "Romero Electric (mock)"),
    ]
    for k, v in fields:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.85 * inch, y, f"{k}:")
        c.setFont("Helvetica", 10)
        c.drawString(3.0 * inch, y, v)
        y -= 0.24 * inch
    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Attachments declared (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for a in ["Stamped drawings (P4.1)", "Load calc summary (P2.1)", "EVSE cut sheet (P1)", "EMS brief (P2)"]:
        c.drawString(1.0 * inch, y, f"- {a}")
        y -= 0.22 * inch
    c.showPage()
    c.save()


def write_p4_supporting_attachments(path: Path) -> None:
    # Create a cover that lists the typical electrical attachments; merge existing evidence PDFs where available.
    cover = P4_OUTPUTS / "_tmp_P4_supporting_cover.pdf"
    c = canvas.Canvas(str(cover), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "Supporting Attachments — Electrical (Mock)",
        cover.name,
        1,
        subtitle="P4 supporting bundle  |  Date: 2026-01-29",
        banner="EV Charging Site Project — Phase 4 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This file represents a compiled bundle of common electrical supporting attachments included with an AHJ permit submission (mock). It references Phase 1 and Phase 2 evidence pointers.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Included (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    items = [
        "phases/P2/Outputs/P2.1_LoadCalc_Summary_2026-01-22.pdf",
        "phases/P2/Outputs/P2.2_Architecture_Decision_Record_2026-01-22.pdf",
        "phases/P1/Inputs/P1-I04_EVSE_CutSheet_ElectriCharge_L2-7.6-G_revA.pdf",
        "phases/P2/Inputs/P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf",
        "phases/P1/Inputs/P1-I05_AHJ_Electrical_Permitting_CodeBasis_2026-01-17.pdf",
    ]
    for it in items:
        c.drawString(1.0 * inch, y, f"- {it}")
        y -= 0.22 * inch
    c.showPage()
    c.save()

    parts: list[Path] = [cover]
    for p in [
        ROOT / "P2" / "Outputs" / "P2.1_LoadCalc_Summary_2026-01-22.pdf",
        ROOT / "P2" / "Outputs" / "P2.2_Architecture_Decision_Record_2026-01-22.pdf",
        ROOT / "P1" / "Inputs" / "P1-I04_EVSE_CutSheet_ElectriCharge_L2-7.6-G_revA.pdf",
        ROOT / "P2" / "Inputs" / "P2-W04_EMS_TechnicalBrief_revB_2026-01-21.pdf",
        ROOT / "P1" / "Inputs" / "P1-I05_AHJ_Electrical_Permitting_CodeBasis_2026-01-17.pdf",
    ]:
        if p.exists():
            parts.append(p)
    merge_pdfs(path, parts)
    try:
        cover.unlink()
    except OSError:
        pass


def write_p4_submission_receipt(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "AHJ Submission Receipt / Confirmation (Mock)",
        path.name,
        1,
        subtitle="Portal confirmation export  |  Date: 2026-01-29",
        banner="EV Charging Site Project — Phase 4 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    fields = [
        ("AHJ", "City of Palo Alto — Building Division (Electrical Permits)"),
        ("Application number", "EL-2026-01472 (mock)"),
        ("Submission method", "Online portal upload (mock)"),
        ("Submitted by", "Jordan Lee (PM) (mock)"),
        ("Submission date/time", "2026-01-29 14:18 PT (mock)"),
        ("Status", "Submitted (mock)"),
    ]
    for k, v in fields:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.85 * inch, y, f"{k}:")
        c.setFont("Helvetica", 10)
        c.drawString(3.0 * inch, y, v)
        y -= 0.24 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: Mock receipt; replace with actual portal download/screenshot PDF.")
    c.setFillColor(colors.black)
    c.showPage()
    c.save()


def write_p4_tracking_log(path: Path) -> None:
    rows = [
        ["Permit Tracking Log (MOCK)", "", "", ""],
        ["AHJ", "City of Palo Alto — Building Division (Electrical Permits)", "", ""],
        ["Application number", "EL-2026-01472 (mock)", "", ""],
        ["Submission date/time", "2026-01-29 14:18 PT (mock)", "", ""],
        ["Status", "Submitted (mock)", "", ""],
        ["Next milestone", "Plan check comments expected (mock)", "", ""],
    ]
    events = [
        ["Date", "Event", "Evidence file", "Owner"],
        ["2026-01-29", "Submitted P4.2 package", "P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf", "Jordan Lee (mock)"],
        ["2026-02-06", "Plan check comments received", "P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf", "Jordan Lee (mock)"],
    ]
    write_minimal_xlsx(path, [("Summary", rows), ("Events", events)])


def write_p4_compiled_application_package(path: Path, stamped_set: Path, forms: Path, attachments: Path, receipt: Path) -> None:
    cover = P4_OUTPUTS / "_tmp_P4.2_cover.pdf"
    c = canvas.Canvas(str(cover), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "Permit Application Package (Compiled) (Mock)",
        cover.name,
        1,
        subtitle="P4.2 compiled package  |  Application: EL-2026-01472 (mock)",
        banner="EV Charging Site Project — Phase 4 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This compiled PDF represents the complete permit submission package as uploaded to the AHJ portal: forms + stamped drawings + supporting attachments + submission receipt.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Package sections (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for p in [forms, stamped_set, attachments, receipt]:
        c.drawString(1.0 * inch, y, f"- {p.name}")
        y -= 0.22 * inch
    c.showPage()
    c.save()

    merge_pdfs(path, [cover, forms, stamped_set, attachments, receipt])
    try:
        cover.unlink()
    except OSError:
        pass


# -------------------------
# Phase 5 (P5)
# -------------------------


def write_p5_raw_comments(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "AHJ Plan Check Comments (Raw) (Mock)",
        path.name,
        1,
        subtitle="Received: 2026-02-06  |  Application: EL-2026-01472 (mock)",
        banner="EV Charging Site Project — Phase 5 Inputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This document represents mock AHJ plan-check comments as downloaded from the portal. Replace with the actual PDF issued by the AHJ.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Comments (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    comments = [
        "C-01: E-001 one-line — clarify EMS method, monitoring point, and fail-safe behavior; cite code basis.",
        "C-02: E-001 one-line — provide available fault current basis and confirm minimum AIC for OCPDs.",
        "C-03: E-005 notes — add explicit EVSE continuous-load factor statement and labeling requirements.",
        "C-04: E-002/E-004 — standardize EV subpanel designation across plan + schedules (EVSP-1).",
    ]
    for cmt in comments:
        y = draw_wrapped(c, 0.95 * inch, y, f"- {cmt}", 6.8 * inch, font_size=10)
        y -= 0.05 * inch
        if y < 1.6 * inch:
            c.showPage()
            watermark_pdf(c)
            header_footer(c, "AHJ Plan Check Comments (Raw) (Mock)", path.name, 2, banner="EV Charging Site Project — Phase 5 Inputs (MOCK)")
            y = 9.65 * inch
    c.showPage()
    c.save()


def write_p5_comment_log_xlsx(path: Path) -> None:
    parsed = [
        ["AHJ Comment Log (Parsed) (MOCK)", "", "", "", ""],
        ["Application", "EL-2026-01472 (mock)", "", "", ""],
        ["Received", "2026-02-06", "", "", ""],
        ["", "", "", "", ""],
        ["Comment ID", "Location", "Comment", "Owner", "Disposition/Response"],
        ["C-01", "E-001", "Clarify EMS method/monitoring/fail-safe; cite code basis", "Priya Shah, PE (mock)", "Accepted; update one-line + notes"],
        ["C-02", "E-001", "Provide fault current basis; confirm min AIC", "Priya Shah, PE (mock)", "Accepted; add fault basis note"],
        ["C-03", "E-005", "Add continuous-load factor + labeling requirements", "Priya Shah, PE (mock)", "Accepted; expand notes"],
        ["C-04", "E-002/E-004", "Standardize EVSP-1 designation across set", "Sam Ortega (mock)", "Accepted; update labels"],
    ]
    summary = [
        ["Summary (MOCK)", "", ""],
        ["Total comments", 4, ""],
        ["Open", 0, ""],
        ["Resolved", 4, ""],
        ["Resubmission target", "2026-02-12", ""],
    ]
    write_minimal_xlsx(path, [("ParsedLog", parsed), ("Summary", summary)])


def write_p5_redlines(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "Internal Redlines — Revision Set (Mock)",
        path.name,
        1,
        subtitle="Internal review markups prior to resubmission  |  Date: 2026-02-10",
        banner="EV Charging Site Project — Phase 5 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This PDF represents internal redlines used to coordinate revisions in response to AHJ comments. Replace with actual PDF markups exported from the drawing set.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setStrokeColor(colors.red)
    c.setLineWidth(2)
    c.rect(0.75 * inch, 6.8 * inch, 7.0 * inch, 2.4 * inch, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.red)
    c.drawString(0.85 * inch, 9.0 * inch, "REDLINE (mock): Add EMS fail-safe + monitoring point note on E-001")
    c.drawString(0.85 * inch, 8.7 * inch, "REDLINE (mock): Add fault current / AIC basis note on E-001")
    c.drawString(0.85 * inch, 8.4 * inch, "REDLINE (mock): Expand notes on E-005 (continuous load + labeling)")
    c.drawString(0.85 * inch, 8.1 * inch, "REDLINE (mock): Standardize EVSP-1 labels on E-002/E-004")
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.showPage()
    c.save()


def write_p5_revised_set(path: Path, base_stamped_set: Path) -> None:
    # Create a revision cover page; merge with prior stamped set to represent "Rev 1".
    cover = P5_OUTPUTS / "_tmp_P5.2_rev1_cover.pdf"
    c = canvas.Canvas(str(cover), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "Revised Permit Drawing Set — Stamped (Rev 1) (Mock)",
        cover.name,
        1,
        subtitle="Resubmission: 2026-02-12  |  Rev 1 changes address C-01..C-04 (mock)",
        banner="EV Charging Site Project — Phase 5 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This file represents the revised stamped permit set after incorporating AHJ plan-check comments. In this mock package, the revised set is represented by a revision cover plus the previously stamped set.",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Revision summary (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    for line in [
        "Rev 1: Added EMS narrative + fail-safe note and monitoring point label (C-01).",
        "Rev 1: Added fault current / minimum AIC basis statement (C-02).",
        "Rev 1: Expanded electrical notes for continuous load + labeling (C-03).",
        "Rev 1: Standardized EVSP-1 nomenclature across set (C-04).",
    ]:
        c.drawString(1.0 * inch, y, f"- {line}")
        y -= 0.22 * inch
    c.showPage()
    c.save()

    merge_pdfs(path, [cover, base_stamped_set])
    try:
        cover.unlink()
    except OSError:
        pass


def write_p5_response_letter(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "Comment Response Letter (Rev 1) (Mock)",
        path.name,
        1,
        subtitle="Date: 2026-02-12  |  Application: EL-2026-01472 (mock)",
        banner="EV Charging Site Project — Phase 5 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    y = draw_wrapped(
        c,
        0.75 * inch,
        y,
        "This letter provides point-by-point responses to each AHJ plan-check comment and references where updates were made in the revised set (mock).",
        7.0 * inch,
    )
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75 * inch, y, "Responses (mock):")
    y -= 0.26 * inch
    c.setFont("Helvetica", 10)
    responses = [
        ("C-01", "Added EMS narrative, monitoring point label, and fail-safe note on sheet E-001. See Rev 1 cover notes."),
        ("C-02", "Added fault current basis and minimum AIC statement on sheet E-001. See Rev 1 cover notes."),
        ("C-03", "Expanded notes on sheet E-005 to explicitly state continuous-load factor and labeling requirements."),
        ("C-04", "Standardized EV subpanel designation to EVSP-1 across E-002 and E-004."),
    ]
    for cid, txt in responses:
        y = draw_wrapped(c, 0.85 * inch, y, f"{cid}: {txt}", 6.9 * inch, font_size=10)
        y -= 0.05 * inch
        if y < 1.8 * inch:
            c.showPage()
            watermark_pdf(c)
            header_footer(c, "Comment Response Letter (Rev 1) (Mock)", path.name, 2, banner="EV Charging Site Project — Phase 5 Outputs (MOCK)")
            y = 9.65 * inch
    c.setFont("Helvetica", 9)
    c.drawString(0.75 * inch, 2.0 * inch, "Signed (mock): Priya Shah, PE __________________   Date: 2026-02-12")
    c.showPage()
    c.save()


def write_p5_resubmission_receipt(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "AHJ Resubmission Receipt / Confirmation (Mock)",
        path.name,
        1,
        subtitle="Resubmission: 2026-02-12 16:42 PT (mock)  |  Application: EL-2026-01472 (mock)",
        banner="EV Charging Site Project — Phase 5 Outputs (MOCK)",
    )
    c.setFont("Helvetica", 10)
    y = 9.65 * inch
    fields = [
        ("Application number", "EL-2026-01472 (mock)"),
        ("Resubmission date/time", "2026-02-12 16:42 PT (mock)"),
        ("Submitted by", "Jordan Lee (PM) (mock)"),
        ("Status", "Resubmitted (mock)"),
    ]
    for k, v in fields:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.85 * inch, y, f"{k}:")
        c.setFont("Helvetica", 10)
        c.drawString(3.0 * inch, y, v)
        y -= 0.24 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: Mock receipt; replace with actual portal download/screenshot PDF.")
    c.setFillColor(colors.black)
    c.showPage()
    c.save()


def write_p5_approval_notice(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    watermark_pdf(c)
    header_footer(
        c,
        "AHJ Approval / Permit Issuance Notice (Mock)",
        path.name,
        1,
        subtitle="Status: Approved  |  Date: 2026-02-19 (mock)  |  Application: EL-2026-01472 (mock)",
        banner="EV Charging Site Project — Phase 5 Outputs (MOCK)",
    )
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.darkgreen)
    c.drawCentredString(letter[0] / 2, 8.2 * inch, "APPROVED")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    y = 7.7 * inch
    for k, v in [
        ("Application number", "EL-2026-01472 (mock)"),
        ("Approval date/time", "2026-02-19 10:07 PT (mock)"),
        ("Approved set", "P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf (mock reference)"),
        ("Notes", "All plan-check comments resolved (mock)."),
    ]:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.85 * inch, y, f"{k}:")
        c.setFont("Helvetica", 10)
        c.drawString(3.0 * inch, y, v)
        y -= 0.26 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, 1.05 * inch, "NOTE: Mock approval notice; replace with actual AHJ portal letter/download.")
    c.setFillColor(colors.black)
    c.showPage()
    c.save()


def main() -> None:
    ensure_dirs()

    # ---- Phase 4 ----
    p3_6 = P3_OUTPUTS / "P3.6_PermitSet_Unstamped_2026-01-26.pdf"
    if not p3_6.exists():
        raise FileNotFoundError("Missing required P3 output: phases/P3/Outputs/P3.6_PermitSet_Unstamped_2026-01-26.pdf")

    p4_eor = P4_INPUTS / "P4-EOR_ReviewNotes_2026-01-28.pdf"
    p4_1 = P4_OUTPUTS / "P4.1_PermitSet_Stamped_2026-01-29.pdf"
    p4_2_forms = P4_OUTPUTS / "P4.2_AHJ_ApplicationForms_2026-01-29.pdf"
    p4_support = P4_OUTPUTS / "P4.SupportingAttachments_Electrical_2026-01-29.pdf"
    p4_receipt = P4_OUTPUTS / "P4.SubmissionReceipt_AHJ_Confirmation_2026-01-29.pdf"
    p4_tracking = P4_OUTPUTS / "P4.PermitTrackingLog_2026-01-29.xlsx"
    p4_2_compiled = P4_OUTPUTS / "P4.2_PermitApplication_Package_Compiled_2026-01-29.pdf"

    write_p4_eor_review_notes(p4_eor)
    write_p4_stamped_set(p4_1, base_unstamped=p3_6)
    write_p4_application_forms(p4_2_forms)
    write_p4_supporting_attachments(p4_support)
    write_p4_submission_receipt(p4_receipt)
    write_p4_tracking_log(p4_tracking)
    write_p4_compiled_application_package(p4_2_compiled, stamped_set=p4_1, forms=p4_2_forms, attachments=p4_support, receipt=p4_receipt)

    # ---- Phase 5 ----
    p5_raw = P5_INPUTS / "P5-AHJ_PlanCheckComments_Raw_2026-02-06.pdf"
    p5_log = P5_OUTPUTS / "P5.1_AHJ_CommentLog_Parsed_2026-02-06.xlsx"
    p5_redlines = P5_OUTPUTS / "P5.Redlines_InternalReview_2026-02-10.pdf"
    p5_revised = P5_OUTPUTS / "P5.2_PermitSet_Revised_Stamped_Rev1_2026-02-12.pdf"
    p5_letter = P5_OUTPUTS / "P5.3_CommentResponseLetter_Rev1_2026-02-12.pdf"
    p5_resub_receipt = P5_OUTPUTS / "P5.ResubmissionReceipt_AHJ_2026-02-12.pdf"
    p5_approval = P5_OUTPUTS / "P5.4_AHJ_Approval_Notice_2026-02-19.pdf"

    write_p5_raw_comments(p5_raw)
    write_p5_comment_log_xlsx(p5_log)
    write_p5_redlines(p5_redlines)
    write_p5_revised_set(p5_revised, base_stamped_set=p4_1)
    write_p5_response_letter(p5_letter)
    write_p5_resubmission_receipt(p5_resub_receipt)
    write_p5_approval_notice(p5_approval)

    print("Generated Phase 4 package:")
    for f in [p4_eor, p4_1, p4_2_forms, p4_support, p4_receipt, p4_tracking, p4_2_compiled]:
        print(" -", f.relative_to(ROOT))

    print("Generated Phase 5 package:")
    for f in [p5_raw, p5_log, p5_redlines, p5_revised, p5_letter, p5_resub_receipt, p5_approval]:
        print(" -", f.relative_to(ROOT))


if __name__ == "__main__":
    main()

