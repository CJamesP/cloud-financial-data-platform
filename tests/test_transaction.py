from decimal import Decimal
import pytest
from pydantic import ValidationError

from app.models.transaction import Transaction, TransactionType

def test_valid_transaction():
    transaction = Transaction(
        transaction_id="TXN-10001",
        transaction_date="2026-08-15",
        account_id="ACC-001",
        description="Grocery Store",
        category="Groceries",
        amount="84.37",
        transaction_type="debit",
    )

def test_transaction_rejects_zero_amount():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TXN-10002",
            transaction_date="2026-08-15",
            account_id="ACC-001",
            description="Test Transaction",
            category="Test",
            amount="0",
            transaction_type="debit",
        )

def test_transaction_rejects_negative_amount():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TXN-10003",
            transaction_date="2026-08-15",
            account_id="ACC-001",
            description="Test Transaction",
            category="Test",
            amount="-20.00",
            transaction_type="debit",
        )

def test_transaction_rejects_blank_id():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="",
            transaction_date="2026-08-15",
            account_id="ACC-001",
            description="Test Transaction",
            category="Test",
            amount="10",
            transaction_type="debit",
        )