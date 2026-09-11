from decimal import Decimal

from app.database.models import TransactionRecord
from app.models.transaction import Transaction


def test_transaction_can_be_mapped_to_database_record():
    transaction = Transaction(
        transaction_id="TXN-TEST-001",
        transaction_date="2026-09-10",
        account_id="ACC-TEST",
        description="Test Transaction",
        category="Testing",
        amount="25.00",
        transaction_type="debit",
    )

    record = TransactionRecord(
        transaction_id=transaction.transaction_id,
        transaction_date=transaction.transaction_date,
        account_id=transaction.account_id,
        description=transaction.description,
        category=transaction.category,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type.value,
    )

    assert record.transaction_id == "TXN-TEST-001"
    assert record.amount == Decimal("25.00")
    assert record.transaction_type == "debit"