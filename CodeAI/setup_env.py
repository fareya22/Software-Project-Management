"""
Setup script to create .env file with API key
Run this once to configure your API key
"""

import os

def setup_env_file():
    """Create .env file with Mistral API key."""
    api_key = "sZXCqxUG7EN3Dd1WNF88UCpaeJukfdjg"
    
    env_content = f"""# Mistral AI API Configuration
# Get your API key from: https://console.mistral.ai/
MISTRAL_API_KEY={api_key}
"""
    
    env_file = ".env"
    
    if os.path.exists(env_file):
        response = input(f"{env_file} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"[OK] Created {env_file} file with your API key")
        print("[OK] Your API key is now configured!")
        print("\nYou can now use the code generator without setting environment variables.")
    except Exception as e:
        print(f"Error creating .env file: {e}")
        print("\nManual setup:")
        print(f"1. Create a file named '.env' in the project root")
        print(f"2. Add this line: MISTRAL_API_KEY={api_key}")

if __name__ == "__main__":
    setup_env_file()

