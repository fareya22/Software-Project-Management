import os
from dotenv import load_dotenv
print("CWD:", os.getcwd())
print(".env exists:", os.path.exists(".env"))
load_dotenv()
print("Key found:", bool(os.getenv("MISTRAL_API_KEY")))
print("Value:", os.getenv("MISTRAL_API_KEY"))
