import PyPDF2


def extract_from_pdf(file):
    reader = PyPDF2.PdfReader(file, strict=False)
    pdf_text = []

    for page in reader.pages:
        content = page.extract_text()
        pdf_text.append(content)

    return ". ".join(pdf_text)
