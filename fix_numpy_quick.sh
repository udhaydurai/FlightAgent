#!/bin/bash
echo "Fixing NumPy compatibility..."
pip install "numpy<2.0.0" --force-reinstall --quiet
echo "✅ Done! Restart your Python session if needed."
