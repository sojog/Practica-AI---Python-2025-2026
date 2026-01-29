"""
Engine pentru recomandări tururi bazat pe preferințele utilizatorului
"""
from .models import Tour
from django.db.models import Q, Avg
import logging

logger = logging.getLogger(__name__)


class TourRecommendationEngine:
    """Engine pentru matching și scorare tururi"""
    
    def __init__(self):
        pass
    
    def match_tours(self, preferences, limit=5):
        """
        Găsește tururi care match-uiesc preferințele utilizatorului
        
        Args:
            preferences: Dict cu {'categories': [], 'difficulty': '', 'max_duration': int, 'keywords': []}
            limit: Număr maxim de tururi de returnat
            
        Returns:
            QuerySet de tururi sortate după relevanță
        """
        tours = Tour.objects.filter(is_active=True)
        
        # Filtrare după categorie
        if preferences.get('categories'):
            tours = tours.filter(category__in=preferences['categories'])
        
        # Filtrare după dificultate
        if preferences.get('difficulty'):
            tours = tours.filter(difficulty=preferences['difficulty'])
        
        # Filtrare după durată maximă
        if preferences.get('max_duration'):
            tours = tours.filter(duration__lte=preferences['max_duration'])
        
        # Căutare după keywords în nume și descriere
        if preferences.get('keywords'):
            q_objects = Q()
            for keyword in preferences['keywords']:
                q_objects |= Q(name__icontains=keyword) | Q(description__icontains=keyword)
            tours = tours.filter(q_objects)
        
        # Sortare după rating și dată
        tours = tours.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating', '-created_at')
        
        return tours[:limit]
    
    def score_tour(self, tour, preferences):
        """
        Calculează un scor de relevantă pentru un tur
        
        Args:
            tour: Obiect Tour
            preferences: Dict cu preferințe
            
        Returns:
            Float scor între 0 și 100
        """
        score = 0
        
        # Categorie match (40 puncte)
        if tour.category in preferences.get('categories', []):
            score += 40
        
        # Dificultate match (20 puncte)
        if tour.difficulty == preferences.get('difficulty'):
            score += 20
        
        # Durată în range (20 puncte)
        if preferences.get('max_duration'):
            if tour.duration <= preferences['max_duration']:
                score += 20
        
        # Rating (20 puncte)
        avg_rating = tour.average_rating
        if avg_rating > 0:
            score += (avg_rating / 5.0) * 20
        
        return round(score, 2)
    
    def format_tours_for_ai(self, tours):
        """
        Formatează tururile pentru a fi trimise la AI
        
        Args:
            tours: QuerySet sau listă de tururi
            
        Returns:
            Listă de dict-uri cu date relevante
        """
        tours_data = []
        for tour in tours:
            tours_data.append({
                'id': tour.id,
                'name': tour.name,
                'slug': tour.slug,
                'description': tour.description,
                'category': tour.get_category_display(),
                'duration': tour.duration,
                'difficulty': tour.get_difficulty_display(),
                'rating': tour.average_rating,
                'total_reviews': tour.total_reviews,
                'is_premium': tour.is_premium,
                'price': float(tour.price) if tour.price else 0,
            })
        return tours_data
    
    def format_tours_for_response(self, tours):
        """
        Formatează tururile pentru răspunsul JSON către frontend
        Include doar datele necesare pentru afișare în chat
        
        Args:
            tours: QuerySet sau listă de tururi
            
        Returns:
            Listă de dict-uri simplificată
        """
        tours_data = []
        for tour in tours:
            tours_data.append({
                'id': tour.id,
                'name': tour.name,
                'slug': tour.slug,
                'description': tour.description[:150] + '...' if len(tour.description) > 150 else tour.description,
                'category': tour.get_category_display(),
                'duration_hours': round(tour.duration / 60, 1),
                'difficulty': tour.get_difficulty_display(),
                'rating': round(tour.average_rating, 1),
                'cover_image': tour.cover_image.url if tour.cover_image else None,
            })
        return tours_data
