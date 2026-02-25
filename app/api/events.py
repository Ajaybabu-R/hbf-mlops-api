from fastapi import APIRouter, Request
from app.services.enrichment_service import enrich_material

router = APIRouter()

@router.post("/events")
async def handle_event(request: Request):
    events = await request.json()

    for event in events:

        # 1️⃣ Event Grid subscription validation
        if event.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
            return {
                "validationResponse": event["data"]["validationCode"]
            }

        # 2️⃣ Blob created event
        if event.get("eventType") == "Microsoft.Storage.BlobCreated":
            blob_url = event["data"]["url"]

            # Extract full blob name (with extension)
            blob_name = blob_url.split("/")[-1]

            enrich_material(blob_name)

    return {"status": "processed"}