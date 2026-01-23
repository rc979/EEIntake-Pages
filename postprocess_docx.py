from __future__ import annotations

import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def qn(tag: str) -> str:
    # tag like "w:pPr"
    prefix, local = tag.split(":")
    if prefix != "w":
        raise ValueError(f"Unsupported prefix: {prefix}")
    return f"{{{W_NS}}}{local}"


def ensure_child(parent: ET.Element, child_tag: str) -> ET.Element:
    child = parent.find(child_tag, NS)
    if child is None:
        child = ET.SubElement(parent, qn(child_tag))
    return child


def set_margins_docx(document_xml: bytes, margin_in: float = 0.35) -> bytes:
    twips = int(round(margin_in * 1440))
    header_footer = int(round(0.20 * 1440))  # 0.2in

    tree = ET.fromstring(document_xml)
    body = tree.find("w:body", NS)
    if body is None:
        return document_xml

    # sectPr is typically the last element in body
    sectPr = body.find("w:sectPr", NS)
    if sectPr is None:
        # try last child
        for child in reversed(list(body)):
            if child.tag == qn("w:sectPr"):
                sectPr = child
                break
    if sectPr is None:
        sectPr = ET.SubElement(body, qn("w:sectPr"))

    pgMar = sectPr.find("w:pgMar", NS)
    if pgMar is None:
        pgMar = ET.SubElement(sectPr, qn("w:pgMar"))

    # Word uses attributes in w namespace
    pgMar.set(qn("w:top"), str(twips))
    pgMar.set(qn("w:bottom"), str(twips))
    pgMar.set(qn("w:left"), str(twips))
    pgMar.set(qn("w:right"), str(twips))
    pgMar.set(qn("w:header"), str(header_footer))
    pgMar.set(qn("w:footer"), str(header_footer))
    pgMar.set(qn("w:gutter"), "0")

    return ET.tostring(tree, encoding="utf-8", xml_declaration=True)


def enforce_heading_keep_with_next(styles_xml: bytes, heading_style_ids: list[str]) -> bytes:
    tree = ET.fromstring(styles_xml)

    for style_id in heading_style_ids:
        style = None
        for s in tree.findall("w:style", NS):
            if s.get(qn("w:styleId")) == style_id:
                style = s
                break
        if style is None:
            continue

        pPr = style.find("w:pPr", NS)
        if pPr is None:
            pPr = ET.SubElement(style, qn("w:pPr"))

        # Add keepNext and keepLines (avoid heading alone at bottom).
        if pPr.find("w:keepNext", NS) is None:
            ET.SubElement(pPr, qn("w:keepNext"))
        if pPr.find("w:keepLines", NS) is None:
            ET.SubElement(pPr, qn("w:keepLines"))

    return ET.tostring(tree, encoding="utf-8", xml_declaration=True)


def set_repeat_table_headers(document_xml: bytes) -> bytes:
    tree = ET.fromstring(document_xml)
    body = tree.find("w:body", NS)
    if body is None:
        return document_xml

    for tbl in body.iterfind(".//w:tbl", NS):
        first_tr = tbl.find("w:tr", NS)
        if first_tr is None:
            continue
        trPr = first_tr.find("w:trPr", NS)
        if trPr is None:
            trPr = ET.Element(qn("w:trPr"))
            # insert trPr as first child of tr
            first_tr.insert(0, trPr)

        tblHeader = trPr.find("w:tblHeader", NS)
        if tblHeader is None:
            tblHeader = ET.SubElement(trPr, qn("w:tblHeader"))
        tblHeader.set(qn("w:val"), "1")

        # Do NOT add cantSplit; allowing row splitting reduces huge whitespace.

    return ET.tostring(tree, encoding="utf-8", xml_declaration=True)


def _para_text(p: ET.Element) -> str:
    return "".join(t.text or "" for t in p.findall(".//w:t", NS))


def set_page_breaks_for_major_sections(document_xml: bytes) -> bytes:
    """
    Add pageBreakBefore to major section headings (phases + addenda + overview),
    so headings always start on a new page in Word.
    """
    tree = ET.fromstring(document_xml)
    body = tree.find("w:body", NS)
    if body is None:
        return document_xml

    for p in body.findall(".//w:p", NS):
        pPr = p.find("w:pPr", NS)
        if pPr is None:
            continue
        pStyle = pPr.find("w:pStyle", NS)
        if pStyle is None:
            continue
        style_id = pStyle.get(qn("w:val")) or ""
        if style_id not in ("Heading1", "Heading2"):
            continue

        text = _para_text(p).strip()
        if not text:
            continue

        is_major = False

        # Phase sections (Phase 1..Phase 8)
        if text.startswith("Phase "):
            is_major = True

        # Executive front-matter sections
        if text in ("Table of Contents", "Overview", "Introduction"):
            is_major = True

        # Addenda headings may be prefixed by numbers in the markdown (e.g. "12 Addendum A ...")
        if text.startswith("Addendum ") or ("Addendum " in text and text.lstrip()[:2].isdigit()):
            is_major = True

        if not is_major:
            continue

        if pPr.find("w:pageBreakBefore", NS) is None:
            ET.SubElement(pPr, qn("w:pageBreakBefore"))

    return ET.tostring(tree, encoding="utf-8", xml_declaration=True)


def compact_addendum_b_party_table(document_xml: bytes) -> bytes:
    """
    Make Addendum B (Party Directory) reliably fit on one page by:
    - setting a fixed table layout with reasonable column widths
    - tightening paragraph spacing in table cells
    - reducing font size within that table
    """
    tree = ET.fromstring(document_xml)
    body = tree.find("w:body", NS)
    if body is None:
        return document_xml

    def cell_text(tc: ET.Element) -> str:
        return "".join(t.text or "" for t in tc.findall(".//w:t", NS)).strip()

    def set_run_font_9pt(r: ET.Element) -> None:
        rPr = r.find("w:rPr", NS)
        if rPr is None:
            rPr = ET.SubElement(r, qn("w:rPr"))
        sz = ensure_child(rPr, "w:sz")
        szCs = ensure_child(rPr, "w:szCs")
        # w:sz is in half-points; 9pt => 18
        sz.set(qn("w:val"), "18")
        szCs.set(qn("w:val"), "18")

    def tighten_paragraph(p: ET.Element) -> None:
        pPr = p.find("w:pPr", NS)
        if pPr is None:
            pPr = ET.SubElement(p, qn("w:pPr"))
        spacing = pPr.find("w:spacing", NS)
        if spacing is None:
            spacing = ET.SubElement(pPr, qn("w:spacing"))
        spacing.set(qn("w:before"), "0")
        spacing.set(qn("w:after"), "0")
        spacing.set(qn("w:line"), "240")  # single-ish
        spacing.set(qn("w:lineRule"), "auto")

    for tbl in body.iterfind(".//w:tbl", NS):
        first_tr = tbl.find("w:tr", NS)
        if first_tr is None:
            continue
        headers = [cell_text(tc) for tc in first_tr.findall("w:tc", NS)]
        if headers != ["Party", "Works for", "Role", "Email", "Phone"]:
            continue

        # Fixed layout + column widths tuned for a single-page directory table
        widths = [2200, 2000, 3600, 2600, 1600]  # total 12000 twips-ish

        tblPr = tbl.find("w:tblPr", NS)
        if tblPr is None:
            tblPr = ET.Element(qn("w:tblPr"))
            tbl.insert(0, tblPr)
        tblLayout = tblPr.find("w:tblLayout", NS)
        if tblLayout is None:
            tblLayout = ET.SubElement(tblPr, qn("w:tblLayout"))
        tblLayout.set(qn("w:type"), "fixed")

        tblGrid = tbl.find("w:tblGrid", NS)
        if tblGrid is None:
            tblGrid = ET.Element(qn("w:tblGrid"))
            insert_at = 1 if tblPr is not None else 0
            tbl.insert(insert_at, tblGrid)
        else:
            for child in list(tblGrid):
                tblGrid.remove(child)
        for w in widths:
            gridCol = ET.SubElement(tblGrid, qn("w:gridCol"))
            gridCol.set(qn("w:w"), str(w))

        # Tighten spacing + shrink font for all paragraphs/runs in this table
        for p in tbl.iterfind(".//w:p", NS):
            tighten_paragraph(p)
        for r in tbl.iterfind(".//w:r", NS):
            set_run_font_9pt(r)

        break  # only one Addendum B table expected

    return ET.tostring(tree, encoding="utf-8", xml_declaration=True)


def adjust_table_column_widths(document_xml: bytes) -> bytes:
    """
    Narrow ID/source/status/date columns so verbose columns (provenance/criteria/etc) get more room.
    This sets fixed table layout + tblGrid widths for recognized header patterns.
    """
    tree = ET.fromstring(document_xml)
    body = tree.find("w:body", NS)
    if body is None:
        return document_xml

    def cell_text(tc: ET.Element) -> str:
        return "".join(t.text or "" for t in tc.findall(".//w:t", NS)).strip()

    for tbl in body.iterfind(".//w:tbl", NS):
        # Determine header row texts
        first_tr = tbl.find("w:tr", NS)
        if first_tr is None:
            continue
        headers = [cell_text(tc) for tc in first_tr.findall("w:tc", NS)]
        if not headers:
            continue

        col_count = len(headers)

        widths: list[int] | None = None

        # Patterns:
        # 7-col intake checklist: Input ID / Input / Source / Status / Acceptance criteria / Verified by / Date
        if col_count == 7 and headers[0] == "Input ID" and "Acceptance criteria" in headers[4]:
            widths = [700, 1400, 1100, 750, 5600, 1000, 650]  # total ~11200

        # 5-col input register: Input ID / Input / Provenance / Evidence / Verification + downstream use
        if widths is None and col_count == 5 and headers[0] == "Input ID" and ("Provenance" in headers[2] or "Provenance" in " ".join(headers)):
            widths = [700, 1400, 2800, 1500, 4800]

        # 5-col evidence index: Item ID / Work product / Provenance / Evidence reference ID(s) / Inputs + downstream use
        if widths is None and col_count == 5 and headers[0] == "Item ID" and "Work product" in headers[1]:
            widths = [700, 2200, 2600, 2200, 3500]

        # 3-col maps/tables: usually fine; skip.
        if widths is None:
            continue

        # Set fixed layout
        tblPr = tbl.find("w:tblPr", NS)
        if tblPr is None:
            tblPr = ET.Element(qn("w:tblPr"))
            tbl.insert(0, tblPr)
        tblLayout = tblPr.find("w:tblLayout", NS)
        if tblLayout is None:
            tblLayout = ET.SubElement(tblPr, qn("w:tblLayout"))
        tblLayout.set(qn("w:type"), "fixed")

        # Set tblGrid
        tblGrid = tbl.find("w:tblGrid", NS)
        if tblGrid is None:
            tblGrid = ET.Element(qn("w:tblGrid"))
            # insert after tblPr if present
            insert_at = 1 if tblPr is not None else 0
            tbl.insert(insert_at, tblGrid)
        else:
            # clear existing
            for child in list(tblGrid):
                tblGrid.remove(child)
        for w in widths:
            gridCol = ET.SubElement(tblGrid, qn("w:gridCol"))
            gridCol.set(qn("w:w"), str(w))

    return ET.tostring(tree, encoding="utf-8", xml_declaration=True)


def postprocess_docx(in_path: Path, out_path: Path) -> None:
    with zipfile.ZipFile(str(in_path), "r") as zin:
        files = {name: zin.read(name) for name in zin.namelist()}

    # Modify key parts if present
    if "word/document.xml" in files:
        doc = files["word/document.xml"]
        doc = adjust_table_column_widths(doc)
        doc = compact_addendum_b_party_table(doc)
        doc = set_repeat_table_headers(doc)
        doc = set_page_breaks_for_major_sections(doc)
        doc = set_margins_docx(doc, margin_in=0.35)
        files["word/document.xml"] = doc

    if "word/styles.xml" in files:
        styles = files["word/styles.xml"]
        styles = enforce_heading_keep_with_next(styles, ["Heading1", "Heading2", "Heading3", "Heading4"])
        files["word/styles.xml"] = styles

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(out_path), "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)


def main() -> None:
    in_path = Path("exports/EV Charging Project Plan Outline.raw.docx")
    out_path = Path("exports/EV Charging Project Plan Outline.docx")
    if not in_path.exists():
        raise SystemExit(f"Missing input: {in_path}")
    postprocess_docx(in_path, out_path)
    print("Wrote:", out_path)


if __name__ == "__main__":
    main()

