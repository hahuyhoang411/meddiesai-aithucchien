#!/bin/bash

# Setup script for meddies-ai project
# This script installs uv, creates a virtual environment with Python 3.11, and syncs dependencies

set -e  # Exit on any error

echo "🚀 Setting up meddies-ai project..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv from astral..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Verify installation
    if ! command -v uv &> /dev/null; then
        echo "❌ Failed to install uv. Please install manually from https://astral.sh/uv/"
        exit 1
    fi
    echo "✅ uv installed successfully"
else
    echo "✅ uv is already installed"
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "🐍 Creating virtual environment with Python 3.11..."
    uv venv --python 3.11
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and sync dependencies
echo "📋 Syncing dependencies with uv..."
uv sync

echo "🎉 Setup complete! You can now activate the virtual environment with:"
echo "   source .venv/bin/activate"
