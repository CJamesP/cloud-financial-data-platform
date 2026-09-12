#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

BUILD_DIR="$ROOT_DIR/build/lambda/s3_processor"

echo "Building Lambda package..."

rm -rf "$BUILD_DIR"

mkdir -p "$BUILD_DIR"
mkdir -p "$BUILD_DIR/app/models"
mkdir -p "$BUILD_DIR/app/processing"

# Lambda handler
cp \
    "$ROOT_DIR/lambda/s3_processor/lambda_function.py" \
    "$BUILD_DIR/"

# Python package files
cp \
    "$ROOT_DIR/app/__init__.py" \
    "$BUILD_DIR/app/"

cp \
    "$ROOT_DIR/app/models/__init__.py" \
    "$ROOT_DIR/app/models/transaction.py" \
    "$BUILD_DIR/app/models/"

cp \
    "$ROOT_DIR/app/processing/__init__.py" \
    "$ROOT_DIR/app/processing/csv_processor.py" \
    "$BUILD_DIR/app/processing/"

# Third-party Lambda dependencies
uv pip install \
    --target "$BUILD_DIR" \
    --requirement "$ROOT_DIR/lambda/s3_processor/requirements.txt"

echo "Lambda package ready:"
echo "$BUILD_DIR"