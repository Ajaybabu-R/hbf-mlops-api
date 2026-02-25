from fastapi import FastAPI
from app.core.config import settings
from app.core.identity import get_azure_credential
from app.services.blob_service import upload_text, download_text
from app.api.ingestion import router as ingestion_router
from app.api.events import router as events_router
from app.core.keyvault import get_secret

app = FastAPI(title=settings.APP_NAME)

# Register routers
app.include_router(ingestion_router)
app.include_router(events_router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


@app.get("/identity-check")
def identity_check():
    cred = get_azure_credential()
    return {"identity_ready": cred is not None}


@app.get("/kv-test/{secret_name}")
def kv_test(secret_name: str):
    try:
        value = get_secret(secret_name)
        return {"secret_value": value}
    except Exception as e:
        return {"error": str(e)}


@app.post("/blob-test/{filename}")
def blob_upload_test(filename: str):
    upload_text("raw-data", filename, "Hello from Blob Storage 🚀")
    return {"uploaded": filename}


@app.get("/blob-test/{filename}")
def blob_download_test(filename: str):
    content = download_text("raw-data", filename)
    return {"content": content}