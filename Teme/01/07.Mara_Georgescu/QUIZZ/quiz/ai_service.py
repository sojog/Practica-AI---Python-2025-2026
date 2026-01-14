import random
import json
import re
import google.generativeai as genai

from django.conf import settings
import requests



# Translation dictionaries for multilingual support
TRANSLATIONS = {
    'en': {
        'what_is': 'What is',
        'which': 'Which',
        'how': 'How',
        'the_text_discusses': 'The text discusses',
        'according_to_text': 'according to the text',
        'true': 'True',
        'false': 'False',
        'this_statement_is': 'This statement is',
        'accurate': 'accurate',
        'inaccurate': 'inaccurate',
        'based_on_text': 'based on the text content',
        'this_is': 'This is',
        'true_lower': 'true',
        'false_lower': 'false',
        'according_to_material': 'according to the material',
        'complete_definition': 'The complete definition is',
        'complete_sentence': 'The complete sentence is',
        'briefly_explain': 'Briefly explain the concept of',
        'what_significance': 'What is the significance of',
        'in_the_text': 'in the text',
        'define_based_on': 'Define',
        'based_on_reading': 'based on the reading',
        'summarize_main_idea': 'Summarize the main idea of the following sentence',
        'the_sentence_states': 'The sentence states',
        'answers_will_vary': 'Answers will vary',
        'primary_focus': 'What is the primary focus regarding',
        'how_characterized': 'How is',
        'characterized_in_text': 'characterized in the text',
        'which_aspect': 'Which aspect of',
        'is_emphasized': 'is emphasized',
        'explained_as': 'It is explained as a fundamental concept',
        'mentioned_as': 'It is mentioned as a supporting detail',
        'presented_as': 'It is presented as an advanced topic',
        'described_as': 'It is described as a practical application',
        'the_text_states': 'The text states that',
    },
    'ro': {
        'what_is': 'Ce este',
        'which': 'Care',
        'how': 'Cum',
        'the_text_discusses': 'Textul discută despre',
        'according_to_text': 'conform textului',
        'true': 'Adevărat',
        'false': 'Fals',
        'this_statement_is': 'Această afirmație este',
        'accurate': 'corectă',
        'inaccurate': 'incorectă',
        'based_on_text': 'pe baza conținutului textului',
        'this_is': 'Aceasta este',
        'true_lower': 'adevărat',
        'false_lower': 'fals',
        'according_to_material': 'conform materialului',
        'complete_definition': 'Definiția completă este',
        'complete_sentence': 'Propoziția completă este',
        'briefly_explain': 'Explică pe scurt conceptul de',
        'what_significance': 'Care este semnificația',
        'in_the_text': 'în text',
        'define_based_on': 'Definește',
        'based_on_reading': 'pe baza lecturii',
        'summarize_main_idea': 'Rezumă ideea principală a următoarei propoziții',
        'the_sentence_states': 'Propoziția afirmă',
        'answers_will_vary': 'Răspunsurile pot varia',
        'primary_focus': 'Care este focusul principal privind',
        'how_characterized': 'Cum este',
        'characterized_in_text': 'caracterizat în text',
        'which_aspect': 'Care aspect al',
        'is_emphasized': 'este subliniat',
        'explained_as': 'Este explicat ca un concept fundamental',
        'mentioned_as': 'Este menționat ca un detaliu de susținere',
        'presented_as': 'Este prezentat ca un subiect avansat',
        'described_as': 'Este descris ca o aplicație practică',
        'the_text_states': 'Textul afirmă că',
    }
}

def t(key, language='en'):
    """Get translated text for a given key"""
    return TRANSLATIONS.get(language, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))

def generate_quiz_with_ai(text, question_count=10, question_type='mixed', difficulty='medium', language='en'):
    """
    Generate quiz questions using AI (Gemini).
    Falls back to intelligent mock generation if no API key is present.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    
    # 1. Generate questions with Gemini
    if api_key:
        try:
            # Generate directly in the requested language with Gemini
            questions = generate_quiz_with_gemini(text, question_count, question_type, difficulty, language)
            return questions
        except Exception as e:
            print(f"Gemini AI Error: {e}")
    
    # 2. Fallback to intelligent mock generation
    return intelligent_mock_generate_quiz(text, question_count, question_type, difficulty, language)


def generate_quiz_with_gemini(text, question_count, question_type, difficulty, language):
    """
    Generate quiz questions using Google Gemini AI.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    # Use the generic latest flash alias which usually has better free tier availability
    model = genai.GenerativeModel('gemini-flash-latest')
    
    lang_name = "Romanian" if language == 'ro' else "English"
    
    prompt = f"""
    You are an expert educational content creator.
    Analyze the following text and generate {question_count} high-quality, personalized quiz questions in {lang_name}.
    
    Parameters:
    - Type: {question_type}
    - Difficulty: {difficulty}
    - Target Language: {lang_name}
    
    CRITICAL INSTRUCTIONS FOR QUALITY:
    1. STRICTLY PERSONALIZED: Questions must be derived ONLY from the provided text. Do not ask generic questions like "What is the main idea?" unless the text specifically argues for a main idea. Ask about specific details, names, figures, and concepts found IN THE TEXT.
    2. ACCURATE TRANSLATION: If the source text is in English and target is Romanian (or vice versa), ensure the translation is natural, idiomatic, and academically precise. Avoid literal "machine translation" artifacts.
    3. DEEP COMPREHENSION: Ask questions that require understanding relationships (X happened because of Y), implications, and specific definitions given in the text.
    4. PLAUSIBLE DISTRACTORS: For multiple choice, wrong answers (distractors) should be plausible but incorrect based on the text.
    5. DETAILED EXPLANATION: The explanation must cite the specific logic or sentence from the text that proves the answer.
    
    Text to Analyze:
    {text[:15000]}
    
    Output Format:
    Return ONLY a valid JSON array of objects with this structure:
    [
        {{
            "question_text": "Question in {lang_name}",
            "question_type": "multiple_choice", "true_false", "fill_in_blank", or "short_answer",
            "correct_answer": "Complete correct answer",
            "options": ["option1", "option2", "option3", "option4"], // required for multiple_choice, exactly 4
            "explanation": "Explanation in {lang_name}"
        }}
    ]
    
    Rules for JSON:
    - For true_false, correct_answer must be "True" or "False" (or translated equivalents if requested generally, but usually True/False strings are expected by the backend logic - check if backend needs "True"/"False" string or localized. WE WILL USE English "True"/"False" for the value key to be safe, but the text can be localized in UI). 
    - Actually, keep correct_answer as "True"/"False" for boolean logic, but Question Text should be in {lang_name}.
    """
    
    response = model.generate_content(prompt)
    
    # Extract JSON from response
    content = response.text
    # Remove markdown code blocks if present
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    # Sanitize JSON: remove trailing commas before closing brackets/braces
    import re
    content = re.sub(r',\s*]', ']', content)
    content = re.sub(r',\s*}', '}', content)
    
    questions = json.loads(content)
    
    # Add order and ensure types are correct
    for i, q in enumerate(questions):
        q['order'] = i + 1
        # Ensure question_type matches requested if it was specific
        if question_type != 'mixed':
            q['question_type'] = question_type
        
        # Sanitize question type to valid choices
        valid_types = ['multiple_choice', 'true_false', 'fill_in_blank', 'short_answer']
        if q.get('question_type') not in valid_types:
            # Fallback based on content or random
            if 'options' in q and len(q['options']) > 0:
                q['question_type'] = 'multiple_choice'
            elif q['question_text'].lower().startswith('true') or q['question_text'].lower().startswith('false') or 'true' in str(q.get('options', [])).lower():
                q['question_type'] = 'true_false'
            else:
                q['question_type'] = 'short_answer'
            
    return questions

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

def intelligent_mock_generate_quiz(text, question_count=10, question_type='mixed', difficulty='medium', language='en'):
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
        # Determine question format
        if question_type == 'mixed':
            q_format = random.choice(['multiple_choice', 'true_false', 'fill_in_blank', 'short_answer'])
        else:
            q_format = question_type
        
        # Select question category
        q_category = random.choice(question_types_pool) if question_types_pool else 'general'
        
        # Generate question based on category and format (pass language to all functions)
        if q_format == 'multiple_choice':
            question = generate_intelligent_mc(i + 1, info, q_category, difficulty, language)
        elif q_format == 'true_false':
            question = generate_intelligent_tf(i + 1, info, q_category, difficulty, language)
        elif q_format == 'fill_in_blank':
            question = generate_intelligent_fib(i + 1, info, q_category, difficulty, language)
        elif q_format == 'short_answer':
            question = generate_intelligent_sa(i + 1, info, q_category, difficulty, language)
        else:
            # Default fallback
            question = generate_intelligent_mc(i + 1, info, q_category, difficulty, language)
        
        questions.append(question)
    
    return questions

def generate_intelligent_mc(number, info, category, difficulty, language='en'):
    """Generate intelligent multiple choice question based on extracted information"""
    
    if category == 'definition' and info['definitions']:
        # Question about a definition
        definition = random.choice(info['definitions'])
        # Try to extract the subject
        match = re.search(r'^([A-Z][a-zA-Z\s]+)\s+(is|are|means)', definition)
        if match:
            subject = match.group(1).strip()
            # Create question
            question_text = f"{t('what_is', language)} {subject}?"
            
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
                'explanation': f"{t('according_to_text', language)}: {definition[:150]}...",
                'order': number
            }
    
    elif category == 'concept' and info['concepts']:
        # Question about a key concept
        concept = random.choice(info['concepts'])
        
        templates = [
            f"{t('which', language)} statement best describes {concept}?",
            f"{t('what_is', language)} the role of {concept} in the text?",
            f"{t('according_to_material', language)}, {concept} is primarily:",
            f"{t('the_text_discusses', language)} {concept} in the context of:"
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
        f"{t('primary_focus', language)} {concept}?",
        f"{t('how_characterized', language)} {concept} {t('characterized_in_text', language)}?",
        f"{t('which_aspect', language)} {concept} {t('is_emphasized', language)}?"
    ]
    
    options = [
        t('explained_as', language),
        t('mentioned_as', language),
        t('presented_as', language),
        t('described_as', language)
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

def generate_intelligent_tf(number, info, category, difficulty, language='en'):
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
            'options': [t('true', language), t('false', language)],
            'explanation': f"{t('this_statement_is', language)} {t('true_lower' if is_true else 'false_lower', language)} {t('according_to_text', language)}.",
            'order': number
        }
    
    elif category == 'concept' and info['concepts']:
        # True/False about a concept
        concept = random.choice(info['concepts'])
        
        if is_true:
            templates = [
                f"{t('the_text_discusses', language)} {concept} as an important concept.",
                f"{concept} is mentioned in the material.",
                f"The text provides information about {concept}."
            ]
        else:
            templates = [
                f"{t('the_text_states', language)} {concept} is irrelevant.",
                f"{concept} is explicitly contradicted in the material.",
                f"The text dismisses {concept} as unimportant."
            ]
        
        return {
            'question_text': random.choice(templates),
            'question_type': 'true_false',
            'correct_answer': 'True' if is_true else 'False',
            'options': [t('true', language), t('false', language)],
            'explanation': f"{t('this_is', language)} {t('true_lower' if is_true else 'false_lower', language)} - {concept} is {'indeed discussed' if is_true else 'not dismissed'} {t('in_the_text', language)}.",
            'order': number
        }
    
    elif category == 'comprehension' and info['sentences']:
        # True/False based on actual sentence
        sentence = random.choice(info['sentences'])
        
        if is_true:
            statement = sentence
        else:
            # Negate the sentence
            statement = f"{t('the_text_states', language)} " + sentence.lower()
            statement = statement.replace(" is ", " is not ")
            statement = statement.replace(" are ", " are not ")
            statement = statement.replace(" can ", " cannot ")
        
        return {
            'question_text': statement,
            'question_type': 'true_false',
            'correct_answer': 'True' if is_true else 'False',
            'options': [t('true', language), t('false', language)],
            'explanation': f"{t('this_statement_is', language)} {t('accurate' if is_true else 'inaccurate', language)} {t('based_on_text', language)}.",
            'order': number
        }
    
    # Fallback
    if info['sentences']:
        sentence = random.choice(info['sentences'])
        is_true = random.choice([True, False])
        if is_true:
            statement = f"{t('according_to_text', language)}: {sentence}"
        else:
            statement = f"{t('the_text_states', language)} " + sentence[:50] + "..."
            # Simple negation
            negations = [" nu ", " ne-", " niciodată "] if language == 'ro' else [" not ", " never ", " un-"]
            statement += random.choice(negations)
        
        return {
            'question_text': statement,
            'question_type': 'true_false',
            'correct_answer': 'True' if is_true else 'False',
            'options': [t('true', language), t('false', language)],
            'explanation': f"{t('this_is', language)} {t('true_lower' if is_true else 'false_lower', language)} {t('based_on_text', language)}.",
            'order': number
        }
    
    return {
        'question_text': "The text provides information about the topic.",
        'question_type': 'true_false',
        'correct_answer': 'True',
        'options': [t('true', language), t('false', language)],
        'explanation': f"{t('this_is', language)} true {t('according_to_material', language)}.",
        'order': number
    }

def generate_intelligent_fib(number, info, category, difficulty, language='en'):
    """Generate intelligent fill-in-the-blank question"""
    
    if category == 'definition' and info['definitions']:
        definition = random.choice(info['definitions'])
        # Try to find the subject
        match = re.search(r'^([A-Z][a-zA-Z\s]+)\s+(is|are|means)', definition)
        if match:
            subject = match.group(1).strip()
            # Create question by blanking out the subject
            question_text = definition.replace(subject, "__________", 1)
            correct = subject
            
            return {
                'question_text': question_text,
                'question_type': 'fill_in_blank',
                'correct_answer': correct,
                'options': [],
                'explanation': f"{t('complete_definition', language)}: {definition}",
                'order': number
            }
            
    # Fallback to sentence completion
    if info['sentences']:
        sentence = random.choice(info['sentences'])
        words = sentence.split()
        if len(words) > 5:
            # Pick a word to blank out (avoiding small words)
            candidates = [w for w in words if len(w) > 4]
            if candidates:
                target_word = random.choice(candidates)
                # Remove punctuation from target word for the answer
                clean_answer = re.sub(r'[^\w\s]', '', target_word)
                question_text = sentence.replace(target_word, "__________", 1)
                
                return {
                    'question_text': question_text,
                    'question_type': 'fill_in_blank',
                    'correct_answer': clean_answer,
                    'options': [],
                    'explanation': f"{t('complete_sentence', language)}: {sentence}",
                    'order': number
                }
    
    # Ultimate fallback
    return generate_intelligent_tf(number, info, category, difficulty, language)

def generate_intelligent_sa(number, info, category, difficulty, language='en'):
    """Generate intelligent short answer question"""
    
    if category == 'concept' and info['concepts']:
        concept = random.choice(info['concepts'])
        templates = [
            f"{t('briefly_explain', language)} {concept}.",
            f"{t('what_significance', language)} {concept} {t('in_the_text', language)}?",
            f"{t('define_based_on', language)} {concept} {t('based_on_reading', language)}."
        ]
        
        return {
            'question_text': random.choice(templates),
            'question_type': 'short_answer',
            'correct_answer': f"Answers should define or explain {concept}",
            'options': [],
            'explanation': f"{concept} is a key topic. Your answer should demonstrate understanding of its role in the text.",
            'order': number
        }
        
    if info['sentences']:
        sentence = random.choice(info['sentences'])
        return {
            'question_text': f"{t('summarize_main_idea', language)}: " + sentence,
            'question_type': 'short_answer',
            'correct_answer': t('answers_will_vary', language),
            'options': [],
            'explanation': f"{t('the_sentence_states', language)}: {sentence}",
            'order': number
        }

    # Ultimate fallback
    return generate_intelligent_mc(number, info, category, difficulty, language)

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
    
def get_ai_explanation(question_text, correct_answer, user_query, language='en'):
    """
    Get an explanation for a quiz question using AI (Gemini).
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    lang_name = "Romanian" if language == 'ro' else "English"
    
    if not api_key:
        return "I'm sorry, I cannot provide an explanation without an API key."

    prompt = f"""
    You are a helpful educational tutor.
    The user is taking a quiz and needs help with a question.
    
    Use the following Context:
    Question: {question_text}
    Correct Answer: {correct_answer}
    
    User Query: {user_query}
    
    Task:
    Provide a clear, encouraging, and pedagogically sound explanation in {lang_name}.
    If the user is asking why the answer is correct, explain the logic.
    If the user is confused, clarify the concept.
    Keep the tone friendly and supportive.
    """

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Explanation Error: {e}")
        return f"I'm sorry, I encountered an error while generating the explanation. The correct answer is: {correct_answer}."
