from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import requests
import os

app = FastAPI()

# Корневой маршрут — ОБЯЗАТЕЛЕН для Render
@app.get("/")
def root():
    return {"status": "ok", "service": "excel-json-server"}

# Webhook Nodul
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        excel_stream = io.BytesIO(await file.read())
        df = pd.read_excel(excel_stream)

        records = df.to_dict(orient="records")

        if MAKE_WEBHOOK_URL:
            requests.post(MAKE_WEBHOOK_URL, json=records)

        return {"status": "success", "rows": len(records)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
