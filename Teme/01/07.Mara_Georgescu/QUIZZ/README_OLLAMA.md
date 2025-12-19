# Ollama Integration for Translation

This project supports using [Ollama](https://ollama.com/) for local AI-powered translations. This is an alternative to using external APIs like Google Gemini or OpenAI.

## Setup Instructions

### 1. Install Ollama
Download and install Ollama from [ollama.com](https://ollama.com/).

### 2. Pull a Model
Open your terminal and pull a model that supports translation (e.g., `llama3` or `mistral`).
```bash
ollama pull llama3
```

### 3. Start Ollama
Ensure the Ollama server is running. By default, it runs on `http://localhost:11434`.

### 4. Install Python Library
Install the `ollama` Python library:
```bash
python -m pip install ollama
```

## How it Works in QUIZZ

The `ai_service.py` module includes a `translate_with_ollama` function that communicates with your local Ollama instance.

### Configuration
You can specify the model to use in your `settings.py`:
```python
OLLAMA_MODEL = 'llama3'
```

### Usage
The system will attempt to use Ollama for translating dynamically generated content if configured.
