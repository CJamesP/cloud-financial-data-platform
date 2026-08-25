from pathlib import Path

from app.processing.csv_processor import process_csv


def test_process_csv_returns_valid_and_invalid_transactions():
    file_path = Path("sample_data/transactions.csv")

    valid, invalid = process_csv(file_path)

    assert len(valid) == 3
    assert len(invalid) == 5


def test_process_csv_tracks_invalid_row_number():
    file_path = Path("sample_data/transactions.csv")

    _, invalid = process_csv(file_path)

    assert invalid[0]["row_number"] == 5
    assert invalid[0]["row"]["transaction_id"] == "TXN-10004"


def test_process_csv_detects_duplicate_transaction_id():
    file_path = Path("sample_data/transactions.csv")

    _, invalid = process_csv(file_path)

    duplicate_record = next(
        record
        for record in invalid
        if record["errors"][0].get("type") == "duplicate_transaction"
    )

    assert duplicate_record["row_number"] == 8
    assert duplicate_record["row"]["transaction_id"] == "TXN-10001"