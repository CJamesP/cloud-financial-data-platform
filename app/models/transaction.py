from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"

class Transaction(BaseModel):
    transaction_id: str = Field(min_length=1)
    transaction_date: date
    account_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    category: str = Field(min_length=1)
    amount: Decimal = Field(gt=0)
    transaction_type: TransactionType
