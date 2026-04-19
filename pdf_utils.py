from pypdf import PdfReader

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = "\n".join(page.extract_text() for page in reader.pages)
    return text