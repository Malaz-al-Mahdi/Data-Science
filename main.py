import ollama
from fastapi import FastAPI
from neo4j import GraphDatabase
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# --- 1. Configuration ---
NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Praktikum_DBMS_G6"

app = FastAPI(title="Medical Symptom Analyzer (Local AI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

class SymptomRequest(BaseModel):
    text: str

# --- 2. Analysis Endpoint ---
@app.post("/analyze")
async def analyze_symptoms(request: SymptomRequest):
    identified_symptoms = []

    try:
        # Lokaler LLM Aufruf mit Ollama
        response = ollama.chat(model='llama3.2:1b', messages=[
            {
                'role': 'system',
                'content': 'You are a medical assistant. Extract symptoms and return ONLY a comma-separated list of MeSH terms.'
            },
            {
                'role': 'user',
                'content': f'Extract symptoms from: "{request.text}"'
            },
        ])

        # Ergebnis säubern
        raw_text = response['message']['content']
        identified_symptoms = [s.strip() for s in raw_text.split(",")]
        print(f"Ollama identified: {identified_symptoms}")

    except Exception as e:
        print(f"Ollama Error: {e}")
        identified_symptoms = ["Headache", "Fever"] # Minimaler Fallback

    # --- Neo4j Subgraph Matching ---
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Disease)-[r:HAS_SYMPTOM]->(s:Symptom)
            WHERE s.name IN $symptoms
            RETURN d.name AS disease, sum(r.tfidf) AS score
            ORDER BY score DESC 
            LIMIT 5
        """, symptoms=identified_symptoms)

        results = [dict(record) for record in result]

    return {
        "matched_mesh_terms": identified_symptoms,
        "diagnosis_suggestions": results,
        "engine": "Local Llama 3.2 via Ollama"
    }

if __name__ == "__main__":
    app.mount("/static", StaticFiles(directory="static"), name="static")
    uvicorn.run(app, host="0.0.0.0", port=8000)