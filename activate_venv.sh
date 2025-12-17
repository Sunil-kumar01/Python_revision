#!/bin/bash
# Quick activation script for the Langchain virtual environment

echo "🚀 Activating Langchain Virtual Environment..."
echo ""
source "$(dirname "$0")/src/Langchain_project/.venv/bin/activate"
echo "✅ Virtual Environment Active!"
echo "   You'll see (.venv) in your prompt"
echo ""
echo "📝 Quick commands:"
echo "   python src/Langchain_project/weather.py  - Run weather app"
echo "   deactivate                                 - Exit virtual environment"
echo ""
