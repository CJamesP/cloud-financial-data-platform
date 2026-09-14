#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

BUILD_DIR="$ROOT_DIR/build/lambda/s3_processor"

echo "Building Lambda package..."

rm -rf "$BUILD_DIR"

mkdir -p "$BUILD_DIR"
mkdir -p "$BUILD_DIR/app/models"
mkdir -p "$BUILD_DIR/app/processing"
mkdir -p "$BUILD_DIR/app/database"

# Lambda handler
cp \
    "$ROOT_DIR/lambda/s3_processor/lambda_function.py" \
    "$BUILD_DIR/"

# Root app package
cp \
    "$ROOT_DIR/app/__init__.py" \
    "$BUILD_DIR/app/"

# Pydantic transaction model
cp \
    "$ROOT_DIR/app/models/__init__.py" \
    "$ROOT_DIR/app/models/transaction.py" \
    "$BUILD_DIR/app/models/"

# CSV processing
cp \
    "$ROOT_DIR/app/processing/__init__.py" \
    "$ROOT_DIR/app/processing/csv_processor.py" \
    "$BUILD_DIR/app/processing/"

# Database code
cp \
    "$ROOT_DIR/app/database/__init__.py" \
    "$ROOT_DIR/app/database/config.py" \
    "$ROOT_DIR/app/database/database.py" \
    "$ROOT_DIR/app/database/models.py" \
    "$ROOT_DIR/app/database/repository.py" \
    "$BUILD_DIR/app/database/"

# Third-party Lambda dependencies
uv pip install \
    --target "$BUILD_DIR" \
    --requirement "$ROOT_DIR/lambda/s3_processor/requirements.txt"

echo "Lambda package ready:"
echo "$BUILD_DIR"