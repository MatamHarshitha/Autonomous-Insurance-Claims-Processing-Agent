import pdfplumber
import pandas as pd

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


acord_text = extract_text_from_pdf("ACORD-Automobile-Loss-Notice-12.05.16 (1).pdf")
dummy_text = extract_text_from_pdf("dummydata.pdf")
print("ACORD PDF Text:")
print(acord_text)
print("\n" + "="*50 + "\n")
print("Dummy Data PDF Text:")
print(dummy_text)
