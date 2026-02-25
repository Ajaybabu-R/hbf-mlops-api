from datetime import datetime
import json
from app.services.blob_service import upload_text, download_text, blob_exists


def enrich_material(blob_name: str):
    """
    Idempotent enrichment logic triggered by Event Grid.

    Flow:
    - If already enriched → skip
    - Read JSON from raw-data
    - Add enrichment metadata
    - Write enriched JSON to processed-data
    """

    try:
        # 🛑 Idempotency Check
        if blob_exists("processed-data", blob_name):
            print(f"Skipping enrichment — already processed: {blob_name}")
            return {"status": "already_processed"}

        # 1️⃣ Read original file
        original_content = download_text("raw-data", blob_name)

        try:
            original_data = json.loads(original_content)
        except Exception:
            original_data = {"raw_content": original_content}

        # 2️⃣ Enrich data
        enriched_data = {
            "original_data": original_data,
            "enriched_at": datetime.utcnow().isoformat(),
            "status": "enriched"
        }

        # 3️⃣ Write enriched output
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