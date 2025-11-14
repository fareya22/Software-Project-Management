# AI Code Generator and Evaluator (Assignment-2)

A prototype AI agent system for generating code based on user queries and evaluating code correctness using CodeBLEU metric. This is designed as an industry-usable AI assistant for developers.

## Features

- **Code Generation Agent**: Generates code based on natural language queries
  - Returns ONLY code (no explanations or markdown)
  - Supports multiple languages (Python, C++, Java, JavaScript, etc.)
  - Can output code as specific file types

- **CodeBLEU Evaluator**: Evaluates generated code correctness
  - Uses CodeBLEU metric combining BLEU, syntax match, dataflow match, and AST match
  - Provides detailed evaluation reports
  - Determines code correctness based on threshold

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Mistral AI API key (choose one method):

   **Option A: Using .env file (Recommended)**
   ```bash
   python setup_env.py
   ```
   This will create a `.env` file with your API key automatically.

   **Option B: Manual .env file**
   Create a `.env` file in the project root:
   ```
   MISTRAL_API_KEY=your-api-key-here
   ```

   **Option C: Environment variable**
   ```bash
   export MISTRAL_API_KEY="your-api-key-here"  # Linux/Mac
   ```
   ```powershell
   $env:MISTRAL_API_KEY="your-api-key-here"    # Windows PowerShell
   ```

**Note**: This project uses Mistral AI's Codestral model, which is specifically optimized for code generation and supports 80+ programming languages.

## Usage

### Web UI (Streamlit) - Easily run in your PC

1. Activate your virtual environment
   - PowerShell:
     ```
     .\.venv\Scripts\Activate.ps1
     ```
2. Install dependencies (first time)
   ```
   pip install -r requirements.txt
   ```
3. Ensure your `.env` contains `MISTRAL_API_KEY=...`
4. Start the app:
   ```
   streamlit run app.py
   ```
5. Your browser will open to the UI. Enter a prompt, choose a language, and generate code. Optionally paste reference code to evaluate with CodeBLEU.

### Command Line Interface

**Generate code only:**
```bash
python main.py "Create a Python function to calculate factorial"
```

**Generate code and save to file:**
```bash
python main.py "Create a Python function to calculate factorial" -o factorial.py
```

**Generate code with specific language:**
```bash
python main.py "Create a function to calculate factorial" -l python
```

**Generate and evaluate against reference code:**
```bash
python main.py "Create a Python function to calculate factorial" -e reference.py
```

### Python API

```python
from main import AICodeAssistant

# Initialize assistant
assistant = AICodeAssistant(api_key="your-mistral-api-key")

# Generate code (returns ONLY code, no explanations)
code = assistant.generate("Create a Python function to calculate factorial")
print(code)

# Evaluate generated code
reference_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

results = assistant.evaluate(code, reference_code, language="python")
print(f"CodeBLEU Score: {results['codebleu']}")
print(f"Correct: {results['is_correct']}")

# Generate and evaluate in one step
result = assistant.generate_and_evaluate(
    query="Create a Python function to calculate factorial",
    reference_code=reference_code,
    language="python"
)
```

## Code Generator Agent

The `CodeGenerator` class generates code based on user queries:

- **Input**: Natural language query describing desired code
- **Output**: Pure code string (no explanations, no markdown)
- **Languages**: Auto-detects or explicitly supports Python, C++, Java, JavaScript, TypeScript, Go, Rust

### Key Features:
- Returns ONLY code (as per requirements)
- Can generate specific file types
- Handles markdown code blocks if present in response
- Uses Mistral AI's Codestral model (optimized for code generation)
- Supports 80+ programming languages
- Configurable model (default: codestral-latest, also supports codestral-mamba-latest)

## CodeBLEU Evaluator

The `CodeBLEUEvaluator` class evaluates code correctness:

- **Metrics**:
  - BLEU Score: N-gram overlap between generated and reference code
  - Syntax Match: Keyword and structure similarity
  - Dataflow Match: Variable usage pattern similarity
  - AST Match: Abstract Syntax Tree similarity

- **CodeBLEU Score**: Weighted combination of all metrics
- **Correctness Threshold**: Code is considered correct if CodeBLEU >= 0.75

## Project Structure

```
.
├── code_generator.py      # AI code generation agent
├── code_evaluator.py      # CodeBLEU evaluation tool
├── main.py                # Main interface and CLI
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Example Workflow

1. **Developer asks for code:**
   ```bash
   python main.py "Create a Python class for a binary search tree"
   ```

2. **Agent generates code (outputs ONLY code):**
   ```python
   class TreeNode:
       def __init__(self, val=0, left=None, right=None):
           self.val = val
           self.left = left
           self.right = right

   class BinarySearchTree:
       def __init__(self):
           self.root = None
       
       def insert(self, val):
           # ... implementation
   ```

3. **Evaluate correctness (if reference available):**
   ```bash
   python main.py "Create a Python class for a binary search tree" -e reference_bst.py
   ```

## Requirements

- Python 3.8+
- Mistral AI API key (get from https://console.mistral.ai/)
- Internet connection (for API calls)

## Why Mistral Codestral?

- **Specialized for Code**: Codestral is specifically designed for code generation tasks
- **80+ Languages**: Supports Python, Java, C++, JavaScript, and many more
- **Better Performance**: Optimized for code completion, test writing, and code generation
- **Free Beta Available**: Free access during beta period for IDE integration
- **No Rate Limits Issues**: More reliable API compared to alternatives

## Notes

- The code generator is designed to return ONLY code, making it suitable for direct integration into development workflows
- CodeBLEU evaluation requires reference code for comparison
- The system is a prototype and can be extended with additional features like:
  - Support for more programming languages
  - Enhanced AST parsing
  - Integration with code execution for runtime validation
  - Batch processing capabilities

## License

This is a prototype project for demonstration purposes.

