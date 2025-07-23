from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import mysql.connector
import pandas as pd
import requests
import io
import matplotlib.pyplot as plt

app = FastAPI()

# 🗃️ MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "pass123",
    "database": "ecommerce"
}

# 🧾 Request Format
class Question(BaseModel):
    query: str
    visualize: bool = False
    stream: bool = False

# 🔍 Generate SQL using Ollama Phi
def generate_sql(question: str) -> str:
    prompt = f"""
You are an expert SQL generator. Given a user's natural language question, return only a valid MySQL query to answer it, using the ecommerce database schema. Don't add any explanation.

Schema: (example)
adsalesandmetrics(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold),
eligibilitytable(eligibility_datetime_utc, item_id, eligibility, message),
totalsalesandmetrics(date, item_id, total_sales, total_units_ordered)

Question: {question}
SQL:
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi", "prompt": prompt, "stream": False}
    )
    response.raise_for_status()
    text = response.json()["response"].strip()

    # Clean and return only SQL
    if ";" not in text:
        text += ";"
    return text.split(";")[0].strip() + ";"

# 🔎 Execute SQL
def fetch_data(sql_query: str) -> pd.DataFrame:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
    finally:
        cursor.close()
        conn.close()
    return df

# 📊 Create a plot if requested
def create_plot(df: pd.DataFrame) -> io.BytesIO:
    plt.figure(figsize=(10, 6))
    df.plot()
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# 🔁 For streaming output
def stream_text(text: str):
    for word in text.split():
        yield f"data: {word}\n\n"

# 🚀 Main endpoint
@app.post("/ask")
def answer(question: Question):
    try:
        # Step 1: Get SQL
        sql = generate_sql(question.query)

        # Step 2: Run SQL
        df = fetch_data(sql)

        # Step 3: Build base response
        result = df.to_dict(orient="records")
        response_data = {
            "question": question.query,
            "sql_query": sql,
            "result": result
        }

        # Step 4: Visualization
        if question.visualize and not df.empty:
            buf = create_plot(df)
            return StreamingResponse(buf, media_type="image/png")

        # Step 5: Streaming
        if question.stream:
            full_text = f"Question: {question.query}\nSQL: {sql}\nResult: {result}"
            return StreamingResponse(stream_text(full_text), media_type="text/event-stream")

        return JSONResponse(content=response_data)

    except mysql.connector.Error as sql_err:
        return JSONResponse(status_code=500, content={"error": f"MySQL Error: {sql_err}"})
    except requests.exceptions.RequestException as http_err:
        return JSONResponse(status_code=500, content={"error": f"Ollama Error: {http_err}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
