# Autonomous Insurance Claims Processing Agent

This project is a lightweight system for processing First Notice of Loss (FNOL) insurance claim documents in PDF format. It extracts structured information, identifies missing fields, and routes claims to appropriate workflows using rule-based logic.

---

## Overview

The system processes insurance claim PDFs and performs:

- Text extraction from PDF documents
- Structured field extraction using regex patterns
- Validation of mandatory claim fields
- Rule-based claim routing
- JSON output generation for downstream systems

---

## Features

###  PDF Processing
- Extracts raw text from FNOL PDF documents using `pdfplumber`

###  Field Extraction
- Uses regex patterns to extract key insurance claim fields such as:
  - Policy Number
  - Policyholder Name
  - Date of Loss
  - Location
  - Description of Incident
  - Estimated Damage
  - Claim Type
  - Contact Details
  - Time of Incident

###  Data Validation
- Identifies missing or incomplete mandatory fields
- Normalizes extracted values into a structured format

###  Claim Routing Engine
Routes claims based on business rules:

- Missing mandatory fields → **Manual Review**
- Suspicious keywords (fraud indicators) → **Investigation Flag**
- Injury-related claims → **Specialist Queue**
- Damage < $25,000 → **Fast-track Processing**
- Damage ≥ $25,000 → **Standard Review**

###  Output
- Returns structured JSON output per claim
- Supports batch processing of multiple FNOL records

---

## Processing Pipeline

1. **PDF Extraction**
   - Extract text using `pdfplumber`

2. **Record Segmentation**
   - Split multiple claims using policy number markers

3. **Field Extraction**
   - Apply regex patterns to extract structured data

4. **Normalization**
   - Map extracted fields into a standard schema

5. **Validation**
   - Detect missing mandatory fields

6. **Routing Decision**
   - Apply rule-based classification logic

7. **Output Generation**
   - Return structured JSON result

---

## Routing Rules

| Condition | Route |
|----------|------|
| Missing mandatory fields | Manual Review |
| Fraud-related keywords detected | Investigation Flag |
| Injury in claim type or description | Specialist Queue |
| Estimated damage < $25,000 | Fast-track |
| Estimated damage ≥ $25,000 | Standard Review |

---

## Mandatory Fields

The system expects the following core fields:

- Policy Number
- Policyholder Name
- Date of Loss
- Time of Incident
- Location
- Description of Incident
- Claim Type
- Contact Details
- Estimated Damage

---

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd claims-agent