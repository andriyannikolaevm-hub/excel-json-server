from fastapi import FastAPI, UploadFile, File
import pandas as pd
import requests

MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/ВСТАВИШЬ_ПОЗЖЕ"

app = FastAPI()

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)
    df.columns = [c.strip().lower() for c in df.columns]

    name_col = next((c for c in df.columns if c in ["наименование работ", "name", "работа"]), None)
    unit_col = next((c for c in df.columns if c in ["единица измерения", "unit", "ед"]), None)

    records = [{"name": str(row[name_col]), "unit": str(row[unit_col])} for _, row in df.iterrows()]

    requests.post(MAKE_WEBHOOK_URL, json=records)

    return {"sent": len(records), "ok": True}
