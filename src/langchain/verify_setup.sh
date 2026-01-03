#!/bin/bash
# Quick verification of all 10 setup steps

echo "🔍 LangChain Chatbot - Setup Verification"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Step 1: Python
echo "✅ Step 1/10: Python"
python3 --version 2>/dev/null && echo "   ✓ Python installed" || echo "   ✗ Python missing"
echo ""

# Step 2: Packages
echo "✅ Step 2/10: Python Packages"
python3 -c "import langchain_core" 2>/dev/null && echo "   ✓ langchain-core installed" || echo "   ✗ langchain-core missing"
python3 -c "import langchain_community" 2>/dev/null && echo "   ✓ langchain-community installed" || echo "   ✗ langchain-community missing"
python3 -c "import langchain_openai" 2>/dev/null && echo "   ✓ langchain-openai installed" || echo "   ✗ langchain-openai missing"
python3 -c "import streamlit" 2>/dev/null && echo "   ✓ streamlit installed" || echo "   ✗ streamlit missing"
python3 -c "import dotenv" 2>/dev/null && echo "   ✓ python-dotenv installed" || echo "   ✗ python-dotenv missing"
echo ""

# Step 3: Ollama (optional)
echo "✅ Step 3/10: Ollama (Optional)"
if command -v ollama &> /dev/null; then
    echo "   ✓ Ollama installed"
else
    echo "   ⚠️  Ollama not installed (optional - for free local AI)"
fi
echo ""

# Step 4: Ollama Server (optional)
echo "✅ Step 4/10: Ollama Server (Optional)"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✓ Ollama server running"
else
    echo "   ⚠️  Ollama server not running (optional)"
fi
echo ""

# Step 5: Models (optional)
echo "✅ Step 5/10: Ollama Models (Optional)"
if command -v ollama &> /dev/null; then
    if ollama list 2>/dev/null | grep -q "gemma2"; then
        echo "   ✓ gemma2 model downloaded"
    else
        echo "   ⚠️  No models downloaded (run: ollama pull gemma2:2b)"
    fi
else
    echo "   ⚠️  Ollama not available"
fi
echo ""

# Step 6: Environment File
echo "✅ Step 6/10: Environment Configuration"
if [ -f .env ]; then
    echo "   ✓ .env file exists"
else
    echo "   ✗ .env file missing"
fi
if [ -f .env.example ]; then
    echo "   ✓ .env.example exists"
else
    echo "   ✗ .env.example missing"
fi
echo ""

# Step 7: Chatbot Files
echo "✅ Step 7/10: Chatbot Files"
[ -f chatbot/app.py ] && echo "   ✓ app.py (OpenAI version)" || echo "   ✗ app.py missing"
[ -f chatbot/localama.py ] && echo "   ✓ localama.py (Ollama version)" || echo "   ✗ localama.py missing"
[ -f chatbot/demo_free.py ] && echo "   ✓ demo_free.py (FREE version)" || echo "   ✗ demo_free.py missing"
echo ""

# Step 8: Documentation
echo "✅ Step 8/10: Documentation"
[ -f README.md ] && echo "   ✓ README.md" || echo "   ✗ README.md missing"
[ -f HOW_TO_RUN.md ] && echo "   ✓ HOW_TO_RUN.md" || echo "   ✗ HOW_TO_RUN.md missing"
echo ""

# Step 9: Requirements
echo "✅ Step 9/10: Requirements Files"
[ -f requirements.txt ] && echo "   ✓ requirements.txt" || echo "   ✗ requirements.txt missing"
[ -f requirements_simple.txt ] && echo "   ✓ requirements_simple.txt" || echo "   ✗ requirements_simple.txt missing"
echo ""

# Step 10: Working Chatbot
echo "✅ Step 10/10: Chatbot Functionality"
if python3 -c "import streamlit, langchain_core" 2>/dev/null; then
    echo "   ✓ All core imports working"
    echo "   ✓ Ready to run chatbot!"
else
    echo "   ✗ Some imports failing"
fi
echo ""

echo "=========================================="
echo "📊 SUMMARY"
echo "=========================================="
echo ""

# Count ready versions
READY=0
echo "Available Chatbot Versions:"

if python3 -c "import streamlit, langchain_core" 2>/dev/null; then
    echo "   ✅ demo_free.py - FREE (No setup required)"
    READY=$((READY+1))
fi

if [ -f .env ] && grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "   ✅ app.py - OpenAI (API key configured)"
    READY=$((READY+1))
else
    echo "   ⚠️  app.py - OpenAI (needs API key in .env)"
fi

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ localama.py - Ollama (server running)"
    READY=$((READY+1))
else
    echo "   ⚠️  localama.py - Ollama (needs ollama serve)"
fi

echo ""
echo "🎯 READY TO USE: $READY/3 versions"
echo ""

echo "=========================================="
echo "🚀 HOW TO RUN"
echo "=========================================="
echo ""
echo "FREE Version (Works Now!):"
echo "   streamlit run chatbot/demo_free.py"
echo ""
echo "OpenAI Version (Need API Key):"
echo "   1. Add key to .env: OPENAI_API_KEY=sk-..."
echo "   2. streamlit run chatbot/app.py"
echo ""
echo "Ollama Version (Need Ollama):"
echo "   1. ollama serve"
echo "   2. ollama pull gemma2:2b"
echo "   3. streamlit run chatbot/localama.py"
echo ""
echo "=========================================="
