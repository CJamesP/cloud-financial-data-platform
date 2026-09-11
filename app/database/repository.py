from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import TransactionRecord
from app.models.transaction import Transaction


def save_transactions(
    db: Session,
    transactions: list[Transaction],
) -> int:
    records = [
        TransactionRecord(
            transaction_id=transaction.transaction_id,
            transaction_date=transaction.transaction_date,
            account_id=transaction.account_id,
            description=transaction.description,
            category=transaction.category,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type.value,
        )
        for transaction in transactions
    ]

    db.add_all(records)
    db.commit()

    return len(records)


def get_transactions(db: Session) -> list[TransactionRecord]:
    statement = select(TransactionRecord).order_by(TransactionRecord.id)

    return list(db.scalars(statement).all())