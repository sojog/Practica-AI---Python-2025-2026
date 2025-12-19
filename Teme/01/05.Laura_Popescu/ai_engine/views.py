from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .utils import generate_gift_suggestions
from birthdata.models import Birthdate
from django.shortcuts import get_object_or_404
import json

# Helper for testing user (same as in birthdata views)
from django.contrib.auth.models import User
def get_default_user():
    user = User.objects.first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    return user

def get_gift_suggestions(request, pk):
    """
    API endpoint to get gift suggestions for a specific birthdate contact.
    Uses caching to avoid repeated API calls.
    """
    from .models import GiftSuggestion
    
    # For now, simplistic permissions:
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdate = get_object_or_404(Birthdate, pk=pk, user=user)
    
    # Check if we should regenerate (force new API call)
    regenerate = request.GET.get('regenerate', 'false').lower() == 'true'
    
    # Try to get cached suggestions first
    if not regenerate:
        cached_suggestions = GiftSuggestion.objects.filter(birthdate=birthdate)[:3]
        if cached_suggestions.exists():
            # Return cached suggestions
            suggestions = [
                {"item": s.item, "reason": s.reason}
                for s in cached_suggestions
            ]
            return JsonResponse({'suggestions': suggestions, 'cached': True})
    
    # No cache or regenerate requested - call AI API
    try:
        suggestions = generate_gift_suggestions(birthdate.name, birthdate)
        
        # Clear old cached suggestions if regenerating
        if regenerate:
            GiftSuggestion.objects.filter(birthdate=birthdate).delete()
        
        # Save new suggestions to cache
        for suggestion in suggestions:
            if isinstance(suggestion, dict) and 'item' in suggestion:
                GiftSuggestion.objects.create(
                    birthdate=birthdate,
                    item=suggestion['item'],
                    reason=suggestion.get('reason', '')
                )
        
        return JsonResponse({'suggestions': suggestions, 'cached': False})
    
    except Exception as e:
        # If API fails, try to return cached suggestions as fallback
        cached_suggestions = GiftSuggestion.objects.filter(birthdate=birthdate)[:3]
        if cached_suggestions.exists():
            suggestions = [
                {"item": s.item, "reason": s.reason}
                for s in cached_suggestions
            ]
            return JsonResponse({
                'suggestions': suggestions, 
                'cached': True,
                'note': 'Using cached suggestions due to API error'
            })
        else:
            # No cache available, return error
            return JsonResponse({
                'suggestions': [{"item": "Error occurred", "reason": str(e)}],
                'cached': False
            })


def gift_suggestions_page_view(request, pk):
    """
    Renders the styled Gift Ideas page (which will then fetch suggestions via AJAX).
    """
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdate = get_object_or_404(Birthdate, pk=pk, user=user)
    return render(request, 'gift_suggestions.html', {'birthdate': birthdate})

def ai_dashboard_view(request):
    """
    Renders the AI Insights Dashboard landing page.
    """
    return render(request, 'ai_dashboard.html')

def analyze_birthdate_view(request):
	context = {}
	return render(request, 'analyze_birthdate.html', context)

def compatibility_dashboard_view(request):
    """
    Renders user interface to select two contacts for compatibility check.
    """
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdates = Birthdate.objects.filter(user=user).order_by('first_name', 'last_name')
    return render(request, 'compatibility.html', {'birthdates': birthdates})

def compatibility_result_view(request):
    """
    Renders the compatibility matching page.
    """
    person_a_id = request.GET.get('person_a')
    person_b_id = request.GET.get('person_b')
    
    if not person_a_id or not person_b_id:
        return compatibility_dashboard_view(request)
        
    user = request.user if request.user.is_authenticated else get_default_user()
    person_a = get_object_or_404(Birthdate, pk=person_a_id, user=user)
    person_b = get_object_or_404(Birthdate, pk=person_b_id, user=user)
    
    context = {
        'person_a': person_a,
        'person_b': person_b
    }
    return render(request, 'compatibility_result.html', context)

def get_compatibility_api_v2(request):
    """
    API endpoint to calculate or retrieve cached compatibility.
    """
    from .models import Compatibility
    from .utils import generate_compatibility_v2
    
    person_a_id = request.GET.get('person_a')
    person_b_id = request.GET.get('person_b')
    regenerate = request.GET.get('regenerate', 'false').lower() == 'true'
    
    user = request.user if request.user.is_authenticated else get_default_user()
    person_a = get_object_or_404(Birthdate, pk=person_a_id, user=user)
    person_b = get_object_or_404(Birthdate, pk=person_b_id, user=user)
    
    # Ensure consistent ordering for lookup (lower ID first)
    if person_a.pk > person_b.pk:
        person_a, person_b = person_b, person_a
        swapped = True
    else:
        swapped = False
        
    # Check cache
    if not regenerate:
        cached = Compatibility.objects.filter(person_a=person_a, person_b=person_b).first()
        if cached:
            return JsonResponse({
                'score': cached.compatibility_score,
                'verdict': cached.short_verdict,
                'analysis': cached.analysis,
                'cached': True
            })

    # Generate new
    try:
        # Pass original objects (even if swapped for storage lookup) so names match prompt
        # Actually, for storage we want consistent ID order, but for prompt we might want to respect user selection?
        # Let's just use the consistent order for storage and prompt to keep it simple.
        data = generate_compatibility_v2(person_a, person_b)
        
        # Save to cache
        if regenerate:
            Compatibility.objects.filter(person_a=person_a, person_b=person_b).delete()
            
        Compatibility.objects.create(
            person_a=person_a,
            person_b=person_b,
            compatibility_score=data.get('score', 50),
            short_verdict=data.get('verdict', 'Unknown'),
            analysis=data.get('analysis', 'No analysis.')
        )
        
        return JsonResponse({
            'score': data.get('score', ''),
            'verdict': data.get('verdict', ''),
            'analysis': data.get('analysis', ''),
            'cached': False
        })
        
    except Exception as e:
         return JsonResponse({
            'score': 0,
            'verdict': "Error",
            'analysis': str(e),
            'error': True
        })

def smart_gifting_view(request):
    """
    Displays all contacts for easy access to gift suggestions.
    """
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdates = Birthdate.objects.filter(user=user).order_by('first_name', 'last_name')
    return render(request, 'smart_gifting.html', {'birthdates': birthdates})


def social_aura_dashboard_view(request):
    """
    Displays all contacts for easy access to social aura analysis.
    """
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdates = Birthdate.objects.filter(user=user).order_by('first_name', 'last_name')
    return render(request, 'social_aura_dashboard.html', {'birthdates': birthdates})

def social_aura_view(request, pk):
    """
    Renders the Social Aura specific page for a contact.
    """
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdate = get_object_or_404(Birthdate, pk=pk, user=user)
    return render(request, 'social_aura.html', {'birthdate': birthdate})

def get_social_aura(request, pk):
    """
    API endpoint to get social aura for a contact.
    """
    from .models import SocialAura
    from .utils import generate_social_aura
    
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdate = get_object_or_404(Birthdate, pk=pk, user=user)
    
    regenerate = request.GET.get('regenerate', 'false').lower() == 'true'
    
    # Try cache
    if not regenerate:
        cached_aura = SocialAura.objects.filter(birthdate=birthdate).first()
        if cached_aura:
            return JsonResponse({
                'description': cached_aura.description,
                'keywords': cached_aura.keywords,
                'cached': True
            })
            
    # Generate new
    try:
        data = generate_social_aura(birthdate.name, birthdate, birthdate.notes)
        
        # Save to cache
        if regenerate:
            SocialAura.objects.filter(birthdate=birthdate).delete()
            
        SocialAura.objects.create(
            birthdate=birthdate,
            description=data.get('description', 'No description available.'),
            keywords=data.get('keywords', 'Unknown')
        )
        
        return JsonResponse({
            'description': data.get('description', ''),
            'keywords': data.get('keywords', ''),
            'cached': False
        })
        
    except Exception as e:
        return JsonResponse({
            'description': "Error analyzing aura.",
            'keywords': "Error",
            'error': str(e)
        })
