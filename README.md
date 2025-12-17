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
└── src/Langchain_project/        # Virtual Environment Learning Project
    ├── .venv/                    # 🔒 VIRTUAL ENVIRONMENT (hidden in VS Code)
    ├── weather.py                # Example API project
    ├── VenV_learning.py          # Virtual environment notes
    ├── requirements.txt          # Project dependencies
    └── .env.example              # Environment variable template
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

### Option 2: Langchain Project (With Virtual Environment)

#### Step 1: Activate the Virtual Environment
```bash
cd /Users/sunilkumar/Downloads/Python_revision
source src/Langchain_project/.venv/bin/activate
```

**You'll see `(.venv)` in your terminal prompt:**
```
(.venv) sunilkumar@MacBookAir Python_revision %
```

**Status**: ✅ **Using VIRTUAL ENVIRONMENT** (isolated from system)

#### Step 2: Set up your API key (first time only)
```bash
cp src/Langchain_project/.env.example src/Langchain_project/.env
# Then edit .env and add your OpenWeather API key
```

#### Step 3: Run the project
```bash
python src/Langchain_project/weather.py
```

#### Step 4: When finished, deactivate
```bash
deactivate
```

**Status**: ❌ **Back to SYSTEM Python**

---

## 📦 Installing Packages

### In Virtual Environment (Recommended for Langchain project)
```bash
source src/Langchain_project/.venv/bin/activate
pip install requests python-dotenv
pip freeze > src/Langchain_project/requirements.txt  # Save dependencies
deactivate
```

### Installing from requirements.txt (on another machine)
```bash
source src/Langchain_project/.venv/bin/activate
pip install -r src/Langchain_project/requirements.txt
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
/Users/sunilkumar/Downloads/Python_revision/src/Langchain_project/.venv/bin/python  ← Isolated!
```

---

## 📝 Quick Reference Card

| Action | Command | Environment |
|--------|---------|-------------|
| Run regular file | `python3 src/function.py` | System Python |
| Activate venv | `source src/Langchain_project/.venv/bin/activate` | Virtual Env |
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
