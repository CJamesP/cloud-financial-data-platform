from pathlib import Path

from app.database.database import SessionLocal
from app.database.repository import save_transactions
from app.processing.csv_processor import process_csv


def import_csv(file_path: Path):
    valid_transactions, invalid_transactions = process_csv(file_path)

    with SessionLocal() as db:
        saved_count = save_transactions(db, valid_transactions)

    return {
        "saved_count": saved_count,
        "invalid_count": len(invalid_transactions),
        "invalid_transactions": invalid_transactions,
    }


if __name__ == "__main__":
    result = import_csv(Path("sample_data/transactions.csv"))

    print(f"Saved transactions: {result['saved_count']}")
    print(f"Invalid transactions: {result['invalid_count']}")