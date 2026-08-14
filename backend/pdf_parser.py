import io
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes


def is_scanned(pdf_bytes: bytes) -> bool:
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    return len(text.strip()) < 50

# kotak
def extract_tables_native(pdf_bytes: bytes) -> list:
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        rows = []
        for i, page in enumerate(pdf.pages):
            table = page.extract_table()
            if table:
                rows.extend(table)
    return rows

def extract_tables_native(pdf_bytes: bytes) -> list:
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        rows = []
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            if not tables:
                fallback = page.extract_table(table_settings={
                    "vertical_strategy": "text",
                    "horizontal_strategy": "text",
                })
                tables = [fallback] if fallback else []

            page_row_count = sum(len(t) for t in tables)

            for table in tables:
                rows.extend(table)
    return rows


def extract_text_ocr(pdf_bytes: bytes) -> str:
    images = convert_from_bytes(pdf_bytes)
    pages = [pytesseract.image_to_string(img) for img in images]
    return "\n".join(pages)


# def parse_pdf(uploaded_file) -> str:
#     uploaded_file.seek(0)
#     pdf_bytes = uploaded_file.read()

#     if not pdf_bytes.startswith(b"%PDF"):
#         raise ValueError("Uploaded file is not a valid PDF.")

#     if is_scanned(pdf_bytes):
#         return extract_text_ocr(pdf_bytes)
#     return extract_text_native(pdf_bytes)