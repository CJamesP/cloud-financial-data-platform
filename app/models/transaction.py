from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


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

    @field_validator(
        "transaction_id",
        "account_id",
        "description",
        "category",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError("must not be blank")

        return stripped_value


class TransactionRead(Transaction):
    id: int

    model_config = ConfigDict(from_attributes=True)