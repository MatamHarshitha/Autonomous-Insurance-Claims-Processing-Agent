# Autonomous-Insurance-Claims-Processing-Agent
This project implements an AI-powered insurance claims processing agent that automatically extracts structured information from insurance documents (PDFs), identifies missing mandatory fields, and recommends whether a claim can be auto-processed or requires manual review.

The system is designed to be modular, extensible, and production-ready, following best practices for document processing and AI-assisted extraction.

The solution follows a three-step pipeline:

Step 1: Document Text Extraction

•	Insurance documents (PDFs) are processed using a PDF text extraction utility.

•	The extracted raw text serves as input to the AI model.

Step 2: AI-Based Information Extraction

•	The extracted text is passed to a Large Language Model (LLM).

•	A structured prompt enforces:

•	JSON-only output

•	Predefined schema

•	null values for missing fields

•	Ignoring labels, placeholders, and form headings

•	The model extracts:

•	Policy information

•	Incident details

•	Involved parties

•	Asset details

•	Other mandatory claim fields

Step 3: Validation & Routing

•	The extracted JSON is validated.

•	Missing mandatory fields are identified.

•	Based on completeness, the system:

•	Recommends AUTO_PROCESSING or MANUAL_REVIEW

•	Provides a clear reasoning for the decision




Tech Stack
•	Python 3.11+
•	OpenAI API
•	PDF text extraction
•	dotenv for environment variable management
•	Git for version control



Steps to Run:
1.	 Clone the repository:
git clone https://github.com/xyz/Autonomous-Insurance-Claims-Processing-Agent.git
cd Autonomous-Insurance-Claims-Processing-Agent

2.	Create and activate a virtual environment:
Windows:
python -m venv venv
venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

3.	Install dependencies:
pip install -r requirements.txt

4.	Set environment variables:
Create a .env file in the project root:
OPENAI_API_KEY=”your_openai_api_key_here”

5.	Run the claims processing pipeline:
python src/routing.py

6.	Project Structure:
├── docs/                   # Input insurance documents (PDFs)
├── src/
│   ├── code.py              # PDF text extraction logic
│   ├── llm.py               # LLM prompt + extraction logic
│   ├── routing.py           # Final validation & routing (ENTRY POINT)
│   └── __pycache__/
├── .env.example             # Environment variable template
├── .gitignore
├── README.md
├── requirements.txt
└── venv/                    # Local virtual environment (ignored)


