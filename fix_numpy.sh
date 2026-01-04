#!/bin/bash
# Fix NumPy compatibility issue

echo "Fixing NumPy compatibility issue..."
echo "Downgrading NumPy to < 2.0.0"

pip install "numpy<2.0.0" --force-reinstall

echo ""
echo "✅ NumPy downgraded. You may need to restart your Python session."
