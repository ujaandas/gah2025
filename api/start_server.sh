#!/bin/bash

# Startup script for LangGraph Testing Platform API

echo "🚀 Starting LangGraph Testing Platform API..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if uvicorn is installed
if ! command -v uvicorn &> /dev/null; then
    echo "❌ uvicorn not found. Please install dependencies:"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the api directory
cd "$SCRIPT_DIR"

echo "📂 Working directory: $(pwd)"
echo "🌐 Server will be available at: http://localhost:8000"
echo "📚 API docs: http://localhost:8000/docs"
echo "📖 ReDoc: http://localhost:8000/redoc"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the server
uvicorn main:app --reload --port 8000 --host 0.0.0.0

