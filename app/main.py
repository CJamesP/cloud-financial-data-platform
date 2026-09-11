from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.repository import get_transactions
from app.models.transaction import TransactionRead


app = FastAPI()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "financial-data-api",
    }


@app.get("/transactions", response_model=list[TransactionRead])
def read_transactions(
    db: Annotated[Session, Depends(get_db)],
):
    return get_transactions(db)