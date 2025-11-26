from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import os
import requests

from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)

app = FastAPI()

# Webhook NODUL куда отправляем JSON
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")


@app.get("/")
async def home():
    return {"status": "ok", "message": "Excel JSON server is running. Use POST /upload"}


# Swagger UI вручную (Render не подхватывает стандартный)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Swagger UI"
    )


@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        # читаем Excel
        excel_bytes = await file.read()
        excel_stream = io.BytesIO(excel_bytes)

        df = pd.read_excel(excel_stream)
        records = df.to_dict(orient="records")

        # отправляем JSON в Nodul/Maker
        if MAKE_WEBHOOK_URL:
            requests.post(MAKE_WEBHOOK_URL, json=records)

        return {"status": "success", "rows": len(records)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
