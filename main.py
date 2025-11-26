from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import requests
import os

app = FastAPI()

# Webhook Nodul — куда отправляем JSON
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")


@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        # Чтение Excel из бинарного потока
        excel_stream = await file.read()
        df = pd.read_excel(io.BytesIO(excel_stream), engine="openpyxl")

        # Excel → JSON
        records = df.to_dict(orient="records")

        # Если есть вебхук Nodul — отправляем в Nodul
        if MAKE_WEBHOOK_URL:
            requests.post(MAKE_WEBHOOK_URL, json={"data": records})

        return {
            "status": "success",
            "rows": len(records),
            "data": records
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

