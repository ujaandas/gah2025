#!/bin/bash
# Comprehensive dependency installation script for API and Backend

echo "🔧 Installing ALL dependencies for API and Backend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📂 Project root: $PROJECT_ROOT"

# Install API dependencies
echo ""
echo "📦 Installing API dependencies..."
cd "$SCRIPT_DIR"
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ API dependencies installed"
else
    echo "❌ Failed to install API dependencies"
    exit 1
fi

# Install Backend dependencies (if venv exists, use it)
echo ""
echo "📦 Installing Backend dependencies..."

if [ -d "$PROJECT_ROOT/backend/venv" ]; then
    echo "   Using backend venv..."
    source "$PROJECT_ROOT/backend/venv/bin/activate"
    pip install -r "$PROJECT_ROOT/backend/requirements.txt"
    if [ $? -eq 0 ]; then
        echo "✅ Backend dependencies installed in venv"
    else
        echo "❌ Failed to install backend dependencies in venv"
        exit 1
    fi
else
    echo "   No venv found, installing globally..."
    pip install -r "$PROJECT_ROOT/backend/requirements.txt"
    if [ $? -eq 0 ]; then
        echo "✅ Backend dependencies installed globally"
    else
        echo "❌ Failed to install backend dependencies"
        exit 1
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All dependencies installed successfully!"
echo ""
echo "Key packages installed:"
echo "  • fastapi"
echo "  • uvicorn"
echo "  • pydantic"
echo "  • langgraph"
echo "  • langchain-core"
echo "  • ollama"
echo "  • httpx"
echo "  • grandalf"
echo ""
echo "You can now start the API:"
echo "  cd $SCRIPT_DIR"
echo "  uvicorn main:app --reload --port 8001"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

