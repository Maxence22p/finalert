from fastapi import APIRouter, HTTPException
from app.models.transaction import TransactionCreate, TransactionResponse
from app.database import get_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=dict)
async def create_transaction(transaction: TransactionCreate):
    collection = get_collection("transactions")
    doc = transaction.model_dump()
    doc["created_at"] = datetime.utcnow()
    result = await collection.insert_one(doc)
    return {"id": str(result.inserted_id), "message": "Transaction créée"}

@router.get("/")
async def list_transactions(status: str = None, limit: int = 20):
    collection = get_collection("transactions")
    query = {}
    if status:
        query["status"] = status
    cursor = collection.find(query).limit(limit)
    results = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        results.append(doc)
    return results

@router.get("/{transaction_id}")
async def get_transaction(transaction_id: str):
    collection = get_collection("transactions")
    doc = await collection.find_one({"_id": ObjectId(transaction_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    doc["id"] = str(doc.pop("_id"))
    return doc