from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from app.services.blob_service import upload_text

router = APIRouter()


class IngestionRequest(BaseModel):
    material_name: str
    description: str
    source: str


@router.post("/ingest")
def ingest_material(request: IngestionRequest):
    ingestion_id = str(uuid4())

    metadata = {
        "ingestion_id": ingestion_id,
        "material_name": request.material_name,
        "description": request.description,
        "source": request.source,
        "created_at": datetime.utcnow().isoformat()
    }

    # Store metadata as JSON file in Blob
    blob_name = f"{ingestion_id}.json"
    upload_text("raw-data", blob_name, str(metadata))

    return {
        "status": "ingested",
        "ingestion_id": ingestion_id
    }