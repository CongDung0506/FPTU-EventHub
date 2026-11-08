import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PRIMARY = RGBColor(242, 111, 33)   # FPT Orange #F26F21
NAVY = RGBColor(0, 75, 145)        # FPT Navy #004B91
TEXT_MAIN = RGBColor(30, 41, 59)   # Slate 800 #1E293B
MUTED = RGBColor(100, 116, 139)    # Slate 500 #64748B
BG_LIGHT = "F8FAFC"
BG_HEADER = "004B91"
BORDER_COLOR = "CBD5E1"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_styled_paragraph(p, text, default_color=TEXT_MAIN, default_size=10.5, default_bold=False, default_italic=False):
    # Regex to tokenize markdown: bold (**...**), inline code (`...`), italic (*...*)
    tokens = re.split(r'(\*\*.*?\*\*|`.*?`|\*.*?\*|\[.*?\]\(.*?\))', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('**') and token.endswith('**'):
            run = p.add_run(token[2:-2])
            run.font.name = 'Segoe UI'
            run.font.size = Pt(default_size)
            run.font.bold = True
            run.font.color.rgb = default_color
        elif token.startswith('`') and token.endswith('`'):
            run = p.add_run(token[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(default_size * 0.95)
            run.font.color.rgb = RGBColor(194, 65, 12) # Rust / dark orange
            run.font.bold = True
        elif token.startswith('*') and token.endswith('*') and len(token) > 2:
            run = p.add_run(token[1:-1])
            run.font.name = 'Segoe UI'
            run.font.size = Pt(default_size)
            run.font.italic = True
            run.font.color.rgb = default_color
        elif token.startswith('[') and '](' in token and token.endswith(')'):
            label = token[1:token.index('](')]
            url = token[token.index('](')+2:-1]
            run = p.add_run(label)
            run.font.name = 'Segoe UI'
            run.font.size = Pt(default_size)
            run.font.color.rgb = RGBColor(2, 132, 199) # Blue link
            run.font.underline = True
        else:
            run = p.add_run(token)
            run.font.name = 'Segoe UI'
            run.font.size = Pt(default_size)
            run.font.bold = default_bold
            run.font.italic = default_italic
            run.font.color.rgb = default_color

def convert_md_to_docx(md_path, docx_path, doc_title="TÀI LIỆU DỰ ÁN FPTU EVENTHUB"):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Segoe UI'
    style_normal.font.size = Pt(10.5)
    style_normal.font.color.rgb = TEXT_MAIN
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(4)

    lines = md_text.splitlines()
    i = 0
    in_code_block = False
    code_lines = []

    while i < len(lines):
        line = lines[i]

        # Handle code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                # Output code box table
                t = doc.add_table(rows=1, cols=1)
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                cell = t.cell(0, 0)
                set_cell_background(cell, "F1F5F9")
                set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
                cp = cell.paragraphs[0]
                cp.paragraph_format.line_spacing = 1.15
                cp.paragraph_format.space_after = Pt(0)
                c_run = cp.add_run('\n'.join(code_lines))
                c_run.font.name = 'Consolas'
                c_run.font.size = Pt(9.0)
                c_run.font.color.rgb = RGBColor(30, 41, 59)
                p_after = doc.add_paragraph()
                p_after.paragraph_format.space_after = Pt(4)
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        stripped = line.strip()

        # Empty line
        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if stripped in ('---', '***', '___'):
            # subtle divider paragraph
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run("—" * 55)
            run.font.color.rgb = MUTED
            run.font.size = Pt(8)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1
            continue

        # Blockquote (> ...)
        if stripped.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            # Add callout table
            t = doc.add_table(rows=1, cols=1)
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = t.cell(0, 0)
            set_cell_background(cell, BG_LIGHT)
            set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
            tcPr = cell._tc.get_or_add_tcPr()
            borders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:left w:val="single" w:sz="24" w:space="0" w:color="F26F21"/>'
                f'<w:top w:val="none"/>'
                f'<w:right w:val="none"/>'
                f'<w:bottom w:val="none"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(borders)
            for q_idx, q_line in enumerate(quote_lines):
                if q_idx == 0:
                    qp = cell.paragraphs[0]
                else:
                    qp = cell.add_paragraph()
                qp.paragraph_format.line_spacing = 1.2
                qp.paragraph_format.space_after = Pt(2)
                add_styled_paragraph(qp, q_line, default_color=TEXT_MAIN, default_size=10.0)
            doc.add_paragraph().paragraph_format.space_after = Pt(4)
            continue

        # Markdown Table (| ... |)
        if stripped.startswith('|') and stripped.endswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            
            # Parse table rows
            raw_rows = []
            for tl in table_lines:
                # Remove leading and trailing pipe
                trimmed = tl.strip()[1:-1]
                cells = [c.strip() for c in trimmed.split('|')]
                # Check if separator row
                if all(re.match(r'^:?-+:?$', c) for c in cells):
                    continue
                raw_rows.append(cells)
            
            if raw_rows:
                num_cols = max(len(r) for r in raw_rows)
                # Normalize row cell count
                norm_rows = []
                for r in raw_rows:
                    if len(r) < num_cols:
                        r.extend([''] * (num_cols - len(r)))
                    norm_rows.append(r[:num_cols])

                t = doc.add_table(rows=len(norm_rows), cols=num_cols)
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                set_table_borders(t, BORDER_COLOR)

                for row_idx, r_data in enumerate(norm_rows):
                    row = t.rows[row_idx]
                    is_header = (row_idx == 0)
                    for col_idx, cell_value in enumerate(r_data):
                        c = row.cells[col_idx]
                        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                        set_cell_margins(c, top=80, bottom=80, left=120, right=120)
                        if is_header:
                            set_cell_background(c, BG_HEADER)
                            cp = c.paragraphs[0]
                            cp.paragraph_format.space_after = Pt(0)
                            cp.paragraph_format.line_spacing = 1.15
                            add_styled_paragraph(cp, cell_value, default_color=RGBColor(255, 255, 255), default_size=9.5, default_bold=True)
                        else:
                            fill_color = BG_LIGHT if row_idx % 2 == 1 else "FFFFFF"
                            set_cell_background(c, fill_color)
                            cp = c.paragraphs[0]
                            cp.paragraph_format.space_after = Pt(0)
                            cp.paragraph_format.line_spacing = 1.15
                            add_styled_paragraph(cp, cell_value, default_color=TEXT_MAIN, default_size=9.0)

                doc.add_paragraph().paragraph_format.space_after = Pt(6)
            continue

        # Headings (#)
        if stripped.startswith('# '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            add_styled_paragraph(p, stripped[2:].strip(), default_color=NAVY, default_size=16.0, default_bold=True)
            i += 1
            continue

        if stripped.startswith('## '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(11)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            add_styled_paragraph(p, stripped[3:].strip(), default_color=PRIMARY, default_size=13.0, default_bold=True)
            i += 1
            continue

        if stripped.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            add_styled_paragraph(p, stripped[4:].strip(), default_color=NAVY, default_size=11.5, default_bold=True)
            i += 1
            continue

        if stripped.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            add_styled_paragraph(p, stripped[5:].strip(), default_color=TEXT_MAIN, default_size=10.5, default_bold=True)
            i += 1
            continue

        # Bullet lists (* or -)
        if re.match(r'^\s*[\*\-]\s+', line):
            indent_level = len(re.match(r'^\s*', line).group()) // 2
            text_val = re.sub(r'^\s*[\*\-]\s+', '', line).strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.25 * (indent_level + 1))
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.2
            add_styled_paragraph(p, text_val, default_color=TEXT_MAIN, default_size=10.0)
            i += 1
            continue

        # Numbered lists (1. 2. etc)
        if re.match(r'^\s*\d+\.\s+', line):
            text_val = re.sub(r'^\s*\d+\.\s+', '', line).strip()
            num_match = re.match(r'^\s*(\d+)\.\s+', line).group(1)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.2
            num_run = p.add_run(f"{num_match}. ")
            num_run.font.name = 'Segoe UI'
            num_run.font.bold = True
            num_run.font.color.rgb = PRIMARY
            add_styled_paragraph(p, text_val, default_color=TEXT_MAIN, default_size=10.0)
            i += 1
            continue

        # Standard Paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        add_styled_paragraph(p, stripped, default_color=TEXT_MAIN, default_size=10.5)
        i += 1

    doc.save(docx_path)
    print(f"Exported DOCX successfully to: {docx_path}")

if __name__ == '__main__':
    convert_md_to_docx(
        r"C:\Users\truon\fptu_eventhub\DAC_TA_YEU_CAU_FPTU_EVENTHUB.md",
        r"C:\Users\truon\fptu_eventhub\DAC_TA_YEU_CAU_FPTU_EVENTHUB.docx"
    )
    convert_md_to_docx(
        r"C:\Users\truon\fptu_eventhub\NOI_DUNG_26_SLIDES_CANVA.md",
        r"C:\Users\truon\fptu_eventhub\NOI_DUNG_26_SLIDES_CANVA.docx"
    )
    convert_md_to_docx(
        r"C:\Users\truon\fptu_eventhub\README.md",
        r"C:\Users\truon\fptu_eventhub\HUONG_DAN_DU_AN_README.docx"
    )
