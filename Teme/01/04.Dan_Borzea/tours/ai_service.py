"""
Serviciu pentru comunicare cu Ollama API
Gestionează conversațiile cu AI și extrage preferințele utilizatorilor
"""
import requests
import json
import logging

logger = logging.getLogger(__name__)


class OllamaService:
    """Serviciu pentru interacțiune cu Ollama API"""
    
    def __init__(self, base_url="http://localhost:11434", model="gemma3:270m"):
        self.base_url = base_url
        self.model = model
        self.chat_endpoint = f"{base_url}/api/chat"
        
    def chat(self, messages, stream=False):
        """
        Trimite mesaje către Ollama și returnează răspunsul
        
        Args:
            messages: Listă de dicts cu format {'role': 'user/assistant', 'content': 'text'}
            stream: Bool, dacă să streameze răspunsul
            
        Returns:
            Dict cu răspunsul de la Ollama sau None dacă eroare
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        
        try:
            response = requests.post(self.chat_endpoint, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Eroare comunicare cu Ollama: {e}")
            return None
    
    def get_initial_prompt(self):
        """Returnează prompt-ul inițial pentru AI"""
        return {
            'role': 'system',
            'content': '''Ești un asistent prietenos pentru recomandări de tururi turistice în România.
Rolul tău este să:
1. Întrebi utilizatorii despre preferințele lor în mod natural și prietenos
2. Să identifici ce tip de experiență caută (istoric, cultural, gastronomic, viață de noapte)
3. Să afli cât timp au disponibil și ce nivel de dificultate preferă
4. Să recomanzi tururi pe baza preferințelor lor

Fii concis și natural. Pune maxim 1-2 întrebări pe mesaj.
Răspunde DOAR în limba română.'''
        }
    
    def build_recommendation_prompt(self, preferences, tours_data):
        """
        Construiește un prompt pentru a genera recomandări pe baza tururilor disponibile
        
        Args:
            preferences: Dict cu preferințele utilizatorului
            tours_data: Listă de tururi match-uite
            
        Returns:
            String cu prompt-ul complet
        """
        tours_description = "\n".join([
            f"- {tour['name']}: {tour['description'][:100]}... (Categorie: {tour['category']}, Durată: {tour['duration']} min, Rating: {tour['rating']:.1f}⭐)"
            for tour in tours_data[:5]  # Maxim 5 tururi
        ])
        
        return f"""Pe baza preferințelor utilizatorului: {preferences}

Am găsit următoarele tururi potrivite:
{tours_description}

Te rog să recomanzi aceste tururi într-un mod natural și entuziast, explicând de ce sunt potrivite pentru utilizator.
Menționează caracteristicile importante ale fiecărui tur.
Răspunde în limba română, fii prietenos și concis."""
    
    def extract_preferences_from_conversation(self, messages):
        """
        Analizează conversația și extrage preferințele utilizatorului
        
        Args:
            messages: Listă de mesaje din conversație
            
        Returns:
            Dict cu preferințe: {'category': [], 'difficulty': '', 'duration': None, 'interests': []}
        """
        user_messages = [msg['content'].lower() for msg in messages if msg['role'] == 'user']
        full_text = ' '.join(user_messages)
        
        preferences = {
            'categories': [],
            'difficulty': None,
            'max_duration': None,
            'keywords': []
        }
        
        # Detectare categorii
        if any(word in full_text for word in ['istoric', 'istorie', 'monument', 'palat', 'castel']):
            preferences['categories'].append('istoric')
        if any(word in full_text for word in ['cultura', 'cultural', 'muzeu', 'artă', 'arte']):
            preferences['categories'].append('cultural')
        if any(word in full_text for word in ['mâncare', 'food', 'gastronomic', 'restaurant', 'tradițional']):
            preferences['categories'].append('gastronomic')
        if any(word in full_text for word in ['noapte', 'party', 'distracție', 'bar', 'club']):
            preferences['categories'].append('viata_noapte')
        
        # Detectare dificultate
        if any(word in full_text for word in ['ușor', 'relaxat', 'liniștit', 'simplu']):
            preferences['difficulty'] = 'usor'
        elif any(word in full_text for word in ['dificil', 'challenging', 'intens', 'activ']):
            preferences['difficulty'] = 'dificil'
        elif any(word in full_text for word in ['mediu', 'moderat']):
            preferences['difficulty'] = 'mediu'
        
        # Detectare durată (în minute)
        if 'oră' in full_text or 'ora' in full_text:
            # Simplificat - căutăm numere
            import re
            numbers = re.findall(r'\d+', full_text)
            if numbers:
                hours = int(numbers[0])
                preferences['max_duration'] = hours * 60
        
        # Keywords importante
        important_keywords = ['biserică', 'catedrală', 'parc', 'piață', 'centru', 'vechi', 'nou']
        preferences['keywords'] = [kw for kw in important_keywords if kw in full_text]
        
        return preferences
    
    def get_conversation_state(self, messages):
        """
        Determină starea conversației pentru a decide next step
        
        Returns:
            'greeting', 'gathering_info', 'ready_for_recommendations'
        """
        if len(messages) <= 1:
            return 'greeting'
        elif len(messages) < 4:
            return 'gathering_info'
        else:
            # Verifică dacă avem suficiente preferințe
            prefs = self.extract_preferences_from_conversation(messages)
            if prefs['categories'] or prefs['keywords']:
                return 'ready_for_recommendations'
            return 'gathering_info'
