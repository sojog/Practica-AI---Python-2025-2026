"""
AI Service for Quiz Generation
This module provides AI-powered quiz generation functionality.

For production: Use OpenAI or Google Gemini API
For development (no API key): Use intelligent mock generation
"""

import random
import json
import re

# Translation dictionaries for question templates
TRANSLATIONS = {
    'en': {
        'what_is': 'What is',
        'the_text_discusses': 'The text discusses',
        'according_to_text': 'according to the text',
        'true': 'True',
        'false': 'False',
        'this_is_true': 'This is true',
        'this_is_false': 'This is false',
        'complete_sentence': 'The complete sentence is',
        'briefly_explain': 'Briefly explain',
        'what_significance': 'What is the significance of',
        'define_based_on': 'Define based on the reading',
    },
    'ro': {
        'what_is': 'Ce este',
        'the_text_discusses': 'Textul discută despre',
        'according_to_text': 'conform textului',
        'true': 'Adevărat',
        'false': 'Fals',
        'this_is_true': 'Acesta este adevărat',
        'this_is_false': 'Acesta este fals',
        'complete_sentence': 'Propoziția completă este',
        'briefly_explain': 'Explică pe scurt',
        'what_significance': 'Care este semnificația',
        'define_based_on': 'Definește pe baza lecturii',
    }
}

def get_text(key, language='en'):
    """Get translated text for a given key"""
    return TRANSLATIONS.get(language, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'][key])

def generate_quiz_with_ai(text, question_count=10, question_type='mixed', difficulty='medium', language='en'):
    """
    Generate quiz questions using AI (or intelligent mock if no API key).
    
    Args:
        text (str): The note text to generate questions from
        question_count (int): Number of questions to generate
        question_type (str): 'multiple_choice', 'true_false', 'fill_in_blank', 'short_answer', or 'mixed'
        difficulty (str): 'easy', 'medium', 'hard', or 'mixed'
        language (str): 'en' for English, 'ro' for Romanian
    
    Returns:
        list: List of question dictionaries
    """
    # TODO: When API key is available, uncomment and use real AI
    # return real_generate_quiz(text, question_count, question_type, difficulty, language)
    
    # For now, use intelligent mock generation
    return intelligent_mock_generate_quiz(text, question_count, question_type, difficulty, language)
