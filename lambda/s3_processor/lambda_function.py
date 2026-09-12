import json
from pathlib import Path
from urllib.parse import unquote_plus

import boto3

from app.processing.csv_processor import process_csv


s3 = boto3.client("s3")


def handler(event, context):
    print("Received S3 event:")
    print(json.dumps(event))

    results = []

    for record in event.get("Records", []):
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = unquote_plus(record["s3"]["object"]["key"])

        print(f"Processing: s3://{bucket_name}/{object_key}")

        local_file = Path("/tmp") / Path(object_key).name

        s3.download_file(
            bucket_name,
            object_key,
            str(local_file),
        )

        valid, invalid = process_csv(local_file)

        print(f"Valid transactions: {len(valid)}")
        print(f"Invalid transactions: {len(invalid)}")

        for invalid_record in invalid:
            print(
                f"Invalid row {invalid_record['row_number']}: "
                f"{invalid_record['errors']}"
            )

        results.append(
            {
                "bucket": bucket_name,
                "key": object_key,
                "valid_count": len(valid),
                "invalid_count": len(invalid),
            }
        )

    return {
        "statusCode": 200,
        "results": results,
    }