from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import requests
import os

app = FastAPI()

MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        # читаем бинарные данные
        excel_bytes = await file.read()

        # создаём поток
        excel_stream = io.BytesIO(excel_bytes)

        # Чётко указываем движок Excel
        df = pd.read_excel(excel_stream, engine="openpyxl")

        records = df.to_dict(orient="records")

        # отправляем обратно в Nodul Webhook
        if MAKE_WEBHOOK_URL:
            requests.post(MAKE_WEBHOOK_URL, json=records)

        return {
            "status": "success",
            "rows": len(records)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
