"""
Example usage of the AI Code Generator and Evaluator
"""

from main import AICodeAssistant
import os

# Example 1: Simple code generation
def example_generate_code():
    """Example: Generate code based on a query."""
    print("=" * 60)
    print("Example 1: Generate Code")
    print("=" * 60)
    
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Please set MISTRAL_API_KEY environment variable")
        print("Get your API key from: https://console.mistral.ai/")
        return
    
    assistant = AICodeAssistant(api_key=api_key)
    
    query = "Create a Python function to calculate the Fibonacci sequence up to n terms"
    print(f"\nQuery: {query}\n")
    print("Generated Code (ONLY code, no explanations):")
    print("-" * 60)
    
    code = assistant.generate(query, language="python")
    print(code)
    print("-" * 60)


# Example 2: Generate and evaluate code
def example_generate_and_evaluate():
    """Example: Generate code and evaluate it against reference."""
    print("\n" + "=" * 60)
    print("Example 2: Generate and Evaluate Code")
    print("=" * 60)
    
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Please set MISTRAL_API_KEY environment variable")
        print("Get your API key from: https://console.mistral.ai/")
        return
    
    assistant = AICodeAssistant(api_key=api_key)
    
    query = "Create a Python function to calculate factorial"
    reference_code = """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
    
    print(f"\nQuery: {query}\n")
    print("Reference Code:")
    print("-" * 60)
    print(reference_code)
    print("-" * 60)
    
    result = assistant.generate_and_evaluate(
        query=query,
        reference_code=reference_code,
        language="python"
    )
    
    print("\nGenerated Code:")
    print("-" * 60)
    print(result["generated_code"])
    print("-" * 60)
    
    print("\nEvaluation Results:")
    print("-" * 60)
    report = assistant.evaluator.get_evaluation_report(
        result["generated_code"],
        reference_code,
        "python"
    )
    print(report)


# Example 3: Generate different language code
def example_multiple_languages():
    """Example: Generate code in different languages."""
    print("\n" + "=" * 60)
    print("Example 3: Generate Code in Different Languages")
    print("=" * 60)
    
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Please set MISTRAL_API_KEY environment variable")
        print("Get your API key from: https://console.mistral.ai/")
        return
    
    assistant = AICodeAssistant(api_key=api_key)
    
    queries = [
        ("Python", "Create a function to reverse a string", "python"),
        ("Java", "Create a method to reverse a string", "java"),
        ("C++", "Create a function to reverse a string", "cpp"),
    ]
    
    for lang_name, query, lang_code in queries:
        print(f"\n{lang_name} Code Generation:")
        print(f"Query: {query}\n")
        print("Generated Code:")
        print("-" * 60)
        code = assistant.generate(query, language=lang_code)
        print(code)
        print("-" * 60)


if __name__ == "__main__":
    # Run examples
    try:
        example_generate_code()
        example_generate_and_evaluate()
        example_multiple_languages()
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set MISTRAL_API_KEY environment variable")
        print("   Get your API key from: https://console.mistral.ai/")
        print("2. Installed all dependencies: pip install -r requirements.txt")

