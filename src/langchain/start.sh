#!/bin/bash
# Quick start script for the chatbot

cd "$(dirname "$0")"

echo "🚀 Starting Chatbot..."
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv .venv"
    echo "Then: source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running!"
    echo "Start Ollama first, then run this script again"
    exit 1
fi

echo "✅ Ollama is running"
echo "✅ Starting Streamlit app..."
echo ""
echo "📍 Access at: http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

.venv/bin/python -m streamlit run chatbot/localama.py
