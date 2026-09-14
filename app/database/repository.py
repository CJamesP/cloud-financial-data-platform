from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import TransactionRecord
from app.models.transaction import Transaction


def save_transactions(
    db: Session,
    transactions: list[Transaction],
) -> int:
    transaction_ids = [
        transaction.transaction_id
        for transaction in transactions
    ]

    existing_ids = set(
        db.scalars(
            select(TransactionRecord.transaction_id).where(
                TransactionRecord.transaction_id.in_(transaction_ids)
            )
        ).all()
    )

    new_transactions = [
        transaction
        for transaction in transactions
        if transaction.transaction_id not in existing_ids
    ]

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
        for transaction in new_transactions
    ]

    db.add_all(records)
    db.commit()

    return len(records)


def get_transactions(db: Session) -> list[TransactionRecord]:
    statement = select(TransactionRecord).order_by(TransactionRecord.id)

    return list(db.scalars(statement).all())