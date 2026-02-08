import pymupdf

def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    page=""

    for text in doc:
        page+=text.get_text()+"\n"

    doc.close()
    return page



pdf_path="docs\insurance.pdf"




