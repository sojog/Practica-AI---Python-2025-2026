"""
AI Service for Quiz Generation
This module provides AI-powered quiz generation functionality.

For production: Use OpenAI or Google Gemini API
For development (no API key): Use intelligent mock generation
"""

import random
import json
import re

def generate_quiz_with_ai(text, question_count=10, question_type='mixed', difficulty='medium'):
    """
    Generate quiz questions using AI (or intelligent mock if no API key).
    
    Args:
        text (str): The note text to generate questions from
        question_count (int): Number of questions to generate
        question_type (str): 'multiple_choice', 'true_false', or 'mixed'
        difficulty (str): 'easy', 'medium', 'hard', or 'mixed'
    
    Returns:
        list: List of question dictionaries
    """
    # TODO: When API key is available, uncomment and use real AI
    # return real_generate_quiz(text, question_count, question_type, difficulty)
    
    # For now, use intelligent mock generation
    return intelligent_mock_generate_quiz(text, question_count, question_type, difficulty)

def extract_key_information(text):
    """
    Extract key information from text for intelligent question generation.
    
    Returns:
        dict: Contains sentences, definitions, concepts, numbers, etc.
    """
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Extract potential definitions (sentences with "is", "are", "means", "refers to")
    definitions = []
    for sent in sentences:
        if any(word in sent.lower() for word in [' is ', ' are ', ' means ', ' refers to ', ' defined as ']):
            definitions.append(sent)
    
    # Extract important concepts (capitalized words, repeated terms)
    words = text.split()
    word_freq = {}
    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word)
        if len(clean_word) > 3 and clean_word[0].isupper():
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    # Get most frequent important terms
    important_terms = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]
    concepts = [term[0] for term in important_terms]
    
    # Extract numbers and facts
    numbers = re.findall(r'\b\d+\.?\d*\b', text)
    
    # Extract lists (sentences with commas or "and")
    lists = []
    for sent in sentences:
        if sent.count(',') >= 2 or ' and ' in sent.lower():
            lists.append(sent)
    
    return {
        'sentences': sentences[:30],  # Limit to 30 most relevant
        'definitions': definitions[:10],
        'concepts': concepts,
        'numbers': numbers[:10],
        'lists': lists[:10],
        'text_length': len(text)
    }

def intelligent_mock_generate_quiz(text, question_count=10, question_type='mixed', difficulty='medium'):
    """
    Generate intelligent quiz questions by analyzing the text content.
    Creates questions based on actual information extracted from the text.
    """
    # Extract key information from text
    info = extract_key_information(text)
    
    questions = []
    question_types_pool = []
    
    # Build question pool based on available information
    if info['definitions']:
        question_types_pool.extend(['definition'] * 3)
    if info['concepts']:
        question_types_pool.extend(['concept'] * 3)
    if info['sentences']:
        question_types_pool.extend(['comprehension'] * 2)
    if info['lists']:
        question_types_pool.extend(['list_based'] * 2)
    
    # Fallback if no specific information found
    if not question_types_pool:
        question_types_pool = ['general'] * 10
    
    for i in range(question_count):
        # Determine question format (MC or T/F)
        if question_type == 'mixed':
            q_format = random.choice(['multiple_choice', 'true_false'])
        else:
            q_format = question_type
        
        # Select question category
        q_category = random.choice(question_types_pool) if question_types_pool else 'general'
        
        # Generate question based on category and format
        if q_format == 'multiple_choice':
            question = generate_intelligent_mc(i + 1, info, q_category, difficulty)
        else:
            question = generate_intelligent_tf(i + 1, info, q_category, difficulty)
        
        questions.append(question)
    
    return questions

def generate_intelligent_mc(number, info, category, difficulty):
    """Generate intelligent multiple choice question based on extracted information"""
    
    if category == 'definition' and info['definitions']:
        # Question about a definition
        definition = random.choice(info['definitions'])
        # Try to extract the subject
        match = re.search(r'^([A-Z][a-zA-Z\s]+)\s+(is|are|means)', definition)
        if match:
            subject = match.group(1).strip()
            # Create question
            question_text = f"What is {subject}?"
            
            # Extract the actual definition
            parts = re.split(r'\s+(?:is|are|means)\s+', definition, maxsplit=1)
            if len(parts) > 1:
                correct = parts[1].strip()
            else:
                correct = "A key concept discussed in the text"
            
            # Generate plausible distractors
            distractors = [
                f"A {random.choice(['method', 'technique', 'approach'])} not mentioned in the text",
                f"An {random.choice(['outdated', 'alternative', 'unrelated'])} concept",
                f"A {random.choice(['theoretical', 'practical', 'experimental'])} framework"
            ]
            
            options = [correct] + distractors[:3]
            random.shuffle(options)
            
            return {
                'question_text': question_text,
                'question_type': 'multiple_choice',
                'correct_answer': correct,
                'options': options,
                'explanation': f"According to the text: {definition[:150]}...",
                'order': number
            }
    
    elif category == 'concept' and info['concepts']:
        # Question about a key concept
        concept = random.choice(info['concepts'])
        
        templates = [
            f"Which statement best describes {concept}?",
            f"What role does {concept} play in the text?",
            f"According to the material, {concept} is primarily:",
            f"The text discusses {concept} in the context of:"
        ]
        
        correct_options = [
            f"A central concept that is thoroughly explained",
            f"An important element discussed in detail",
            f"A key topic covered in the material",
            f"A fundamental principle explained in the text"
        ]
        
        distractors = [
            f"A minor detail mentioned briefly",
            f"An unrelated concept from another field",
            f"A concept explicitly contradicted in the text",
            f"A topic not addressed in the material"
        ]
        
        options = [random.choice(correct_options)] + random.sample(distractors, 3)
        random.shuffle(options)
        
        return {
            'question_text': random.choice(templates),
            'question_type': 'multiple_choice',
            'correct_answer': options[0],
            'options': options,
            'explanation': f"{concept} is a key concept discussed in the text and plays an important role in understanding the material.",
            'order': number
        }
    
    elif category == 'comprehension' and info['sentences']:
        # Question testing comprehension of a sentence
        sentence = random.choice(info['sentences'])
        
        # Extract a key phrase
        words = sentence.split()
        if len(words) > 5:
            key_phrase = ' '.join(words[:min(5, len(words))])
            
            question_text = f"What does the text state about '{key_phrase}'?"
            
            correct = sentence[:100] + "..." if len(sentence) > 100 else sentence
            
            distractors = [
                "This is not mentioned in the text",
                "The text contradicts this statement",
                "This is an unrelated concept"
            ]
            
            options = [correct] + distractors
            random.shuffle(options)
            
            return {
                'question_text': question_text,
                'question_type': 'multiple_choice',
                'correct_answer': correct,
                'options': options,
                'explanation': f"The text explicitly states: {sentence}",
                'order': number
            }
    
    # Fallback: general question
    if info['concepts']:
        concept = random.choice(info['concepts'])
    else:
        concept = "the main topic"
    
    templates = [
        f"What is the primary focus regarding {concept}?",
        f"How is {concept} characterized in the text?",
        f"Which aspect of {concept} is emphasized?"
    ]
    
    options = [
        "It is explained as a fundamental concept",
        "It is mentioned as a supporting detail",
        "It is presented as an advanced topic",
        "It is described as a practical application"
    ]
    
    random.shuffle(options)
    
    return {
        'question_text': random.choice(templates),
        'question_type': 'multiple_choice',
        'correct_answer': options[0],
        'options': options,
        'explanation': "This question tests understanding of how the concept is presented in the text.",
        'order': number
    }

def generate_intelligent_tf(number, info, category, difficulty):
    """Generate intelligent true/false question based on extracted information"""
    
    is_true = random.choice([True, False])
    
    if category == 'definition' and info['definitions']:
        # True/False about a definition
        definition = random.choice(info['definitions'])
        
        if is_true:
            # Use actual definition
            statement = definition
        else:
            # Modify definition to make it false
            statement = definition.replace(' is ', ' is not ')
            statement = statement.replace(' are ', ' are not ')
        
        return {
            'question_text': statement,
            'question_type': 'true_false',
            'correct_answer': 'True' if is_true else 'False',
            'options': ['True', 'False'],
            'explanation': f"This statement is {'true' if is_true else 'false'} according to the text.",
            'order': number
        }
    
    elif category == 'concept' and info['concepts']:
        # True/False about a concept
        concept = random.choice(info['concepts'])
        
        if is_true:
            templates = [
                f"The text discusses {concept} as an important concept.",
                f"{concept} is mentioned in the material.",
                f"The text provides information about {concept}."
            ]
        else:
            templates = [
                f"The text states that {concept} is irrelevant.",
                f"{concept} is explicitly contradicted in the material.",
                f"The text dismisses {concept} as unimportant."
            ]
        
        return {
            'question_text': random.choice(templates),
            'question_type': 'true_false',
            'correct_answer': 'True' if is_true else 'False',
            'options': ['True', 'False'],
            'explanation': f"This is {'true' if is_true else 'false'} - {concept} is {'indeed discussed' if is_true else 'not dismissed'} in the text.",
            'order': number
        }
    
    elif category == 'comprehension' and info['sentences']:
        # True/False based on actual sentence
        sentence = random.choice(info['sentences'])
        
        if is_true:
            statement = sentence
        else:
            # Negate the sentence
            statement = "The text states that " + sentence.lower()
            statement = statement.replace(" is ", " is not ")
            statement = statement.replace(" are ", " are not ")
            statement = statement.replace(" can ", " cannot ")
        
        return {
            'question_text': statement,
            'question_type': 'true_false',
            'correct_answer': 'True' if is_true else 'False',
            'options': ['True', 'False'],
            'explanation': f"This statement is {'accurate' if is_true else 'inaccurate'} based on the text content.",
            'order': number
        }
    
    # Fallback
    if info['concepts']:
        concept = random.choice(info['concepts'])
        statement = f"The text discusses {concept}."
        is_true = True
    else:
        statement = "The text contains information about the topic."
        is_true = True
    
    return {
        'question_text': statement,
        'question_type': 'true_false',
        'correct_answer': 'True' if is_true else 'False',
        'options': ['True', 'False'],
        'explanation': f"This is {'true' if is_true else 'false'} according to the material.",
        'order': number
    }

def real_generate_quiz(text, question_count, question_type, difficulty):
    """
    Real AI-powered quiz generation (requires API key).
    Uncomment and configure when API key is available.
    """
    # Example using OpenAI (uncomment when ready):
    """
    import openai
    import os
    
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    prompt = f'''
    Analyze the following text and generate {question_count} high-quality {question_type} questions at {difficulty} difficulty level.
    
    Focus on:
    1. Key concepts and definitions
    2. Important relationships and connections
    3. Main ideas and supporting details
    4. Critical facts and information
    
    Text:
    {text[:4000]}  # Limit context length
    
    Return JSON format:
    [
        {{
            "question_text": "Clear, specific question?",
            "question_type": "multiple_choice" or "true_false",
            "correct_answer": "Correct answer",
            "options": ["option1", "option2", "option3", "option4"],  # for multiple choice
            "explanation": "Detailed explanation referencing the text"
        }}
    ]
    '''
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert educational quiz generator. Create questions that test deep understanding of the material."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    questions = json.loads(response.choices[0].message.content)
    
    # Add order
    for i, q in enumerate(questions):
        q['order'] = i + 1
    
    return questions
    """
    
    raise NotImplementedError("Real AI generation requires API key configuration")
