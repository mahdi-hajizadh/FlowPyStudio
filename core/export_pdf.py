from fpdf import FPDF


def save_code_as_pdf(code_text, filename="flowchart_code.pdf"):
    """Save the generated code as a PDF.

    Wrap long lines within the page and replace characters that the built-in Courier font cannot encode.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=11)

    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    for line in code_text.split("\n"):
        safe_line = _make_pdf_safe(line)
        if safe_line == "":
            pdf.ln(6)
            continue
        pdf.multi_cell(page_width, 6, txt=safe_line)

    pdf.output(filename)
    return filename


def _make_pdf_safe(text: str) -> str:
    """Replace characters outside Latin-1 with a question mark for the built-in Courier font."""
    return text.encode("latin-1", "replace").decode("latin-1")
