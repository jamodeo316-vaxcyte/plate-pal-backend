import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def make_pdf_text(text):
    styles = getSampleStyleSheet()
    text_style = ParagraphStyle(
        "Text",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
    )

    pdf_text = Paragraph(text.strip(), text_style)

    return pdf_text

def make_pdf_plot(plot, doc):
    plot_buffer = io.BytesIO()
    plot.savefig(plot_buffer, format="png", bbox_inches="tight", dpi=150)
    plot_buffer.seek(0)

    image_reader = ImageReader(plot_buffer)
    iw, ih = image_reader.getSize()
    page_width, _ = letter
    max_width = page_width - (doc.leftMargin + doc.rightMargin)
    scale = min(1.0, max_width / float(iw))

    pdf_plot = Image(plot_buffer, width=iw * scale, height=ih * scale)

    return pdf_plot

def make_pdf_table(table, doc):
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        "SmallHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10
    )
    row_style = ParagraphStyle(
        "SmallBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10
    )

    headers = list(map(str, table.columns.tolist()))
    headers = [Paragraph(h, header_style) for h in headers]
    rows = table.astype(str).values.tolist()
    rows = [[Paragraph(c, row_style) for c in row] for row in rows]
    table_data = [headers] + rows

    max_width = getattr(doc, "width", letter[0] - (doc.leftMargin + doc.rightMargin))
    n_cols = len(headers)
    col_widths = [max_width / n_cols] * n_cols

    pdf_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    pdf_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.black),
        ("ALIGN",      (0, 0), (-1, 0), "CENTER"),
        ("ALIGN",      (0, 1), (-1, -1), "LEFT"),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("GRID",       (0, 0), (-1, -1), 0.25, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))

    return pdf_table

def get_assay_report(data):
    assay_summary, results_summary = data['assay_summary'], data['results_summary']
    curve_plot, results_table = data['curve_plot'], data['results_table']
    standard_names = data['curve_fit']['standard_names']
    standard_results = results_table[results_table['Sample Label'].isin(standard_names)]
    sample_results = results_table[~results_table['Sample Label'].isin(standard_names)]

    file_name = data['file_name']
    current_datetime = datetime.now().strftime("%-m/%-d/%Y %-I:%M:%S %p")
    file_summary = f"This report was produced by Vaxcyte's Plate Pal on {current_datetime} using {file_name}."

    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, topMargin=48)
    styles = getSampleStyleSheet()

    story = [
        Paragraph("Bicinchoninic Acid (BCA) Assay Report", styles["Title"]),
        Spacer(1, 8),
        Paragraph("Assay Summary", styles["Heading2"]),
        make_pdf_text(assay_summary),
        Spacer(1, 6),
        Paragraph("Results Summary", styles["Heading2"]),
        make_pdf_text(results_summary),
        Spacer(1, 6),
        Paragraph("Standard Curve", styles["Heading2"]),
        make_pdf_plot(curve_plot, doc),
        Spacer(1, 6),
        Paragraph('Standard Results', styles["Heading2"]),
        Spacer(1, 6),
        make_pdf_table(standard_results, doc),
        Spacer(1, 6),
        Paragraph('Sample Results', styles["Heading2"]),
        Spacer(1, 6),
        make_pdf_table(sample_results, doc),
        Spacer(1, 15),
        make_pdf_text(file_summary)
    ]

    doc.build(story)
    pdf_buffer.seek(0)
    assay_report = pdf_buffer.getvalue()

    data['assay_report'] = assay_report

    return data