# PubMed Symptom Knowledge Graph Analyzer

Automated medical decision support system that maps natural language symptom descriptions to clinical diagnoses. This tool utilizes a Neo4j Knowledge Graph and a local LLM to rank potential diseases using weighted TF-IDF scores derived from PubMed data.

---

## 1. Overview

The system provides a full-stack solution to bridge the gap between informal patient language and structured medical knowledge. It operates in two main phases:

1.  **Semantic Extraction**: A local LLM (Llama 3.2) parses raw text to identify standardized MeSH (Medical Subject Headings) terms.
2.  **Graph Classification**: Matches identified symptoms against a reference database of 147,978 relationships using weighted similarity scores.

---

## 2. Installation

### 2.1 Create Environment
```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
### 2.2 Install Dependencies

The system requires FastAPI for the backend, Neo4j for the database, and Ollama for the local AI:

``` Bash
pip install fastapi uvicorn neo4j pydantic pandas requests ollama
```
## 3. Setup Local Services

### 3.1 Ollama: Install from ollama.com and pull the model:


``` Bash
ollama pull llama3.2:1b
```
### 3.2 Neo4j

Ensure a local instance is running on port 7687.

Default User: neo4j

Password: Praktikum_DBMS_G6 (or as configured in your instance)
## Usage
### 4.1 Data Import

First, build the Knowledge Graph by running the import script:

``` Bash
python import_data.py
```
### 4.2 Start Application

Launch the FastAPI backend:

``` Bash
python main.py
```
### 4.3 Configuration & Access

Input: Open static/index.html in your browser and enter symptoms in natural language.

Backend: The server runs on http://127.0.0.1:8000.

Matching: The system calculates the sum of TF-IDF weights for all connected diseases.

## 5. How It Works
The analyzer utilizes high-precision graph features and local AI for clinical relevance:

* Zero-Shot Extraction: The LLM is strictly prompted to return only clinical MeSH terms, eliminating conversational noise.

* Normalization Pipeline: Automatically sanitizes AI output (capitalization and whitespace) to ensure exact matches with Neo4j nodes.

* TF-IDF Weighting: Scores diseases based on how specific a symptom is to a condition, rather than just frequency.

* Privacy-First Architecture: All medical data processing is performed 100% locally through Ollama, ensuring data protection.

## 6. Output
Results are displayed in a responsive web interface and include:

Identified Terms: The clinical MeSH terms extracted from the input.

Suggested Disease: The name of the matching reference condition.

Match Score: The confidence score based on the cumulative TF-IDF weights.

## 7. Project Structure
```text
├── static/           # Frontend: index.html and CSS styles
├── main.py           # FastAPI backend and LLM orchestration
├── import_data.py    # Data ingestion script for Neo4j
├── requirements.txt  # Project dependencies
└── README.md         # Documentation
```
Authors
```text
Lasha Beridze

Rodiana Koukouzeli

Malaz al Mahdi
```
Supervisors: Prof'in. Dr. Lena Wiese & Dr. Ahmed Al-Ghezi (Goethe University Frankfurt)
