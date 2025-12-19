import os
import django
import sys

# Setup Django
sys.path.append('f:\\practica link\\Practica-AI---Python-2025-2026\\Teme\\01\07.Mara_Georgescu\\QUIZZ')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QUIZZ.settings')
django.setup()

from quiz.ai_service import generate_quiz_with_ollama

test_text = """
Vasile Voiculescu a fost un scriitor român, medic și poet. 
A fost unul dintre colaboratorii revistei "Gândirea" și un reprezentant de seamă al tradiționalismului românesc.
"""

print("Testing Ollama AI (make sure Ollama is running and llama3 is pulled)...")
try:
    # Temporarily bypass Gemini to test Ollama
    questions = generate_quiz_with_ollama(test_text, question_count=2, question_type='multiple_choice', difficulty='medium', language='ro')
    for q in questions:
        print(f"Q: {q['question_text']}")
        print(f"A: {q['correct_answer']}")
        print(f"Explanation: {q['explanation']}")
        print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
    print("Tip: Ensure Ollama is running and you have pulled the model: ollama pull llama3")
