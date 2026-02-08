
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
llm = OpenAI()

def extractinfo(text):
    prompt = f"""
You are an insurance claims assistant.

Rules:
- Return ONLY valid JSON
- Use exact field names
- If a value is missing, return null
- Do NOT add explanations

JSON format:
{{
  "policyInformation": {{
    "policyNumber": null,
    "policyholderName": null,
    "effectiveDates": null
  }},
  "incidentInformation": {{
    "date": null,
    "time": null,
    "location": null,
    "description": null
  }},
  "involvedParties": {{
    "claimant": null,
    "thirdParties": null,
    "contactDetails": null
  }},
  "assetDetails": {{
    "assetType": null,
    "assetId": null,
    "estimatedDamage": null
  }},
  "otherMandatoryFields": {{
    "claimType": null,
    "attachments": null,
    "initialEstimate": null
  }}
}}

Text:
{text}
"""
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return json.loads(response.choices[0].message.content)
