from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile
from tours.models import Favorite, Review
from analytics.models import TourCompletion
from django import forms


class RegisterForm(forms.ModelForm):
    """Form pentru înregistrare"""
    password1 = forms.CharField(label='Parolă', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmă parola', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
        widgets = {
            'role': forms.Select(choices=CustomUser.ROLE_CHOICES)
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Parolele nu coincid')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Create profile
            Profile.objects.create(user=user)
        return user


def register_view(request):
    """View pentru înregistrare"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bun venit, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """View pentru autentificare"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bine ai revenit, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Nume de utilizator sau parolă incorecte.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """View pentru logout"""
    logout(request)
    messages.success(request, 'Ai fost deconectat cu succes.')
    return redirect('home')


@login_required
def profile_view(request):
    """View pentru profil utilizator"""
    user = request.user
    
    # Get favorites
    favorites = Favorite.objects.filter(user=user).select_related('tour')
    
    # Get reviews
    reviews = Review.objects.filter(user=user).select_related('tour')
    
    # Get tour completions
    completions = TourCompletion.objects.filter(user=user).select_related('tour')
    
    # Update profile stats
    profile, created = Profile.objects.get_or_create(user=user)
    profile.total_tours_completed = completions.count()
    profile.total_reviews = reviews.count()
    profile.save()
    
    context = {
        'profile': profile,
        'favorites': favorites,
        'reviews': reviews,
        'completions': completions,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """View pentru editare profil"""
    user = request.user
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.bio = request.POST.get('bio', '')
        user.phone = request.POST.get('phone', '')
        
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        
        user.save()
        messages.success(request, 'Profilul a fost actualizat cu succes!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/edit_profile.html')
