
import json
import re
import pdfplumber


def extract_fields_from_record(record_text):
    fields = {}

    patterns = {
         "Policy Number": r"POLICY NUMBER:\s*([A-Z0-9\-]+)",
    "Policyholder Name": r"INSURED NAME:\s*([A-Za-z ]+)",
    "Date": r"DATE OF LOSS:\s*([\d/]+)",
    "Time": r"TIME:\s*([^\n\r]*)",
    "Location": r"LOCATION:\s*([^\n\r]*)",
    "Description": r"DESCRIPTION(?: OF ACCIDENT)?:\s*(.*?)(?=ESTIMATE|CLAIM TYPE|$)",
    "Estimated Damage": r"ESTIMATE AMOUNT:\s*\$?([\d,\.]+)",
    "Initial Estimate": r"INITIAL ESTIMATE:\s*\$?([\d,\.]+)",   
    "Claim Type": r"CLAIM TYPE:\s*([A-Za-z ]+)",
    "Contact Details": r"CONTACT:\s*([^\n\r]*)",
    "Asset ID": r"ASSET ID:\s*([A-Z0-9\-]+)",                  
    "Third Parties": r"THIRD PARTIES:\s*([^\n\r]*)",           
    "Attachments": r"ATTACHMENTS:\s*([^\n\r]*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, record_text, re.IGNORECASE | re.DOTALL)

        if match:
            value = match.group(1).strip()
            value = value.replace("\n", " ").strip()

            if (
                not value or
                "acord" in value.lower() or
                "corporation" in value.lower() or
                "page" in value.lower()
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

    for key in template:
        if key in extracted:
            template[key] = extracted[key]

    if template["Policyholder Name"]:
        template["Claimant"] = template["Policyholder Name"]

    return template


def process_fnol(full_text):
  
    extracted = extract_fields_from_record(full_text)
    normalized = normalize_output(extracted)

    mandatory_fields = [
        "Policy Number",
        "Policyholder Name",
        "Description",
        "Claim Type"
    ]

    missing = [
        f for f in mandatory_fields
        if not normalized.get(f)
    ]

   
    description = str(normalized.get("Description", "")).lower()
    damage_str = str(normalized.get("Estimated Damage", "0")).replace(",", "")

    try:
        damage = float(damage_str)
    except:
        damage = 0

    if missing:
        route = "Manual review"
        reasoning = "Missing mandatory fields: " + ", ".join(missing)
    elif any(word in description for word in ["fraud", "inconsistent", "staged"]):
        route = "Investigation Flag"
        reasoning = "Suspicious keywords detected in description."
    elif "injury" in description:
        route = "Specialist Queue"
        reasoning = "Claim involves potential injuries."
    elif damage < 25000:
        route = "Fast-track"
        reasoning = f"Damage amount ${damage} is below threshold."
    else:
        route = "Standard Review"
        reasoning = "Claim meets standard processing criteria."

    return [{
        "extractedFields": normalized,
        "missingFields": missing,
        "recommendedRoute": route,
        "reasoning": reasoning
    }]


def load_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


if __name__ == "__main__":
    files = [
        "ACORD-Automobile-Loss-Notice-12.05.16 (1).pdf",
        "dummy.pdf"
    ]

    for file_name in files:
        print(f"\nProcessing file: {file_name}\n")

        text = load_pdf_text(file_name)
        result = process_fnol(text)

        print(json.dumps(result, indent=4))