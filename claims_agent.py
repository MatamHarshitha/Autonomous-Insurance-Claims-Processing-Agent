


import json
import re
import os
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = None
_api_key = os.getenv("OPENAI_API_KEY")

if _api_key:
    client = OpenAI(api_key=_api_key)


def extract_fields_from_record(record_text):
    fields = {}

    patterns = {
        "Policy Number": r"POLICY NUMBER:\s*([^\n]*)",
        "Policyholder Name": r"INSURED NAME:\s*([^\n]*)",
        "Date": r"DATE OF LOSS:\s*([^\n]*)",
        "Location": r"LOCATION:\s*([^\n]*)",
        "Description": r"DESCRIPTION(?::| OF ACCIDENT:)\s*([^\n]*)",
        "Estimated Damage": r"ESTIMATE AMOUNT:\s*\$?([^\n]*)",
        "Claim Type": r"CLAIM TYPE:\s*([^\n]*)",
        "Contact Details": r"CONTACT:\s*([^\n]*)",
        "Time": r"TIME:\s*([^\n]*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, record_text, re.IGNORECASE)

        if match:
            value = match.group(1).strip()

            if (
                not value or
                "leave this blank" in value.lower() or
                "insured name" in value.lower() or
                "policy number" in value.lower()
            ):
                fields[key] = None
            else:
                fields[key] = value
        else:
            fields[key] = None

    fields["Asset Type"] = "Vehicle"

    return fields




def get_output_template():
    return {
        "Policy Number": None,
        "Policyholder Name": None,
        "Date": None,
        "Time": None,
        "Location": None,
        "Description": None,
        "Claimant": None,
        "Third Parties": None,
        "Contact Details": None,
        "Asset Type": "Vehicle",
        "Asset ID": None,
        "Estimated Damage": None,
        "Claim Type": None,
        "Attachments": None,
        "Initial Estimate": None
    }


def normalize_output(extracted):
    template = get_output_template()

    mapping = {
        "Policy Number": "Policy Number",
        "Policyholder Name": "Policyholder Name",
        "Date": "Date",
        "Location": "Location",
        "Description": "Description",
        "Estimated Damage": "Estimated Damage",
        "Claim Type": "Claim Type",
        "Contact Details": "Contact Details"
    }

    for key, value in mapping.items():
        if extracted.get(value):
            template[key] = extracted[value]

    if template["Policyholder Name"]:
        template["Claimant"] = template["Policyholder Name"]

    return template


def process_batch_fnol(full_text):
    records = re.split(r'(?=POLICY NUMBER:)', full_text)
    all_results = []

    for record in records:
        if not record.strip():
            continue

        extracted = extract_fields_from_record(record)
        normalized = normalize_output(extracted)

        mandatory_fields = ["Policy Number",
    "Policyholder Name",
    "Description",
    "Claim Type"]
        missing =  [
    f for f in mandatory_fields
    if not normalized.get(f) or str(normalized.get(f)).strip() == ""
]

        description = str(normalized.get("Description", "")).lower()
        damage_str = str(normalized.get("Estimated Damage", "0")).replace(",", "")

        try:
            damage = float(damage_str)
        except ValueError:
            damage = 0

        if missing:
            route = "Manual review"
            reasoning = f"Missing mandatory fields: {', '.join(missing)}"
        elif any(word in description for word in ["fraud", "inconsistent", "staged"]):
            route = "Investigation Flag"
            reasoning = "Suspicious keywords detected in description."
        elif "injury" in str(normalized.get("Claim Type", "")).lower() or "injury" in description:
            route = "Specialist Queue"
            reasoning = "Claim involves potential injuries."
        elif damage < 25000:
            route = "Fast-track"
            reasoning = f"Damage amount ${damage} is below the $25,000 threshold."
        else:
            route = "Standard Review"
            reasoning = "Claim meets standard processing criteria."

        all_results.append({
            "extractedFields": normalized,
            "missingFields": missing,
            "recommendedRoute": route,
            "reasoning": reasoning
        })

    return all_results


def load_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


if __name__ == "__main__":
    files = ["ACORD-Automobile-Loss-Notice-12.05.16 (1).pdf", "dummy.pdf"]

    for file_name in files:
        text = load_pdf_text(file_name)
        result = process_batch_fnol(text)
        print(json.dumps(result, indent=4))