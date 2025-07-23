from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import pandas as pd
import requests

app = FastAPI()

# MySQL config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "pass123",
    "database": "ecommerce"
}

# Request model
class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(question: Question):
    prompt = f"""
You are an expert SQL generator. Given a user's natural language question, return only a valid MySQL query to answer it, using the ecommerce database schema.

Question: {question.query}
SQL:
"""

    try:
        # Step 1: Ask Ollama Phi
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()
        response_json = response.json()
        sql_query = response_json["response"].strip().split(";")[0] + ";"  # Extract SQL

        # Step 2: Run SQL on MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

        result = df.to_dict(orient="records")

        cursor.close()
        conn.close()

        return {
            "question": question.query,
            "sql_query": sql_query,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}
