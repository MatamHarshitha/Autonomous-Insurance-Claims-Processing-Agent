from llm import extractinfo
from code import extract_text_from_pdf


def routingroutes(extracted_fields):
    missing_fields = []
    mandatory_checks = {
        "Policy Number": extracted_fields["policyInformation"]["policyNumber"],
        "Incident Date": extracted_fields["incidentInformation"]["date"],
        "Incident Description": extracted_fields["incidentInformation"]["description"],
        "Estimated Damage": extracted_fields["assetDetails"]["estimatedDamage"],
        "Claim Type": extracted_fields["otherMandatoryFields"]["claimType"]
    }
    for field, value in mandatory_checks.items():
        if value is None or not value or value.strip() == "":
            missing_fields.append(field)
    
    description = extracted_fields["incidentInformation"]["description"]
    claim_type = extracted_fields["otherMandatoryFields"]["claimType"]
    damage = extracted_fields["assetDetails"]["estimatedDamage"]
    if missing_fields:
        route = "MANUAL_REVIEW"
        reason = "Mandatory fields are missing."
    elif any(word in description for word in ["fraud", "inconsistent", "staged"]):
        route = "INVESTIGATION"
        reason = "Accident description contains potential fraud indicators."
    elif "injury" in claim_type:
        route = "SPECIALIST_QUEUE"
        reason = "Claim involves injury and requires specialist handling."
    elif damage.isdigit() and int(damage) < 25000:
        route = "FAST_TRACK"
        reason = "Estimated damage is below 25,000 and all mandatory fields are present."
    else:
        route = "MANUAL_REVIEW"
        reason = "Claim does not meet fast-track criteria."


    return {
        "route": route,
        "reason": reason,
        "missing_fields": missing_fields
    }


text = extract_text_from_pdf("docs/insurance.pdf")
extracted_fields = extractinfo(text)
# print(routingroutes(extracted_fields))


routing_result = routingroutes(extracted_fields)

final_output = {
    "extractedFields": extracted_fields,
    "missingFields": routing_result["missing_fields"],
    "recommendedRoute": routing_result["route"],
    "reasoning": routing_result["reason"]
}

import json
print(json.dumps(final_output, indent=2))
