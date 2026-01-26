import os

# Fix for Protobuf error: MUST BE BEFORE ANY OTHER IMPORTS
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import google.generativeai as genai

def list_available_models():
    # Using the key provided by the user
    api_key = 'AIzaSyAiaa6pUE0ZTNKwWSAG2qoz18Q3ogcpiCk'
    
    if not api_key:
        print("API Key is required.")
        return

    try:
        genai.configure(api_key=api_key)
        print("\nFetching available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_available_models()
