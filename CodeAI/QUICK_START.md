# Quick Start Guide

## Step-by-Step Instructions to Run the Code

### Step 1: Activate Your Virtual Environment

**On Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**On Windows Command Prompt (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**On Linux/Mac:**
```bash
source .venv/bin/activate
```

After activation, you should see `(.venv)` at the beginning of your command prompt.

### Step 2: Install Dependencies

Once your virtual environment is activated, install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- mistralai (for code generation)
- python-dotenv (for .env file support)
- nltk (for CodeBLEU evaluation)
- tree-sitter (for AST parsing)

### Step 3: Verify .env File

Make sure your `.env` file exists with your API key:
```bash
# Check if .env exists (should show your API key)
type .env
```

If it doesn't exist or is missing the key, run:
```bash
python setup_env.py
```

### Step 4: Run the Code Generator

**Basic usage - Generate code:**
```bash
python main.py "Create a Python function to calculate factorial"
```

**Generate code and save to file:**
```bash
python main.py "Create a Python function to calculate factorial" -o factorial.py
```

**Generate code in specific language:**
```bash
python main.py "Create a function to reverse a string" -l python
```

**Generate and evaluate code:**
```bash
python main.py "Create a Python function to calculate factorial" -e reference.py
```

### Step 5: Test with Example Script

You can also run the example script:
```bash
python example_usage.py
```

## Complete Example Session

```powershell
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Verify API key is set
type .env

# 4. Generate code
python main.py "Create a Python class for a binary search tree"

# 5. When done, deactivate (optional)
deactivate
```

## Troubleshooting

**If you get "ModuleNotFoundError":**
- Make sure your virtual environment is activated
- Run `pip install -r requirements.txt`

**If you get "Mistral API key required":**
- Check that `.env` file exists: `type .env`
- Make sure it contains: `MISTRAL_API_KEY=your-key-here`

**If activation script fails:**
- On PowerShell, you might need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then try activating again

## Notes

- Always activate your virtual environment before running the code
- The `.env` file is already configured with your API key
- You don't need to manually set environment variables if using `.env` file

