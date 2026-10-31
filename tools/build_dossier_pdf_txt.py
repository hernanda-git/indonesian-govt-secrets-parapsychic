import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ROOT = r"C:\Workspace\indonesian-govt-secrets-parapsychic"
PDF_DIR = os.path.join(ROOT, "pdf")
TXT_DIR = os.path.join(ROOT, "txt")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)

md_files = [
    "README.md",
    "01_US_STATE_DEPT_PARANORMAL_CABLES.md",
    "02_INDONESIA_GOVT_PARAPSYCHIC_INTELLIGENCE.md",
    "03_US_EMBASSY_JAKARTA_CABLES_ON_MYSTICISM.md",
    "04_CHRONOLOGICAL_DECLASSIFIED_TIMELINE.md",
    "05_PRIMARY_SOURCES_ARCHIVAL_GUIDE.md"
]

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=16,
    leading=20,
    textColor=colors.HexColor('#1a237e'),
    spaceAfter=12
)
h2_style = ParagraphStyle(
    'DocH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    textColor=colors.HexColor('#283593'),
    spaceBefore=12,
    spaceAfter=6
)
h3_style = ParagraphStyle(
    'DocH3',
    parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#303f9f'),
    spaceBefore=8,
    spaceAfter=4
)
body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor('#212121'),
    spaceAfter=4
)
bullet_style = ParagraphStyle(
    'DocBullet',
    parent=body_style,
    leftIndent=15,
    firstLineIndent=-10,
    spaceAfter=3
)
table_cell_style = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7,
    leading=9,
    textColor=colors.HexColor('#212121')
)
table_header_style = ParagraphStyle(
    'TableHeader',
    parent=table_cell_style,
    fontName='Helvetica-Bold',
    textColor=colors.white
)

def format_inline(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    # restore allowed tags if any, or re-apply formatting
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # code
    text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
    return text

def convert_md_to_pdf_and_txt(md_name):
    base_name = os.path.splitext(md_name)[0]
    md_path = os.path.join(ROOT, md_name)
    txt_path = os.path.join(TXT_DIR, base_name + ".txt")
    pdf_path = os.path.join(PDF_DIR, base_name + ".pdf")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Write TXT verbatim
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created TXT: {txt_path}")
    
    # Build Story for ReportLab
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    story = []
    lines = content.split('\n')
    
    in_code_block = False
    code_lines = []
    
    in_table = False
    table_data = []
    
    for line in lines:
        stripped = line.strip()
        
        # Code blocks
        if stripped.startswith('```'):
            if in_code_block:
                code_text = '\n'.join(code_lines)
                story.append(Preformatted(code_text, ParagraphStyle('CodeStyle', fontName='Courier', fontSize=6.5, leading=8.5, backColor=colors.HexColor('#f5f5f5'))))
                story.append(Spacer(1, 4))
                in_code_block = False
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            continue
        
        if in_code_block:
            code_lines.append(line)
            continue
            
        # Tables
        if stripped.startswith('|') and stripped.endswith('|'):
            if not in_table:
                in_table = True
                table_data = []
            # check if separator line
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped[1:-1].split('|')]
            table_data.append(cells)
            continue
        else:
            if in_table:
                # Flush table
                if table_data:
                    formatted_table = []
                    for row_idx, row in enumerate(table_data):
                        formatted_row = []
                        for cell in row:
                            st = table_header_style if row_idx == 0 else table_cell_style
                            # replace br with newline
                            cell_text = cell.replace('<br>', '\n').replace('&lt;br&gt;', '\n')
                            cell_text = format_inline(cell_text).replace('\n', '<br/>')
                            formatted_row.append(Paragraph(cell_text, st))
                        formatted_table.append(formatted_row)
                    
                    t = Table(formatted_table, repeatRows=1)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cfd8dc')),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                        ('TOPPADDING', (0, 0), (-1, -1), 3),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                        ('LEFTPADDING', (0, 0), (-1, -1), 4),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 6))
                in_table = False
                table_data = []
        
        # Headers
        if stripped.startswith('# '):
            story.append(Paragraph(format_inline(stripped[2:]), title_style))
        elif stripped.startswith('## '):
            story.append(Paragraph(format_inline(stripped[3:]), h2_style))
        elif stripped.startswith('### '):
            story.append(Paragraph(format_inline(stripped[4:]), h3_style))
        elif stripped.startswith('#### '):
            story.append(Paragraph(format_inline(stripped[5:]), h3_style))
        elif stripped.startswith('* ') or stripped.startswith('- '):
            item_text = "&bull; " + format_inline(stripped[2:])
            story.append(Paragraph(item_text, bullet_style))
        elif re.match(r'^\d+\.\s', stripped):
            match = re.match(r'^(\d+\.)\s(.*)$', stripped)
            num = match.group(1)
            rest = match.group(2)
            item_text = f"{num} " + format_inline(rest)
            story.append(Paragraph(item_text, bullet_style))
        elif stripped == '---':
            story.append(Spacer(1, 4))
        elif stripped == '':
            story.append(Spacer(1, 3))
        else:
            story.append(Paragraph(format_inline(stripped), body_style))
            
    doc.build(story)
    print(f"Created PDF: {pdf_path}")

for md in md_files:
    convert_md_to_pdf_and_txt(md)
print("All dossier PDFs and TXTs generated successfully.")
