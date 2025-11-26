from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import requests
import os

app = FastAPI()

# Webhook Nodul / Make куда отправляем JSON
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")

@app.post("/upload")
async def upload_excel(file: bytes = File(...)):
    try:
        # Загружаем Excel из байтов
        excel_stream = io.BytesIO(file)

        df = pd.read_excel(excel_stream)

        records = df.to_dict(orient="records")

        # отправка обратно в Nodul
        if MAKE_WEBHOOK_URL:
            requests.post(MAKE_WEBHOOK_URL, json=records)

        return {"status": "success", "rows": len(records)}

    except Exception as e:
        return {"status": "error", "message": str(e)}

