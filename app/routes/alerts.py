from fastapi import APIRouter
from app.database import get_collection

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/")
async def get_alerts():
    """Retourne les transactions failed avec retry_count > 3"""
    collection = get_collection("transactions")
    query = {
        "status": "failed",
        "retry_count": {"$gt": 3}
    }
    cursor = collection.find(query)
    alerts = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        alerts.append(doc)
    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }
