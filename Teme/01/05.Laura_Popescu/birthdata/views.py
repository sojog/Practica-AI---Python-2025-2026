from django.shortcuts import render, redirect, get_object_or_404
from .models import Birthdate
from .forms import BirthdateForm
from django.contrib.auth.models import User

# Helper to get a default user for testing since we don't have login flow active yet
def get_default_user():
    user = User.objects.first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    return user

def add_birthdate_view(request):
    if request.method == "POST":
        form = BirthdateForm(request.POST)
        if form.is_valid():
            birthdate = form.save(commit=False)
            birthdate.user = request.user if request.user.is_authenticated else get_default_user()
            birthdate.save()
            return render(request, 'success_add_birthdate.html')
    else:
        form = BirthdateForm()
    
    return render(request, 'add_birthdate.html', {'form': form})

import calendar

def list_birthdates_view(request):
    user = request.user if request.user.is_authenticated else get_default_user()
    
    from django.utils import timezone
    today = timezone.now().date()
    current_month_number = today.month

    # 1. Fetch all birthdates for user
    all_birthdates = Birthdate.objects.filter(user=user)
    
    # 2. Organize by month
    months = []
    current_month_data = None
    
    for i in range(1, 13):
        month_name = calendar.month_name[i]
        birthdates_in_month = all_birthdates.filter(birthdate__month=i).order_by('birthdate__day')
        
        month_data = {
            'name': month_name,
            'number': i,
            'birthdates': birthdates_in_month
        }
        
        months.append(month_data)
        
        if i == current_month_number:
            current_month_data = month_data

    # Create a list of "rest of the months" if needed, or just pass full list
    # User said "lower, the next months".
    # Let's pass full list, and template can filter if we want to exclude current, 
    # but often seeing the full year grid is better.
    # However, to be strictly "Hero + Others", I'll show current in Hero, and All in grid?
    # Or Current in Hero, and Others in Grid. 
    # Let's filter out current from the "months" list passed to context if we want to avoid duplication?
    # "they can be how they are now, it s fine" -> implies the grid structure is fine.
    # I'll pass both.
    
    return render(request, 'list_birthdates.html', {'months': months, 'current_month': current_month_data})

def edit_birthdate_view(request, pk):
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdate = get_object_or_404(Birthdate, pk=pk, user=user)
    
    if request.method == "POST":
        form = BirthdateForm(request.POST, instance=birthdate)
        if form.is_valid():
            form.save()
            return redirect('/birthdata/list/') # Redirect to list after edit
    else:
        form = BirthdateForm(instance=birthdate)

    return render(request, 'edit_birthdate.html', {'form': form, 'birthdate': birthdate})

def delete_birthdate_view(request, pk):
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdate = get_object_or_404(Birthdate, pk=pk, user=user)
    
    if request.method == "POST":
        birthdate.delete()
        return redirect('/birthdata/list/')
        
    return render(request, 'delete_birthdate.html', {'birthdate': birthdate})

def details_birthdate_view(request, pk):
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdate = get_object_or_404(Birthdate, pk=pk, user=user)
    return render(request, 'detail_birthdate.html', {'birthdate': birthdate})

def contacts_view(request):
    user = request.user if request.user.is_authenticated else get_default_user()
    birthdates = Birthdate.objects.filter(user=user).order_by('first_name', 'last_name') # Sort by Name
    return render(request, 'contacts.html', {'birthdates': birthdates})
