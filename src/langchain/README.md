# 🤖 LangChain Chatbot Projects

Two chatbot implementations using LangChain:

## 📁 Projects

### 1. **app.py** - OpenAI ChatGPT (Paid)
- Uses OpenAI GPT-3.5-turbo
- Requires API key
- Cloud-based, fast, high quality

### 2. **localama.py** - Ollama (Free, Local)
- Uses Ollama with Gemma model
- Completely free
- Runs locally on your machine

---

## 🚀 OPTION 1: OpenAI Version (Paid but Best Quality)

### Step 1: Install Dependencies
```bash
cd /Users/sunilkumar/Downloads/Python_revision/src/langchain
pip install -r requirements.txt
```

### Step 2: Create .env File
```bash
# Copy example and add your key
cp .env.example .env
nano .env  # or use any text editor
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
LANGCHAIN_API_KEY=ls_xxxxx  # optional
```

### Step 3: Run the App
```bash
streamlit run chatbot/app.py
```

### Step 4: Open Browser
- Go to: http://localhost:8501
- Enter your questions
- Get AI responses!

---

## 🆓 OPTION 2: Ollama Version (Free, No API Key)

### Step 1: Install Ollama
```bash
# Download from: https://ollama.ai/download
# Or use Homebrew:
brew install ollama
```

### Step 2: Start Ollama Server
```bash
# In a new terminal:
ollama serve
```

### Step 3: Pull Gemma Model
```bash
# In another terminal:
ollama pull gemma2:2b
```

### Step 4: Install Python Dependencies
```bash
cd /Users/sunilkumar/Downloads/Python_revision/src/langchain
pip install -r requirements.txt
```

### Step 5: Run Local Chatbot
```bash
streamlit run chatbot/localama.py
```

### Step 6: Open Browser
- Go to: http://localhost:8501
- Chat for free!

---

## ⚡ Quick Commands

### Run OpenAI Version:
```bash
cd /Users/sunilkumar/Downloads/Python_revision/src/langchain
streamlit run chatbot/app.py
```

### Run Ollama Version:
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run chatbot
cd /Users/sunilkumar/Downloads/Python_revision/src/langchain
streamlit run chatbot/localama.py
```

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'langchain_openai'"
**Solution:**
```bash
pip install langchain-openai
```

### Issue: "Missing OPENAI_API_KEY"
**Solution:**
1. Create `.env` file in `/src/langchain/`
2. Add: `OPENAI_API_KEY=sk-your-key-here`

### Issue: "Ollama connection failed"
**Solution:**
```bash
# Check if Ollama is running:
curl http://localhost:11434/api/tags

# If not, start it:
ollama serve
```

### Issue: "Model not found"
**Solution:**
```bash
# Pull the model:
ollama pull gemma2:2b

# Or use different model:
ollama pull llama2
```

---

## 📊 Comparison

| Feature | OpenAI (app.py) | Ollama (localama.py) |
|---------|----------------|---------------------|
| **Cost** | Paid (~$0.002/1K tokens) | Free |
| **Quality** | Excellent | Good |
| **Speed** | Very Fast | Moderate |
| **Privacy** | Cloud | Local |
| **Setup** | Easy (just API key) | Medium (install Ollama) |
| **Internet** | Required | Not required |

---

## 🎯 Recommended for Interview

**Show BOTH versions:**

1. **Start with Ollama** (localama.py)
   - "This is completely free and runs locally"
   - "No API costs, good for development"
   - "Privacy-focused, data stays on machine"

2. **Then show OpenAI** (app.py)
   - "For production, I can use GPT-4"
   - "Better quality, faster responses"
   - "Easy to scale in cloud"

3. **Explain Trade-offs**
   - "Development: Use Ollama (free)"
   - "Production: Use OpenAI (better quality)"
   - "I can switch between models easily"

---

## 🔥 Available Models

### OpenAI (app.py):
- `gpt-3.5-turbo` - Fast, cheap
- `gpt-4` - Best quality
- `gpt-4-turbo` - Fast + good

### Ollama (localama.py):
- `gemma2:2b` - Small, fast
- `llama2` - General purpose
- `llama3` - Latest
- `mistral` - Good quality
- `codellama` - For code

Change model in code:
```python
# In localama.py, line 25:
MODEL_NAME = "gemma2:2b"  # Change this
```

---

## 📁 Project Structure

```
src/langchain/
├── chatbot/
│   ├── app.py           # OpenAI version
│   └── localama.py      # Ollama version
├── requirements.txt      # Python packages
├── .env                 # API keys (create this)
├── .env.example         # Template
├── start.sh             # Quick start script
└── README.md            # This file
```

---

## ✅ Complete Setup (All Steps)

### For Ollama (Recommended to Start):

```bash
# Step 1: Install Ollama
brew install ollama

# Step 2: Start Ollama server (keep running)
ollama serve &

# Step 3: Pull model
ollama pull gemma2:2b

# Step 4: Install Python packages
cd /Users/sunilkumar/Downloads/Python_revision/src/langchain
pip install -r requirements.txt

# Step 5: Run chatbot
streamlit run chatbot/localama.py

# Step 6: Open browser at http://localhost:8501
```

### For OpenAI (If you have API key):

```bash
# Step 1: Install packages
cd /Users/sunilkumar/Downloads/Python_revision/src/langchain
pip install -r requirements.txt

# Step 2: Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-actual-key-here
EOF

# Step 3: Run chatbot
streamlit run chatbot/app.py

# Step 4: Open browser at http://localhost:8501
```

---

## 🎓 What to Explain in Interview

**Architecture:**
- "I used LangChain framework for LLM orchestration"
- "Streamlit for quick web UI"
- "Supports multiple LLM backends (OpenAI, Ollama)"

**Technical Choices:**
- "ChatPromptTemplate for structured prompts"
- "Output parsers for clean responses"
- "Environment variables for security"
- "Error handling for failed API calls"

**Production Considerations:**
- "Can switch models based on cost/quality needs"
- "Local models for development, cloud for production"
- "LangChain tracing for debugging"
- "Modular design - easy to add memory, tools"

---

## 🚀 You're Ready!

Choose your path:
- **Free & Local**: Use Ollama (localama.py)
- **Best Quality**: Use OpenAI (app.py) with API key

Both are production-ready and interview-ready! 🎉
