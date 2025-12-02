from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Tour, Location, Review, Favorite, Comment, OfflineContent
from analytics.models import TourView
import json


def home(request):
    """Homepage cu tururi featured"""
    featured_tours = Tour.objects.filter(is_active=True)[:6]
    categories = Tour.CATEGORY_CHOICES
    
    # Statistici
    total_tours = Tour.objects.filter(is_active=True).count()
    total_locations = Location.objects.count()
    
    context = {
        'featured_tours': featured_tours,
        'categories': categories,
        'total_tours': total_tours,
        'total_locations': total_locations,
    }
    return render(request, 'home.html', context)


def tour_list(request):
    """Listă tururi cu filtrare și căutare"""
    tours = Tour.objects.filter(is_active=True)
    
    # Filtrare după categorie
    category = request.GET.get('category')
    if category:
        tours = tours.filter(category=category)
    
    # Filtrare după premium
    premium = request.GET.get('premium')
    if premium == 'true':
        tours = tours.filter(is_premium=True)
    elif premium == 'false':
        tours = tours.filter(is_premium=False)
    
    # Filtrare după dificultate
    difficulty = request.GET.get('difficulty')
    if difficulty:
        tours = tours.filter(difficulty=difficulty)
    
    # Căutare
    search_query = request.GET.get('search')
    if search_query:
        tours = tours.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Sortare
    sort = request.GET.get('sort', '-created_at')
    tours = tours.order_by(sort)
    
    # Paginare
    paginator = Paginator(tours, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Tour.CATEGORY_CHOICES,
        'difficulties': Tour.DIFFICULTY_CHOICES,
        'current_category': category,
        'current_difficulty': difficulty,
        'search_query': search_query,
    }
    return render(request, 'tours/tour_list.html', context)


def tour_detail(request, slug):
    """Detalii tur cu hartă și locații"""
    tour = get_object_or_404(Tour, slug=slug, is_active=True)
    locations = tour.locations.all().prefetch_related('images')
    
    # Track vizualizare
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    
    TourView.objects.create(
        tour=tour,
        user=request.user if request.user.is_authenticated else None,
        session_id=session_id,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # Reviews
    reviews = tour.reviews.all().select_related('user')[:10]
    
    # Comentarii (doar root comments, replies sunt nested)
    comments = tour.comments.filter(parent=None).select_related('user').prefetch_related('replies')
    
    # Check dacă utilizatorul are tur în favorite
    is_favorite = False
    user_review = None
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, tour=tour).exists()
        try:
            user_review = Review.objects.get(user=request.user, tour=tour)
        except Review.DoesNotExist:
            pass
    
    # Prepare locations pentru hartă (JSON)
    locations_data = [
        {
            'id': loc.id,
            'name': loc.name,
            'lat': float(loc.latitude),
            'lng': float(loc.longitude),
            'order': loc.order,
            'description': loc.description[:100] + '...' if len(loc.description) > 100 else loc.description
        }
        for loc in locations
    ]
    
    context = {
        'tour': tour,
        'locations': locations,
        'locations_json': json.dumps(locations_data),
        'reviews': reviews,
        'comments': comments,
        'is_favorite': is_favorite,
        'user_review': user_review,
        'average_rating': tour.average_rating,
        'total_reviews': tour.total_reviews,
    }
    return render(request, 'tours/tour_detail.html', context)


def location_detail(request, location_id):
    """Detalii locație"""
    location = get_object_or_404(Location, id=location_id)
    images = location.images.all()
    
    # Next și previous location în tur
    next_location = Location.objects.filter(tour=location.tour, order__gt=location.order).order_by('order').first()
    prev_location = Location.objects.filter(tour=location.tour, order__lt=location.order).order_by('-order').first()
    
    context = {
        'location': location,
        'images': images,
        'next_location': next_location,
        'prev_location': prev_location,
    }
    return render(request, 'tours/location_detail.html', context)


@login_required
def add_review(request, tour_id):
    """Adaugă review la tur"""
    if request.method == 'POST':
        tour = get_object_or_404(Tour, id=tour_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        review, created = Review.objects.update_or_create(
            tour=tour,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if created:
            messages.success(request, 'Review adăugat cu succes!')
        else:
            messages.success(request, 'Review actualizat cu succes!')
        
        return redirect('tours:tour_detail', slug=tour.slug)
    
    return redirect('home')


@login_required
def toggle_favorite(request, tour_id):
    """Toggle favorite pentru tur"""
    if request.method == 'POST':
        tour = get_object_or_404(Tour, id=tour_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, tour=tour)
        
        if not created:
            favorite.delete()
            is_favorite = False
            message = 'Tur eliminat din favorite'
        else:
            is_favorite = True
            message = 'Tur adăugat la favorite'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'is_favorite': is_favorite})
        
        messages.success(request, message)
        return redirect('tour_detail', slug=tour.slug)
    
    return redirect('home')


@login_required
def add_comment(request, tour_id):
    """Adaugă comentariu la tur"""
    if request.method == 'POST':
        tour = get_object_or_404(Tour, id=tour_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)
        
        Comment.objects.create(
            tour=tour,
            user=request.user,
            content=content,
            parent=parent
        )
        
        messages.success(request, 'Comentariu adăugat cu succes!')
        return redirect('tour_detail', slug=tour.slug)
    
    return redirect('home')


@login_required
def download_tour(request, tour_id):
    """Marchează tur pentru offline access"""
    tour = get_object_or_404(Tour, id=tour_id)
    
    # Check dacă e premium și user nu are acces
    if tour.is_premium and not request.user.is_staff:
        messages.error(request, 'Acest tur este premium. Contactează administratorul pentru acces.')
        return redirect('tour_detail', slug=tour.slug)
    
    offline_content, created = OfflineContent.objects.get_or_create(
        user=request.user,
        tour=tour
    )
    
    if created:
        messages.success(request, f'Turul "{tour.name}" a fost descărcat pentru acces offline!')
    else:
        messages.info(request, 'Acest tur este deja disponibil offline.')
    
    return redirect('tour_detail', slug=tour.slug)


def search_tours(request):
    """Căutare și filtrare avansată"""
    query = request.GET.get('q', '')
    
    tours = Tour.objects.filter(is_active=True)
    
    if query:
        tours = tours.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(locations__name__icontains=query)
        ).distinct()
    
    context = {
        'tours': tours,
        'query': query,
    }
    return render(request, 'tours/search_results.html', context)
