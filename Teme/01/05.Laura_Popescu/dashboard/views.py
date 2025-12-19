from django.shortcuts import render
from birthdata.models import Birthdate
from django.contrib.auth.models import User

# Helper to get a default user for testing
def get_default_user():
    user = User.objects.first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    return user

def profile_dashboard_view(request):
	context = {}
	return render(request, 'profile.html', context)

from django.utils import timezone

def home_view(request):
    user = request.user if request.user.is_authenticated else get_default_user()
    
    # Stats
    total_contacts = Birthdate.objects.filter(user=user).count()
    
    # Logic to find the absolute next birthday
    today = timezone.now().date()
    current_month = today.month
    current_day = today.day

    # 1. Check for remaining birthdays in current month
    next_birthday = Birthdate.objects.filter(
        user=user, 
        birthdate__month=current_month, 
        birthdate__day__gte=current_day
    ).order_by('birthdate__day').first()

    # 2. If none, check upcoming months in same year
    if not next_birthday:
        next_birthday = Birthdate.objects.filter(
            user=user,
            birthdate__month__gt=current_month
        ).order_by('birthdate__month', 'birthdate__day').first()

    # 3. If still none (e.g. end of year), check beginning of next year
    if not next_birthday:
        next_birthday = Birthdate.objects.filter(
            user=user
        ).order_by('birthdate__month', 'birthdate__day').first()

    upcoming_birthdays_count = Birthdate.objects.filter(user=user, birthdate__month=current_month).count()
    
    # Gift Ideas Count - Placeholder (could be real if we stored suggestions)
    gift_ideas = 0 
    
    context = {
        'total_contacts': total_contacts,
        'upcoming_birthdays': upcoming_birthdays_count,
        'gift_ideas': gift_ideas,
        'next_birthday': next_birthday
    }
    return render(request, 'home.html', context)

def ui_test_view(request):
    return render(request, 'ui_test.html')
