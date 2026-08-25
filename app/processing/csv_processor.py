import csv

from pathlib import Path

from pydantic import ValidationError

from app.models.transaction import Transaction


def process_csv(file_path: Path):
    valid_transactions = []
    invalid_transactions = []

    with file_path.open(mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row_number, row in enumerate(reader, start=2):
            try:
                transaction = Transaction(**row)
                valid_transactions.append(transaction)

            except ValidationError as error:
                invalid_transactions.append(
                    {
        "row_number": row_number,
        "row": row,
        "errors": error.errors(),
                    }
                )

    return valid_transactions, invalid_transactions




if __name__ == "__main__":
    sample_file = Path("sample_data/transactions.csv")

    valid, invalid = process_csv(sample_file)

    print(f"Valid transactions: {len(valid)}")
    print(f"Invalid transactions: {len(invalid)}")