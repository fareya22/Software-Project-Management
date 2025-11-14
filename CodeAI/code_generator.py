"""
AI Code Generator Agent
Generates code based on user queries and returns ONLY code (no explanations)
Uses Mistral AI's Codestral API - optimized for code generation
"""

import re
import os
from typing import Optional, Dict
from mistralai import Mistral

# Try to load from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional


class CodeGenerator:
    """
    AI agent that generates code based on user queries.
    Returns only code without any explanations or markdown formatting.
    Uses Mistral AI's Codestral - a specialized code generation model.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "codestral-latest"):
        """
        Initialize the code generator.
        
        Args:
            api_key: Mistral API key. If None, will try to get from environment.
            model: Model to use for code generation (default: codestral-latest)
                   Options: codestral-latest, codestral-mamba-latest
        """
        api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("Mistral API key required. Set MISTRAL_API_KEY environment variable or pass api_key parameter.")
        
        self.client = Mistral(api_key=api_key)
        self.model = model
    
    def generate_code(self, query: str, language: Optional[str] = None) -> str:
        """
        Generate code based on user query.
        
        Args:
            query: User's code generation request
            language: Target programming language (python, cpp, java, etc.)
        
        Returns:
            Pure code string without any explanations or markdown
        """
        # Determine language from query if not specified
        if not language:
            language = self._detect_language(query)
        
        # Create prompt that emphasizes code-only output
        prompt = self._create_prompt(query, language)
        
        try:
            # Use Mistral AI's chat completion API
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a code generation agent. You MUST respond with ONLY code. No explanations, no markdown formatting, no comments about the code. Just pure code. If the user asks for a specific file type, provide only that code."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,  # Lower temperature for more deterministic code
                max_tokens=4000
            )
            
            # Extract response content
            if hasattr(chat_response, 'choices') and len(chat_response.choices) > 0:
                generated_text = chat_response.choices[0].message.content.strip()
            else:
                raise Exception("Invalid response format from Mistral API")
            
            # Extract code from response (remove markdown code blocks if present)
            code = self._extract_code(generated_text, language)
            
            return code
            
        except ImportError as e:
            raise Exception(f"Mistral AI SDK not installed. Install with: pip install mistralai. Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating code: {str(e)}")
    
    def _create_prompt(self, query: str, language: str) -> str:
        """Create a prompt that emphasizes code-only output."""
        lang_instruction = f"Generate {language} code" if language else "Generate code"
        return f"{lang_instruction} for the following request. Return ONLY the code, no explanations:\n\n{query}"
    
    def _detect_language(self, query: str) -> str:
        """Detect programming language from query."""
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in ['python', 'py', '.py']):
            return 'python'
        elif any(keyword in query_lower for keyword in ['c++', 'cpp', 'cplusplus', '.cpp', '.hpp']):
            return 'cpp'
        elif any(keyword in query_lower for keyword in ['java', '.java']):
            return 'java'
        elif any(keyword in query_lower for keyword in ['javascript', 'js', '.js', '.ts']):
            return 'javascript'
        elif any(keyword in query_lower for keyword in ['typescript', 'ts', '.ts']):
            return 'typescript'
        elif any(keyword in query_lower for keyword in ['go', 'golang', '.go']):
            return 'go'
        elif any(keyword in query_lower for keyword in ['rust', '.rs']):
            return 'rust'
        else:
            return 'python'  # Default to Python
    
    def _extract_code(self, text: str, language: str) -> str:
        """
        Extract pure code from response, removing markdown code blocks.
        """
        # Remove markdown code blocks (```language ... ```)
        patterns = [
            rf'```{language}\s*\n(.*?)\n```',
            rf'```\s*\n(.*?)\n```',
            rf'```{language}(.*?)```',
            rf'```(.*?)```'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # If no code blocks found, return the text as-is (assuming it's already code)
        return text.strip()
    
    def generate_code_file(self, query: str, language: Optional[str] = None, filename: Optional[str] = None) -> str:
        """
        Generate code and return it as if it were a file.
        
        Args:
            query: User's code generation request
            language: Target programming language
            filename: Optional filename to include in response
        
        Returns:
            Code string ready to be saved as a file
        """
        code = self.generate_code(query, language)
        
        if filename:
            return f"# File: {filename}\n{code}"
        
        return code

