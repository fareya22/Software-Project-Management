import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import re
from difflib import SequenceMatcher

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

class Message(BaseModel):
    message: str

class CodeGenerationRequest(BaseModel):
    query: str
    language: str = "python"

class CodeValidationRequest(BaseModel):
    generated_code: str
    reference_code: str
    language: str = "python"

def extract_code_block(text, language):
    """Extract code from markdown code blocks"""
    pattern = rf"```{language}\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return text

def calculate_codebleu(generated_code, reference_code, language):
    """
    Calculate CodeBLEU-like score between generated and reference code.
    Uses token matching and structural similarity.
    Score range: 0.0 to 1.0
    """
    try:
        # Tokenize both codes
        gen_tokens = re.findall(r'\b\w+\b|[^\w\s]', generated_code)
        ref_tokens = re.findall(r'\b\w+\b|[^\w\s]', reference_code)
        
        if not ref_tokens:
            return 0.0
        
        # Calculate token-level similarity
        gen_set = set(gen_tokens)
        ref_set = set(ref_tokens)
        token_overlap = len(gen_set & ref_set) / len(ref_set) if ref_set else 0
        
        # Calculate sequence similarity (structure)
        sequence_matcher = SequenceMatcher(None, generated_code, reference_code)
        sequence_ratio = sequence_matcher.ratio()
        
        # Calculate line-level similarity
        gen_lines = [line.strip() for line in generated_code.split('\n') if line.strip()]
        ref_lines = [line.strip() for line in reference_code.split('\n') if line.strip()]
        
        matching_lines = sum(1 for line in gen_lines if line in ref_lines)
        line_ratio = matching_lines / len(ref_lines) if ref_lines else 0
        
        # Weighted combination (CodeBLEU-inspired)
        # 40% token match, 40% sequence similarity, 20% line match
        final_score = (0.4 * token_overlap + 0.4 * sequence_ratio + 0.2 * line_ratio)
        
        return min(1.0, max(0.0, final_score))
    except Exception as e:
        print(f"Error calculating score: {e}")
        return 0.0

@app.post("/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """Generate code based on user query"""
    try:
        prompt = f"""You are an expert code generation AI. Generate ONLY the code without any explanations or comments.
        
User Request: {request.query}
Language: {request.language}

Requirements:
1. Return ONLY the code - no explanations, no markdown, no text
2. Make the code production-ready and well-structured
3. Include proper error handling
4. Use best practices for the {request.language} language
5. If applicable, include comments only for complex logic

Generate the code now:"""

        response = model.generate_content(prompt)
        generated_code = response.text.strip()
        
        # Clean up markdown if present
        generated_code = extract_code_block(generated_code, request.language) or generated_code
        
        return {
            "code": generated_code,
            "language": request.language,
            "status": "success"
        }
    except Exception as e:
        return {
            "code": "",
            "language": request.language,
            "status": "error",
            "error": str(e)
        }

@app.post("/validate-code")
async def validate_code(request: CodeValidationRequest):
    """Validate generated code using CodeBLEU metric"""
    try:
        # Clean up code blocks if present
        generated = extract_code_block(request.generated_code, request.language) or request.generated_code
        reference = extract_code_block(request.reference_code, request.language) or request.reference_code
        
        # Calculate CodeBLEU score
        score = calculate_codebleu(generated, reference, request.language)
        
        # Determine quality level
        if score >= 0.85:
            quality = "Excellent"
        elif score >= 0.70:
            quality = "Good"
        elif score >= 0.50:
            quality = "Fair"
        else:
            quality = "Poor"
        
        return {
            "codebleu_score": round(score, 4),
            "quality": quality,
            "generated_code": generated,
            "reference_code": reference,
            "language": request.language,
            "status": "success"
        }
    except Exception as e:
        return {
            "codebleu_score": 0.0,
            "quality": "Error",
            "status": "error",
            "error": str(e)
        }

@app.post("/chat")
async def chat(msg: Message):
    try:
        # Enhanced prompt for better formatted responses
        enhanced_prompt = f"""Please provide a clear, well-organized response to: "{msg.message}"

CRITICAL FORMATTING RULES - FOLLOW THESE EXACTLY:
• Use **bold** for important terms and headings
• Use ### for main section headings
• Use ## for subsection headings
• Use numbered lists (1. 2. 3.) for steps
• Use proper paragraph breaks with blank lines
• For code blocks, use ```python and ``` with proper indentation
• Keep technical explanations simple but accurate and short
• Structure responses with clear sections

STRICTLY AVOID:
• Using *• combinations (this creates ugly formatting)
• Random asterisks anywhere in text
• Using * for bullet points
• Poorly formatted lists
• Walls of text without breaks
• Any markdown syntax that creates visual clutter
• Inconsistent indentation in code blocks

For code explanations:
• Use clear numbered sections (1. 2. 3.)
• Explain each part step by step
• Use proper code block formatting with ```python
• Keep code indentation clean and readable
• Use bullet points for detailed explanations within sections

Response Structure:
1. Use numbered sections for main parts
2. Explain code components easily
3. Include practical examples where relevant

Question: {msg.message}"""

        response = model.generate_content(enhanced_prompt)

        # Clean and format the response
        formatted_response = response.text.strip()

        # Basic formatting improvements
        formatted_response = formatted_response.replace('\n\n\n', '\n\n')  # Remove excessive line breaks
        formatted_response = formatted_response.replace('* ', '• ')  # Convert asterisks to bullets
        formatted_response = formatted_response.replace('- ', '• ')  # Convert dashes to bullets
        formatted_response = formatted_response.replace('*•', '')  # Remove *• combinations
        formatted_response = formatted_response.replace('**', '**')  # Ensure proper bold markers

        # Ensure proper spacing
        lines = formatted_response.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)

        formatted_response = '\n\n'.join(cleaned_lines)

        return {"response": formatted_response}
    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)