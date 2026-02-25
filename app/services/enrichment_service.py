from datetime import datetime
import json
from app.services.blob_service import upload_text, download_text


def enrich_material(blob_name: str):
    """
    Enrichment logic triggered by Event Grid.

    Flow:
    - Read JSON from raw-data container
    - Add enrichment metadata
    - Write enriched JSON to processed-data container
    """

    try:
        # 1️⃣ Read original file from raw-data
        original_content = download_text("raw-data", blob_name)

        # Convert string JSON to dict (if valid JSON)
        try:
            original_data = json.loads(original_content)
        except Exception:
            original_data = {"raw_content": original_content}

        # 2️⃣ Add enrichment fields
        enriched_data = {
            "original_data": original_data,
            "enriched_at": datetime.utcnow().isoformat(),
            "status": "enriched"
        }

        # 3️⃣ Write enriched output to processed-data
        upload_text(
            "processed-data",
            blob_name,
            json.dumps(enriched_data)
        )

        print(f"Enrichment completed for {blob_name}")

        return enriched_data

    except Exception as e:
        print(f"Enrichment failed for {blob_name}: {str(e)}")
        raise