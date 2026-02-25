from datetime import datetime
from app.services.blob_service import upload_text, download_text


def enrich_material(ingestion_id: str):
    """
    Enrichment logic triggered by Event Grid.
    Current version:
    - Reads metadata JSON from raw-data container
    - Adds enrichment timestamp
    - Writes enriched file to processed-data container
    """

    try:
        # Read original metadata
        blob_name = f"{ingestion_id}.json"
        content = download_text("raw-data", blob_name)

        enriched_data = {
            "ingestion_id": ingestion_id,
            "original_content": content,
            "enriched_at": datetime.utcnow().isoformat(),
            "status": "enriched"
        }

        # Save enriched file
        upload_text(
            "processed-data",
            blob_name,
            str(enriched_data)
        )

        print(f"Enrichment completed for {ingestion_id}")

        return enriched_data

    except Exception as e:
        print(f"Enrichment failed for {ingestion_id}: {str(e)}")
        raise