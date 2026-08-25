from pathlib import Path

from app.processing.csv_processor import process_csv

def test_process_csv_returns_valid_and_invalid_transactions():
    file_path = Path("sample_data/transactions.csv")

    valid, invalid = process_csv(file_path)

    assert len(valid) == 3
    assert len(invalid) == 3
    assert invalid[0]["row_number"] == 5
    assert invalid[0]["row"]["transaction_id"] == "TXN-10004"