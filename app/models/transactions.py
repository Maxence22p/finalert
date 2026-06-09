from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TransactionStatus(str, Enum):
    success = "success"
    failed = "failed"
    pending = "pending"

class TransactionCreate(BaseModel):
    amount: float
    client_id: str
    status: TransactionStatus = TransactionStatus.pending
    retry_count: int = 0

class TransactionResponse(BaseModel):
    id: str
    amount: float
    client_id: str
    status: TransactionStatus
    retry_count: int
    created_at: datetime