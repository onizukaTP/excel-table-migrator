import sys
import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress headers/footers on title page
        if self._pageNumber == 1:
            self.restoreState()
            return

        # Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 11 * inch - 36, "STUDENT EVALUATION MIGRATION TOOL — TECHNICAL SPECIFICATION")
        self.setFont("Helvetica", 8)
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "MYSQL FLAT DATABASE TABLES")
        
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 32, "CONFIDENTIAL & PROPRIETARY — DATA MIGRATION PROTOCOL")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)

        self.restoreState()

def format_inline(text):
    """Format markdown inline code and bolding."""
    text_clean = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text_clean = re.sub(r'`([^`]+)`', r'<font face="Courier" size="7.5">\1</font>', text_clean)
    text_clean = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text_clean)
    return text_clean

def split_markdown_table_row(line):
    """Splits a markdown table line by unescaped pipe (|) characters."""
    line_trimmed = line.strip()
    if line_trimmed.startswith("|"):
        line_trimmed = line_trimmed[1:]
    if line_trimmed.endswith("|"):
        line_trimmed = line_trimmed[:-1]

    # Split by '|' NOT preceded by '\'
    raw_cells = re.split(r'(?<!\\)\|', line_trimmed)
    cleaned_cells = [cell.strip().replace(r'\|', '|') for cell in raw_cells]
    return cleaned_cells

def build_pdf(md_filepath: str, pdf_filepath: str):
    doc = SimpleDocTemplate(
        pdf_filepath,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    PRIMARY = colors.HexColor("#0f172a")     # Slate 900
    ACCENT = colors.HexColor("#2563eb")      # Blue 600
    TEXT_COLOR = colors.HexColor("#334155")  # Slate 700
    CODE_BG = colors.HexColor("#f8fafc")     # Slate 50
    CODE_BORDER = colors.HexColor("#cbd5e1") # Slate 300

    # Custom Typography Styles
    styles.add(ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        'SecHeading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'SecHeading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=ACCENT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_COLOR,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_COLOR,
        leftIndent=12,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        'CodeLine',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor("#0f172a")
    ))

    styles.add(ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=0
    ))

    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=TEXT_COLOR
    ))

    story = []

    # Document Header
    story.append(Paragraph("Student Evaluation MySQL Flat Table Specification", styles['DocTitle']))
    story.append(Paragraph("Formal Technical Documentation — MySQL Dedicated Flat Tables & 15-Char Register Number Primary Key", styles['DocSubTitle']))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=8))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Database Engine:</b> MySQL Server 8.0+", styles['TableCell']),
            Paragraph("<b>Primary Key:</b> <code>id (VARCHAR(50))</code>", styles['TableCell']),
            Paragraph("<b>Conflict Strategy:</b> <code>ON DUPLICATE KEY UPDATE</code>", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tables:</b> Dedicated Per-Semester", styles['TableCell']),
            Paragraph("<b>Package:</b> <code>student_migrator</code>", styles['TableCell']),
            Paragraph("<b>File Formats:</b> Excel (.xlsx) & CSV (.csv)", styles['TableCell'])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[2.3*inch, 2.3*inch, 2.4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Read Markdown
    with open(md_filepath, "r", encoding="utf-8") as f:
        md_text = f.read()

    lines = md_text.splitlines()
    in_code_block = False
    code_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code Block Handler
        if line.strip().startswith("```"):
            if in_code_block:
                in_code_block = False
                
                code_table_rows = []
                for c_line in code_lines:
                    escaped_line = c_line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
                    p_c = Paragraph(escaped_line if escaped_line else "&nbsp;", styles['CodeLine'])
                    code_table_rows.append([p_c])

                if code_table_rows:
                    t_code = Table(code_table_rows, colWidths=[6.85 * inch])
                    t_code.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
                        ('BOX', (0,0), (-1,-1), 0.5, CODE_BORDER),
                        ('TOPPADDING', (0,0), (-1,-1), 1),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                        ('LEFTPADDING', (0,0), (-1,-1), 4),
                        ('RIGHTPADDING', (0,0), (-1,-1), 4),
                    ]))
                    story.append(Spacer(1, 3))
                    story.append(t_code)
                    story.append(Spacer(1, 5))
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Markdown Table Handler
        if "|" in line and i + 1 < len(lines) and "|---" in lines[i+1]:
            table_lines = [line]
            i += 2  # skip separator line
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1
            
            table_data = []
            for idx, tline in enumerate(table_lines):
                cells = split_markdown_table_row(tline)
                row_cells = []
                for cell_txt in cells:
                    cell_formatted = format_inline(cell_txt)
                    if idx == 0:
                        row_cells.append(Paragraph(cell_formatted, styles['TableHeader']))
                    else:
                        row_cells.append(Paragraph(cell_formatted, styles['TableCell']))
                table_data.append(row_cells)

            if table_data:
                num_cols = len(table_data[0])
                header_cells = split_markdown_table_row(table_lines[0])
                header_str = " ".join(c.lower() for c in header_cells)

                if num_cols == 2:
                    col_widths = [1.8 * inch, 5.0 * inch]
                elif num_cols == 3:
                    col_widths = [2.0 * inch, 1.4 * inch, 3.4 * inch]
                elif num_cols == 4:
                    col_widths = [1.5 * inch, 1.3 * inch, 1.4 * inch, 2.6 * inch]
                else:
                    col_widths = [(6.8 * inch) / num_cols] * num_cols

                t = Table(table_data, colWidths=col_widths, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('LEFTPADDING', (0,0), (-1,-1), 5),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
                ]))
                story.append(Spacer(1, 4))
                story.append(t)
                story.append(Spacer(1, 6))
            continue

        # Headers
        if line.startswith("## "):
            h_text = line[3:].strip()
            story.append(Spacer(1, 6))
            story.append(Paragraph(h_text, styles['SecHeading1']))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=4))
            i += 1
            continue

        if line.startswith("### "):
            h_text = line[4:].strip()
            story.append(Paragraph(h_text, styles['SecHeading2']))
            i += 1
            continue

        # Bullet Lists
        if line.strip().startswith("- "):
            b_text = line.strip()[2:]
            story.append(Paragraph(f"• &nbsp; {format_inline(b_text)}", styles['CustomBullet']))
            i += 1
            continue

        # Regular Text
        p_text = line.strip()
        if p_text and not p_text.startswith("---") and not p_text.startswith("#"):
            story.append(Paragraph(format_inline(p_text), styles['CustomBody']))

        i += 1

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully regenerated optimized PDF: {pdf_filepath}")

if __name__ == "__main__":
    md_file = "structure.md"
    pdf_file = "structure.pdf"
    build_pdf(md_file, pdf_file)
