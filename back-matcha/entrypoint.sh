#!/bin/bash
set -e

echo "database seed..."
python ./seed/__init__.py

echo "Starting application..."
exec python app.py