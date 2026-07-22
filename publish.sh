#!/bin/bash
# publish.sh - Automated script to build and publish to PyPI

set -e

echo "🔨 Building package..."
python -m build

echo "📦 Uploading to PyPI..."
python -m twine upload dist/* --non-interactive

echo "✅ Package published successfully!"
echo "📍 View at: https://pypi.org/project/car-rental-api/"
