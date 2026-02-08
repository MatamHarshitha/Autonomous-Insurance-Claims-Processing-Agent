# Autonomous-Insurance-Claims-Processing-Agent
This project implements an AI-powered insurance claims processing agent that automatically extracts structured information from insurance documents (PDFs), identifies missing mandatory fields, and recommends whether a claim can be auto-processed or requires manual review.

The system is designed to be modular, extensible, and production-ready, following best practices for document processing and AI-assisted extraction.

The solution follows a three-step pipeline:
Step 1: Document Text Extraction

Insurance documents (PDFs) are processed using a PDF text extraction utility.

The extracted raw text serves as input to the AI model.

Step 2: AI-Based Information Extraction

The extracted text is passed to a Large Language Model (LLM).

A structured prompt enforces:

JSON-only output

Predefined schema

null values for missing fields

Ignoring labels, placeholders, and form headings

The model extracts:

Policy information

Incident details

Involved parties

Asset details

Other mandatory claim fields

Step 3: Validation & Routing

The extracted JSON is validated.

Missing mandatory fields are identified.

Based on completeness, the system:

Recommends AUTO_PROCESSING or MANUAL_REVIEW

Provides a clear reasoning for the decision
