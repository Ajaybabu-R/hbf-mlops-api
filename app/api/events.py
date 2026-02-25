from fastapi import APIRouter, Request
from app.services.enrichment_service import enrich_material

router = APIRouter()


@router.post("/events")
async def handle_event(request: Request):
    events = await request.json()

    for event in events:
        # Event Grid validation event
        if event.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
            return {"validationResponse": event["data"]["validationCode"]}

        # Blob created event
        if event.get("eventType") == "Microsoft.Storage.BlobCreated":
            blob_url = event["data"]["url"]
            ingestion_id = blob_url.split("/")[-1].replace(".json", "")
            enrich_material(ingestion_id)

    return {"status": "processed"}