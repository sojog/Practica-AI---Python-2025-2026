import ollama
import json
import logging

logger = logging.getLogger(__name__)

def generate_gift_suggestions(name, birthdate_obj):
    """
    Generates gift suggestions using Ollama (local AI) based on the contact's details.
    """
    try:
        # Construct a prompt based on available data
        notes = birthdate_obj.notes if birthdate_obj.notes else "No specific interests listed."
        
        prompt = f"""Generate 3 specific gift ideas for {name}.

Interests: {notes}
Birthdate: {birthdate_obj.birthdate}

Return ONLY valid JSON:
[
    {{"item": "Product Name", "reason": "Why it fits"}}, 
    {{"item": "Product Name", "reason": "Why it fits"}},
    {{"item": "Product Name", "reason": "Why it fits"}}
]

Make products specific (e.g., "Sony WH-1000XM5" not "headphones") and available in Europe."""

        # Call Ollama API
        response = ollama.chat(
            model='gemma3:270m',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        text_response = response['message']['content'].strip()
        
        # Clean up potential markdown code blocks
        if text_response.startswith('```json'):
            text_response = text_response.replace('```json', '').replace('```', '')
        elif text_response.startswith('```'):
            text_response = text_response.replace('```', '')

        try:
            suggestions = json.loads(text_response)
            if isinstance(suggestions, list):
                # Ensure each item is a dict
                validated_suggestions = []
                for item in suggestions:
                    if isinstance(item, str):
                        validated_suggestions.append({"item": item, "reason": "Based on your contact's profile."})
                    elif isinstance(item, dict) and "item" in item:
                        validated_suggestions.append(item)
                return validated_suggestions
            else:
                 return [{"item": "Unexpected response format", "reason": "Please try regenerating."}]
                 
        except json.JSONDecodeError:
            logger.warning(f"Failed to decode JSON from Ollama: {text_response}")
            # Try to return the text as suggestions, converting to objects
            lines = [line.strip().lstrip('- ').lstrip('* ') for line in text_response.split('\n') if line.strip()]
            return [{"item": line, "reason": "AI suggested this gift."} for line in lines[:3]]

    except Exception as e:
        logger.exception("Error generating suggestions with Ollama")
        return [{"item": "Error occurred", "reason": "Unable to generate: " + str(e)}]

def generate_social_aura(name, birthdate_obj, notes=None):
    """
    Generates a social aura description and keywords using Ollama.
    """
    try:
        user_notes = notes if notes else "No specific traits listed."
        zodiac = birthdate_obj.zodiac_sign if hasattr(birthdate_obj, 'zodiac_sign') else "Unknown"
        
        prompt = f"""Analyze the "Social Aura" of {name}.
        
Details:
- Zodiac: {zodiac}
- Birthdate: {birthdate_obj.birthdate}
- Traits/Notes: {user_notes}

Your Task:
1. Write a short, engaging paragraph (max 2 sentences) describing their vibe in a social group. Are they the leader, the peacemaker, the life of the party, or the mysterious observer?
2. Provide exactly 3 short keywords that capture their energy.

Return ONLY valid JSON:
{{
    "description": "The short paragraph here.",
    "keywords": "Keyword1, Keyword2, Keyword3"
}}
"""

        response = ollama.chat(
            model='gemma3:270m',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        text_response = response['message']['content'].strip()
        
        # Clean up code blocks
        if text_response.startswith('```json'):
            text_response = text_response.replace('```json', '').replace('```', '')
        elif text_response.startswith('```'):
            text_response = text_response.replace('```', '')

        try:
            data = json.loads(text_response)
            return data
        except json.JSONDecodeError:
            logger.warning(f"Failed to decode JSON aura: {text_response}")
            return {
                "description": "A unique individual with a mysterious energy that draws others in.",
                "keywords": "Mysterious, Unique, Magnetic"
            }

    except Exception as e:
        logger.exception("Error generating social aura")
        return {
            "description": "Unable to read the stars at this moment.",
            "keywords": "Error, Retry, Later"
        }

def generate_compatibility_v2(person_a, person_b):
    """
    Generates compatibility analysis between two contacts using Ollama.
    """
    try:
        zodiac_a = person_a.zodiac_sign if hasattr(person_a, 'zodiac_sign') else "Unknown"
        zodiac_b = person_b.zodiac_sign if hasattr(person_b, 'zodiac_sign') else "Unknown"
        
        prompt = f"""Analyze the compatibility between two people:
        
Person A ({person_a.full_name}):
- Zodiac: {zodiac_a}
- Notes: {person_a.notes if person_a.notes else "N/A"}

Person B ({person_b.full_name}):
- Zodiac: {zodiac_b}
- Notes: {person_b.notes if person_b.notes else "N/A"}

Your Task:
1. Provide a compatibility score from 0 to 100.
2. Provide a short, catchy verdict (max 3 words, e.g., "Dynamic Duo", "Fiery Clash").
3. Write a DETAILED analysis paragraph (approx. 4-5 sentences). Explain WHY they score this way, referencing their zodiac traits and any provided notes. Discuss strengths and potential challenges in their dynamic.

Return the result in exactly this format:
SCORE: [number]
VERDICT: [text]
ANALYSIS: [text]
"""

        response = ollama.chat(
            model='gemma3:270m',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        text_response = response['message']['content'].strip()
        print(f"DEBUG: Raw AI Response: {text_response}")
        
        # Robust Regex Parsing
        import re
        score_match = re.search(r'SCORE:?\s*(\d+)', text_response, re.IGNORECASE)
        verdict_match = re.search(r'VERDICT:?\s*(.+?)(?:\n|ANALYSIS)', text_response, re.IGNORECASE | re.DOTALL)
        analysis_match = re.search(r'ANALYSIS:?\s*(.+)', text_response, re.IGNORECASE | re.DOTALL)
        
        score = int(score_match.group(1)) if score_match else 75
        
        verdict = verdict_match.group(1).strip() if verdict_match else "Mystery Match"
        # Cleaning verdict
        verdict = verdict.replace('*', '').strip()
        if verdict.startswith('"') and verdict.endswith('"'):
            verdict = verdict[1:-1]
            
        if analysis_match:
            analysis = analysis_match.group(1).strip()
        else:
            # Fallback: excessive text cleaning to find the paragraph
            # Remove lines that start with SCORE or VERDICT
            lines = text_response.split('\n')
            clean_lines = [l for l in lines if not re.match(r'^(SCORE|VERDICT)', l, re.IGNORECASE)]
            analysis = "\n".join(clean_lines).strip()
            
        if not analysis or len(analysis) < 10:
            analysis = "The stars suggest a connection, but the details are currently clouded."

        return {
            "score": score,
            "verdict": verdict,
            "analysis": analysis
        }

    except Exception as e:
        logger.exception("Error generating compatibility")
        return {
            "score": 0,
            "verdict": "Error",
            "analysis": f"Unable to calculate compatibility: {str(e)}"
        }


