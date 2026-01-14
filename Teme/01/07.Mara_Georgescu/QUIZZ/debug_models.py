
import os
import google.generativeai as genai
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Load .env file manually
def load_env(path):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Basic parsing
                    try:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
                    except ValueError:
                        pass

load_env(BASE_DIR / '.env')
api_key = os.environ.get('GEMINI_API_KEY')

print(f"Key loaded: {bool(api_key)}")
if api_key:
    # Print first few chars to verify (safe)
    print(f"Key prefix: {api_key[:5]}...")

    try:
        genai.configure(api_key=api_key)
        print("\nAvailable Models for generateContent:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
