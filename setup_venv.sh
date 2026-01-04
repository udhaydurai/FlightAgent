#!/bin/bash
# Setup script for virtual environment

echo "=========================================="
echo "Setting up Python Virtual Environment"
echo "=========================================="

# Check if venv already exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing venv..."
        rm -rf venv
    else
        echo "Using existing venv..."
        source venv/bin/activate
        pip install -r requirements.txt
        echo "✅ Virtual environment ready!"
        exit 0
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Virtual environment setup complete!"
echo "=========================================="
echo ""
echo "To activate in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To test the connection, run:"
echo "  python api/test_connection.py"
echo ""
