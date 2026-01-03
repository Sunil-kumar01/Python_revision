#!/bin/bash
# Complete setup script for LangChain chatbot

set -e  # Exit on error

echo "🚀 LangChain Chatbot - Complete Setup"
echo "======================================"
echo ""

cd "$(dirname "$0")"

# Step 1: Check Python
echo "✅ Step 1/10: Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Install Python 3.8+"
    exit 1
fi
python3 --version
echo ""

# Step 2: Install Python dependencies
echo "✅ Step 2/10: Installing Python packages..."
pip install -r requirements.txt --quiet
echo "Installed: langchain, streamlit, ollama packages"
echo ""

# Step 3: Check if Ollama is installed
echo "✅ Step 3/10: Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not installed!"
    echo "Install with: brew install ollama"
    echo "Or download from: https://ollama.ai/download"
    echo ""
    read -p "Continue without Ollama? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    SKIP_OLLAMA=true
else
    echo "Ollama installed: $(ollama --version)"
fi
echo ""

# Step 4: Start Ollama server
if [ -z "$SKIP_OLLAMA" ]; then
    echo "✅ Step 4/10: Starting Ollama server..."
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Starting Ollama in background..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
        echo "Ollama server started"
    else
        echo "Ollama already running"
    fi
else
    echo "⏭️  Step 4/10: Skipping Ollama server (not installed)"
fi
echo ""

# Step 5: Pull Gemma model
if [ -z "$SKIP_OLLAMA" ]; then
    echo "✅ Step 5/10: Pulling Gemma model (may take a few minutes)..."
    if ollama list | grep -q "gemma2:2b"; then
        echo "Model gemma2:2b already downloaded"
    else
        echo "Downloading gemma2:2b (~1.6GB)..."
        ollama pull gemma2:2b
    fi
else
    echo "⏭️  Step 5/10: Skipping model download (Ollama not installed)"
fi
echo ""

# Step 6: Create .env file if not exists
echo "✅ Step 6/10: Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template"
    echo "⚠️  Add your OPENAI_API_KEY to .env for app.py"
else
    echo ".env file already exists"
fi
echo ""

# Step 7: Verify installations
echo "✅ Step 7/10: Verifying installations..."
python3 -c "import langchain_core; print('langchain-core:', langchain_core.__version__)" || echo "❌ langchain-core missing"
python3 -c "import langchain_community; print('langchain-community: OK')" || echo "❌ langchain-community missing"
python3 -c "import streamlit; print('streamlit:', streamlit.__version__)" || echo "❌ streamlit missing"
echo ""

# Step 8: Test Ollama connection
if [ -z "$SKIP_OLLAMA" ]; then
    echo "✅ Step 8/10: Testing Ollama connection..."
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Ollama API responding ✓"
        echo "Available models:"
        ollama list
    else
        echo "❌ Ollama API not responding"
        echo "Run: ollama serve"
    fi
else
    echo "⏭️  Step 8/10: Skipping Ollama test (not installed)"
fi
echo ""

# Step 9: Check .env configuration
echo "✅ Step 9/10: Checking configuration..."
if [ -f .env ]; then
    if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
        echo "⚠️  OpenAI API key not set in .env"
        echo "   app.py will not work without it"
    else
        echo "OpenAI API key configured ✓"
    fi
fi
echo ""

# Step 10: Display next steps
echo "✅ Step 10/10: Setup Complete!"
echo ""
echo "======================================"
echo "🎉 All done! Choose how to run:"
echo "======================================"
echo ""
echo "OPTION 1: Ollama Chatbot (Free, Local)"
echo "---------------------------------------"
if [ -z "$SKIP_OLLAMA" ]; then
    echo "   streamlit run chatbot/localama.py"
    echo "   Then open: http://localhost:8501"
else
    echo "   ⚠️  Install Ollama first: brew install ollama"
fi
echo ""
echo "OPTION 2: OpenAI Chatbot (Paid, Best Quality)"
echo "---------------------------------------"
echo "   1. Add your API key to .env:"
echo "      nano .env"
echo "   2. Run:"
echo "      streamlit run chatbot/app.py"
echo "   3. Open: http://localhost:8501"
echo ""
echo "======================================"
echo "📚 Documentation: cat README.md"
echo "======================================"
