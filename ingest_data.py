import pandas as pd
import numpy as np
import requests
from io import StringIO
from neo4j import GraphDatabase

# URLs from the Aufgabenstellung
URL_DISEASES = "https://static-content.springer.com/esm/art%3A10.1038%2Fncomms5212/MediaObjects/41467_2014_BFncomms5212_MOESM1043_ESM.txt"
URL_SYMPTOMS = "https://static-content.springer.com/esm/art%3A10.1038%2Fncomms5212/MediaObjects/41467_2014_BFncomms5212_MOESM1044_ESM.txt"
URL_GRAPH = "https://static-content.springer.com/esm/art%3A10.1038%2Fncomms5212/MediaObjects/41467_2014_BFncomms5212_MOESM1045_ESM.txt"

# Connection with a Neo4j database which would be installed localy
URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "Praktikum_DBMS_G6"

def load_data(url):
    r = requests.get(url)
    return pd.read_csv(StringIO(r.text), sep='\t')

def main():
    # load the Data from the URL's
    df_dis = load_data(URL_DISEASES)
    df_sym = load_data(URL_SYMPTOMS)
    df_edges = load_data(URL_GRAPH)

    df_edges.columns = ['symptom_name', 'disease_name', 'occurrence', 'tfidf']

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("Importiere Daten in Neo4j...")

        session.run("UNWIND $data AS row MERGE (:Disease {name: row['MeSH Disease Term']})",
                    data=df_dis.to_dict('records'))

        session.run("UNWIND $data AS row MERGE (:Symptom {name: row['MeSH Symptom Term']})",
                    data=df_sym.to_dict('records'))

        session.run("""
            UNWIND $data AS row
            MATCH (d:Disease {name: row.disease_name})
            MATCH (s:Symptom {name: row.symptom_name})
            MERGE (d)-[r:HAS_SYMPTOM]->(s)
            SET r.co_occurrence = toFloat(row.occurrence),
                r.tfidf = toFloat(row.tfidf)
        """, data=df_edges.to_dict('records'))

    driver.close()
    print("Import erfolgreich abgeschlossen!")

if __name__ == "__main__":
    main()
