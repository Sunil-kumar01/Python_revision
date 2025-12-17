# Python Learning Project

## 📁 Project Structure

```
Python_revision/
├── src/                           # Your Python learning files
│   ├── Classes.py                # Class examples
│   ├── function.py               # Function examples
│   ├── modules.py                # Module examples
│   └── ... (other learning files)
│
└── src/langchain/               # LangChain / chatbot project
   ├── .venv/                   # 🔒 Virtual environment (hidden in VS Code)
   ├── chatbot/app.py           # Your ChatGPT/LLM app entrypoint
   ├── requirements.txt         # Project dependencies (generated)
   └── .env                     # API keys (not committed)
```

## 🎯 Understanding Virtual Environments

### What is a Virtual Environment?
A virtual environment is an **isolated Python workspace** for your project. Think of it like a separate room where your project lives with its own set of tools (packages), independent from your system Python.

### Why Use It?
- ✅ Each project gets its own packages (no conflicts)
- ✅ Easy to share your project with others
- ✅ Keeps your system Python clean

---

## 🚀 How to Use This Project

### Option 1: Regular Python Files (No Virtual Environment)
Run any file in `src/` using your system Python:

```bash
cd /Users/sunilkumar/Downloads/Python_revision
python3 src/modules.py
```

**Status**: ❌ **Using SYSTEM Python** (global installation)

---

### Option 2: LangChain Project (With Virtual Environment)

#### Step 1: Activate the Virtual Environment
```bash
cd /Users/sunilkumar/Downloads/Python_revision
source src/langchain/.venv/bin/activate
```

**You'll see `(.venv)` in your terminal prompt:**
```
(.venv) sunilkumar@MacBookAir Python_revision %
```

**Status**: ✅ **Using VIRTUAL ENVIRONMENT** (isolated from system)

#### Step 2: Set up your API keys (first time only)
```bash
# Edit src/langchain/.env and add your keys (OPENAI_API_KEY, LANGCHAIN_API_KEY, etc.)
```

#### Step 3: Run the project
```bash
python src/langchain/chatbot/app.py
```

#### Step 4: When finished, deactivate
```bash
deactivate
```

**Status**: ❌ **Back to SYSTEM Python**

---

## 📦 Installing Packages

### In Virtual Environment (Recommended for LangChain project)
```bash
source src/langchain/.venv/bin/activate
pip install -r src/langchain/requirements.txt  # or install new packages, then freeze
pip freeze > src/langchain/requirements.txt     # Save dependencies
deactivate
```

### Installing from requirements.txt (on another machine)
```bash
source src/langchain/.venv/bin/activate
pip install -r src/langchain/requirements.txt
deactivate
```

---

## 🔍 How to Tell Which Python You're Using

Run this command to check:
```bash
which python
```

**System Python:**
```
/usr/local/bin/python3  ← System-wide installation
```

**Virtual Environment:**
```
/Users/sunilkumar/Downloads/Python_revision/src/langchain/.venv/bin/python  ← Isolated!
```

---

## 📝 Quick Reference Card

| Action | Command | Environment |
|--------|---------|-------------|
| Run regular file | `python3 src/function.py` | System Python |
| Activate venv | `source src/langchain/.venv/bin/activate` | Virtual Env |
| Check which Python | `which python` | - |
| Deactivate venv | `deactivate` | Back to System |
| Install package | `pip install <package>` | Current active env |

---

## 💡 Tips for Beginners

1. **Look at your terminal prompt:**
   - `(.venv)` visible = Virtual Environment ✅
   - No `(.venv)` = System Python ❌

2. **When to use virtual environment:**
   - Working on Langchain_project
   - Installing packages for a specific project
   - Sharing your project with others

3. **When system Python is OK:**
   - Running simple learning scripts in `src/`
   - Practicing basic Python concepts

4. **VS Code hides these folders automatically:**
   - `.venv/` (virtual environment)
   - `__pycache__/` (Python cache)
   - `.DS_Store` (macOS files)

---
## 🔐 Security Note

Never commit these files to GitHub:
- `.env` (contains your API keys)
- `.venv/` or `env/` (virtual environment folders)
- `__pycache__/` (cache files)

They're already listed in `.gitignore` for safety!

---

## 🛠️ Common mistake (what went wrong) and how to avoid it

**Problem you hit:** ran `app.py` with the wrong interpreter (`env/bin/python`) so required packages were missing, and a pip install failed with "No space left on device".

**Fix you used:**
1) Activate the correct venv: `source src/langchain/.venv/bin/activate`
2) Free space: `pip cache purge`
3) Install deps without cache: `pip install --no-cache-dir langchain-openai langchain-core langchain-community streamlit python-dotenv openai`
4) Freeze deps: `pip freeze > src/langchain/requirements.txt`
5) Run with the same venv active: `python src/langchain/chatbot/app.py`

**How to avoid next time:**
- Always check for `(.venv)` in your prompt before running or installing.
- If you see import errors, confirm `which python` shows `src/langchain/.venv/bin/python`.
- Keep dependencies in `src/langchain/requirements.txt` and install inside the active venv.

---

## 🧭 Quick Runbook: Local Ollama Chatbot (`localama.py`)

Follow these steps any time you want to run the local Ollama chatbot.

1) Activate the project venv
```bash
cd /Users/sunilkumar/Downloads/Python_revision
source src/langchain/.venv/bin/activate
```

2) Ensure the model is installed (one-time)
```bash
ollama pull gemma3:1b
```

3) Start the Streamlit app
```bash
streamlit run src/langchain/chatbot/localama.py --server.port 8514 --server.headless true
```

4) Open the app
- Local URL: http://localhost:8514
- The UI shows the active model and the Ollama endpoint.

5) If you see a 404 about the model
- Run the pull command again: `ollama pull gemma3:1b`
- Verify models: `curl -s http://localhost:11434/api/tags | jq -r '.models[].name'`

6) When finished
```bash
deactivate
```

**Key checks before running:**
- Terminal prompt shows `(.venv)`
- `which python` → `/Users/sunilkumar/Downloads/Python_revision/src/langchain/.venv/bin/python`
- `which streamlit` → `/Users/sunilkumar/Downloads/Python_revision/src/langchain/.venv/bin/streamlit`

**What changed in this project (beginner summary):**
- Fixed the Ollama model name to the exact tag: `gemma3:1b`.
- Set `BASE_URL` to `http://localhost:11434` so Streamlit hits the local Ollama server.
- Added UI captions that show the active model and available models (via `/api/tags`).
- Confirmed the app runs from the venv (`source src/langchain/.venv/bin/activate`).
